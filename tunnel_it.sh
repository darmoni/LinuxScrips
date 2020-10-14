# if you need to use your in office desktop and have trouble with dns resolution, please hard code your dns settings to have 10.10.10.226 as primary DNS
# fire up vpn
# start tunnel
# make sure browser has proxy pointed to sock5 127.0.0.1 port 1080
# ssh -D 1080  xcast@10.10.10.31
#
# Proxy settings for a browser:
# Manual proxy configuration:
# SOCKS Host 127.0.0.1:1080
# SOCKS v5
# No proxy for: 172.17.42.0/16








# Using sudo
TRYUNNEL=0
if [ ! $(pgrep -f vpnc-connect) ]; then sudo vpnc-connect default; sudo ufw enable
ssh nir@ubuntu-darmoni.xcastlabs.com 'nohup  ~/bin/start_rpmbuilds.sh &' &
else echo 'VPN is Already on'; \
TRYUNNEL=1
ssh nir@ubuntu-darmoni.xcastlabs.com 'ls -l > /dev/null'
fi

if [ "1" != "$TRYUNNEL" ] ; then echo "done";
else if [ $(pgrep -f 'ssh -D ') ]
	then echo 'Tunnel is already on';
	#else ssh -D 1080  nir@10.10.10.55;
	else ssh -D 1080  ndarmoni@10.10.10.31;
	fi
fi

# Using sudo
if [ "" == "$(pgrep -f vpnc-connect)" ]; then sudo vpnc-connect default
else echo 'VPN is Already on'
[[ $(ps -ef | grep 'ssh -D ' | grep -v $$ ) ]] && echo 'Tunnel is already on' || ssh -D 1080  xcast@10.10.10.31
fi
 
   