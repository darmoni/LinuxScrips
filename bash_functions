#!/bin/sh
# $Id$ $Date$
function me {
  echo $LOGNAME
}

export -f me

function log_me () {
    #topic='server'
    topic=${1:-*}
    DBACK=${2:-0}
    TMSTAMP=$(expr `date +%s` - 86400 '*' ${DBACK})
    DAY=$(date +%Y%m%d -d "1970-01-01 UTC ${TMSTAMP} sec")

    #log_name_pattern="$topic*.node*.log"
    log_name_pattern=$topic
    #today=$( date +%Y%m%d)
    logservers='logserver3-la.siptalk.com'
    #logserver_cmd="/usr/bin/ssh xcast@logserver3-la.siptalk.com "
    #for my_mserver in container1-la.xcastlabs.net container2-la.xcastlabs.net ; do
    for my_topic in container*-la.xcastlabs.net pbxdata1n1-la.siptalk.com; do
        for logserver in $logservers ; do
            logserver_cmd="/usr/bin/ssh xcast@$logserver "
            log_name="ls -lSrh logs/servers/$my_topic/$DAY/* | grep $log_name_pattern | grep -v 'job-'"
            CMD="$logserver_cmd '$log_name'"
            #echo $CMD
            #echo
            eval $CMD | grep --color ${topic}
        done
        #echo $ls_log |$SHELL
    done
    echo
    for my_topic in container*-chi.xcastlabs.net; do
        for logserver in  logserver2-chi.siptalk.com; do
            logserver_cmd="/usr/bin/ssh xcast@$logserver "
            log_name="ls -lSrh logs/servers/$my_topic/$DAY/* | grep $log_name_pattern | grep -v 'job-'"
            CMD="$logserver_cmd '$log_name'"
            #echo $CMD
            #echo
            eval $CMD | grep --color ${topic}
        done
        #echo $ls_log |$SHELL
    done

}

function flog () {
    for logserver  in logserver3-la.siptalk.com logserver2-chi.siptalk.com; do
        CMD="/usr/bin/ssh xcast@$logserver flog $*"
        eval $CMD | grep --color ${topic}
    done
}

function flog2 () {
    for logserver  in logserver3-la.siptalk.com logserver2-chi.siptalk.com; do
        CMD="/usr/bin/ssh xcast@$logserver flog2 $*"
        eval $CMD | grep --color ${topic}
        echo
    done
}

function timestamp {

  date +%F-%T
}

export -f timestamp

function refresh {

 . ~/.bashrc
}

export refresh

function funcs {

   readlink -f ~nir/bin/bash_functions
}

export -f funcs


function aliases {

   echo '~/.bash_aliases'
}

export -f aliases

function killadb {

  adb kill-server
}

export -f killadb

function adb_devices {

  adb devices | grep -v 'List of devices attached'| sed 's/\t/_/g' | cut -d '_' -f1
}

export -f adb_devices


function fb_devices {

  fastboot devices | cut -f1
#  echo "fastboot devices | grep -vE 'finished|waiting|Done|OKAY|\.\.\.' | sed 's/\t/_/g' | cut -d '_' -f1 "

}

export -f fb_devices

function ver()
{
 for device in $(adb_devices) ; do
    APver=$(adb -s $device shell getprop ro.build.fingerprint | sed -e "s/.*\[//" -e "s/\]//")
    BPver=$(adb -s $device shell getprop gsm.version.baseband | sed -e "s/.*\[//" -e "s/\]//")
    FSGver=$(adb -s $device shell getprop ril.baseband.config.ver_num | sed -e "s/.*\[//" -e "s/\]//")
    echo "Serial Number: $device"
    echo "AP:  $APver"
    echo "BP:  $BPver"
    echo "FSG: $FSGver"
    done
}

export -f ver

function myfsg {

  cat $TOP/$fsg

}

export -f myfsg

function mymdm {

  cat $TOP/$modem

}

export -f mymdm


function cmp8994 {

   grep -n $* 8994*

}

export -f cmp8994


function root {
   adb root
   adb wait-for-devices
}

export -f root

function unsetup() {

  root
  adb shell sqlite3 /data/data/com.android.providers.settings/databases/settings.db "update global set value=1 where name='device_provisioned';"
  adb shell sqlite3 /data/data/com.android.providers.settings/databases/settings.db "update secure set value=1 where name='user_setup_complete';"

}

export -f unsetup

