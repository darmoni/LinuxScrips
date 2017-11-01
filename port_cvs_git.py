#!/usr/bin/env python
'''
awk '!/_CVSTAG=\$/ && /^[[:alpha:]]+_CVSTAG=/' build*sh |sort | uniq
ACD_CVSTAG=R2017-04-19
ACD_CVSTAG=R2017-10-10

ACDMON_CVSTAG=R2017-03-20

CNFMON_CVSTAG=R2017-03-13

COAST_CVSTAG=R2016-09-07

CODECS_CVSTAG=r2011-04-19

CONFDEP_CVSTAG=R2016-10-27

CONSOLE_CVSTAG=R2017-06-29

DASHMAN_CVSTAG=R2017-06-29

DB_CVSTAG=R2016-12-29
DB_CVSTAG=R2017-06-06
DB_CVSTAG=R2017-07-12
DB_CVSTAG=R2017-10-24

EVSRV_CVSTAG=R2017-03-28
EVSRV_CVSTAG=R2017-04-19

HERMES_CVSTAG=R2017-07-31

INDEXCDRS_CVSTAG=R2016-12-27

MAPP_CVSTAG=R2017-02-03-new
MAPP_CVSTAG=R2017-06-29

MIDDLE_CVSTAG=R2016-12-15
MIDDLE_CVSTAG=R2017-10-24

MIDMISC_CVSTAG=R2007-10-30

MSERVER_CVSTAG=R2017-01-25
MSERVER_CVSTAG=R2017-06-05
MSERVER_CVSTAG=R2017-09-25

SIPPROXY_CVSTAG=R2017-05-31
SIPPROXY_CVSTAG=R2017-10-24

SIPSTACK_CVSTAG=R2015-01-22
SIPSTACK_CVSTAG=R2016-03-09
SIPSTACK_CVSTAG=R2017-05-17

SPARSER_CVSTAG=R2014-10-15
SPARSER_CVSTAG=R2015-10-15
SPARSER_CVSTAG=R2016-12-15
SPARSER_CVSTAG=R2017-06-29

TBLOCK_CVSTAG=R2016-03-23

TUI_CVSTAG=R2016-09-07

UPDATER_CVSTAG=R2016-09-07

UTILS_CVSTAG=R2015-01-22
UTILS_CVSTAG=R2015-10-15
UTILS_CVSTAG=R2016-10-05
UTILS_CVSTAG=R2016-12-29
UTILS_CVSTAG=R2017-03-27
UTILS_CVSTAG=R2017-06-29
UTILS_CVSTAG=R2017-09-20

VOICELOADER_CVSTAG=R2016-09-07
VOICELOADER_CVSTAG=R2017-09-21

WPHONE_CVSTAG=R2017-06-29

XBROKER_CVSTAG=R2015-01-22



awk '/cvs .+ Registrator/ {print $(NF),$(NF-1);}' build*sh |sort | uniq | awk '{print "cvs_paths.update({\"" $1 "\":\"" $2 "\"})";}'



awk '!/_CVSTAG=\$/ && /^[[:alpha:]]+_CVSTAG=/ { gsub("="," ",$0); print "cvs_tags.update({\"" $1 "\":\"" $2 "\"})";}' build*sh |sort | uniq


git clone git@scm.xcastlabs.net:chi/phoneplatform/Registrator.git --recurse-submodules

'''

cvs_tags={}
cvs_paths={}
git_projects={}

