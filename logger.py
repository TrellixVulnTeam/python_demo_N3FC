#coding:utf-8

import logging
import configContral


logName_logger=configContral.logName_configContral
levels_logger=configContral.levels_configContral

#第一步，创建一个logger
logger1=logging.getLogger()
if levels_logger.upper()=="DEBUG":
    logger1.setLevel(logging.DEBUG)
elif levels_logger.upper()=="INFO":
    logger1.setLevel(logging.INFO)
elif levels_logger.upper()=="WARNING":
    logger1.setLevel(logging.WARNING)
elif levels_logger.upper()=="ERROR":
    logger1.setLevel(logging.ERROR)
else:
    logger1.setLevel(logging.CRITICAL)

#第二步，创建一个handler，用于写入日志文件
logfile=configContral.configPath_configContral+logName_logger
fileHendler=logging.FileHandler(logfile)
#fileHendler.setLevel(logging.DEBUG) # 输出到文件里的日志级别

#第三步，创建一个handler，用于输出控制台
outputFile_handler=logging.StreamHandler()

#第四步，定义handler的输出格式
formatter=logging.Formatter("%(asctime)s - %(name)s - %(levelname)s %(message)s")
fileHendler.setFormatter(formatter)
outputFile_handler.setFormatter(formatter)


#第五步，将logger添加到handler里面
logger1.addHandler(fileHendler)
logger1.addHandler(outputFile_handler)
#日志