function hello() {
   echo "Hello, $1!"
}

export -f hello

function mymenu() {
  my_menu.py

}

export -f mymenu

function typetest() {

 message="$2$1$3"
 hello $message
 Type $message
}

export -f typetest

function logcat() {
  adb logcat $*
}

export -f logcat

function flash_it() {
if [ ! -n "$1" ]; then
    guess=$(ls -1trF fastboot*.tar.gz | tail -1)
    folder=$(echo $guess | sed 's/fastboot.//' | sed 's/\.tar\.gz//')
else
  folder=$1;
fi
echo $folder
test -d $folder && pushd $folder
arch=fastboot?$folder\.tar\.gz
echo $arch
echo "untar $arch"
untar $arch
# test -e $arch && tar -zxf $arch && printf "\a"
echo "prepare to flash $folder"
test -d $folder && pushd $folder
}

export -f flash_it

function get_keys_version (){

keys='serialno|version|keys|ro.boot|MBM-NG-V|fingerprint'
devices=$(fb_devices)
if [ ! -z "$devices" ] ; then
   getvar | grep -iE $keys
fi
devices=$(adb_devices)
  for device in $devices ; do
    echo serialno: $device
    adb -s $device shell getprop | grep -iE $keys;
    echo
  done
}

export -f get_keys_version

export BP_vers="M8994_1236|M8994_1233|MDM9625_|ONEBIN_BP_|ULTRA_M_BP_|ULTRA_BP_|9615_|msm8960bp_|vanquish_bp_|qinara_bp_|asanti_bp_|SASQUATCH_BP_|MSM8960PROBP_|MSM8960PRO_BP_"

function get_ver () {
   strings -a NON-HLOS.bin | grep -iE $BP_vers | grep -v mdm
}

export -f get_ver

function Type ( ) {
    echo $1
    adb shell input text $1

}

export -f Type

function wifi {

year='2015'
wifistringincludes2014="InternetAccess"
wifistringincludes="GuestAccess"

Type "$wifistringincludes$year"
}

export -f wifi


function echo_if_dir {
  [[ -d $1 ]] && echo $1
}

function ltr {
    ls -ltr $*
}

export -f ltr

function flsrt () {

  ls -lSrF  $*| grep / | tail
}

export -f flsrt

function lsrt {

  ls -Srl $* | tail
}

export -f lsrt


#alias ltrt='ls -ltrF  | tail'
#alias fltr='ls -ltrF  | grep /'
#alias fltrh='ls -ltrF | grep / | head'
#alias fltrt='ls -ltrF | grep / | tail'

function ltrh () {
    ls -ltrF $*| head
}

export -f ltrh

function ltrt () {
  ls -ltrF $* | tail
}

export -f ltrt

function fltrh () {

  ls -ltrF  $* | grep / | head
}

export -f fltrh

function fltr () {
  ls -ltrF  $* | grep /
}

export -f fltr

function fltrt () {
  ls -ltrF $* | grep / | tail
}

export -f fltrt


function getvar () {

    for d in $(fb_devices) ; do
    echo serialno: $d
    if [ -n "$1" ] ; then
        fastboot -s $d getvar $* 2>&1
    else
        fastboot -s $d getvar all 2>&1
    fi
    echo
    done
}

export -f getvar

function scream {

  mplayer ~/Downloads/Wilhelm_Scream.ogg > /dev/null 2>&1

}

export -f scream

function mybeep () {

   mplayer -ss 0:0:51 ~/Downloads/test_cbr.mp3 > /dev/null 2>&1

}

export -f mybeep

function playit () {

cvlc --play-and-exit $* 2> /dev/null
}


function bflash {

echo pushd mbm-ci
echo unzip blankflash.zip
echo pushd blankflash
echo ./qboot blank-flash
}

export -f bflash

function show_image() {

  python  ~/bin/show_image.py -q -i $1

}

export -f show_image

function newest () {

ls -t $($*) | head -1

}

export -f newest

function save_partition() {

if [ -n "$2" ] ; then
  device=$1
  partition=$2
  echo $1 $2
  $(fastboot -s $device oem partition dump $partition)
  mv $partition.img "$device.$partition.img"
else
  echo 'Usage: save_partition <serial_number> <partition_name>'
fi
}

export -f save_partition

#device=`adb_device` && adb -s $device reboot-bootloader 2>/dev/null

#device=`fb_device`
#echo $device


