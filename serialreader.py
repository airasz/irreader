from serial import Serial
from tkinter import Tk, Text, Scrollbar, RIGHT, Y

# Serial port configuration
serialPort = "/dev/ttyUSB0"  # Change this to your port
baudRate = 9600
ser = Serial(serialPort, baudRate, timeout=0)

# Create a Tkinter window
root = Tk()
root.wm_title("Reading Serial")

# Create a scrollbar
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

# Create a text box to display the serial output
log = Text(root, width=50, height=20)
log.pack()

# Attach the text box to the scrollbar
log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log.yview)


result=""

# Function to read from serial and update the text field
def readSerial():
	global result

	while True:
		c = ser.read()  # Attempt to read a character from Serial
		if len(c) == 0:
			break  # Exit if no data is read
		result = c.decode('utf-8')
		# result.partition('\n')[0]
		# print(result)
		# log.delete	('1.0', 'end')
		# log.set=""
		log.insert('end', result)
		# Insert the read character into the text box
		# log.insert('end', c.decode('utf-8'))  # Decode bytes to string
	if len(result) > 10:
		print(result)
	root.after(100, readSerial)  # Schedule the next read

# Start reading from serial after a short delay
root.after(100, readSerial)

# Start the Tkinter main loop
root.mainloop()
