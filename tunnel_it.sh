# Using sudo
TRYUNNEL=0
if [ ! $(pgrep -f vpnc-connect) ]; then sudo vpnc-connect default; sudo ufw enable
ssh nir@ubuntu-darmoni.xcastlabs.com 'nohup  ~/bin/start_rpmbuilds.sh &'
else echo 'VPN is Already on'; \
TRYUNNEL=1
ssh nir@ubuntu-darmoni.xcastlabs.com 'ls -l > /dev/null'
fi

if [ "1" != "$TRYUNNEL" ] ; then echo "done";
else if [ $(pgrep -f 'ssh -D ') ]
	then echo 'Tunnel is already on';
	else ssh -D 1080  nir@10.10.10.55;
	fi
fi

