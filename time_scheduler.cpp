#include <iostream>
#include <string>
#include <unistd.h>
using namespace std;
int main(int args, char * argv[]){
    string comm = "python test_scheduler.py";
    const char * command = comm.c_str();
    system(command);
    pid_t mp = fork();

    return 0;
};