function save_dev() {

device=$1
if [ -n "$1" ] ; then
  for ptv in hob dhob modemst1 modemst2 ; do echo $ptv ;  save_partition $device $ptv ;  done
else
  echo 'Usage: save_dev <serial number>'
fi
}

export -f save_dev

function save_devs() {
  for device in $(fb_devices) ;
    do mkdir -p $device &&  pushd $device && save_dev $device && popd ; done
}

export -f save_devs

function erase_data () {
  if [ -n "$1" ] ; then fastboot -s $1 -w
  fi
}

export -f erase_data


function erase_devs {
  for device in $(fb_devices) ; do erase_data $device ;done
}

export -f erase_devs

function factory_upgrade {

   save_devs && \
   for device in $(fb_devices) ; do erase_data $device ; done && \
   if [ -e flashall.sh ] ; then flashall.sh ; fi
}

export -f factory_upgrade


function sideload8994 () {

 if [ -e "$1" ] ; then
    device=" -s $1 "
  else
    device=""
 fi

 adb $device root
 adb $device wait-for-device
 adb $device shell busybox mount -o remount,rw,nosuid,nodev,relatime,user_xattr,barrier=1,data=ordered /dev/block/platform/soc.0/by-name/modem /firmware
 adb $device shell rm /firmware/image/modem*
 adb $device push  modem_proc/split_bins /firmware/image
 adb $device reboot

}

export -f sideload8994

function flashem () {

    dlist="$*"
    if [ -z "$dlist" ];then
       dlist+=$(fb_devices)
    fi
    if [ -z "$dlist" ];then
        echo "No devices where found!"
        exit $E_BADARGS
    fi
    for device in $dlist; do
        gnome-terminal -t "flashing $device..." -x bash -c "flashall.sh -d $device; echo -n \"Press any key to exit...\"; read -n 1 -s"
    done
}

export -f flashem

function get_relnotes () {
relnotes=$1

wget --user=$(me) --ask-password $1

}

function get_multiple_relnotes () {

  for rels in $* ; do
    mkdir -p $rels
    pushd $rels
    get_relnotes http://artifacts.mot.com/artifactory/kinzie/5.1.1/$rels/kinzie_verizon/user/bldccfg_test-keys/ReleaseNotes.html
    popd
  done;

}

function filter_crs () {

key=$2
if [ -z "$key" ];then
key=IKSWL
fi

echo $key

grep -n -B14 'href="http://idart.mot.com/browse/' $1 | grep -E $key

}

function jira_rel_crs () {

  jira_q_test="\"SW Version(s) Integrated\" ~ "
  jira_q=""
  echo $jira_q
  counter=0

  for rels in $* ; do
   ((counter++))
    if [ $counter -gt 1 ]; then jira_q="$jira_q or "
    fi
    jira_q="$jira_q $jira_q_test\"$rels\" "
  done;
  echo "http://idart.mot.com/issues/?jql=$jira_q"

}

function conf_call () {
  dial="$1\;$2\#"
  echo "$1;$2#"
  Type $dial
}

export -f conf_call

function du2dh (){
 du2d $* | head
}

export -f du2dh

function du2d (){

  du_d 2 $*
}

export -f du2d

function du_d (){

  #a=$1
  du --max-depth $* | sort -gr
}

export -f du_d

function clean_ws {

perl -lapi -e 's/^\s+$|\s+$//g' $*
# perl -lapi -e 's/^\s+$/\n/g' $*
# perl -lapi -e 's/\s+$//g' $*
#  perl -lapi -e 's/^\s+|\s+$//g' $*
}

export -f clean_ws

function clean_all_while_space {

for file in *.?pp ;do clean_ws $file ;done

}

export -f clean_all_while_space

function kill_procs(){

if [ -n "$1" ] ; then
   proc_name=$1
   echo "killing all proc named $proc_name"
   for id in $(ps -C $proc_name -o pid=) ; do echo "kill $id" ; done
fi
}
export -f kill_procs

function lsx(){
   find $1 -maxdepth 1  -executable   -type f
}

export -f lsx

function stage_srv {
    echo 'stage1n1-la.siptalk.com'
}

function dev64 {
   echo 'xdev64'
}
export -f dev64

function webdev {
   echo 'dev3n1'
}

function xclickit {
   domain="siptalk.com"
   ssh xcast@bdsupportdb-02.$domain
}

function clickit {
   domain="siptalk.com"
   ssh ndarmoni@bdsupportdb-02.$domain
}

