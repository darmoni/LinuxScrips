/*

cat test_hardlink.cpp | awk '/#define E/ {print "errors[" $3 "]=\"" $0 "}\";"}'

*/

/*
/usr/include/asm-generic/errno-base.h

#define EPERM        1  // Operation not permitted * /
#define ENOENT       2  // No such file or directory * /
#define ESRCH        3  // No such process * /
#define EINTR        4  // Interrupted system call * /
#define EIO      5  // I/O error * /
#define ENXIO        6  // No such device or address * /
#define E2BIG        7  // Argument list too long * /
#define ENOEXEC      8  // Exec format error * /
#define EBADF        9  // Bad file number * /
#define ECHILD      10  // No child processes * /
#define EAGAIN      11  // Try again * /
#define ENOMEM      12  // Out of memory * /
#define EACCES      13  // Permission denied * /
#define EFAULT      14  // Bad address * /
#define ENOTBLK     15  // Block device required * /
#define EBUSY       16  // Device or resource busy * /
#define EEXIST      17  // File exists * /
#define EXDEV       18  // Cross-device link * /
#define ENODEV      19  // No such device * /
#define ENOTDIR     20  // Not a directory * /
#define EISDIR      21  // Is a directory * /
#define EINVAL      22  // Invalid argument * /
#define ENFILE      23  // File table overflow * /
#define EMFILE      24  // Too many open files * /
#define ENOTTY      25  // Not a typewriter * /
#define ETXTBSY     26  // Text file busy * /
#define EFBIG       27  // File too large * /
#define ENOSPC      28  // No space left on device * /
#define ESPIPE      29  // Illegal seek * /
#define EROFS       30  // Read-only file system * /
#define EMLINK      31  // Too many links * /
#define EPIPE       32  // Broken pipe * /
#define EDOM        33  // Math argument out of domain of func * /
#define ERANGE      34  // Math result not representable * /


/usr/include/asm-generic/errno.h
#ifndef _ASM_GENERIC_ERRNO_H
#define _ASM_GENERIC_ERRNO_H

#include <asm-generic/errno-base.h>

#define EDEADLK     35  // Resource deadlock would occur * /
#define ENAMETOOLONG    36  // File name too long * /
#define ENOLCK      37  // No record locks available * /
#define ENOSYS      38  // Function not implemented * /
#define ENOTEMPTY   39  // Directory not empty * /
#define ELOOP       40  // Too many symbolic links encountered * /
#define EWOULDBLOCK EAGAIN  // Operation would block * /
#define ENOMSG      42  // No message of desired type * /
#define EIDRM       43  // Identifier removed * /
#define ECHRNG      44  // Channel number out of range * /
#define EL2NSYNC    45  // Level 2 not synchronized * /
#define EL3HLT      46  // Level 3 halted * /
#define EL3RST      47  // Level 3 reset * /
#define ELNRNG      48  // Link number out of range * /
#define EUNATCH     49  // Protocol driver not attached * /
#define ENOCSI      50  // No CSI structure available * /
#define EL2HLT      51  // Level 2 halted * /
#define EBADE       52  // Invalid exchange * /
#define EBADR       53  // Invalid request descriptor * /
#define EXFULL      54  // Exchange full * /
#define ENOANO      55  // No anode * /
#define EBADRQC     56  // Invalid request code * /
#define EBADSLT     57  // Invalid slot * /

#define EDEADLOCK   EDEADLK

#define EBFONT      59  // Bad font file format * /
#define ENOSTR      60  // Device not a stream * /
#define ENODATA     61  // No data available * /
#define ETIME       62  // Timer expired * /
#define ENOSR       63  // Out of streams resources * /
#define ENONET      64  // Machine is not on the network * /
#define ENOPKG      65  // Package not installed * /
#define EREMOTE     66  // Object is remote * /
#define ENOLINK     67  // Link has been severed * /
#define EADV        68  // Advertise error * /
#define ESRMNT      69  // Srmount error * /
#define ECOMM       70  // Communication error on send * /
#define EPROTO      71  // Protocol error * /
#define EMULTIHOP   72  // Multihop attempted * /
#define EDOTDOT     73  // RFS specific error * /
#define EBADMSG     74  // Not a data message * /
#define EOVERFLOW   75  // Value too large for defined data type * /
#define ENOTUNIQ    76  // Name not unique on network * /
#define EBADFD      77  // File descriptor in bad state * /
#define EREMCHG     78  // Remote address changed * /
#define ELIBACC     79  // Can not access a needed shared library * /
#define ELIBBAD     80  // Accessing a corrupted shared library * /
#define ELIBSCN     81  // .lib section in a.out corrupted * /
#define ELIBMAX     82  // Attempting to link in too many shared libraries * /
#define ELIBEXEC    83  // Cannot exec a shared library directly * /
#define EILSEQ      84  // Illegal byte sequence * /
#define ERESTART    85  // Interrupted system call should be restarted * /
#define ESTRPIPE    86  // Streams pipe error * /
#define EUSERS      87  // Too many users * /
#define ENOTSOCK    88  // Socket operation on non-socket * /
#define EDESTADDRREQ    89  // Destination address required * /
#define EMSGSIZE    90  // Message too long * /
#define EPROTOTYPE  91  // Protocol wrong type for socket * /
#define ENOPROTOOPT 92  // Protocol not available * /
#define EPROTONOSUPPORT 93  // Protocol not supported * /
#define ESOCKTNOSUPPORT 94  // Socket type not supported * /
#define EOPNOTSUPP  95  // Operation not supported on transport endpoint * /
#define EPFNOSUPPORT    96  // Protocol family not supported * /
#define EAFNOSUPPORT    97  // Address family not supported by protocol * /
#define EADDRINUSE  98  // Address already in use * /
#define EADDRNOTAVAIL   99  // Cannot assign requested address * /
#define ENETDOWN    100 // Network is down * /
#define ENETUNREACH 101 // Network is unreachable * /
#define ENETRESET   102 // Network dropped connection because of reset * /
#define ECONNABORTED    103 // Software caused connection abort * /
#define ECONNRESET  104 // Connection reset by peer * /
#define ENOBUFS     105 // No buffer space available * /
#define EISCONN     106 // Transport endpoint is already connected * /
#define ENOTCONN    107 // Transport endpoint is not connected * /
#define ESHUTDOWN   108 // Cannot send after transport endpoint shutdown * /
#define ETOOMANYREFS    109 // Too many references: cannot splice * /
#define ETIMEDOUT   110 // Connection timed out * /
#define ECONNREFUSED    111 // Connection refused * /
#define EHOSTDOWN   112 // Host is down * /
#define EHOSTUNREACH    113 // No route to host * /
#define EALREADY    114 // Operation already in progress * /
#define EINPROGRESS 115 // Operation now in progress * /
#define ESTALE      116 // Stale NFS file handle * /
#define EUCLEAN     117 // Structure needs cleaning * /
#define ENOTNAM     118 // Not a XENIX named type file * /
#define ENAVAIL     119 // No XENIX semaphores available * /
#define EISNAM      120 // Is a named type file * /
#define EREMOTEIO   121 // Remote I/O error * /
#define EDQUOT      122 // Quota exceeded * /

#define ENOMEDIUM   123 // No medium found * /
#define EMEDIUMTYPE 124 // Wrong medium type * /
#define ECANCELED   125 // Operation Canceled * /
#define ENOKEY      126 // Required key not available * /
#define EKEYEXPIRED 127 // Key has expired * /
#define EKEYREVOKED 128 // Key has been revoked * /
#define EKEYREJECTED    129 // Key was rejected by service * /

// for robust mutexes * /
#define EOWNERDEAD  130 // Owner died * /
#define ENOTRECOVERABLE 131 // State not recoverable * /

#endif
#endif * /
*/

