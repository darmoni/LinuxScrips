#!/bin/bash -x


function me {
  echo $LOGNAME
}

export -f me

function timestamp {

  date +%F-%T
}

export -f timestamp

function refresh {

 . ~/.bashrc
}

export refresh

function funcs {

   echo "$HOME/bin/bash_functions"
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
 for device in `adb_devices` ; do
    APver=`adb -s $device shell getprop ro.build.fingerprint | sed -e "s/.*\[//" -e "s/\]//"`
    BPver=`adb -s $device shell getprop gsm.version.baseband | sed -e "s/.*\[//" -e "s/\]//"`
    FSGver=`adb -s $device shell getprop ril.baseband.config.ver_num | sed -e "s/.*\[//" -e "s/\]//"`
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
    guess=`ls -1trF fastboot*.tar.gz | tail -1`
    folder=`echo $guess | sed 's/fastboot.//' | sed 's/\.tar\.gz//'`
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
devices=`fb_devices`
if [ ! -z "$devices" ] ; then
   getvar | grep -iE $keys
fi
devices=`adb_devices`
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
  if [ -d $1 ] ; then echo $1
  fi
}

function ltr {

if [ -n "$1" ] ; then
  for file in $* ; do echo_if_dir $file ; ls -ltr $file ;done
else
  ls -ltr
fi
}

export -f ltr

function flsrt () {

if [ -n "$1" ] ; then
  for file in $* ; do echo_if_dir $file ; ls -lSrF $file | grep / ; done |tail
else
  ls -lSrF  | grep / | tail
fi

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

if [ -n "$1" ] ; then
  for file in $* ; do echo_if_dir $file ; ls -ltrF $file ; done | head
else
  ls -ltrF | head
fi

}

export -f ltrh

function ltrt () {

if [ -n "$1" ] ; then
  for file in $* ; do echo_if_dir $file ; ls -ltrF $file ; done | tail
else
  ls -ltrF | tail
fi

}

export -f ltrt

function fltrh () {

if [ -n "$1" ] ; then
  for file in $* ; do echo_if_dir $file ; ls -ltrF $file | grep / ; done | head
else
  ls -ltrF  | grep / | head
fi

}

export -f fltrh

function fltr () {

if [ -n "$1" ] ; then
  for file in $* ; do echo_if_dir $file ; ls -ltrF $file | grep / ; done
else
  ls -ltrF  | grep /
fi

}

export -f fltr

function fltrt () {

if [ -n "$1" ] ; then
  for file in $* ; do echo_if_dir $file ; ls -ltrF $file | grep / ; done | tail
else
  ls -ltrF  | grep / | tail
fi

}

export -f fltrt


function getvar () {

for d in `fb_devices` ; do
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
  `fastboot -s $device oem partition dump $partition`
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
  for device in `fb_devices` ;
    do mkdir -p $device &&  pushd $device && save_dev $device && popd ; done
}

export -f save_devs

function erase_data () {
  if [ -n "$1" ] ; then fastboot -s $1 -w
  fi
}

export -f erase_data


function erase_devs {
  for device in `fb_devices` ; do erase_data $device ;done
}

export -f erase_devs

function factory_upgrade {

   save_devs && \
   for device in `fb_devices` ; do erase_data $device ; done && \
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
       dlist+=`fb_devices`
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

wget --user=`me` --ask-password $1

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

function du2dh {
 du2d | head
}

export -f du2dh

function du2d {

  du_d 2
}

export -f du2d

function du_d (){

  a=$1
  du --max-depth $a | sort -gr
}

export -f du_d

function clean_ws {

 perl -lapi -e 's/^\s+$/\n/g' $*
 perl -lapi -e 's/\s+$//g' $*

#  perl -lapi -e 's/^\s+|\s+$//g' $*
}

export -f clean_ws

function clean_all_while_space {

for file in *.?pp ;do clean_ws $file ;done

}

export -f clean_all_while_space
function dev() {
#ignore input for now, use default
	pushd ~/tools
}

export -f dev


