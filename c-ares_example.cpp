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

int
main(void)
{
    ares_channel channel;
    int status;
    struct ares_options options;
    int optmask = 0;

    status = ares_library_init(ARES_LIB_INIT_ALL);
    if (status != ARES_SUCCESS){
        printf("ares_library_init: %s\n", ares_strerror(status));
        return 1;
    }
    //options.sock_state_cb_data;
    options.sock_state_cb = state_cb;
    optmask |= ARES_OPT_SOCK_STATE_CB;

    status = ares_init_options(&channel, &options, optmask);
    if(status != ARES_SUCCESS) {
        printf("ares_init_options: %s\n", ares_strerror(status));
        return 1;
    }

    ares_gethostbyname(channel, "google.com", AF_INET, callback, NULL);
    //ares_gethostbyname(channel, "google.com", AF_INET6, callback, NULL);
    wait_ares(channel);
    ares_destroy(channel);
    ares_library_cleanup();
    printf("fin\n");
    return 0;
}