#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <map>
#include <iostream>
using namespace std;

map<int,string> errors;
void map_errors() {
    //errors[0]="cat test_hardlink.cpp | awk '/#define E/ {print "errors[" $3 "]=\"" $0 "}\";"}' }";
    errors[1]="#define EPERM        1  // Operation not permitted * / }";
    errors[2]="#define ENOENT       2  // No such file or directory * /}";
    errors[3]="#define ESRCH        3  // No such process * /}";
    errors[4]="#define EINTR        4  // Interrupted system call * /}";
    errors[5]="#define EIO      5  // I/O error * /}";
    errors[6]="#define ENXIO        6  // No such device or address * /}";
    errors[7]="#define E2BIG        7  // Argument list too long * /}";
    errors[8]="#define ENOEXEC      8  // Exec format error * /}";
    errors[9]="#define EBADF        9  // Bad file number * /}";
    errors[10]="#define ECHILD      10  // No child processes * /}";
    errors[11]="#define EAGAIN      11  // Try again * /}";
    errors[12]="#define ENOMEM      12  // Out of memory * /}";
    errors[13]="#define EACCES      13  // Permission denied * /}";
    errors[14]="#define EFAULT      14  // Bad address * /}";
    errors[15]="#define ENOTBLK     15  // Block device required * /}";
    errors[16]="#define EBUSY       16  // Device or resource busy * /}";
    errors[17]="#define EEXIST      17  // File exists * /}";
    errors[18]="#define EXDEV       18  // Cross-device link * /}";
    errors[19]="#define ENODEV      19  // No such device * /}";
    errors[20]="#define ENOTDIR     20  // Not a directory * /}";
    errors[21]="#define EISDIR      21  // Is a directory * /}";
    errors[22]="#define EINVAL      22  // Invalid argument * /}";
    errors[23]="#define ENFILE      23  // File table overflow * /}";
    errors[24]="#define EMFILE      24  // Too many open files * /}";
    errors[25]="#define ENOTTY      25  // Not a typewriter * /}";
    errors[26]="#define ETXTBSY     26  // Text file busy * /}";
    errors[27]="#define EFBIG       27  // File too large * /}";
    errors[28]="#define ENOSPC      28  // No space left on device * /}";
    errors[29]="#define ESPIPE      29  // Illegal seek * /}";
    errors[30]="#define EROFS       30  // Read-only file system * /}";
    errors[31]="#define EMLINK      31  // Too many links * /}";
    errors[32]="#define EPIPE       32  // Broken pipe * /}";
    errors[33]="#define EDOM        33  // Math argument out of domain of func * /}";
    errors[34]="#define ERANGE      34  // Math result not representable * /}";
    errors[35]="#define EDEADLK     35  // Resource deadlock would occur * /}";
    errors[36]="#define ENAMETOOLONG    36  // File name too long * /}";
    errors[37]="#define ENOLCK      37  // No record locks available * /}";
    errors[38]="#define ENOSYS      38  // Function not implemented * /}";
    errors[39]="#define ENOTEMPTY   39  // Directory not empty * /}";
    errors[40]="#define ELOOP       40  // Too many symbolic links encountered * /}";
    errors[EAGAIN]="#define EWOULDBLOCK EAGAIN  // Operation would block * /}";
    errors[42]="#define ENOMSG      42  // No message of desired type * /}";
    errors[43]="#define EIDRM       43  // Identifier removed * /}";
    errors[44]="#define ECHRNG      44  // Channel number out of range * /}";
    errors[45]="#define EL2NSYNC    45  // Level 2 not synchronized * /}";
    errors[46]="#define EL3HLT      46  // Level 3 halted * /}";
    errors[47]="#define EL3RST      47  // Level 3 reset * /}";
    errors[48]="#define ELNRNG      48  // Link number out of range * /}";
    errors[49]="#define EUNATCH     49  // Protocol driver not attached * /}";
    errors[50]="#define ENOCSI      50  // No CSI structure available * /}";
    errors[51]="#define EL2HLT      51  // Level 2 halted * /}";
    errors[52]="#define EBADE       52  // Invalid exchange * /}";
    errors[53]="#define EBADR       53  // Invalid request descriptor * /}";
    errors[54]="#define EXFULL      54  // Exchange full * /}";
    errors[55]="#define ENOANO      55  // No anode * /}";
    errors[56]="#define EBADRQC     56  // Invalid request code * /}";
    errors[57]="#define EBADSLT     57  // Invalid slot * /}";
    errors[EDEADLK]="#define EDEADLOCK   EDEADLK}";
    errors[59]="#define EBFONT      59  // Bad font file format * /}";
    errors[60]="#define ENOSTR      60  // Device not a stream * /}";
    errors[61]="#define ENODATA     61  // No data available * /}";
    errors[62]="#define ETIME       62  // Timer expired * /}";
    errors[63]="#define ENOSR       63  // Out of streams resources * /}";
    errors[64]="#define ENONET      64  // Machine is not on the network * /}";
    errors[65]="#define ENOPKG      65  // Package not installed * /}";
    errors[66]="#define EREMOTE     66  // Object is remote * /}";
    errors[67]="#define ENOLINK     67  // Link has been severed * /}";
    errors[68]="#define EADV        68  // Advertise error * /}";
    errors[69]="#define ESRMNT      69  // Srmount error * /}";
    errors[70]="#define ECOMM       70  // Communication error on send * /}";
    errors[71]="#define EPROTO      71  // Protocol error * /}";
    errors[72]="#define EMULTIHOP   72  // Multihop attempted * /}";
    errors[73]="#define EDOTDOT     73  // RFS specific error * /}";
    errors[74]="#define EBADMSG     74  // Not a data message * /}";
    errors[75]="#define EOVERFLOW   75  // Value too large for defined data type * /}";
    errors[76]="#define ENOTUNIQ    76  // Name not unique on network * /}";
    errors[77]="#define EBADFD      77  // File descriptor in bad state * /}";
    errors[78]="#define EREMCHG     78  // Remote address changed * /}";
    errors[79]="#define ELIBACC     79  // Can not access a needed shared library * /}";
    errors[80]="#define ELIBBAD     80  // Accessing a corrupted shared library * /}";
    errors[81]="#define ELIBSCN     81  // .lib section in a.out corrupted * /}";
    errors[82]="#define ELIBMAX     82  // Attempting to link in too many shared libraries * /}";
    errors[83]="#define ELIBEXEC    83  // Cannot exec a shared library directly * /}";
    errors[84]="#define EILSEQ      84  // Illegal byte sequence * /}";
    errors[85]="#define ERESTART    85  // Interrupted system call should be restarted * /}";
    errors[86]="#define ESTRPIPE    86  // Streams pipe error * /}";
    errors[87]="#define EUSERS      87  // Too many users * /}";
    errors[88]="#define ENOTSOCK    88  // Socket operation on non-socket * /}";
    errors[89]="#define EDESTADDRREQ    89  // Destination address required * /}";
    errors[90]="#define EMSGSIZE    90  // Message too long * /}";
    errors[91]="#define EPROTOTYPE  91  // Protocol wrong type for socket * /}";
    errors[92]="#define ENOPROTOOPT 92  // Protocol not available * /}";
    errors[93]="#define EPROTONOSUPPORT 93  // Protocol not supported * /}";
    errors[94]="#define ESOCKTNOSUPPORT 94  // Socket type not supported * /}";
    errors[95]="#define EOPNOTSUPP  95  // Operation not supported on transport endpoint * /}";
    errors[96]="#define EPFNOSUPPORT    96  // Protocol family not supported * /}";
    errors[97]="#define EAFNOSUPPORT    97  // Address family not supported by protocol * /}";
    errors[98]="#define EADDRINUSE  98  // Address already in use * /}";
    errors[99]="#define EADDRNOTAVAIL   99  // Cannot assign requested address * /}";
    errors[100]="#define ENETDOWN    100 // Network is down * /}";
    errors[101]="#define ENETUNREACH 101 // Network is unreachable * /}";
    errors[102]="#define ENETRESET   102 // Network dropped connection because of reset * /}";
    errors[103]="#define ECONNABORTED    103 // Software caused connection abort * /}";
    errors[104]="#define ECONNRESET  104 // Connection reset by peer * /}";
    errors[105]="#define ENOBUFS     105 // No buffer space available * /}";
    errors[106]="#define EISCONN     106 // Transport endpoint is already connected * /}";
    errors[107]="#define ENOTCONN    107 // Transport endpoint is not connected * /}";
    errors[108]="#define ESHUTDOWN   108 // Cannot send after transport endpoint shutdown * /}";
    errors[109]="#define ETOOMANYREFS    109 // Too many references: cannot splice * /}";
    errors[110]="#define ETIMEDOUT   110 // Connection timed out * /}";
    errors[111]="#define ECONNREFUSED    111 // Connection refused * /}";
    errors[112]="#define EHOSTDOWN   112 // Host is down * /}";
    errors[113]="#define EHOSTUNREACH    113 // No route to host * /}";
    errors[114]="#define EALREADY    114 // Operation already in progress * /}";
    errors[115]="#define EINPROGRESS 115 // Operation now in progress * /}";
    errors[116]="#define ESTALE      116 // Stale NFS file handle * /}";
    errors[117]="#define EUCLEAN     117 // Structure needs cleaning * /}";
    errors[118]="#define ENOTNAM     118 // Not a XENIX named type file * /}";
    errors[119]="#define ENAVAIL     119 // No XENIX semaphores available * /}";
    errors[120]="#define EISNAM      120 // Is a named type file * /}";
    errors[121]="#define EREMOTEIO   121 // Remote I/O error * /}";
    errors[122]="#define EDQUOT      122 // Quota exceeded * /}";
    errors[123]="#define ENOMEDIUM   123 // No medium found * /}";
    errors[124]="#define EMEDIUMTYPE 124 // Wrong medium type * /}";
    errors[125]="#define ECANCELED   125 // Operation Canceled * /}";
    errors[126]="#define ENOKEY      126 // Required key not available * /}";
    errors[127]="#define EKEYEXPIRED 127 // Key has expired * /}";
    errors[128]="#define EKEYREVOKED 128 // Key has been revoked * /}";
    errors[129]="#define EKEYREJECTED    129 // Key was rejected by service * /}";
    errors[130]="#define EOWNERDEAD  130 // Owner died * /}";
    errors[131]="#define ENOTRECOVERABLE 131 // State not recoverable * /}";

}
int main() {

    map_errors();
    string org(__FILE__);
    string temp("/tmp/_" + org);
    if(link (org.c_str(), temp.c_str())){
        int the_errno=errno;
        map<int,string>::iterator the_error_name=errors.find(the_errno);

        cout << "link (" << org << "," << temp << ") failed with errno(" <<  the_errno << ")";
        if(errors.end() != the_error_name) cout << endl << the_error_name->second << endl;
        else cout << endl;
        /*
        char buffer[256];
        sprintf(buffer,"grep ' %d ' %s\n", errno, __FILE__);
        system(buffer);
        cout << "link (__FILE__," << temp << ") failed with errno(" <<  errno << ")\n";
*/
    }
    //cout << "ENOLCK = " << ENOLCK << endl;
}
