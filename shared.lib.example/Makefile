gcc -c -Wall -Werror -fpic foo.c
gcc -shared -o libfoo.so foo.o
Step 3: Linking with a shared library
As you can see, that was actually pretty easy. We have a shared library. Let’s compile our main.c and link it with libfoo. We’ll call our final program “test.” Note that the -lfoo option is not looking for foo.o, but libfoo.so. GCC assumes that all libraries start with ‘lib’ and end with .so or .a (.so is for shared object or shared libraries, and .a is for archive, or statically linked libraries).
gcc -L`pwd` -Wall -o test main.c -lfoo



Step 4: Making the library available at runtime
Using LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH
#LD_LIBRARY_PATH=/home/username/foo:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=`pwd`:$LD_LIBRARY_PATH
