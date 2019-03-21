/* $Id$ $Date$
*/

#include <map>          // std::map
#include <string>       // std::string
#include <iostream>     // std::cout
#include <sstream>      // std::stringstream, std::stringbuf
#include <typeinfo>     // typeid(T).name()
#include <cxxabi.h>
#include <ctime>

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
};

typedef field<int> int_history;
typedef field<string> string_history;

string event(string table_name, map<string,anyfield * > m);

int main ()
{
    time_t test = -1;
    int64_t utest = test;
    cout << test << " Size of (time_t) " << sizeof(test) << "\n";
    cout << 1+ utest << " Size of (int64_t) " << sizeof(utest) << "\n";

    map<string,anyfield * > m;
    //    m["INT"]=new field<int>("INT",3);
    m["INT"]=new int_history("INT",3);
    field<int> *t = new int_history("INT2",123);
    t->set(15);
    m["INT2"]=t;
    field<string> *s = new string_history ("STR","meh");
    s->set("duh");
    m[s->get_name()]=s;
    cout << "this should show something '" << s->to_string() << "'\n";
    s->set("okay, Meh");
    cout << "this should show another thing '" << s->to_string() << "'\n";
    cout << "size of map: "<< m.size() << "\n";
    cout << "this should show nothing '" << m["INT"]->to_string() << "'\n";

    int_history *t_int = NULL;
    string_history *t_str = NULL;

    cout << event("table=fields",m);
    if(m.size() > 0)
    {
        anyfield * p = m.begin()->second;
        if (t_int = dynamic_cast<int_history *>(p))
        {
            t_int->set(1984);
        }
        else if (t_str = dynamic_cast<string_history *>(p))
        {
            t_str->set("1984");
        }
    }
    cout << event("table=fields",m);
}

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

string event(string table_name, map<string,anyfield * > m)
{
    string record="";
    bool empty=true;
    for (map<string,anyfield * >::iterator i=m.begin() ; i != m.end(); ++i)
    {
         string delta=i->second->to_string();
         if(delta.length() == 0) continue;
         if(!empty)record +=';';
         record +=delta;
         empty=false;
    }
    return table_name +" '"+ record + "'\n";
}
