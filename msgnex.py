import serial
import time

# Configure the serial connection
# Replace 'COM3' with your serial port (e.g., '/dev/ttyUSB0' on Linux)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Allow some time for the connection to establish
time.sleep(2)

def send_command(command):
    # Send the command to the Nextion display
    #data=(command + '\xFF\xFF\xFF').encode('utf-8') 
    #print("data: "+str(data))
    ender=b'\xFF\xFF\xFF'
    data=command.encode()
    ser.write((data+ender))  # Nextion commands end with three 0xFF
    #ser.write(b't1.txt="Hello, Nextion!"\xFF\xFF\xFF')  # Nextion commands end with three 0xFF

    # print(b't1.txt="Hello, Nextion!"\xFF\xFF\xFF')
    # ender=b'\xFF\xFF\xFF'
    # ser.write(command+ender)  # Nextion commands end with three 0xFF

    
    
    
# Example: Send a command to set the text of a text box
#send_command(b't1.txt="Hello, hai Nextion!"')  # Assuming 't0' is the ID of your text box
#send_command('t1.txt="Hello, Nextion! encode"')  # Assuming 't0' is the ID of your text box
send_command('page page1')  # Assuming 't0' is the ID of your text box
send_command('t1.txt="Hello, Nextion! encode"')  # Assuming 't0' is the ID of your text box

# Close the serial connection
ser.close()