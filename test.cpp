// $Id$ $Date$

//this is a commented line

#include <iostream>
#include <sstream>
using namespace std;


/*
 * C++ Reserved or Non-graphic Characters
 *
 *
 | C haracter | ASCII Representation | ASCII Value | Escape Sequence |
 | ---------- | --------------------- | ----------- | --------------- |
 | Newline | NL (LF) | 10 | \n |
 | Horizontal tab | HT | 9 | \t |
 | Vertical tab | VT | 11 | \v |
 | Backspace | BS | 8 | \b |
 | Carriage return | CR | 13 | \r |
 | Formfeed | FF | 12 | \f |
 | Alert | BEL | 7 | \a |
 | Backslash | \ | 92 | \\ |
 | Question mark | ? | 63 | \? |
 | Single quotation mark | ' | 39 | \' |
 | Double quotation mark | " | 34 | \" |
 | Octal number | ooo | -- | \ooo |
 | Hexadecimal number | hhh | -- | \xhhh |
 | Null character | NUL | 0 | \0 |

*/
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
    string s(" \t \n This string has leading, \r\fand\vtrailing white-space charsending here\n");
    string replacing(" has ");
    cout << "Before trim \n'" << s << "'\n";
    trim(s);
    auto pos = s.find(replacing);

    cout << "pos =" << pos << "\n";


    cout << "After trim\n'" << s.replace(0, 4, "That").replace(pos,5, " had ") << "'\n";
    //cout << "After trim\n'" << s.replace(pos,5, " had ") << "'\n";
    return 0;
}
