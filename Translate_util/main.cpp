#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>

using namespace std;

int main()
{
    fstream inf("./input.txt"), outf;
    string content, tmp, filename;
    stringstream ss;
    int index = 1;
    while(getline(inf, tmp))
    {
        content+=tmp+' ';
        // int num = count(content.begin(),content.end(),' ');
        int num = content.length();
        if (num > 4600)
        {
            ss.str("");
            ss<<index++;
            string filename = "./output"+ss.str()+".txt";
            outf.open(filename.c_str(), ios::out);
            outf << content;
            outf.close();
            content.clear();
        }
    }
    inf.close();
    ss.str("");
    ss<<index;
    filename = "./output"+ss.str()+".txt";
    outf.open(filename.c_str(), ios::out);
    outf << content;
    outf.close();
    return 0;
}