function xcweb {
   domain="xcastlabs.com"
   ssh -X xcast@$(webdev).$domain
}


function debug_broker1 {
    domain="xbrokert1-chi.siptalk.com"
    ssh -X xcast@$domain
}

function debug_broker2 {
    domain="xbrokert2-chi.siptalk.com"
    ssh -X xcast@$domain
}


function pbxdev {
    domain="pbxdev.xcastlabs.com"
    ssh -X ndarmoni@$domain
}

function xc {
   domain="xcastlabs.com"
   ssh -X xcast@$(dev64).$domain
}

function dev {
    domain="xcastlabs.com"
    ssh -X ndarmoni@$(dev64).$domain
}

function mount_webdev {
	dev_mounting_point="$HOME/Desktop/webdev"
    mkdir -p $dev_mounting_point
    domain="xcastlabs.com"
    sshfs xcast@$(webdev).$domain:nir $dev_mounting_point
}
function mount_dev {
	dev_mounting_point="$HOME/Desktop/sftp"
    mkdir -p $dev_mounting_point
    domain="xcastlabs.com"
    sshfs ndarmoni@$(dev64).$domain: $dev_mounting_point
}
export -f mount_dev

function mount_usr {
	usr_mounting_point="$HOME/Desktop/usr"
    domain="xcastlabs.com"
    mkdir -p $usr_mounting_point
	if [ $? == 0 ]; then
	    sshfs ndarmoni@$(dev64).$domain:/usr $usr_mounting_point
      export ACE_ROOT=$usr_mounting_point/local/ACE_wrappers
	fi
}
export -f mount_usr

function mount_pbxdev {
	pbxdev_mounting_point="$HOME/Desktop/pbxdev"
    mkdir -p $pbxdev_mounting_point
    domain="xcastlabs.com"
    sshfs ndarmoni@pbxdev.$domain: $pbxdev_mounting_point
}
export -f mount_pbxdev

function show(){

    cat $1 | egrep -v '^#|^$'
}

export -f show

alias dirty="cvs status 2>&1 | grep Status |grep  -v 'Status: Up-to-date' | grep -v 'cvs status:'"

#function dirty{
#    cvs status 2>&1 | grep Status |grep  -v 'Status: Up-to-date' | grep -v 'cvs status:'
#}

#export -f dirty

function Column() {
// column=$1
 awk '{print $c}' c=${1:-1}
}
export -f Column

function ts() {
unset TS

if [ -z "$*" ]; then
    #TS=$(date +%.s)
    TS=$(date +%s.%N)
else
    LongTS="$*"
    echo "$LongTS" | egrep -q '[^0-9]'
    if [ $? -ne 0 ];
    then
            len=$(echo "$*" | wc -m)
            #echo "len=$len"
            if [ $len \> 19 ] ;
            then
                #echo "LongTS=$LongTS"
                nano=${LongTS:10}
                dt=${LongTS:0:10}
                TS="$dt.$nano"
                #echo $TS
            fi
    fi
    echo "LongTS=$LongTS, TS=$TS"
    if [ "" == "$TS" ] ; then
        #echo "We are in the other long numeric ts section"
        echo  "$LongTS" | egrep -q '[^0-9\.]'
        if [ $? -ne 0 ];then
            #echo "We are in the pointed ts section"
            TS=$LongTS
            #echo "LongTS=$LongTS, TS=$TS"
        fi
    fi
fi
#echo $TS
LTM=$(date  --rfc-3339=ns -d "1970-01-01 UTC $TS sec " 2>/dev/null)
if [ $? -ne 0  -o  -z "$TS" ]; then
    echo Incorrect date: $*
    return 1
fi

UTM=$(date -u "+%Y-%m-%d %H:%M:%S.%N UTC" -d "1970-01-01 UTC $TS sec ")

echo -e $TS '  ===>  ' $LTM '  ===>  ' $UTM

}
export -f ts

export SIP_DOMAIN="10.10.10.55"
function apt_help () {
	if [ -z $1 ];then
		what='netinet/sctp.h'
	else
		what=$1
	fi
	echo  apt-file search $what
}
function cmp_tmp () {
    for file in Makefile *cpp *h ; do echo $file ; diff $file $(pwd|sed 's/work_torm/work/')/$file ;done
}

function active() {
   sudo netstat -anp 
}

function show_symbols () {
    nm -anC $1
}
function switch_on () {
    ssh xcast@tswitch3.siptalk.com
}

