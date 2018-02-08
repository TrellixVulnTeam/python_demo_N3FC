#!/user/bin/python3
#coding:utf-8
import interface_run
import unittest
import pymysql
import logger
import configContral
import comm


class login(unittest.TestCase):
    def setup(self):
        print("方法调用前")

    def test_Login(self):
        testFile = open("./user.txt",'r')
        testDataList = testFile.readlines()
        for i in testDataList:
            params = {}
            testList = i.split(",")
            params['userName'] = testList[0]
            params['password'] = testList[1]
            params['uniform'] = '1'
            data = interface_run.run('/api/system/tokenLogin', params,'')
            #self.assertEqual(data['code'],testList[2].replace('\n',''),'测试失败')
            if data['code']==testList[2].replace('\n',''):
                if data['code']=='200':
                    comsumerName=data['center']['comsumerName']
                    roleName=data['role']['roleName']
                    mobile=data['user']['mobile']
                    configContral.token=data['token']
                    db = pymysql.connect(host="192.168.106.76", port=3306, db="arc_collection_test", user="eCityArcTest",password="rickControl@test", charset="utf8")  # 链接数据库
                    cursor = db.cursor()
                    cursor.execute("SELECT op.name, ro.role_name,op.mobile FROM sys_operator as op,sys_operator_role as op_ro,sys_role as ro  WHERE op.user_name='%s' and op.id=op_ro.operator_id AND op_ro.role_id=ro.id" %(params['userName']))
                    data_userInfo = cursor.fetchall()  # 获取查询结果
                    cursor.close()
                    for i in data_userInfo:
                        comsumerName = i[0]
                        roleName = i[1]
                        mobile = i[2]

                    if comsumerName==data['center']['comsumerName'] and roleName==data['role']['roleName'] and mobile==data['user']['mobile']:
                        logger.logger1.info('数据获取正确')
                    else:
                        logger.logger1.debug('数据获取失败，实际数据：%s %s %s，期望数据;%s %s %s'%(data['center']['comsumerName'],data['role']['roleName'],data['user']['mobile'],comsumerName,roleName,mobile))
                        #print('数据获取失败，实际数据：%s %s %s，期望数据;%s %s %s'%(data['center']['comsumerName'],data['role']['roleName'],data['user']['mobile'],comsumerName,roleName,mobile))
                else:
                    logger.logger1.info('登录测试用例执行成功')

            else:
                logger.logger1.info('登录测试用例执行失败：userName=%s,password=%s，respond=%s'%(params['userName'],params['password'],data))
        testFile.close()
    def tearDown(self):
        print("方法调用后")

