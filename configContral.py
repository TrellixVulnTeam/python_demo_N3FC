#coding:utf-8

import configparser

cp=configparser.ConfigParser()
cp.read('./config.ini')
logName_configContral=cp.get('MAIN','logName')
logPath_configContral=cp.get('MAIN','logPath')
configPath_configContral=cp.get('MAIN','configPath')
levels_configContral=cp.get('MAIN','levels')
token=cp.get('LOGIN','token')

login_testCase_list=cp.get('TESTCASE','login_testCase_list').strip('|').split('|')
