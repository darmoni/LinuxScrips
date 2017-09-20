test_hardlink: errnos.txt errnos.awk test_hardlink.cpp Makefile
	g++     test_hardlink.cpp -o test_hardlink

errnos.txt : /usr/include/asm-generic/errno-base.h /usr/include/asm-generic/errno.h Makefile errnos.awk
	@(cat /usr/include/asm-generic/errno-base.h /usr/include/asm-generic/errno.h | awk -f errnos.awk > errnos.txt)
