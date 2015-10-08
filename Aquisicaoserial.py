import array
import struct
from datetime import datetime


def startAccessPoint(ser):
    ser.write(makeByteString([0xFF, 0x07, 0x03]))
    # raw_input("Please turn your watch to sync mode and turn on the transceiver (though if the transciever is already on you may have to turn it off then on again), then press enter...")
    # print("AccessPoint Started")
    ser.read(3)


def stopAccessPoint(ser):
    ser.write(makeByteString([0xFF, 0x09, 0x03]))
    # print("AccessPoint Stopped")
    ser.read(3)


def getProductID(ser):
    ser.write(makeByteString([0xff, 0x20, 0x07, 0x00, 0x00, 0x00, 0x00]))
    return ser.read(7)


def getStatus(ser):
    ser.write(makeByteString([0xff, 0x00, 0x04, 0x00]))
    status = ser.read(4)
    if len(status) != 4:
        # print("Incorrect Length")
        return
    else:
        if status[3] == '\x00':
            print("Idle")
            return '\x00'
        elif status[3] == '\x01':
            print('Simpliciti Stopped')
            return '\x01'
        elif status[3] == '\x02':
            print('Simpliciti Trying to Link')
            return '\x02'
        elif status[3] == '\x03':
            print('Simpliciti Linked')
            return '\x03'
        elif status[3] == '\x06':
            print('No Error')
            return '\x06'
        elif status[3] == '\x05':
            print('Error')
            return '\x05'
        else:
            print(status[3])
            return status[3]

def getData(ser):
    ser.write('\xff\x08\x07\x00\x00\x00\x00')
    return struct.unpack("!bbbbbbb", ser.read(7))


def obtem_amostra(ser, amostra):
    data = getData(ser)
    if data[3] == 1:
        amostra.append(data[4])
        amostra.append(data[5])
        amostra.append(data[6])
        return True
    else:
        return False

def aquisicao(file_name, numero_dados, filtro = 1):
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)

    startAccessPoint(ser)
    status = getStatus(ser)
    if status == '\x03':
        getData(ser)
        i=1
        if filtro == 0:
            print('inicio sem filtro')
            #start = datetime.now()
            while i<= numero_dados:
                data = getData(ser)
                if data[3]==1:
                    writeData(file_name, data, i)
                    i+=1
            #done = datetime.now()
            #print('done')
            #deltat = done - start
            #print(deltat.total_seconds())
            stopAccessPoint(ser)
            ser.close()
            
        elif filtro == 1:
            print ('inicio com filtro')
            Try = True
            while Try:
                data_n_menos2 = getData(ser)
                if data_n_menos2[3] == 1:
                    Try = False
            Try = True
            while Try:
                data_n_menos1 = getData(ser)
                if data_n_menos1[3] == 1:
                    Try = False
            writeData(file_name, data_n_menos2, 1)
            writeData(file_name, data_n_menos1, 2)
            i+=2
            while i<= numero_dados:
                data_n = getData(ser)
                if data_n[3] == 1:
                    data_n[4] == (data_n[4] + data_n_menos1[4] + data_n_menos2[4])/3
                    data_n[5] == (data_n[5] + data_n_menos1[5] + data_n_menos2[5])/3
                    data_n[6] == (data_n[6] + data_n_menos1[6] + data_n_menos2[6])/3
                    writeData(file_name, data_n, i)
                    i+=1
                    data_n_menos2 = data_n_menos1
                    data_n_menos1 = data_n
            stopAccessPoint(ser)
            ser.close()
                    
    else:
        print('Simplicit not linked, try again')
        stopAccessPoint(ser)
        ser.close()


def makeByteString(arr):
   return array.array('B', arr).tostring()


def writeData(file_name, data, index):
    data_file = open(file_name, "a")
    hora = datetime.now().time().isoformat()
    data_file.write(hora[0:8]+":"+hora[9:12]+" | "+str(index)+"|")
    data_file.write("|"+str(data[4])+"|"+str(data[5])+"|"+str(data[6])+"\n")
    data_file.close()
