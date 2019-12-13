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
void test_syntax_bool (bool val)
{
    string answer = (-1 == val)?"-1": "Other value (Not -1)";
    string sval = (val)? "True" : "False";
    cout << "test_syntax_bool (-1 == " << sval << ") returned " << answer << "\n";
}

std::string remove_ctrl(std::string const& s) {
    std::string result;
    for (int i=0; i<s.length(); ++i) {
        if (s[i] >= 0x20)
            result += s[i];
    }
    return result;
}

void remove_ctrl_cstrings(char* destp, char const* srcp, size_t size) {
    for (size_t i=0; i<size; ++i) {
        if (srcp[i] >= 0x20)
            *destp++ = srcp[i];
    }
    *destp = 0;
}

void remove_ctrl_ref_result_it(std::string& result, std::string const& s)
{
    result.clear();
    result.reserve(s.length());
    for (auto it=s.begin(),end=s.end(); it != end; ++it) {
        if (*it >= 0x20)
            result += *it;
    }
}


int main(void)
{
    string result;
    const unsigned loops = 30000;
    char fooresr [2000];
    char foo[] = "This small change has a dramatic effect on performance.\n"
    "The same timing test now showed an average of only 1.72 microseconds per call, a 13x improvement.\n"
    "This improvement comes from eliminating all the calls to allocate temporary string objects to hold "
    "the concatenation expression result, and the associated copying and deleting of temporaries.\n"
    "Depending on the string implementation, allocation and copying on assignment are also eliminated";

    const string foostr (foo);

    for( int i = 0; i < loops; ++i )
    {
        ;//remove_ctrl_cstrings(fooresr, foo, foostr.size());
    }

    for( int i = 0; i < loops; ++i )
    {
        ;//remove_ctrl_ref_result_it(result, foo);
    }

    for( int i = 0; i < loops; ++i )
    {
        remove_ctrl_cstrings(fooresr, foo, foostr.size());
        remove_ctrl_ref_result_it(result, foo);
        remove_ctrl(foostr);
    }
    return (0);




    for( int val = -1; val < 2; ++val)
    {
        cout << "test_syntax_bool (" << val << ")\n";
        test_syntax_bool(val);
    }
    cout << "\n";

    test_syntax_bool (-1);
    test_syntax_bool (false);
    test_syntax_bool (true);

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
