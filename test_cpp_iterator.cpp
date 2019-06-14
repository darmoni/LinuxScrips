/* $Id$ $Date$
 */

#include <map>
#include <iostream>


using namespace std;
typedef map<unsigned, int> unsiged_int_map;

int main(int argc, char ** argv)
{
    unsiged_int_map my_map;
    my_map[19] =119;
    my_map[12] =112;
    my_map[1]  = 12;
    my_map[15] =115;
    auto ti = my_map.find(12);
    if (ti != my_map.end())
    {
        cout << "Found " << ti->second << "\n";
        --ti;
        //--ti;
        if ( ti == my_map.end())
        {
            cout << "loop counter countdowned \n";
            return 0;
        }
        else
        {
            do
            {
                cout << "running " << ti->second << "\n";
            }
            while (0 < --ti->second );
        }
        return 0;
    }
    cout << "Not Found" << "\n";
    return 0;
}

/*
 * make test_cpp_iterator && ./test_cpp_iterator
 * g++ -std=gnu++17 -pthread     test_cpp_iterator.cpp   -o test_cpp_iterator
 * Found 112
 * running 12
 * running 11
 * running 10
 * running 9
 * running 8
 * running 7
 * running 6
 * running 5
 * running 4
 * running 3
 * running 2
 * running 1
 */