function get_file_from_pbx () {
        time=$(timestamp | sed 's/[:|-]//g');
        if [ -z $1 ];then
            echo "Usage: get_file_from_pbx <path>"
            return
        else
        for what in $* ;
            do
                #what=$1
                base_name=$(basename "$what")
                to_name=$(realpath ~/Downloads/production.$time.$base_name)
                #echo "$what, $base_name, $to_name"
                cmd="scp -p xcast@tswitch3.siptalk.com:$what $to_name"
                echo $cmd
                $($cmd)
                if [ $? == 0 ] ; then echo "$to_name" ; fi
            done
        fi
        }

function get_res_from_pbx () {
        $(get_file_from_pbx 'lib/mserver/app/cpuload.php.res')
        }

function stage_lib_ms_apps () {
    if [ ! -z "$1" ] ; then
        apps=$*;
        time=$(timestamp | sed 's/[:|-]//g');
        srvs='mserver1n1-la.siptalk.com mserver1n2-la.siptalk.com stage1n1-la.siptalk.com'
        SUFFIX=$(ssh xcast@mserver1n1-la.siptalk.com "grep '^%el' /etc/rpm/macros.dist 2> /dev/null| sed -r 's/%(el[0-9]*).*/.\1/'")

        echo "pushd ~/Downloads"
        for app in $apps; do
            echo "scp -p ndarmoni@xdev64.xcastlabs.com:w1/build/Registrator/mapp/$app $app.nir"
            echo "scp -p ndarmoni@pbxdev.xcastlabs.com:work/Registrator/mapp/$app $app$SUFFIX.nir"
            echo "sleep 2"
        done
        for srv in $srvs ; do
            remote="ssh xcast@$srv"
            SUFFIX=$($remote "grep '^%el' /etc/rpm/macros.dist 2> /dev/null| sed -r 's/%(el[0-9]*).*/.\1/'")
            for app in $apps; do
                deploy="cd ~/lib/mserver/app/ && mv ./$app ./$app.$time && cp -p ~/tmp/$app$SUFFIX.nir ./$app"
                verify="ls -l ~/lib/mserver/app/$app"
                kill_master="ps -ef | grep -v grep | grep $app | grep Master"
                remote_deploy="${remote} '${deploy}'"
                remote_verify="${remote} '${verify}'"
                remote_kill_master="${remote} '${kill_master}'"
                #echo "scp -p $app.nir xcast@$srv:tmp/$app.nir"
                echo "scp -p $app$SUFFIX.nir xcast@$srv:tmp/$app$SUFFIX.nir"
                echo "sleep 2"
                echo '#echo on Media servers:'
                echo "${remote_deploy}"
                echo "${remote_verify}"
                echo "${remote_kill_master}"
            done
        done
        echo "popd"
    else echo "need a name of app(s)"
    fi
}
export stage_lib_ms_apps

function stage_acd_recording () {
    time=$(timestamp | sed 's/[:|-]//g');
    app='mappemail_acdrecording.php'
    srvs='mserver1n1-la.siptalk.com mserver1n2-la.siptalk.com'
    echo "pushd ~/Downloads"
    echo "scp -p ndarmoni@xdev64.xcastlabs.com:w1/build/Registrator/mapp/mappemail_acdrecording.php mappemail_acdrecording.php.nir"
    echo 'sleep 2'
    for srv in $srvs ; do
        remote="ssh xcast@$srv"
        verify="ls -l ~/lib/mserver/app/$app"
        deploy="cd ~/lib/mserver/app/ && mv ./$app ./$app.$time && cp -p ~/tmp/$app.nir ./$app"
        remote_deploy="${remote} '${deploy}'"
        remote_verify="${remote} '${verify}'"
        echo "scp -p mappemail_acdrecording.php.nir xcast@$srv:tmp/mappemail_acdrecording.php.nir"
        echo 'sleep 2'
        echo 'echo on Media servers:'
        echo "${remote_deploy}"
        echo 'sleep 2'
        echo "${remote_verify}"
        done
    echo "popd"
}
export stage_acd_recording


