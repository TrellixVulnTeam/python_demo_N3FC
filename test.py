#!/user/bin/python3
# coding:utf-8
import xlrd


# class ExcelUtil:
#     def __init__(self, excel_path, sheet_name):
#
#         # excel_path=excel_path.decode('utf-8')
#         self.data = xlrd.open_workbook(filename=excel_path,encoding_override='utf-8',formatting_info=True)
#         print(1)
#         self.table = self.data.sheet_by_name(sheet_name)
#         print(2)
#         # 获取第一行作为key值
#         self.keys = self.table.row_values(0)
#         # 获取总行数
#         self.rowNum = self.table.nrows
#         # 获取总列数
#         self.colNum = self.table.ncols
#
#     def dict_data(self):
#         if self.rowNum <= 1:
#             print("总行数小于1")
#         else:
#             r = []
#             j = 1
#             for i in range(self.rowNum - 1):
#                 s = {}
#                 # 从第二行取对应values值
#                 values = self.table.row_values(j)
#                 for x in range(self.colNum):
#                     s[self.keys[x]] = values[x]
#                 r.append(s)
#                 j += 1
#             return r

import configContral

if __name__ == "__main__":
    # configContral.login_testCase_list=['admin,123456,200','yxg,123456,200','admin,123,1003','admi,123,1002',',,1002  ']
    # print(configContral.login_testCase_list)
    testList=[]
    for i in configContral.login_testCase_list:
        testList = i.split(",")
        print(testList[2])
    # print(configContral.login_testCase_list)
    # filePath = "./testcase.xls"
    # sheetName = "login"
    # # data = xlrd.open_workbook(u"C:\\Users\\jinlisha\\PycharmProjects\\collection_test\\testcase.xlsx")
    # data = ExcelUtil(filePath, sheetName)
    # data.dict_data()
    # print(data)
