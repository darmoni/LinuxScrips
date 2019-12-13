CXX = g++ -std=gnu++17 -g -O50 -pthread

test_hardlink: test_hardlink.cpp errnos.txt errnos.awk Makefile
	$(CXX)   $(CFLAGS)  $< -o $@

errnos.txt : /usr/include/asm-generic/errno-base.h /usr/include/asm-generic/errno.h Makefile errnos.awk
	@(cat /usr/include/asm-generic/errno-base.h /usr/include/asm-generic/errno.h | awk -f errnos.awk > errnos.txt)

threading_17: threading_17.cpp Makefile
	$(CXX)   $(CFLAGS)  $< -o $@