function stage_media_library () {
    time=$(timestamp | sed 's/[:|-]//g');
    srvs='mserver1n1-la.siptalk.com mserver1n2-la.siptalk.com stage1n1-la.siptalk.com'
    SUFFIX=$(ssh xcast@mserver1n1-la.siptalk.com "grep '^%el' /etc/rpm/macros.dist 2> /dev/null| sed -r 's/%(el[0-9]*).*/.\1/'")
    apps='hstarter libhermes.so'

    echo "pushd ~/Downloads"
    app='hstarter'
    echo "scp -p ndarmoni@xdev64.xcastlabs.com:w1/build/Registrator/mediaframework/Hermes/hstarter/$app $app.nir"
    echo "scp -p ndarmoni@pbxdev.xcastlabs.com:work/Registrator/mediaframework/Hermes/hstarter/$app $app$SUFFIX.nir"
    app='libhermes.so'
    echo "scp -p ndarmoni@xdev64.xcastlabs.com:w1/build/Registrator/mediaframework/Hermes/libs64/$app $app.nir"
    echo "scp -p ndarmoni@pbxdev.xcastlabs.com:work/Registrator/mediaframework/Hermes/libs64/$app $app$SUFFIX.nir"

    echo "sleep 2"

    for srv in $srvs ; do
        remote="ssh xcast@$srv"
        SUFFIX=$($remote "grep '^%el' /etc/rpm/macros.dist 2> /dev/null| sed -r 's/%(el[0-9]*).*/.\1/'")
        for app in $apps; do
            deploy="cd ~/lib/mserver/ && mv ./$app ./$app.$time && cp -p ~/tmp/$app$SUFFIX.nir ./$app"
            verify="ls -l ~/lib/mserver/$app"
            kill_master="sleep 2 && ~/bin/mserver_ctl restart && ~/bin/cserver_ctl restart"
            remote_deploy="${remote} '${deploy}'"
            remote_verify="${remote} '${verify}'"
            remote_kill_master="${remote} '${kill_master}'"
            #echo "scp -p $app.nir xcast@$srv:tmp/$app.nir"
            echo "scp -p $app$SUFFIX.nir xcast@$srv:tmp/$app$SUFFIX.nir"
            echo "sleep 2"
            echo '#echo on Media servers:'
            echo "${remote_deploy}"
            echo "sleep 2"
            echo "${remote_verify}"
        done
        echo "${remote_kill_master}"
    done
    echo "popd"
}

export stage_media_library

function stage_qman () {
    time=$(timestamp | sed 's/[:|-]//g');
    remote="ssh xcast@$(stage_srv)"
    deploy="cd ~/bin && cp -p ~/tmp/qman.nir . && mv qman qman.$time && ./qman_ctl stop && cp -p qman.nir qman && ./qman_ctl start"
    remote_deploy="${remote} '${deploy}'"
    echo "pushd ~/Downloads"
    echo 'scp -p ndarmoni@xdev64.xcastlabs.com:w1/build/Registrator/ACD/qman qman.nir'
    echo "scp -p ndarmoni@xdev64.xcastlabs.com:/net/home/ndarmoni/work/Registrator/ACD/idl/libAcd.so.1.6.0 libAcd.so.1.6.0.nir"
    echo 'sleep 3'
    echo 'scp -p qman.nir xcast@stage1n1-la.siptalk.com:tmp/qman.nir'
    echo 'scp -p libAcd.so.1.6.0.nir xcast@stage1n1-la.siptalk.com:tmp/libAcd.so.1.6.0.nir'
    echo 'sleep 3'
    echo "popd"

    echo 'echo on Staging server:'
    echo "# if ACD/idl/Acd.idl is new,"
    echo "# mv ~/lib/libAcd.so.1.6.0 ~/lib/libAcd.so.1.6.0.$time && cp -p ~/tmp/libAcd.so.1.6.0.nir ~/lib/libAcd.so.1.6.0"
    echo "# ${remote_deploy}"
}
export stage_qman


function stage_indexCDR () {
    time=$(timestamp | sed 's/[:|-]//g');
    srvs=$(stage_srv)
    echo "pushd ~/Downloads"
    echo "scp -p xcast@xdev64.xcastlabs.com:bin/indexCDRs_php indexCDRs_php.nir"
    echo 'sleep 3'
    for srv in $srvs ; do
        remote="ssh xcast@$srv"
        deploy="cd ~/bin && mv ./indexCDRs_php ./indexCDRs_php.$time && cp -p ~/tmp/indexCDRs_php.nir ./indexCDRs_php"
        remote_deploy="${remote} '${deploy}'"
        verify="ls -l ~/bin/indexCDRs_php"
        remote_verify="${remote} '${verify}'"
        echo "scp -p indexCDRs_php.nir xcast@$srv:tmp/indexCDRs_php.nir"
        echo 'sleep 3'
        echo 'echo on Media servers:'
        echo "${remote_deploy}"
        echo 'sleep 3'
        echo "${remote_verify}"
        done
    echo "popd"
}
export stage_indexCDR

