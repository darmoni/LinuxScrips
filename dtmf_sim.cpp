// $Id$Date$


#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <cstdint>
#include <fstream>
#include <typeinfo>

class RTPBuffer
{
public:
    const void * DataPtr() const {return &data;}
    uint32_t Timestamp()const { return ts; };

    RTPBuffer(void* _data, size_t size, uint32_t _ts):
        data(*(uint32_t*)_data),
        ts(_ts)
        {}
private:
    RTPBuffer(){}
    uint32_t data;
    uint32_t ts;
    friend std::ostream & operator<< (std::ostream & os, const RTPBuffer &packet);
};

class DTMFNotification
{
    DTMFNotification(){}
    uint8_t code;
public:
    DTMFNotification(uint8_t c):code(c){}
    uint8_t get_code() {return code;}
};
class DtmfRcver
{
public:
    void Notify(DTMFNotification * dtmfnote) { std::cout << "DTMFNotification Code = " << (int)dtmfnote->get_code() << "\n";}
};

class DtmfSimulator
{
protected:
    std::string name;
    uint32_t    m_last_dtmf_ts;
    int last_eec;
    int last_ec;
    int lastDuration;
    DtmfRcver dtmf_receiver;
    DtmfRcver * m_dtmf_receiver;
public:
    union DTMFData {
        uint32_t		rawdata;
        struct DTMF {
            uint16_t	duration;
            uint8_t		volume		:6;
            uint8_t		reserved	:1;
            uint8_t		eoe			:1;
            uint8_t		code;
        };
        DTMF			dtmf;
        friend std::ostream & operator<< (std::ostream & os, const DTMFData &dtmf);
    };

public:
    DtmfSimulator():
        m_dtmf_receiver(& dtmf_receiver),
        m_last_dtmf_ts(101),
        last_eec(800),
        last_ec(900),
        lastDuration(-1)
        {}
    virtual void OnInboundPacket(RTPBuffer* packet)
    {
        if (true)//  This is a simulation (packet && m_dtmf_receiver && packet->Payload() == m_dtmf_index && packet->DataSize() >= sizeof(DTMFData))
        {
            DTMFData dtmf;
            dtmf.rawdata = /*htonl(*/*(uint32_t*)packet->DataPtr();  //Simulation
            uint32_t current_ts = packet->Timestamp();
            if (m_last_dtmf_ts != current_ts)
            {
                if (dtmf.dtmf.eoe == 0)                               // Not end of event packet
                    SetLastEC(dtmf.dtmf.code);
                m_last_dtmf_ts = current_ts;
                DTMFNotification dtmfnote(dtmf.dtmf.code);
                m_dtmf_receiver->Notify(&dtmfnote);
                SetLastEEC(dtmf.dtmf.code);
            }
            SetLastDuration(dtmf.dtmf.duration);
        }
    }
    int LastEC() const
    {
        return last_ec;
    }
    int LastEEC() const
    {
        return last_eec;
    }
    int LastDuration() const
    {
        return lastDuration;
    }
    void SetLastEC(int _last_ec)
    {
        last_ec = _last_ec;
    }
    void SetLastEEC(int _last_eec)
    {
        last_eec = _last_eec;
    }
    void SetLastDuration(int _last_duration)
    {
        lastDuration = _last_duration;
    }
};
std::ostream & operator<< (std::ostream & os, const DtmfSimulator::DTMFData &dtmf)
{
    os << (int)dtmf.dtmf.code ;
    os << "\t" << (int)dtmf.dtmf.eoe ;
    os << "\t" << (int)dtmf.dtmf.duration;
    return os;
}

std::ostream & operator<< (std::ostream & os, const RTPBuffer &packet)
{
    DtmfSimulator::DTMFData dtmf;
    dtmf.rawdata = *(uint32_t*)packet.DataPtr();
    os << dtmf << "\t" << packet.Timestamp();
    return os;
}
class OriginalDtmfSimulator: public DtmfSimulator
{
    public:
        OriginalDtmfSimulator():
        DtmfSimulator(){}
    virtual void OnInboundPacket(RTPBuffer* packet)
    {
        if (true)//  This is a simulation (packet && m_dtmf_receiver && packet->Payload() == m_dtmf_index && packet->DataSize() >= sizeof(DTMFData))
        {
            DTMFData dtmf;
            dtmf.rawdata = /*htonl(*/*(uint32_t*)packet->DataPtr();  //Simulation
            if (dtmf.dtmf.eoe == 0)
            {
                if (LastEC() != dtmf.dtmf.code || LastDuration() > dtmf.dtmf.duration)
                {
                    DTMFNotification dtmfnote(dtmf.dtmf.code);
                    m_dtmf_receiver->Notify(&dtmfnote);
                    SetLastEC(dtmf.dtmf.code);
                    SetLastEEC(dtmf.dtmf.code);
                }
            } else {
                if (LastEEC() != dtmf.dtmf.code)
                {
                    DTMFNotification dtmfnote(dtmf.dtmf.code);
                    m_dtmf_receiver->Notify(&dtmfnote);
                    SetLastEEC(dtmf.dtmf.code);
                }
            }
            SetLastDuration(dtmf.dtmf.duration);
        }
    }
};

using namespace std;
int main(int argc, char ** argv)
{
    class SimInput
    {
        DtmfSimulator::DTMFData dtmf;
    };
    DtmfSimulator new_sim;
    OriginalDtmfSimulator orig_sim;
    vector<DtmfSimulator * > DtmfSimulators {&new_sim, &orig_sim};
    for (int variant = 0; variant < DtmfSimulators.size() ; ++ variant)
    {
        DtmfSimulator * my_sim = DtmfSimulators[variant & 1];
        cout << " *** " << typeid(*my_sim).name() << " *** \n";
        ifstream is("DTMF_20180828_dtmf_info.csv");
        vector< RTPBuffer > dtmf_input;
        char dummy[128];
        is.getline(dummy,128); // ignore header
        unsigned counter=0;
        uint32_t code, end, duration, ts;
        DtmfSimulator::DTMFData mytest_dtmf;
        while(is) {
            is >> code; mytest_dtmf.dtmf.code = code;
            is >> end; mytest_dtmf.dtmf.eoe = end;
            is >> duration; mytest_dtmf.dtmf.duration = duration;
            is >> ts ; RTPBuffer buff(&mytest_dtmf.rawdata, sizeof(mytest_dtmf), ts);
            dtmf_input.push_back(buff);
            counter++;
        }
        cout << "code\tend\tduration\tTs\n";
        for (auto packet = dtmf_input.begin(); packet != dtmf_input.end(); ++packet)
        {
            cout << *packet << "\n";
            my_sim->OnInboundPacket(&(*packet));
        }
    }
    return (0);
}
