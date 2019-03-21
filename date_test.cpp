/* $Id$ $Date$
*/

#include <float.h>
#include <math.h>
#include <stdio.h>

struct A{
    int i;
    char c;
    A(int _i, char _c):i(_i), c(_c){}
};

struct B: public A{
    double d;
    //B(A _a, double _d): A(_a), d(_d){}
    B(int _i, char _c, double _d): A(_i, _c), d(_d){}
};

void print( struct A a)
{
    printf("i= %d, c =%c\n", a.i, a.c);
}

void print( struct B b)
{
    printf("i= %d, c =%c, d= %f\n", b.i, b.c, b.d);
}

int size_of( struct A * p)
{
    printf("sizeof (*p) = %lu\n", sizeof(*p));
}

int size_of( struct B * p)
{
    printf("sizeof (*p) = %lu\n", sizeof(*p));
}


int main(void)
{
    printf("%d\n", FLT_EVAL_METHOD);
    printf("%zu  %zu\n", sizeof(float),sizeof(float_t));
    printf("%zu  %zu\n", sizeof(double),sizeof(double_t));
    struct A a {0,'0'};
    int i = 2;
    char c = 'N';
    double d = 2.0/3;
    struct B bc {i, c, d};
    struct B b {-1, 'M', 3.5/6};
    size_of(&a);
    size_of(&b);
    print(b);
    return 0;
}