function stage_inbound_fax () {
    time=$(timestamp | sed 's/[:|-]//g');
    srvs=$(stage_srv)
    echo "pushd ~/Downloads"
    echo "scp -p xcast@xdev64.xcastlabs.com:bin/process_inbound_fax.php process_inbound_fax.php.nir"
    echo "scp -p xcast@xdev64.xcastlabs.com:lib/mserver/app/FaxIn.xms FaxIn.xms.nir"
    echo 'sleep 3'
    for srv in $srvs ; do
        remote="ssh xcast@$srv"
        deploy="cd ~/bin && mv ./process_inbound_fax.php ./process_inbound_fax.php.$time && cp -p ~/tmp/process_inbound_fax.php.nir ./process_inbound_fax.php \
        cd ~/lib/mserver/app && mv ./FaxIn.xms ./FaxIn.xms.$time && cp -p ~/tmp/FaxIn.xms.nir ./FaxIn.xms"
        remote_deploy="${remote} '${deploy}'"
        verify="ls -l ~/bin/process_inbound_fax.php ~/lib/mserver/app/FaxIn.xms"
        remote_verify="${remote} '${verify}'"
        echo "scp -p process_inbound_fax.php.nir xcast@$srv:tmp/process_inbound_fax.php.nir"
        echo "scp -p FaxIn.xms.nir xcast@$srv:tmp/FaxIn.xms.nir"
        echo 'sleep 3'
        echo 'echo on Media servers:'
        echo "${remote_deploy}"
        echo 'sleep 3'
        echo "${remote_verify}"
        done
    echo "popd"
}
export stage_inbound_fax

function start_staging_baresip () {
    nohup ~/bin/start_test.py &
}

function start_grafana {
echo 'sudo systemctl daemon-reload
sudo systemctl start grafana-server
systemctl status grafana-server'
}

function flac2mp3 {
echo 'for a in ./*.flac; do
  ffmpeg -i "$a" -qscale:a 0 "${a[@]/%flac/mp3}"
done'
}


function histogram_voicemail () {
    echo 'set @field="accountId"; set @s = concat("select distinct ", @field," , count(", @field, ") from voicemail group by ",@field); prepare stmt from @s; execute stmt;'
    echo '<?php
  $mysqli = new mysqli("localhost", "user", "pass", "test");

  if( mysqli_connect_errno() )
    die("Connection failed: %s\n", mysqli_connect_error());

  $field = "accountId";

  $query = "SELECT $field FROM t";

  $result = $mysqli->query($query);

  while($row = $result->fetch_assoc())
  {
    echo "<p>" . $row["$field"] . "</p>\n";
  }

  $result->close();

  $mysqli->close();
?>'
}

function audio_duration () {
    for f in $* ; do echo $f;
  ffmpeg -i $f 2>&1 |awk '/Duration/ { print substr($2,0,length($2)-1) }'
  done
}

function influx_it {
    echo '# sudo systemctl restart influxdb'
    echo '# sudo vim /etc/influxdb/influxdb.conf'
    influx -database reg_events -execute 'select * from "awesome_policy"./registration_events.*/ limit 3'
    influx -database 'logs' -precision rfc3339 -execute 'select * from /logs.*/ order by time desc limit 6'
    influx -database 'MediaPerfomance' -precision rfc3339 -execute 'SELECT * FROM "awesome_policy"./ReportPerfomance.*.vad.*/ where time > now() -2d  order by time desc limit 3'
    influx -database 'MediaPerfomance' -precision rfc3339 -execute 'SELECT * FROM "awesome_policy"./PacketLoss.*.vad.*/ where time > now() -2d  order by time desc limit 3'
}

function logs_load {
    logs_load.py
}

function which_staging_qman () {
    prog='qman'
    if [ "$1" != "" ] ; then
        for prog in $* ;
            do
                echo $prog
                cmd="rpm -qf bin/$prog"
                rpm=`ssh xcast@stage1n1-la.siptalk.com "$cmd"`
                ssh xcast@stage1n1-la.siptalk.com "rpm -qi $rpm";
            done;
    else ssh xcast@stage1n1-la.siptalk.com 'rpm -qi `rpm -qf bin/qman`';
    fi
}

