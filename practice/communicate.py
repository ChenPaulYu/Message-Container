import serial
port = "/dev/ttyACM0"
serialFromArduino = serial.Serial(port,9600)
serialFromArduino.flushInput()
tmp = 'True'

while True:
    # if(serialFromArduino.isOpen()>0):
    #     input = serialFromArduino.read(1)
    #     print(ord(input))
    if tmp == 'True':
        serialFromArduino.write('1')
    else :
        serialFromArduino.write('0')
