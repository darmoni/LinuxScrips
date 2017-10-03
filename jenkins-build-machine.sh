#!/bin/bash
#ident $Id$Date$
'''
#export CVSROOT=:ext:buildmaster@cvs.xcastlabs.com:/usr/cvsroot
#export CVS_RSH=ssh
echo $CVSROOT
echo $BUILD_TAG
SUFFIX=$(grep '^%el' /etc/rpm/macros.dist 2> /dev/null| sed -r 's/%(el[0-9]*).*/.\1/')
echo $SUFFIX
git clone git@scm.xcastlabs.net:ndarmoni/build.git
cd build
ls -ltr
./build_index_cdrs.sh
myrpm=$(ls -1tr *rpm |tail -1)
echo $myrpm
mv $myrpm ../
cd ..
git init && git remote add origin git@scm.xcastlabs.net:ndarmoni/rpm.pbx.el7.git
git pull origin master
git add $myrpm && git commit -m "$BUILD_TAG" && git push -u origin master

****************************************************
RpmScriptName=build_scriptutils.sh
#!/bin/bash
source ~/.bash_profile
mydir=$(pwd)
echo "starting at $mydir"
mkdir -p "$RpmScriptName-$BUILD_TAG"
cd $RpmScriptName-$BUILD_TAG
build_dir=$(pwd)
#export CVSROOT=:ext:buildmaster@cvs.xcastlabs.com:/usr/cvsroot
#export CVS_RSH=ssh
echo $CVSROOT
echo $BUILD_TAG
SUFFIX=$(grep '^%el' /etc/rpm/macros.dist 2> /dev/null| sed -r 's/%(el[0-9]*).*/.\1/')
echo $SUFFIX
git clone git@scm.xcastlabs.net:ndarmoni/build.git
cd build
ls -ltr
source ./$RpmScriptName
myrpm=$(ls -1tr *rpm |tail -1)
echo $myrpm
cd $mydir
git init && git remote add origin git@scm.xcastlabs.net:ndarmoni/rpm.pbx.el7.git
#git pull origin master
# erase the old rpms
rm -f *rpm
mv $build_dir/build/$myrpm .
git add $myrpm && git commit -m "$BUILD_TAG" && git push -u origin master
cd $mydir

'''

#*********************************

#!/bin/bash

function buildit() {
	source $1
    if [ $? != 0 ]; then exit -1 ; fi
}

source ~/.bash_profile
timestamp=$(date +%F-%T | sed 's/[:|-]//g')
mydir=$(pwd)
echo "starting at $mydir"
if [ "" != "$GIT_COMMIT" ]; then echo "GIT_COMMIT='$GIT_COMMIT'" ; fi
build_dir="$RpmScriptName-$BUILD_TAG-$timestamp"
echo $build_dir
mkdir -p $build_dir
cd $build_dir
echo $build_dir
echo $CVSROOT
echo $BUILD_TAG
SUFFIX=$(grep '^%el' /etc/rpm/macros.dist 2> /dev/null| sed -r 's/%(el[0-9]*).*/.\1/')
echo $SUFFIX
git clone git@scm.xcastlabs.net:ndarmoni/build.git
if [ -e build/$RpmScriptName ] ;
then 
	cd build
	changeLog=$(grep _ChangeLog ./$RpmScriptName | awk '/cp / { print $2;}')
	if [ -e $changeLog ]; then
		cat $changeLog
		ls -ltr
		buildit "./$RpmScriptName"
		myrpm=$(ls -1tr *rpm |tail -1)
		echo $myrpm
		cd $mydir
		# erase the old rpms
		# rm -f *rpm
		mv $build_dir/build/$myrpm .

	else
		echo "$changeLog is not present"
		exit -1
	fi
fi