cvs_tags.update({"ACD_CVSTAG":"R2017-04-19"})
cvs_tags.update({"ACD_CVSTAG":"R2017-10-10"})
cvs_tags.update({"ACDMON_CVSTAG":"R2017-03-20"})
cvs_tags.update({"CNFMON_CVSTAG":"R2017-03-13"})
cvs_tags.update({"COAST_CVSTAG":"R2016-09-07"})
cvs_tags.update({"CODECS_CVSTAG":"r2011-04-19"})
cvs_tags.update({"CONFDEP_CVSTAG":"R2016-10-27"})
cvs_tags.update({"CONSOLE_CVSTAG":"R2017-06-29"})
cvs_tags.update({"DASHMAN_CVSTAG":"R2017-06-29"})
cvs_tags.update({"DB_CVSTAG":"R2016-12-29"})
cvs_tags.update({"DB_CVSTAG":"R2017-06-06"})
cvs_tags.update({"DB_CVSTAG":"R2017-07-12"})
cvs_tags.update({"DB_CVSTAG":"R2017-10-24"})
cvs_tags.update({"EVSRV_CVSTAG":"R2017-03-28"})
cvs_tags.update({"EVSRV_CVSTAG":"R2017-04-19"})
cvs_tags.update({"HERMES_CVSTAG":"R2017-07-31"})
cvs_tags.update({"INDEXCDRS_CVSTAG":"R2016-12-27"})
cvs_tags.update({"MAPP_CVSTAG":"R2017-02-03-new"})
cvs_tags.update({"MAPP_CVSTAG":"R2017-06-29"})
cvs_tags.update({"MIDDLE_CVSTAG":"R2016-12-15"})
cvs_tags.update({"MIDDLE_CVSTAG":"R2017-10-24"})
cvs_tags.update({"MIDMISC_CVSTAG":"R2007-10-30"})
cvs_tags.update({"MSERVER_CVSTAG":"R2017-01-25"})
cvs_tags.update({"MSERVER_CVSTAG":"R2017-06-05"})
cvs_tags.update({"MSERVER_CVSTAG":"R2017-09-25"})
cvs_tags.update({"SIPPROXY_CVSTAG":"R2017-05-31"})
cvs_tags.update({"SIPPROXY_CVSTAG":"R2017-10-24"})
cvs_tags.update({"SIPSTACK_CVSTAG":"R2015-01-22"})
cvs_tags.update({"SIPSTACK_CVSTAG":"R2016-03-09"})
cvs_tags.update({"SIPSTACK_CVSTAG":"R2017-05-17"})
cvs_tags.update({"SPARSER_CVSTAG":"R2014-10-15"})
cvs_tags.update({"SPARSER_CVSTAG":"R2015-10-15"})
cvs_tags.update({"SPARSER_CVSTAG":"R2016-12-15"})
cvs_tags.update({"SPARSER_CVSTAG":"R2017-06-29"})
cvs_tags.update({"TBLOCK_CVSTAG":"R2016-03-23"})
cvs_tags.update({"TUI_CVSTAG":"R2016-09-07"})
cvs_tags.update({"UPDATER_CVSTAG":"R2016-09-07"})
cvs_tags.update({"UTILS_CVSTAG":"R2015-01-22"})
cvs_tags.update({"UTILS_CVSTAG":"R2015-10-15"})
cvs_tags.update({"UTILS_CVSTAG":"R2016-10-05"})
cvs_tags.update({"UTILS_CVSTAG":"R2016-12-29"})
cvs_tags.update({"UTILS_CVSTAG":"R2017-03-27"})
cvs_tags.update({"UTILS_CVSTAG":"R2017-06-29"})
cvs_tags.update({"UTILS_CVSTAG":"R2017-09-20"})
cvs_tags.update({"VOICELOADER_CVSTAG":"R2016-09-07"})
cvs_tags.update({"VOICELOADER_CVSTAG":"R2017-09-21"})
cvs_tags.update({"WPHONE_CVSTAG":"R2017-06-29"})
cvs_tags.update({"XBROKER_CVSTAG":"R2015-01-22"})

