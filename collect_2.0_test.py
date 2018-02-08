#!/user/bin/python3
#coding:utf-8

import interface_run
import unittest
import pymysql
import logger
import configContral
import comm


class collect_test(unittest.TestCase):
    def setup(self):
        print("方法调用前")
        db = pymysql.connect(host="192.168.106.76", port=3306, db="newcs", user="eCityArcTest",
                             password="rickControl@test", charset="utf8")  # 链接数据库
        self.cursor = db.cursor()

    def test_Login(self):  #登录
        # testFile = open("./user_2.0.txt",'r')
        # testDataList = testFile.readlines()
        for i in configContral.login_testCase_list:
            params = ""
            testList = i.split(",")
            print(i)
            print(testList)
            params=params+"userName=%s"%testList[0]
            params=params+"&password=%s"%testList[1]
            data = interface_run.run_post2('/arcSystemUserController/login', params, '')
            if data['code']==int(testList[2]):
                if data['code']==200:
                    configContral.token=data['data']['token']
                    self.cursor.execute("SELECT id,user_name,password,create_time,update_time,create_id,update_id,status,is_delete,token,company_type,employee_id FROM arc_system_user WHERE user_name='%s'" %(testList[0]))
                    data_userInfo = self.cursor.fetchall()  # 获取查询结果
                    self.cursor.execute("SELECT r.id,r.rule_name,r.remark,r.status,r.role_type from arc_system_user as u,arc_sys_user_rule as ur,arc_rule as r WHERE u.user_name='%s' and u.id=ur.sys_user_id and ur.rule_id=r.id" %(testList[0]))
                    data_roleInfo=self.cursor.fetchall()
                    different=0
                    userDict={}
                    userDict_db={}
                    roleDict={}
                    roleDict_db={}
                    userDict=data['data']['user']
                    roleDict=data['data']['role']
                    for k in data_userInfo:
                        userDict_db['id']=k[0]
                        userDict_db['userName']=k[1]
                        userDict_db['password']=k[2]
                        userDict_db['createTime']=k[3].strftime("%Y-%m-%d %H:%M:%S")
                        userDict_db['updateTime']=k[4].strftime("%Y-%m-%d %H:%M:%S")
                        userDict_db['createId']=k[5]
                        userDict_db['updateId']=k[6]
                        userDict_db['status']=k[7]
                        userDict_db['isDelete']=k[8]
                        userDict_db['token']=k[9]
                        userDict_db['companyType']=k[10]
                        userDict_db['employeeId']=k[11]
                    for j in data_roleInfo:
                        roleDict_db['id']=j[0]
                        roleDict_db['ruleName']=j[1]
                        roleDict_db['remark']=j[2]
                        roleDict_db['status']=j[3]
                        roleDict_db['roleType']=j[4]
                    for k in userDict_db.keys():                     # user数据比对
                        if userDict_db['%s'%(k)] == userDict['%s'%(k)]:
                            pass
                        else:
                            logger.logger1.debug(
                                'userName(%s) user字段%s：返回值%s 数据库值%s'%(testList[0], k,userDict['%s'%k], userDict_db['%s'%k]))
                            different = 1  # 置为0

                    for k in roleDict_db.keys():                           # role 数据比对
                        if roleDict_db['%s'%k] == roleDict['%s'%k]:
                            pass
                        else:
                            logger.logger1.debug(
                                'userName(%s) role字段%s：返回值%s 数据库值%s'%(testList[0], k,roleDict['%s'%k], roleDict_db['%s'%k]))
                            different = 1  # 置为0
                    if different==0:
                        logger.logger1.info('userName(%s)登录数据获取正确'%(testList[0]))
                else:
                    logger.logger1.info('登录测试用例执行成功(userName=%s,password=%s，code=%s)'%(testList[0],testList[1],data['code']))
            else:
                logger.logger1.debug('登录测试用例执行失败：userName=%s,password=%s，respond=%s'%(testList[0],testList[1],data))
        # testFile.close()
    # def test_updatePassword(self):  # 修改密码调不通
    

    def tearDown(self):
        print("方法调用后")
        self.cursor.close()  #关闭数据库链接

if __name__=='__main__':

    suite=unittest.TestSuite()
    suite.addTest(collect_test("test_Login"))
    runner=unittest.TextTestRunner()
    runner.run(suite)