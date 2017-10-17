/* $Id$ $Date$
*/

#include <map>          // std::map
#include <string>       // std::string
#include <iostream>     // std::cout
#include <sstream>      // std::stringstream, std::stringbuf

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
string event(string table_name, map<string,anyfield * > m);

int main ()
{
    map<string,anyfield * > m;
    m["INT"]=new field<int>("INT",3);
    field<int> *t = new field<int>("INT2",123);
    t->set(15);
    m["INT2"]=t;
    field<string> *s = new field<string> ("STR","meh");
    s->set("duh");
    m[s->get_name()]=s;
    cout << "this should show something '" << s->to_string() << "'\n";
    s->set("okay, Meh");
    cout << "this should show another thing '" << s->to_string() << "'\n";
    cout << "size of map: "<< m.size() << "\n";
    cout << "this should show nothing '" << m["INT"]->to_string() << "'\n";

    field<int> *t_int = NULL;
    field<string> *t_str = NULL;

    cout << event("table=fields",m);
    if(m.size() > 0)
    {
        anyfield * p = m.begin()->second;
        if (t_int = dynamic_cast<field<int> *>(p))
        {
            t_int->set(1984);
        }
        else if (t_str = dynamic_cast<field<string>*>(p))
        {
            t_str->set("1984");
        }
    }
    cout << event("table=fields",m);
}

template<class T>
string field<T>::to_string()
{
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
