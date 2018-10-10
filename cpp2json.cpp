/* $Id$ $Date$
*/

#include <map>          // std::map
#include <string>       // std::string
#include <iostream>     // std::cout
#include <sstream>      // std::stringstream, std::stringbuf
#include <typeinfo>     // typeid(T).name()
#include <cxxabi.h>

using namespace std;

class anyfield
{
    protected:
    bool clean;
    public:
    anyfield():clean(true){}
    bool is_clean() const { return clean;}
    virtual string to_string(){return "";}
    virtual ~anyfield(){}
};

template<class T>
class field: public anyfield
{
    protected:
    field(field<T> &other):prev(other.prev),next(other.next),name(other.name){clean =(prev == next);}
    T prev;
    T next;
    string name;
    public:
    field( string _name, T val):prev(val),name(_name){}
    virtual string to_string();
    void set(T f){next = f;clean=false;}
    string get_name() const {return name;}
    friend class table;
};

typedef field<int> int_history;
typedef field<string> string_history;
typedef map<string,anyfield * > table_fields;
typedef map<string,anyfield * >::iterator table_fields_iter;
class table{
public:
    table(string _name):table_name(_name){}
    bool read(table_fields & _m);
    void save();
protected:
    table_fields m;
    string event();
private:
    string table_name;
};


int main ()
{
    table_fields m;
    //    m["INT"]=new field<int>("INT",3);
    m["INT"]=new int_history("INT",3);
    field<int> *t = new int_history("INT2",123);
    t->set(15);
    m["INT2"]=t;
    table my_table("test_table");
    my_table.read(m);
    my_table.save();
    cout << "\n";

    field<string> *s = new string_history ("STR","meh");
    s->set("duh");
    m[s->get_name()]=s;
    cout << "this should show something '" << s->to_string() << "'\n";
    s->set("okay, Meh");
    cout << "this should show another thing '" << s->to_string() << "'\n";
    cout << "size of map: "<< m.size() << "\n";
    cout << "this should show nothing '" << m["INT"]->to_string() << "'\n";
    my_table.read(m);

    cout << "\n";
    int_history *t_int = NULL;
    string_history *t_str = NULL;

    for (table_fields_iter i=m.begin() ; i != m.end(); ++i)
    {
        anyfield * p = i->second;
        if (t_int = dynamic_cast<int_history *>(p))
        {
            t_int->set(1984);
        }
        else if (t_str = dynamic_cast<string_history *>(p))
        {
            t_str->set("1984");
        }
    }
    my_table.read(m);
    my_table.save();
    cout << "\n";
}
/* non Json
template<typename T>
string field<T>::to_string()
{
   string n = typeid(T).name();
   if (n == "i") { n.assign("int");}
   else if (n == "j") { n.assign("unsigned int"); }
   else if (n.find("basic_string") >= 0 ) { n.assign("String"); }
   cout << "T is " << n << "\n";
   if (!clean && prev != next)
   {
       stringstream ss;
       ss << name << '-' << prev << ':' << next;
       return ss.str();
   }
   else return "";
}
*/

// JSON
template<typename T>
string field<T>::to_string()
{
   string n = typeid(T).name();
   if (n == "i") { n.assign("int");}
   else if (n == "j") { n.assign("unsigned int"); }
   else if (n.find("basic_string") >= 0 ) { n.assign("String"); }
   //cout << "T is " << n << "\n";
   if (!clean && prev != next)
   {
        stringstream ss;
            ss << "\"" << name << "\":";
            ss << "{\"n\":\"" << next << "\",\"o\":\"" << prev << "}";
       return ss.str();
   }
   else return "";
}

string table::event()
{
    string record="";
    bool empty=true;
    for (table_fields_iter i=m.begin() ; i != m.end(); ++i)
    {
        string delta=i->second->to_string();
        if(delta.length() == 0) continue;
        if(!empty)record +=',';
        record +=delta;
        empty=false;
    }
    return table_name +"\"eventDescr\":{"+ record + "}";
}

void table::save()
{
    cout << "Before Save: \n" << event() << "\n";

    int_history *t_int = NULL;
    string_history *t_str = NULL;
    for (table_fields_iter i=m.begin() ; i != m.end(); ++i)
    {
        if (t_int = dynamic_cast<int_history *>(i->second))
        {
            t_int->prev = t_int->next;
        }
        else if (t_str = dynamic_cast<string_history *>(i->second))
        {
            t_str->prev = t_str->next;
        }
    }
    cout << "After Save: \n" << event() << "\n";
}


bool table::read(table_fields &_m)
{
    string record="";
    bool empty=true;
    for (table_fields_iter i=_m.begin() ; i != _m.end(); ++i)
    {
        m[i->first]=i->second;
    }
    return true;
}
