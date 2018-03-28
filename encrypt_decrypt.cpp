#include <iostream>
#include <sstream>
#include <iomanip>
#include <stdio.h>
#include <cstdlib>
#include <vector>
using namespace std;

const char key[] = "*|\\|[!@7$[)+"; //Any chars will work

string encryptDecrypt(string toEncrypt) {
	string output = toEncrypt;
	
	for (int i = 0; i < toEncrypt.size(); i++)
		output[i] = toEncrypt[i] ^ key[i % (sizeof(key) / sizeof(char))];
	
	return output;
}

string strOfHex2String(string toDecrypt) {
	ostringstream output;
	char ch;
	//cout << "strOfHex2String \n";
	for (int counter = 0; counter < toDecrypt.size(); counter+= 2)
    {
		
		//cout << toDecrypt.substr(counter, 2);
		ch = char(strtoul(toDecrypt.substr(counter, 2).c_str(), NULL, 16));
		//is >> std::hex  >> ch;
		output << ch;
	}
	return output.str();
}


string toHex(const string& s, bool upper_case = true)
{
    ostringstream ret;

    for (string::size_type i = 0; i < s.length(); ++i)
        ret << std::hex << std::setfill('0') << std::setw(2) << (upper_case ? std::uppercase : std::nouppercase) << (int)s[i];

    return ret.str();
}
//#define CREATE
int main(int argc, const char * argv[])
{
    std::vector<string> secrets;
#if defined CREATE
    string strs [3] = {"guest", "n0b0dy", "sip"};
    for (int i = 0 ; i < 3; i++)
		secrets.push_back(strs[i]);
    //
    for (int s = 0; s < secrets.size(); s++)
    {
	    string encrypted = encryptDecrypt(string(secrets[s]));
	    string hexSecret = toHex(encrypted);
	    cout << "Encrypted: " << hexSecret << "\n";
	}
	secrets.clear();
#else
    string configs [3] = {"4D09390F2F", "444C3E4C3F58", "59152C"};
    for (int i = 0 ; i < 3; i++)
		secrets.push_back(configs[i]);
    for (int s = 0; s < secrets.size(); s++)
    {
		string fromHex = strOfHex2String(secrets[s]);
		//cout << fromHex << "\n";
	    string decrypted = encryptDecrypt(fromHex);
	    cout << "Decrypted: " << decrypted << "\n";
	}
#endif
    return 0;
}