class borrowList(unittest.TestCase):
    def setUp(self):
        print("borrowList 方法调用前")
    def test_borrowList_all(self):
        params={}
        params['collectStatus']=''
        params['status']=''
        params['welling']=''
        params['rukuDate']=''
        params['centerName']=''
        params['collectorName']=''
        params['repayDate']=''
        params['caseDate']=''
        params['userPhone']=''
        params['aging']=''
        params['consumerNo']=''
        params['overDueDayMax']=''
        params['overDueDayMin']=''
        params['pageNo']='1'
        params['pageSize']='100'
        '''
        data=interface_run.run('/api/cash/select/borrowList', params,'')# no token
        if data['msg']=='接口请求出错':
            logger.logger1.info('success:no token 无法请求')
        else:
            logger.logger1.debug('false:no token 请求响应 %s'%(data))
        
       '''

        data = interface_run.run('/api/cash/select/borrowList', params, '747')  # 无效token
        if data['code']=='555':
            logger.logger1.info('success: 无效token 无法请求')
        else:
            logger.logger1.debug('false:无效 token 请求响应 %s'%(data))
        data=interface_run.run('/api/cash/select/borrowList', params,configContral.token) # 正常请求
        if data['code']=='200':

           for i in data['borrowList']:
               db = pymysql.connect(host="192.168.106.76", port=3306, db="arc_collection_test", user="eCityArcTest",
                                    password="rickControl@test", charset="utf8")  # 链接数据库
               cursor = db.cursor()
               sql1="SELECT aging,amount,assigned,borrow_no,case_date,collect_center,create_time,id,overdue_day,repay_amount,repay_amount_sum,status,type,update_time,welling,weian_date,user_id FROM arc_data_pool WHERE borrow_no='%s' and is_delete=0"%(i['borrowNo'])
               sql2="SELECT collection_name,collection_status FROM arc_collection  WHERE borrow_no='%s' and is_delete=0"%(i['borrowNo'])
               sql3="SELECT collector_id,id FROM arc_collection_distribution WHERE borrow_no='%s' and is_delete=0"%(i['borrowNo'])
               sql4="SELECT u.id_no,u.phone,u.real_name FROM arc_data_pool as pool , arc_user as u WHERE pool.borrow_no='%s' and pool.is_delete=0 and pool.user_id=u.consumer_no"%(i['borrowNo'])

               cursor.execute(sql1)
               rows1 = cursor.fetchall()  # 获取查询结果
               cursor.execute(sql2)
               rows2=cursor.fetchall()
               cursor.execute(sql3)
               rows3=cursor.fetchall()
               cursor.execute(sql4)
               rows4=cursor.fetchall()
               cursor.close()
               list={}
               list['aging']=rows1[0][0]
               list['amount']=comm.money_format(float(rows1[0][1])/100)
               list['assigned']=rows1[0][2]
               list['borrowNo']=rows1[0][3]
               if rows1[0][4]:
                   list['caseDate'] = rows1[0][4].strftime("%Y.%m.%d %H:%M:%S")
               else:
                   list['caseDate']=None

               list['centerId']=None
               list['collectCenter']=rows1[0][5]
               if rows2:
                   list['collectName'] = rows2[0][0]
                   list['collectionStatus']=int(rows2[0][1])
               else:
                   list['collectName'] = None
                   list['collectionStatus'] = None
               if rows3:
                   list['collectorId'] = int(rows3[0][0])
                   list['disId'] = int(rows3[0][1])
               else:
                   list['collectorId']=None
                   list['disId']=None
               if rows4:
                   list['idNo'] =rows4[0][0]
                   list['phone'] =rows4[0][1]
                   list['realName'] =rows4[0][2]
               else:
                   list['idNo'] =None
                   list['phone'] =None
                   list['realName'] =None
               if rows1[0][6]:
                   list['createTime'] = rows1[0][6].strftime("%Y.%m.%d %H:%M:%S")
               else:
                   list['createTime']=''
               list['id']=int(rows1[0][7])
               list['consumerNo']=rows1[0][16]
               list['overdueDay']=int(rows1[0][8])
               list['repayAmount']=comm.money_format(float(rows1[0][9])/100)
               list['repayAmountSum']=comm.money_format(float(rows1[0][10])/100)
               if rows1[0][15]:
                   list['rukuDate'] = rows1[0][15].strftime("%Y.%m.%d %H:%M:%S")
               else:
                   list['rukuDate']=''
               list['status']=int(rows1[0][11])
               list['type']=int(rows1[0][12])
               if rows1[0][13]:
                   list['updateTime'] = rows1[0][13].strftime("%Y.%m.%d %H:%M:%S")
               else:
                   list['updateTime']=''
               list['welling']=int(rows1[0][14])
               different=1
               for k in i.keys():
                   if list['%s'%(k)]==i['%s'%(k)]:
                       pass
                   else:
                       logger.logger1.debug('borrowNo(%s)案件%s：返回值%s 数据库值%s'%(i['borrowNo'],k,i['%s'%k],list['%s'%k]))
                       different=0 #置为0
               if different:
                   logger.logger1.info('数据完全匹配')
        else:
            logger.logger1.debug('接口请求失败：%s'%data)















        '''
        data = interface_run.run('/api/cash/select/borrowList', params,configContral.token) #pageNo、pageSize为空
        print(data)
        params['pageSize']='0'
        data1=interface_run.run('/api/cash/select/borrowList', params,configContral.token) #pageNo为空、pageSize为0
        print(data1)
        params['pageNo']='0'
        data2=interface_run.run('/api/cash/select/borrowList', params,configContral.token)#pageNo为0，pageSize为0
        print(data2)
        params['']=''
       '''











    def tearDown(self):
        print("borrowList 方法调用后")
if __name__=='__main__':

    suite=unittest.TestSuite()
    suite.addTest(login("test_Login"))
    suite.addTest(borrowList("test_borrowList_all"))
    runner=unittest.TextTestRunner()
    runner.run(suite)

