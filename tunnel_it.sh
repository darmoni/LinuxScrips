# Using sudo
if [ "" == "$(pgrep -f vpnc-connect)" ]; then sudo vpnc-connect default
else echo 'VPN is Already on'; \
ssh nir@ubuntu-darmoni.xcastlabs.com 'ls -l > /dev/null'
[[ $(pgrep -f 'ssh -D ') ]] && echo 'Tunnel is already on' || ssh -D 1080  xcast@10.10.10.31
fi
