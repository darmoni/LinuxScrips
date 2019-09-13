// $Id$ $Date$

//this is a commented line

#include <iostream>
#include <sstream>
using namespace std;

std::string& ltrim(std::string& str, const std::string& chars = "\t\n\v\f\r ")
{
    str.erase(0, str.find_first_not_of(chars));
    return str;
}

std::string& rtrim(std::string& str, const std::string& chars = "\t\n\v\f\r ")
{
    str.erase(str.find_last_not_of(chars) + 1);
    return str;
}

std::string& trim(std::string& str, const std::string& chars = "\t\n\v\f\r ")
{
    return ltrim(rtrim(str, chars), chars);
}

int main(void)
{
    string s(" \t \n This string has leading, and trailing white-space chars   \n");
    string replacing(" has ");
    cout << "Before trim \n'" << s << "'\n";
    trim(s);
    auto pos = s.find(replacing);

    cout << "pos =" << pos << "\n";


    cout << "After trim\n'" << s.replace(0, 4, "That").replace(pos,5, " had ") << "'\n";
    //cout << "After trim\n'" << s.replace(pos,5, " had ") << "'\n";
    return 0;
}