cvs_paths.update({"Registrator/ACD":"$ACD_CVSTAG"})
cvs_paths.update({"Registrator/ACD/idl":"$ACD_CVSTAG"})
cvs_paths.update({"Registrator/coast":"$COAST_CVSTAG"})
cvs_paths.update({"Registrator/confdep":"$CONFDEP_CVSTAG"})
cvs_paths.update({"Registrator/config/xbroker":"HEAD"})
cvs_paths.update({"Registrator/db/balance":"$DB_CVSTAG"})
cvs_paths.update({"Registrator/db/config":"$DB_CVSTAG"})
cvs_paths.update({"Registrator/db":"$DB_CVSTAG"})
#cvs_paths.update({"Registrator/db/dbmon":"$DB_CVSTAG"})
cvs_paths.update({"Registrator/db/idl":"$DB_CVSTAG"})
cvs_paths.update({"Registrator/mapp":"$MAPP_CVSTAG"})
cvs_paths.update({"Registrator/mediaframework/Codecs":"$CODECS_CVSTAG"})
cvs_paths.update({"Registrator/mediaframework/Hermes":"$HERMES_CVSTAG"})
cvs_paths.update({"Registrator/middle/config":"$MIDMISC_CVSTAG"})
cvs_paths.update({"Registrator/middle/fw_scripts":"$MIDMISC_CVSTAG"})
cvs_paths.update({"Registrator/middle/middle_ng/G711":"$MIDDLE_CVSTAG"})
cvs_paths.update({"Registrator/middle/middle_ng/iLBC":"$MIDDLE_CVSTAG"})
cvs_paths.update({"Registrator/middle/middle_ng":"$MIDDLE_CVSTAG"})
cvs_paths.update({"Registrator/middle/natpass_config":"HEAD"})
cvs_paths.update({"Registrator/middle/natpass_scripts":"HEAD"})
cvs_paths.update({"Registrator/middle/rings":"HEAD"})
cvs_paths.update({"Registrator/middle/rings":"$MIDMISC_CVSTAG"})
cvs_paths.update({"Registrator/middle/scripts":"$MIDMISC_CVSTAG"})
cvs_paths.update({"Registrator/middle/sparser":"$SPARSER_CVSTAG"})
cvs_paths.update({"Registrator/middle/stack_na/mserver/config":"$MSERVER_CVSTAG"})
cvs_paths.update({"Registrator/middle/stack_na/mserver/scripts":"$MSERVER_CVSTAG"})
cvs_paths.update({"Registrator/middle/stack_na/proxy_sb/config/":"HEAD"})
cvs_paths.update({"Registrator/middle/stack_na/proxy/scripts/":"HEAD"})
cvs_paths.update({"Registrator/middle/stack_opt/bbua":"$XBROKER_CVSTAG"})
cvs_paths.update({"Registrator/middle/stack_opt/console":"$CONSOLE_CVSTAG"})
cvs_paths.update({"Registrator/middle/stack_opt/mserver":"$MSERVER_CVSTAG"})
cvs_paths.update({"Registrator/middle/stack_opt/mserver/t38":"$T38_CVSTAG"})
cvs_paths.update({"Registrator/middle/stack_opt/proxy":"$SIPPROXY_CVSTAG"})
cvs_paths.update({"Registrator/middle/stack_opt":"$SIPSTACK_CVSTAG"})
cvs_paths.update({"Registrator/middle/stack_opt/teleblock":"$TBLOCK_CVSTAG"})
cvs_paths.update({"Registrator/middle/stack_opt/webphone":"$WPHONE_CVSTAG"})
cvs_paths.update({"Registrator/middle/utils":"$UTILS_CVSTAG"})
cvs_paths.update({"Registrator/monitoring/AcdMon":"$ACDMON_CVSTAG"})
cvs_paths.update({"Registrator/monitoring/cfg":"HEAD"})
cvs_paths.update({"Registrator/monitoring/CnfMon":"$CNFMON_CVSTAG"})
cvs_paths.update({"Registrator/monitoring/DashMan":"$DASHMAN_CVSTAG"})
cvs_paths.update({"Registrator/monitoring/EvService":"$EVSRV_CVSTAG"})
cvs_paths.update({"Registrator/scripts/cdrs":"$INDEXCDRS_CVSTAG"})
cvs_paths.update({"Registrator/scripts/utils":"$SCRIPT_UTILS_CVSTAG"})
cvs_paths.update({"Registrator/tui/composer":"$TUI_CVSTAG"})
cvs_paths.update({"Registrator/updater":"$UPDATER_CVSTAG"})
cvs_paths.update({"Registrator/voice_loader/fonts":"$VOICELOADER_CVSTAG"})
cvs_paths.update({"Registrator/voice_loader/freetype/include":"$VOICELOADER_CVSTAG"})
cvs_paths.update({"Registrator/voice_loader/freetype":"$VOICELOADER_CVSTAG"})
cvs_paths.update({"Registrator/voice_loader/idl":"$VOICELOADER_CVSTAG"})
cvs_paths.update({"Registrator/voice_loader/libx264":"$VOICELOADER_CVSTAG"})
cvs_paths.update({"Registrator/voice_loader/scripts":"$VOICELOADER_CVSTAG"})
cvs_paths.update({"Registrator/voice_loader":"$VOICELOADER_CVSTAG"})
cvs_paths.update({"Registrator/voice_loader/vputil":"$VOICELOADER_CVSTAG"})

