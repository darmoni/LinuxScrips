/* $Id$ $Date$
 */
#include <ares.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdarg.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <iostream>
#include <vector>

#define BYTE_OK(x) ((x) >= 0 && (x) <= 255)

static uint32_t is_addr(const char *str)
{
    int a0, a1, a2, a3, num, length= 0;
    uint32_t s_addr =0;

    num = sscanf(str,"%3d.%3d.%3d.%3d%n",&a0,&a1,&a2,&a3,&length);
    if( (num == 4) &&
        BYTE_OK(a0) && BYTE_OK(a1) && BYTE_OK(a2) && BYTE_OK(a3) &&
        length >= (3+4))
    {
        char buf[120];
        sprintf(buf, "%d.%d.%d.%d\n",a0,a1,a2,a3);
        std::cout << "is_addr(" << str << ") got " << buf << "\n";
        std::cout << "s_addr = " << s_addr << "\n";
        s_addr += a0;
        std::cout << "s_addr = " << s_addr << "\n";
        s_addr <<= 8;
        std::cout << "s_addr = " << s_addr << "\n";
        s_addr += a1;
        std::cout << "s_addr = " << s_addr << "\n";
        s_addr <<= 8;
        std::cout << "s_addr = " << s_addr << "\n";
        s_addr += a2;
        std::cout << "s_addr = " << s_addr << "\n";
        s_addr <<= 8;
        std::cout << "s_addr = " << s_addr << "\n";
        s_addr += a3;
        std::cout << "s_addr = " << s_addr << "\n";
        //*end = str + length;
    }
    return s_addr;
}

static void destroy_addr_list(struct ares_addr_node *head)
{
    while(head)
    {
        struct ares_addr_node *detached = head;
        head = head->next;
        free(detached);
    }
}

static void append_addr_list(struct ares_addr_node **head,
                             struct ares_addr_node *node)
{
    struct ares_addr_node *last;
    node->next = NULL;
    if(*head)
    {
        last = *head;
        while(last->next)
            last = last->next;
        last->next = node;
    }
    else
        *head = node;
}

static void
state_cb(void *data, int s, int read, int write)
{
    printf("Change state fd %d read:%d write:%d\n", s, read, write);
}


static void
callback(void *arg, int status, int timeouts, struct hostent *host)
{

    if(!host || status != ARES_SUCCESS){
        printf("Failed to lookup %s\n", ares_strerror(status));
        return;
    }

    printf("Found address name %s\n", host->h_name);
    char ip[INET6_ADDRSTRLEN];
    int i = 0;

    for (i = 0; host->h_addr_list[i]; ++i) {
        inet_ntop(host->h_addrtype, host->h_addr_list[i], ip, sizeof(ip));
        printf("%s\n", ip);
    }
}

