#include<stdio.h>
int main(int argc,char *argv[],char *envp[]){
    printf("Filename: %s\n",argv[0]);
    for (int i = 0; i < argc; ++i)
        if(i == argc-1) printf("%s",argv[i]);
        else printf("%s,",argv[i]);
    printf("\n");
    return 0;
}