'''
git_project.update({'Registrator/middle/rings':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})
git_project.update({'Registrator/middle/utils':'git@scm.xcastlabs.net:chi/phoneplatform/middle_utils.git'})
git_project.update({'Registrator/voice_loader/vputil':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_project.update({'Registrator/tui/composer':'git@scm.xcastlabs.net:chi/phoneplatform/tui.git'})
#git_project.update({'Registrator/db/dbmon':'git@scm.xcastlabs.net:chi/phoneplatform/tui.git'})
git_project.update({'Registrator/config/xbroker':'git@scm.xcastlabs.net:chi/phoneplatform/tui.git'})
git_project.update({'Registrator/middle/stack_na/proxy_sb/config/':'git@scm.xcastlabs.net:chi/phoneplatform/tui.git'})
git_project.update({'Registrator/middle/config':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})
git_project.update({'Registrator/middle/stack_opt/mserver':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_mserver.git'})
git_project.update({'Registrator/middle/sparser':'git@scm.xcastlabs.net:chi/phoneplatform/middle_sparser.git'})
git_project.update({'Registrator/middle/stack_opt':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt.git'})
git_project.update({'Registrator/voice_loader/freetype':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_project.update({'Registrator/voice_loader':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_project.update({'Registrator/monitoring/cfg':'git@scm.xcastlabs.net:chi/phoneplatform/monitoring_cfg.git'})
git_project.update({'Registrator/db/balance':'git@scm.xcastlabs.net:chi/phoneplatform/db.git'})
git_project.update({'Registrator/monitoring/AcdMon':'git@scm.xcastlabs.net:chi/phoneplatform/monitoring_AcdMon.git'})
git_project.update({'Registrator/monitoring/EvService':'git@scm.xcastlabs.net:chi/phoneplatform/monitoring_EvService.git'})
git_project.update({'Registrator/coast':'git@scm.xcastlabs.net:chi/phoneplatform/coast.git'})
git_project.update({'Registrator/db/idl':'git@scm.xcastlabs.net:chi/phoneplatform/db.git'})
git_project.update({'Registrator/middle/stack_opt/proxy':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_proxy.git'})
git_project.update({'Registrator/voice_loader/fonts':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_project.update({'Registrator/mediaframework/Hermes':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_project.update({'Registrator/ACD':'git@scm.xcastlabs.net:chi/phoneplatform/ACD.git'})
git_project.update({'Registrator/confdep':'git@scm.xcastlabs.net:chi/phoneplatform/confdep.git'})
git_project.update({'Registrator/middle/stack_opt/bbua':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_bbua.git'})
git_project.update({'Registrator/middle/middle_ng':'git@scm.xcastlabs.net:chi/phoneplatform/middle_ng.git'})
git_project.update({'Registrator/middle/stack_na/mserver/config':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_na_mserver.git'})
git_project.update({'Registrator/ACD/idl':'git@scm.xcastlabs.net:chi/phoneplatform/ACD.git'})
git_project.update({'Registrator/middle/stack_opt/console':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_console.git'})
git_project.update({'Registrator/scripts/cdrs':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_console.git'})
git_project.update({'Registrator/middle/middle_ng/iLBC':'git@scm.xcastlabs.net:chi/phoneplatform/middle_ng.git'})
git_project.update({'Registrator/db/config':'git@scm.xcastlabs.net:chi/phoneplatform/db.git'})
git_project.update({'Registrator/middle/stack_opt/webphone':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_webphone.git'})
git_project.update({'Registrator/middle/stack_na/proxy/scripts/':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_na_proxy_scripts.git'})
git_project.update({'Registrator/scripts/utils':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_na_proxy_scripts.git'})
git_project.update({'Registrator/voice_loader/libx264':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_project.update({'Registrator/voice_loader/freetype/include':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_project.update({'Registrator/mediaframework/Codecs':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_project.update({'Registrator/middle/scripts':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})
git_project.update({'Registrator/voice_loader/scripts':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_project.update({'Registrator/middle/stack_opt/mserver/t38':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_mserver_t38.git'})
git_project.update({'Registrator/middle/stack_na/mserver/scripts':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_na_mserver.git'})
git_project.update({'Registrator/middle/middle_ng/G711':'git@scm.xcastlabs.net:chi/phoneplatform/middle_ng.git'})
git_project.update({'Registrator/monitoring/CnfMon':'git@scm.xcastlabs.net:chi/phoneplatform/monitoring_CnfMon.git'})
git_project.update({'Registrator/monitoring/DashMan':'git@scm.xcastlabs.net:chi/phoneplatform/monitoring_DashMan.git'})
git_project.update({'Registrator/db':'git@scm.xcastlabs.net:chi/phoneplatform/db.git'})
git_project.update({'Registrator/mapp':'git@scm.xcastlabs.net:chi/phoneplatform/mapp.git'})
git_project.update({'Registrator/middle/stack_opt/teleblock':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_teleblock.git'})
git_project.update({'Registrator/updater':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_teleblock.git'})
git_project.update({'Registrator/middle/natpass_config':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})
git_project.update({'Registrator/voice_loader/idl':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_project.update({'Registrator/middle/natpass_scripts':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})
git_project.update({'Registrator/middle/fw_scripts':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})
'''
#todo
'''
NOT NEADDED
./print_git_command.sh: line 9: cd: Registrator/db/dbmon: No such file or directory
FIXED (added to Registrator)
./print_git_command.sh: line 11: cd: Registrator/config/xbroker: No such file or directory
./print_git_command.sh: line 43: cd: Registrator/mediaframework/Hermes: No such file or directory
./print_git_command.sh: line 75: cd: Registrator/mediaframework/Codecs: No such file or directory
./print_git_command.sh: line 97: cd: Registrator/updater: No such file or directory
./print_git_command.sh: line 59: cd: Registrator/scripts/cdrs: No such file or directory
./print_git_command.sh: line 69: cd: Registrator/scripts/utils: No such file or directory

FIXED (added to middle)
./print_git_command.sh: line 13: cd: Registrator/middle/stack_na/proxy_sb/config/: No such file or directory

'''
git_projects.update({'Registrator/middle/rings':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})
git_projects.update({'Registrator/middle/utils':'git@scm.xcastlabs.net:chi/phoneplatform/middle_utils.git'})
git_projects.update({'Registrator/voice_loader/vputil':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_projects.update({'Registrator/tui/composer':'git@scm.xcastlabs.net:chi/phoneplatform/tui.git'})
git_projects.update({'Registrator/config/xbroker':'git@scm.xcastlabs.net:chi/phoneplatform/config_xbroker.git'})
git_projects.update({'Registrator/middle/stack_na/proxy_sb/config/':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_na_proxy_sb_config.git'})
git_projects.update({'Registrator/middle/config':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})
git_projects.update({'Registrator/middle/stack_opt/mserver':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_mserver.git'})
git_projects.update({'Registrator/middle/sparser':'git@scm.xcastlabs.net:chi/phoneplatform/middle_sparser.git'})
git_projects.update({'Registrator/middle/stack_opt':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt.git'})
git_projects.update({'Registrator/voice_loader/freetype':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_projects.update({'Registrator/voice_loader':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_projects.update({'Registrator/monitoring/cfg':'git@scm.xcastlabs.net:chi/phoneplatform/monitoring_cfg.git'})
git_projects.update({'Registrator/db/balance':'git@scm.xcastlabs.net:chi/phoneplatform/db.git'})
git_projects.update({'Registrator/monitoring/AcdMon':'git@scm.xcastlabs.net:chi/phoneplatform/monitoring_AcdMon.git'})
git_projects.update({'Registrator/monitoring/EvService':'git@scm.xcastlabs.net:chi/phoneplatform/monitoring_EvService.git'})
git_projects.update({'Registrator/coast':'git@scm.xcastlabs.net:chi/phoneplatform/coast.git'})
git_projects.update({'Registrator/db/idl':'git@scm.xcastlabs.net:chi/phoneplatform/db.git'})
git_projects.update({'Registrator/middle/stack_opt/proxy':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_proxy.git'})
git_projects.update({'Registrator/voice_loader/fonts':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_projects.update({'Registrator/mediaframework/Hermes':'git@scm.xcastlabs.net:chi/phoneplatform/mediaframework_Hermes.git'})
git_projects.update({'Registrator/ACD':'git@scm.xcastlabs.net:chi/phoneplatform/ACD.git'})
git_projects.update({'Registrator/confdep':'git@scm.xcastlabs.net:chi/phoneplatform/confdep.git'})
git_projects.update({'Registrator/middle/stack_opt/bbua':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_bbua.git'})
git_projects.update({'Registrator/middle/middle_ng':'git@scm.xcastlabs.net:chi/phoneplatform/middle_ng.git'})
git_projects.update({'Registrator/middle/stack_na/mserver/config':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_na_mserver.git'})
git_projects.update({'Registrator/ACD/idl':'git@scm.xcastlabs.net:chi/phoneplatform/ACD.git'})
git_projects.update({'Registrator/middle/stack_opt/console':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_console.git'})
git_projects.update({'Registrator/scripts/cdrs':'git@scm.xcastlabs.net:chi/phoneplatform/scripts_cdrs.git'})
git_projects.update({'Registrator/middle/middle_ng/iLBC':'git@scm.xcastlabs.net:chi/phoneplatform/middle_ng.git'})
git_projects.update({'Registrator/db/config':'git@scm.xcastlabs.net:chi/phoneplatform/db.git'})
git_projects.update({'Registrator/middle/stack_opt/webphone':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_webphone.git'})
git_projects.update({'Registrator/middle/stack_na/proxy/scripts/':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_na_proxy_scripts.git'})
git_projects.update({'Registrator/scripts/utils':'git@scm.xcastlabs.net:chi/phoneplatform/scripts_utils.git'})
git_projects.update({'Registrator/voice_loader/libx264':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_projects.update({'Registrator/voice_loader/freetype/include':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_projects.update({'Registrator/mediaframework/Codecs':'git@scm.xcastlabs.net:chi/phoneplatform/mediaframework_Codecs.git'})
git_projects.update({'Registrator/middle/scripts':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})
git_projects.update({'Registrator/voice_loader/scripts':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_projects.update({'Registrator/middle/stack_opt/mserver/t38':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_mserver_t38.git'})
git_projects.update({'Registrator/middle/stack_na/mserver/scripts':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_na_mserver.git'})
git_projects.update({'Registrator/middle/middle_ng/G711':'git@scm.xcastlabs.net:chi/phoneplatform/middle_ng.git'})
git_projects.update({'Registrator/monitoring/CnfMon':'git@scm.xcastlabs.net:chi/phoneplatform/monitoring_CnfMon.git'})
git_projects.update({'Registrator/monitoring/DashMan':'git@scm.xcastlabs.net:chi/phoneplatform/monitoring_DashMan.git'})
git_projects.update({'Registrator/db':'git@scm.xcastlabs.net:chi/phoneplatform/db.git'})
git_projects.update({'Registrator/mapp':'git@scm.xcastlabs.net:chi/phoneplatform/mapp.git'})
git_projects.update({'Registrator/middle/stack_opt/teleblock':'git@scm.xcastlabs.net:chi/phoneplatform/middle_stack_opt_teleblock.git'})
git_projects.update({'Registrator/updater':'git@scm.xcastlabs.net:chi/phoneplatform/updater.git'})
git_projects.update({'Registrator/middle/natpass_config':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})
git_projects.update({'Registrator/voice_loader/idl':'git@scm.xcastlabs.net:chi/phoneplatform/voice_loader.git'})
git_projects.update({'Registrator/middle/natpass_scripts':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})
git_projects.update({'Registrator/middle/fw_scripts':'git@scm.xcastlabs.net:chi/phoneplatform/middle.git'})


class git_project:
    def __init__(self,_path,_remote_path,_tag):
        self.path=_path
        self.remote_path=_remote_path
        self.tag=_tag
    def clone_me(self):
        print("git clone {} {} ".format(self.remote_path, self.path))
        self.cd_co_br()
    def cd_co_br(self):
        if(self.tag != "HEAD"):
            print("pushd {} && git checkout -q {} && git checkout -B branch_{} && popd".format(self.path,self.tag,self.tag))
        else:
            print("pushd {} && git checkout {} && popd".format(self.path,"master"))

for key in cvs_paths:
    tag=cvs_paths[key]
    git=git_projects[key]
    p=git_project(key,git,tag)
    #p.cd_co_br()
    p.clone_me()
    #print("project={};cd $project && remote=$(git config remote.origin.url) && cd - ").format(key) 
    #print('echo "git_projects.update({\'$project\':\'$remote\'})"')
    #print("echo 'pushd {} && git checkout -q {} && git checkout -B branch_{} && popd'".format(key,tag,tag))


