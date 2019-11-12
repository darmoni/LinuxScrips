// CPP code to illustrate 
// erase(iterator pos, iterator end) 

#include <iostream>
#include <map>
#include <string>
using namespace std;


class Demo {
    public:
        void before(string str) const
        {
            cout << "Before erase : ";
            cout << str << endl;
        }
        void after(string str) const
        {
            cout << "After erase : ";
            cout << "'" << str << "'";
        }
        virtual void erase(string) = 0;
};

class Syntax1: public Demo
{
    public:
        void erase(string str)
        {
            Demo::before(str);
            // Deletes all characters
            str.erase();
            Demo::after(str);
        }
};


class Syntax2: public Demo
{
    public:
        void erase(string str)
        {
            Demo::before(str);
            // Deletes all characters except first one
            str.erase(1);
            Demo::after(str);
        }
};


class Syntax3: public Demo
{
    public:
        void erase(string str)
        {
            Demo::before(str);
            // Deletes 4 characters from index number 1
            str.erase(1, 4);
            Demo::after(str);
        }
};


class Syntax4: public Demo
{
    public:
        void erase(string str)
        {
            Demo::before(str);
            // Deletes character at position 4
            str.erase(str.begin() + 4);
            Demo::after(str);
        }
};


class Syntax5: public Demo
{
    public:
        void erase(string str)
        {
            Demo::before(str);
            // Deletes all characters between 0th index and
            // str.end() - 6 
            str.erase(str.begin() + 0, str.end() - 6);
            Demo::after(str);
        }
};

class space: public Demo
{
    public:
        void erase(string str)
        {
            Demo::before(str);
            // Deletes all characters from ' ' to the end, if found in str
            size_t space = str.find(' ');
            if( space != string::npos )
                str.erase(space);
            Demo::after(str);
        }
};


// Driver code 
int main()
{
    map<string, Demo& > syntaxes;

    space space;
    syntaxes.emplace("space", space);
    Syntax1 demo1;
    syntaxes.emplace("Syntax1", demo1);
    Syntax2 demo2;
    syntaxes.emplace("Syntax2", demo2);
    Syntax3 demo3;
    syntaxes.emplace("Syntax3", demo3);
    Syntax4 demo4;
    syntaxes.emplace("Syntax4", demo4);
    Syntax5 demo5;
    syntaxes.emplace("Syntax5", demo5);

	string str("Hello World!");

    for ( auto iter : syntaxes)
    {
        string mystr = str;
        cout << iter.first << " : " << endl;
        iter.second.erase(mystr);
	    cout << endl;
    }

	return 0;
} 
