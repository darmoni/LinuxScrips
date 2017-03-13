#include <stdio.h>
#include <stdlib.h>
#include <iostream>


const char * s1 = "test";
const char * s2 = "test";
char s3[] = "test";
char s4[] = "test";
char * const s5 = s4;
char * const s6 = "test";
int main()
{
printf("Hello World!\n");
// s1[0] = 'a'; FORBIDDEN
printf("s1=%s, s2=%s\n",s1,s2);
char const * const s7(++s2);
printf("s3=%s, s4=%s\n",s3,s4);
printf("s5=%s, s6=%s, s7=%s\n",s5,s6,s7);
s1++;
s3[0] = 'a';
//s4++; // FORBIDDEN
s5[0] = 'a';
//s6[0] = 'a'; // core dump
//s6++; // FORBIDDEN
//s7++; // FORBIDDEN
printf("s1=%s, s2=%s\n",s1,s2);
printf("s3=%s, s4=%s\n",s3,s4);
printf("s5=%s, s6=%s, s7=%s\n",s5,s6,s7);
}
