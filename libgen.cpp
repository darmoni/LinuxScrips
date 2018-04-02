#include <libgen.h>
#include <string.h>
#include <iostream>

using namespace std;
int break_path(const string & fullpath, string & _basename, string & ext, string & _dirname, string & new_fullpath, string replace_ext="")
{
    char p_file_path [200];
    strncpy(p_file_path,fullpath.c_str(),fullpath.size()+1);
    _basename.assign(basename(p_file_path));
    _dirname.assign(dirname(p_file_path));
    ext.assign("");
    std::size_t found = _basename.rfind(".");
    new_fullpath.assign(_dirname+'/'+_basename);        
    if (found!=std::string::npos)                   // extention exists
    {
        ext.assign(_basename.substr(found+1));
        if(replace_ext.size() == 0){
            return 3;
        }
        else                                        // extention exists, and we replace it
        {
            _basename.replace(_basename.find(ext),ext.length(),replace_ext);
            ext.assign(replace_ext);
            new_fullpath.assign(_dirname+'/'+_basename);
            return 4;
        }
    }
    if(replace_ext.size() > 0){                     // no extention, adding if we have a replace_ext
        _basename.append('.'+replace_ext);
        ext.assign(replace_ext);
        new_fullpath.assign(_dirname+'/'+_basename);        
        return 3;
    }
    return 2;
}

int main(int, char * [])
{
    string file_path="siptalk64.xcastlabs.com/ee/voicemail-25513.video";
    string base, dir, ext, new_name;
    
    int counter=0;
    counter=break_path(file_path, base, ext, dir, new_name,"h264");
    if(counter > 0)
    {
        cout << counter << " , " << file_path << " , " << base<< " , " << ext<< " , " << dir << "\n";
        cout << "New file name = " << new_name << "\n";
    }
    counter=break_path(file_path, base, ext, dir, new_name/*,"h264"*/);
    if(counter > 0)
    {
        cout << counter << " , " << file_path << " , " << base<< " , " << ext<< " , " << dir << "\n";
        cout << "New file name = " << new_name << "\n";
    }
    counter=break_path("siptalk64.xcastlabs.com/ee/voicemail-25513", base, ext, dir, new_name/*,"h264"*/);
    if(counter > 0)
    {
        cout << counter << " , " << file_path << " , " << base<< " , " << ext<< " , " << dir << "\n";
        cout << "New file name = " << new_name << "\n";
    }
    counter=break_path("siptalk64.xcastlabs.com/ee/voicemail-25513", base, ext, dir, new_name,"h264");
    if(counter > 0)
    {
        cout << counter << " , " << file_path << " , " << base<< " , " << ext<< " , " << dir << "\n";
        cout << "New file name = " << new_name << "\n";
    }
    char p_file_path [file_path.size()+1];
    strncpy(p_file_path,file_path.c_str(),file_path.size()+1);
    return 0;
    std::cout << "original file_path '" << p_file_path << "'\n";
    std::cout << "basename '" << basename(p_file_path) << "' Correct\n";
    std::cout << "dirname '" << dirname(p_file_path) << "' Correct\n";
    //strncpy(p_file_path,file_path.c_str(),file_path.size());
    std::cout << "basename '" << basename(p_file_path) << "' Oops!!! Let's fix that:\n";
    strncpy(p_file_path,file_path.c_str(),file_path.size());
    std::cout << "dirname '" << dirname(p_file_path) << "' Correct\n";
    strncpy(p_file_path,file_path.c_str(),file_path.size());
    std::cout << "basename '" << basename(p_file_path) << "' Correct\n";;
    std::cout << "basename '" << basename(p_file_path) << "' Correct\n";;
    std::cout << "original file_path '" << file_path << "'\n";    
}
