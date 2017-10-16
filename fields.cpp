/* $Id$ $Date$
*/

#include <vector>       // std::vector
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
};
string event(string table_name, vector<anyfield * > v);

int main ()
{
    vector<anyfield * > v;
    v.push_back(new field<int>("INT",3));
    field<int> *t = new field<int>("INT2",123);
    t->set(15);
    v.push_back(t);
    field<string> *s = new field<string> ("STR","meh");
    s->set("duh");
    v.push_back(s);
    cout << "this should show something '" << s->to_string() << "'\n";
    s->set("okay, Meh");
    cout << "this should show another thing '" << s->to_string() << "'\n";
    cout << "size of vector: "<< v.size() << "\n";
    cout << "this should show nothing '" << t->to_string() << "'\n";
    
    field<int> *t_int = NULL;
    field<string> *t_str = NULL;

    cout << event("table=fields",v);
    anyfield * p = v[0];
    if (t_int = dynamic_cast<field<int> *>(p))
    {
        t_int->set(1984);
    }
    else if (t_str = dynamic_cast<field<string>*>(p))
    {
        t_str->set("1984");
    }
    cout << event("table=fields",v);
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

string event(string table_name, vector<anyfield * > v)
{
    string record="";
    bool empty=true;
    for (int i=0 ; i < v.size(); ++i)
    {
         string delta=v[i]->to_string();
         if(delta.length() == 0) continue;
         if(!empty)record +=';';
         record +=delta;
         empty=false;
    }
    return table_name +" '"+ record + "'\n";
}
