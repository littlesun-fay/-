import serial
import serial.tools.list_ports


# ser = serial.Serial()

# port_list = list(serial.tools.list_ports.comports())
# port = str(port_list[0]).split(" ")[0]
# ser.port = port
# ser.baudrate = 115200
# ser.open()

# while(True):
# 	da = ser.readline()
# 	print(da)

# da = "b'-60.2199 -9.1779 -45.6980\r\n'"


def jiexi(da):
    string_d = str(da)
    string_len = len(string_d)
    upd = string_d[0:string_len - 5]
    welld = upd.split("'")
    nd = welld[1].split(" ")
    d = []
    for n in nd:
        if n != "":
            d.append(n)  # 解析串口接收到的数据
    return d


# print(jiexi(da))