function start_virtualenv () {
    export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python
    export WORKON_HOME=$HOME/Envs
    export PROJECT_HOME=$HOME/VirtualProjects
    export VIRTUALENVWRAPPER_LOG_FILE=hook.log
    export VIRTUALENVWRAPPER_SCRIPT=/usr/local/bin/virtualenvwrapper.sh
    source $VIRTUALENVWRAPPER_SCRIPT
    echo "#workon demosite
    #mkvirtualenv <environment name>
    #mkproject [-f|--force] [-t template] [virtualenv options] project_name
    #mkvirtualenv [-a project_path] [-i package] [-r requirements_file] [virtualenv options] env_name
    #setvirtualenvproject <env> <prj>
"
}

function all_log ()
{
    sed -E 's/\-[[:xdigit:]]{8}[\.|\-]/-*/g' | sed -E 's/\.[[:digit:]]+\.log/.*log/' | sed -E 's/container[1-9]+\-/container*\-/'
}

function all_log_param ()
{
    echo $1 | all_log
}

function build_this_rpm () {
    for build in $* ; do 
    echo $build
    curl -X POST \
     -F token=TOKEN \
     -F ref=REF_NAME \
     https://scm.xcastlabs.net/api/v4/projects/58/trigger/pipeline;
     done
}
#this is for CORBA
export LD_LIBRARY_PATH=/usr/local/lib/
export OMNINAMES_LOGDIR=/var/log/omniNames/
export OMNIORBBASE=/home/nir/omniorb/omniORB-4.2.1

#setting -up git prompt
# Git
GIT_PS1_SHOWDIRTYSTATE='y'
GIT_PS1_SHOWSTASHSTATE='y'
GIT_PS1_SHOWUNTRACKEDFILES='y'
#GIT_PS1_DESCRIBE_STYLE='describe'
GIT_PS1_DESCRIBE_STYLE='contains'
#GIT_PS1_DESCRIBE_STYLE='branch'
GIT_PS1_SHOWUPSTREAM='auto'
#GIT_PS1_SHOWUPSTREAM='y'
GIT_PS1_SHOWCOLORHINTS='y'

source /etc/bash_completion.d/git-prompt

#if [ "$color_prompt" = yes ]; then
    PROMPT_COMMAND='__git_ps1 "\e]0;${debian_chroot:+($debian_chroot)}\u@\h \w\a[${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]: \[\033[01;34m\]\W\[\033[00m\] ]" " \$ "'
#else
#    PROMPT_COMMAND='__git_ps1 "\e]0;${debian_chroot:+($debian_chroot)}\u@\h \W\a[${debian_chroot:+($debian_chroot)}\u@\h: \W ]" " \$ "'
#fi

#PROMPT_COMMAND='__git_ps1 "\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \W\a[${debian_chroot:+($debian_chroot)}\u@\h: \W ]" " \$ "'

# If this is an xterm set the title to user@host:dir
#case "$TERM" in
#xterm*|rxvt*)
#    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
#    ;;
#*)
#    ;;
#esac


TOP_DIR=/home/nir/repo

function _these_are_set_in_bashrc {
#setting -up git prompt
# Git
GIT_PS1_SHOWDIRTYSTATE='y'
GIT_PS1_SHOWSTASHSTATE='y'
GIT_PS1_SHOWUNTRACKEDFILES='y'
#GIT_PS1_DESCRIBE_STYLE='describe'
GIT_PS1_DESCRIBE_STYLE='contains'
#GIT_PS1_DESCRIBE_STYLE='branch'
GIT_PS1_SHOWUPSTREAM='auto'
#GIT_PS1_SHOWUPSTREAM='y'
GIT_PS1_SHOWCOLORHINTS='y'
source /etc/bash_completion.d/git-prompt
}

#alias lsx='find  -type f -executable -maxdepth 1'
alias gdbbt='gdb -q -n -ex bt -batch'
alias gdbbtfull='gdb -q -n -ex "bt full" -batch'
alias rm='rm -i'
alias wdiff='git difftool -y -x "diff -y -W $COLUMNS"'
#usage  mserver]$ for core in `ls -1tr` ; do echo $core ; gdbbt /usr/local/registrator/lib/mserver/app/mapp $core; done > mapp.bt.txt 2>&1
#10909090909909 * 979090909090909 +1

# 1090909090909090909090909 