static void
wait_ares(ares_channel channel)
{
    for(;;){
        struct timeval *tvp, tv;
        fd_set read_fds, write_fds;
        int nfds;

        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        nfds = ares_fds(channel, &read_fds, &write_fds);
        if(nfds == 0){
            break;
        }
        tvp = ares_timeout(channel, NULL, &tv);
        select(nfds, &read_fds, &write_fds, NULL, tvp);
        ares_process(channel, &read_fds, &write_fds);
    }
}
using namespace std;
#define BUF_SIZE 500
int
main(void)
{
    ares_channel channel;
    int status;
    struct ares_options options;
    std::vector<const char*> server_names= {"10.10.10.226", "8.8.8.8"};

    struct ares_addr_node *servers = NULL;
    /* User-specified name servers override default ones. */
    struct ares_addr_node * srvr = (struct ares_addr_node *)(malloc(sizeof(struct ares_addr_node)));
    struct hostent *hostent;
    int optmask = 0;

    for (auto optarg = server_names.begin() ; optarg != server_names.end(); optarg++)
    {
        cout << *optarg << "\n";
        struct addrinfo hints;
        struct addrinfo *result, *rp;
        int sfd, s, j;
        size_t len;
        ssize_t nread;
        char buf[BUF_SIZE];
        /* Obtain address(es) matching host/port */

        memset(&hints, 0, sizeof(struct addrinfo));
        hints.ai_family = AF_UNSPEC;    /* Allow IPv4 or IPv6 */
        hints.ai_socktype = SOCK_DGRAM; /* Datagram socket */
        hints.ai_flags = 0;
        hints.ai_protocol = 0;          /* Any protocol */
        const char PORT[] = "12345";

        s = getaddrinfo(*optarg, PORT, &hints, &result);
        if (s != 0) {
            fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(s));
            exit(EXIT_FAILURE);
        }

        if (!srvr)
        {
            fprintf(stderr, "Line %d, Out of memory!\n",__LINE__);
            destroy_addr_list(servers);
            return 1;
        }
        append_addr_list(&servers, srvr);
        if (ares_inet_pton(AF_INET, *optarg, &srvr->addr.addr4) > 0)
            srvr->family = AF_INET;
        else if (ares_inet_pton(AF_INET6, *optarg, &srvr->addr.addr6) > 0)
            srvr->family = AF_INET6;
        else
        {
            hostent = getaddrinfo(*optarg);
            if (!hostent)
            {
                fprintf(stderr, "adig: server %s not found.\n", *optarg);
                destroy_addr_list(servers);
                return 1;
            }
            switch (hostent->h_addrtype)
            {
                case AF_INET:
                    srvr->family = AF_INET;
                    memcpy(&srvr->addr.addr4, hostent->h_addr,
                        sizeof(srvr->addr.addr4));
                    break;
                case AF_INET6:
                    srvr->family = AF_INET6;
                    memcpy(&srvr->addr.addr6, hostent->h_addr,
                        sizeof(srvr->addr.addr6));
                    break;
                default:
                    fprintf(stderr,
                            "adig: server %s unsupported address family.\n", *optarg);
                    destroy_addr_list(servers);
                    return 1;
            }
        }
    }
    /* Notice that calling ares_init_options() without servers in the
     * options struct and with ARES_OPT_SERVERS set simultaneously in
     * the options mask, results in an initialization with no servers.
     * When alternative name servers have been specified these are set
     * later calling ares_set_servers() overriding any existing server
     * configuration. To prevent initial configuration with default
     * servers that will be discarded later, ARES_OPT_SERVERS is set.
     * If this flag is not set here the result shall be the same but
     * ares_init_options() will do needless work. */
    optmask |= ARES_OPT_SERVERS;


    //struct in_addr servers[] ={"10.10.10.226", "8.8.8.8"};
    status = ares_library_init(ARES_LIB_INIT_ALL);
    if (status != ARES_SUCCESS){
        printf("ares_library_init: %s\n", ares_strerror(status));
        return 1;
    }
    //options.sock_state_cb_data;
    options.sock_state_cb = state_cb;
    optmask |= ARES_OPT_SOCK_STATE_CB;
    //optmask |= ARES_OPT_SERVERS;

    status = ares_init_options(&channel, &options, optmask);
    if(status != ARES_SUCCESS) {
        printf("ares_init_options: %s\n", ares_strerror(status));
        return 1;
    }
    if(servers)
    {
        status = ares_set_servers(channel, servers);
        destroy_addr_list(servers);
        if (status != ARES_SUCCESS)
        {
            fprintf(stderr, "ares_init_options: %s\n",
                    ares_strerror(status));
            return 1;
        }
    }

    //int default_servers = ares_get_servers(channel, &servers);
    ares_gethostbyname(channel, "google.com", AF_INET, callback, NULL);
    //ares_gethostbyname(channel, "google.com", AF_INET6, callback, NULL);
    wait_ares(channel);
    ares_destroy(channel);
    ares_library_cleanup();
    printf("fin\n");
    return 0;
}
