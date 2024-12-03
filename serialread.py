import tkinter as tk
from tkinter import ttk
import serial
import threading
import subprocess

count=0
# Function to read serial data
def read_serial():
	global count
	try:
		while True:
			if ser.in_waiting > 0:  # Check if there is data in the serial buffer
				line = ser.readline().decode('utf-8').strip()  # Read, decode, and strip the newline
				count+=1
				if count==1:
					update_textbox(line)  # Update the textbox with the received data
				if count > 2:
					count=0
				# update_textbox(str(count) + " > "+line)  # Update the textbox with the received data
	except Exception as e:
		update_textbox(f"Error: {e}")

# Function to update the tkinter Text widget
def update_textbox(line):
	text_box2.delete("1.0", "end")
	text_box2.insert(tk.END, line)
	filtr = text_filter.get(1.0, "end-1c")
	if filtr != "":
		if filtr in line:
			print("contain FF")
			dfn= text_difiner.get(1.0, "end-1c")
			if dfn!= "":
				line= dfn+ " "+ line
			text_box.insert(tk.END, f"{line}\n")
			text_box.see(tk.END)  # Scroll to the end

# Start the serial reading in a separate thread
def start_reading():
	thread = threading.Thread(target=read_serial, daemon=True)
	thread.start()

# Main Tkinter window
root = tk.Tk()
root.title("Serial Reader")

# Text box to display data
text_box = tk.Text(root, height=20, width=50)
text_box.pack(padx=10, pady=10)

# Text box to display data
text_box2 = tk.Text(root, height=1, width=50)
text_box2.pack(padx=10, pady=10)

topBottomFrame = tk.Frame(root, padx=20, bg="#ffff44")
topBottomFrame.pack(side="top", fill="x")

flbel=tk.Label(topBottomFrame,text="result filter")
flbel.pack()

# Text box to display data
text_filter = tk.Text(topBottomFrame, height=1, width=30 )
text_filter.pack(padx=0, pady=10)
text_filter.insert(tk.END,"FF")

fldfn=tk.Label(topBottomFrame,text="variable to store")
fldfn.pack()

# Text box to display data
text_difiner = tk.Text(topBottomFrame, height=1, width=20)
text_difiner.pack(padx=0, pady=10)
text_difiner.insert(tk.END,"KEY_")

# Button to start reading
start_button = ttk.Button(root, text="Start Reading", command=start_reading)
start_button.pack(pady=10)

# sport=''
# def cekport():
#     global sport
#     output = result= subprocess.check_output("dmesg | grep tty", shell=True)
#     tty =  output.decode("utf-8")
#     if "ttyUSB" in tty:
#        itty=tty.index("ttyUSB")
#        sport = '/dev/'+tty[itty:(itty+7)]
#        # sport = '/dev/ttyUSB0'
#     else:
#        sport = '/dev/ttyS1'
#
# root.title("Serial Reader on " + sport)
# cekport()
# con = serial.Serial(
#     port=sport,
#     baudrate=9600,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS,
# )
for i in range(9):
	# Configure the serial port
	try:
		ser = serial.Serial('/dev/ttyUSB'+str(i), baudrate=9600, timeout=1)  # Replace 'COM3' with your port
		root.title("Serial Reader on " + 'ttyUSB'+str(i))
		break
	except Exception as e:
		text_box.insert(tk.END, f"Error: {e}\n")

# Start the Tkinter event loop
root.mainloop()
