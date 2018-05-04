
/* ident $Id$ $Date$ */

#include <iostream>
#include <algorithm>
#include <string>

bool IsQuotesOrLowASCII(char c)
{
    if(c < ' ') return true;
    switch(c)
    {
    case '"':
    case '\'':
        return true;
    default:
        return false;
    }
}

int main()
{
    std::string str="'\"Message Center\"' <blahdi'da\n@nob\to'dy.email.com:";
    str.erase(std::remove_if(str.begin(), str.end(), &IsQuotesOrLowASCII), str.end());
    std::cout << str << "\n";
}
