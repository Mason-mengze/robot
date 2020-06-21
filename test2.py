
#----------------------- block program start ----------------------
#--------定义类和函数--------
class UbtRobotTemperature(Structure):
_fields_ = [
#---------define field, array int type, 3 len--------
("data", c_int*3)
]
#--------定义指针--------
ubtRobotEnv = pointer(UbtRobotTemperature())
#--------调用接口--------
api.ubtReadSensorValue("environment", ubtRobotEnv, sizeof(UbtRobotTemperature))
#--------显示数据--------
print ubtRobotEnv[0].data[:]
#----------------------- block program end ----------------------
api.ubtRobotDisconnect("15013672783","v1.0.9.83-g4bbb9326", "127.0.0.1")
api.ubtRobotDeinitialize()
