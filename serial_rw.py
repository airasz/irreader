import tkinter as tk
import customtkinter
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTk
from CTkListbox import *
from tkinter import ttk
import serial
import threading
import subprocess
import pyperclip
import os
import serial.tools.list_ports

BACKGROUND = "#d9d9d9"
FOREGROUND = "black"
BUTTON_BACKGROUND = "#08b19a"
BUTTON_ACTIVE_BACKGROUND = "#1fcaf5"


# creates correctly formatted buttons
def formatted_buttons(
frame,
text="",
bg=BUTTON_BACKGROUND,
fg=FOREGROUND,
justify="left",
activebackground=BUTTON_ACTIVE_BACKGROUND,
command="",
activeforeground=FOREGROUND,
):
	button = tk.Button(
		frame,
		text=text,
		bg=bg,
		fg=fg,
		justify=justify,
		activebackground=activebackground,
		activeforeground=activeforeground,
		command=command,
	)
	return button
def mybutton(
frame,
text="",
bg=BUTTON_BACKGROUND,
fg=FOREGROUND,
justify="left",
activebackground=BUTTON_ACTIVE_BACKGROUND,
command="",
activeforeground=FOREGROUND,):
	btn = CTkButton(frame, text=text, 
	fg_color=BUTTON_BACKGROUND, command=command, corner_radius=50)
	return btn

def mytextbox(frame , height, width, bordercolor, bg, fg):
	ctb=customtkinter.CTkTextbox(frame, height=height, width=width, border_color=bordercolor, bg_color=bg, fg_color=fg, corner_radius=12, border_width=1)
	return ctb
def mylabel (frame, txt, bg, justify, tcolor):
	cl=customtkinter.CTkLabel(frame, text=txt, fg_color=bg, justify=justify, text_color= tcolor )
	return cl
def list_com_ports():
	ports = serial.tools.list_ports.comports()
	available_ports = []
	for port in ports:
		available_ports.append(port.device)
	return available_ports

ser = serial.Serial(None, baudrate=9600, timeout=1) 
count=0


# window=CTk()
# def CenterWindowToDisplay(Screen: root, width: int, height: int, scale_factor: float = 1.0):
#     """Centers the window to the main display/monitor"""
#     screen_width = Screen.winfo_screenwidth()
#     screen_height = Screen.winfo_screenheight()
#     x = int(((screen_width/2) - (width/2)) * scale_factor)
#     y = int(((screen_height/2) - (height/1.5)) * scale_factor)
#     return f"{width}x{height}+{x}+{y}"



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
def write_serial(data):
	global available_ports
	try:
		# with serial.Serial(port, baudrate=115200, timeout=1) as ser:
		ser.write(data.encode("utf-8"))
		print(f"Message sent: {data}")
		return True
		# print(f"Message sent to {i}: {message}")
	except serial.SerialException as e:
		print(f"Failed to send message to {port}: {e}")
		# available_ports = list_available_ports()
		return False
# Function to update the tkinter Text widget
def update_textbox(line):
	applog(line+"\n")
	filtr = text_filter.get(1.0, "end-1c")
	if filtr != "":
		if filtr in line:
			# print("contain "+ filtr)
			dfn= text_pre_str.get(1.0, "end-1c")
			poststring= text_post_str.get(1.0, "end-1c")
			if dfn!= "":
				line= dfn+  line
			if poststring!=" ":
				line+=poststring
			text_box.insert(tk.END, f"{line}\n")
			text_box.see(tk.END)  # Scroll to the end


def applog(msg):
	# text_box2.delete("1.0", "end")
	text_box2.insert(tk.END, msg)

# Start the serial reading in a separate thread
def start_reading():
	start_button.configure(state="disabled")
	thread = threading.Thread(target=read_serial, daemon=True)
	thread.start()

def cleartb():
	text_box.delete("1.0", "end")	

def copytoclip():
	filtr = text_box.get(1.0, "end-1c")
	pyperclip.copy(filtr)
	# subprocess.run("pbcopy", text=True, input=filtr)
# Main Tkinter window
root = customtkinter.CTk()
root.title("Serial Reader")

# topFrame = tk.Frame(root, padx=0, bg="#ffff44")
topFrame=customtkinter.CTkFrame(root,border_width=1,border_color="#000000",fg_color="#0060ea", width=300, height=100)
topFrame.pack(side="top", fill="x")
topTopFrame= customtkinter.CTkFrame(topFrame, width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#ff0066")
topTopFrame.pack(side="top", padx=5, pady=5)
topLeftFrame= customtkinter.CTkFrame(topFrame, width=300,  border_width=1, border_color="#aaff00", fg_color="#ff0066")
topLeftFrame.pack(side="left", padx=5, pady=5)
topRightFrame= customtkinter.CTkFrame(topFrame, width=300, border_width=1, border_color="#aaff00", fg_color="#ff0066")
topRightFrame.pack(side="left", padx=5, pady=5)
topNextFrame= customtkinter.CTkFrame(topFrame, width=300, border_width=1, border_color="#aaff00", fg_color="#ff0066")
topNextFrame.pack(side="left", padx=5, pady=5)


subTopLeftFrame1= customtkinter.CTkFrame(topLeftFrame, width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#ff0066")
subTopLeftFrame1.pack(side="top", padx=5, pady=5)
subTopLeftFrame2= customtkinter.CTkFrame(topLeftFrame, width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#ff0066")
subTopLeftFrame2.pack(side="bottom", padx=5, pady=5)
subTopLeftFrame3= customtkinter.CTkFrame(topLeftFrame, width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#ff0066")
subTopLeftFrame3.pack(side="bottom", padx=5, pady=5)
subTopRightFrame1= customtkinter.CTkFrame(topRightFrame, width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#ff0066")
subTopRightFrame1.pack(side="top", padx=5, pady=5)
subTopRightFrame2= customtkinter.CTkFrame(topRightFrame, width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#ff0066")
subTopRightFrame2.pack(side="bottom", padx=5, pady=5)
subTopRightFrame3= customtkinter.CTkFrame(topRightFrame, width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#ff0066")
subTopRightFrame3.pack(side="bottom", padx=5, pady=5)


botomframe= customtkinter.CTkFrame(root, width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#017066")
botomframe.pack(side="bottom", fill="x")
middleFrame= customtkinter.CTkFrame(root, width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#aa8800")
middleFrame.pack( fill="x")
# resultFrame = tk.Frame(topFrame, padx=20, pady=4, bg="#2266ff")
resultFrame=customtkinter.CTkFrame(middleFrame, width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#049589")
# resultFrame.pack(fill="x",side="bottom") 

filterFrame = customtkinter.CTkFrame(middleFrame, width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#00a6a0")
#filterFrame.pack(fill="x",side="top") 

postreadFrame= customtkinter.CTkFrame(filterFrame,  border_width=1, border_color="#aaff00", fg_color="#00b8cc")
#postreadFrame.pack(fill="x",side="right") 

# Text box to display data
# text_box = tk.Text(resultFrame, height=20, width=50)
text_box= mytextbox(resultFrame, height=300, width=500, bordercolor="#ffff00", fg="transparent", bg="transparent" )
text_box.pack(padx=1, pady=1 , fill="x")

buttonFrame = customtkinter.CTkFrame(resultFrame,width=300, height=100, border_width=1, border_color="#aaff00", fg_color="#b85f07")
buttonFrame.pack(fill="x", side="bottom") 

# Button to clear text area
clear_button = CTkButton(buttonFrame, text="clear", command=cleartb, corner_radius=50)
clear_button.pack(side="left",pady=2,padx=5)

# Button copy to clipboard
# ctc_button = ttk.Button(buttonFrame, text="copy to clipboard", command=copytoclip)
ctc_button = mybutton(buttonFrame,text="copy to clipboard",bg=BUTTON_BACKGROUND,activebackground=BUTTON_ACTIVE_BACKGROUND,command=copytoclip)
ctc_button.pack(side="left",pady=2, padx=5)

clr_btn=mybutton(buttonFrame,text="clear text",bg=BUTTON_BACKGROUND,activebackground=BUTTON_ACTIVE_BACKGROUND,command=cleartb,)
clr_btn.pack(side="left",pady=2, padx=5)
# Text box to display data
text_box2=mytextbox(botomframe, height=80, width=500, bordercolor="#ffff00", fg="transparent", bg="transparent" )
text_box2.pack(padx=2, fill="x",pady=3)


# flbel=tk.Label(filterFrame,text="result filter")
flbel=mylabel(filterFrame, txt="result filter", bg="transparent", justify="right", tcolor="#ffaa54")
flbel.pack(side="left", padx=10)
# Text box to display data
# text_filter = tk.Text(filterFrame, height=1, width=30 )
text_filter = mytextbox(filterFrame, height=1, width=100, bordercolor="#ffff00", fg="transparent", bg="transparent" )
text_filter.pack(side="left", padx=0, pady=10)
text_filter.insert(tk.END,"FD")



# fldfn=tk.Label(postreadFrame,text="pre string", bg="#222222", fg="#ffffff")
fldfn=mylabel(postreadFrame, txt="pre string", bg="transparent", justify="right", tcolor="#ffaa54")
fldfn.pack(side="left",padx=3)

# Text box to display data
# text_pre_str = tk.Text(postreadFrame, height=1, width=20)
text_pre_str= mytextbox(postreadFrame, height=1, width=200, bordercolor="#ffff00", fg="transparent",bg="transparent" )
text_pre_str.pack(padx=3, pady=10, side="left")
text_pre_str.insert(tk.END,"KEY_ = \"")
# Text box to display data

# fldfn=tk.Label(postreadFrame,text="post string", bg="#222222", fg="#ffffff")
fldfnn=mylabel(postreadFrame, txt="post string", bg="transparent", justify="right", tcolor="#ffaa54")
fldfnn.pack(side="left", padx=4)

# text_post_str = tk.Text(postreadFrame, height=1, width=20)
text_post_str=  mytextbox(postreadFrame, height=1, width=100, bordercolor="#ffff00", fg="transparent",bg="transparent" )
text_post_str.pack(side="left", padx=4, pady=10)
text_post_str.insert(tk.END,"\"")

# Create a dropdown list (combobox)
# port_dropdown = ttk.Combobox(botomframe, state="readonly", width=30)
port_dropdown= customtkinter.CTkComboBox(buttonFrame, state="readonly", values=["sapi","kebo", "babi"], width=100, border_width=2,border_color="#01595a")
port_dropdown.pack(pady=5, padx=3,side="left")


# Button to start reading
# start_button = ttk.Button(botomframe, text="Start Reading", command=start_reading)
start_button= mybutton(buttonFrame,text="Start Reading",bg=BUTTON_BACKGROUND,activebackground=BUTTON_ACTIVE_BACKGROUND,command=start_reading)
start_button.pack(pady=10)

open_button= mybutton(topTopFrame,text="open",bg=BUTTON_BACKGROUND,activebackground=BUTTON_ACTIVE_BACKGROUND,command=start_reading)
open_button.pack(pady=10, padx=5, side="left")

label_device=mylabel(topTopFrame, txt="Serial Port", bg="transparent", justify="right", tcolor="#ffaa54")
label_device.pack(side="left", padx=10)
device_dropdown= customtkinter.CTkComboBox(topTopFrame, state="readonly", values=["/ttyUSB0","/ttyUSB2", "/ttyUSB1"], width=100, border_width=2,border_color="#01595a")
device_dropdown.pack(pady=5, padx=3,side="left")
cb_rts= customtkinter.CTkCheckBox(topTopFrame, text="RTS", fg_color="#01595a", border_width=2, border_color="#01595a")
cb_rts.pack(pady=5, padx=3,side="left")
cb_dtr= customtkinter.CTkCheckBox(topTopFrame, text="DTR", fg_color="#01595a", border_width=2, border_color="#01595a")
cb_dtr.pack(pady=5, padx=3,side="left")
cb_ar= customtkinter.CTkCheckBox(topTopFrame, text="Auto Reconnect", fg_color="#01595a", border_width=2, border_color="#01595a")
cb_ar.pack(pady=5, padx=3,side="left")

label_baud=mylabel(subTopLeftFrame1, txt="Baudrate", bg="transparent", justify="right", tcolor="#ffaa54")
label_baud.pack(side="left", padx=10)
baudrate_dropdown= customtkinter.CTkComboBox(subTopLeftFrame1, state="readonly", values=["9600","115200", "230400"], width=100, border_width=2,border_color="#01595a")
baudrate_dropdown.pack(pady=5, padx=3,side="left")
label_flow=mylabel(subTopLeftFrame2, txt="Flow Control", bg="transparent", justify="right", tcolor="#ffaa54")
label_flow.pack(side="left", padx=10)
flowrate_dropdown= customtkinter.CTkComboBox(subTopLeftFrame2, state="readonly", values=["None","XON/XOFF", "RTS/CTS"], width=100, border_width=2,border_color="#01595a")
flowrate_dropdown.pack(pady=5, padx=3,side="left")
label_openmode=mylabel(subTopLeftFrame3, txt="Open Mode", bg="transparent", justify="right", tcolor="#ffaa54")
label_openmode.pack(side="left", padx=10)
openmode_dropdown= customtkinter.CTkComboBox(subTopLeftFrame3, state="readonly", values=["Blocking","Non Blocking"], width=100, border_width=2,border_color="#01595a")
openmode_dropdown.pack(pady=5, padx=3,side="left")
label_databit=mylabel(subTopRightFrame1, txt="Data Bit", bg="transparent", justify="right", tcolor="#ffaa54")
label_databit.pack(side="left", padx=10)
databit_dropdown= customtkinter.CTkComboBox(subTopRightFrame1, state="readonly", values=["5","6", "7", "8"], width=100, border_width=2,border_color="#01595a")
databit_dropdown.pack(pady=5, padx=3,side="left")
label_parity=mylabel(subTopRightFrame2, txt="Parity", bg="transparent", justify="right", tcolor="#ffaa54")
label_parity.pack(side="left", padx=10)
parity_dropdown= customtkinter.CTkComboBox(subTopRightFrame2, state="readonly", values=["None","Even", "Odd"], width=100, border_width=2,border_color="#01595a")
parity_dropdown.pack(pady=5, padx=3,side="left")
label_stopbit=mylabel(subTopRightFrame3, txt="Stop Bit", bg="transparent", justify="right", tcolor="#ffaa54")
label_stopbit.pack(side="left", padx=10)
stopbit_dropdown= customtkinter.CTkComboBox(subTopRightFrame3, state="readonly", values=["1","2"], width=100, border_width=2,border_color="#01595a")
stopbit_dropdown.pack(pady=5, padx=3,side="left")

cb_ctrl_char= customtkinter.CTkCheckBox(topNextFrame, text="Control Character", fg_color="#01595a", border_width=2, border_color="#01595a")
cb_ctrl_char.pack(pady=5, padx=3,side="left")
cb_show_timestamp= customtkinter.CTkCheckBox(topNextFrame, text="Show Timestamp", fg_color="#01595a", border_width=2, border_color="#01595a")
cb_show_timestamp.pack(pady=5, padx=3,side="left")

hystory_listbox=CTkListbox(middleFrame, height=300, border_width=2,border_color="#01595a")
hystory_listbox.pack(pady=5, padx=3,side="left", fill="x")
hystory_listbox.insert(0, "Hystory here..")
# label_baud=mylabel(topTopFrame, txt="Baudrate", bg="transparent", justify="right", tcolor="#ffaa54")


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






def on_port_select(event):
	"""Handle the event when a new item is selected in the combobox."""
	selected_port = port_dropdown.get()
	#     print(f"Selected Port: {selected_port}")
	# text_box.insert(tk.END, f"Selected Port: {selected_port}\n")
	applog( f"Selected Port: {selected_port}\n")
	
	if selected_port!= 'COM1':
		if ser and ser.is_open():			
			text_box.insert(tk.END, f"Serial Port: {ser} is open, try to close\n")
			ser.close()
		ser = serial.Serial(selected_port, baudrate=9600, timeout=1)  # Replace 'COM3' with your port

		# pass
	else:
		pass
	root.title("Serial Readerdrop on " + port)


if os.name== 'nt':
	print("we in windows")
	# text_box.insert(tk.END, "we in windows\n")    
	applog( "we in windows\n")
	com_ports = list_com_ports()
	accepted_port=[]
	portn=0
	if com_ports:
		# print("Available COM ports:")
		# port_dropdown['values'] = com_ports	
		port_dropdown.configure(values=com_ports)
		# accepted_port.append(port)
		# text_box.insert(tk.END, "Available COM ports:\n")
		applog( "Available COM ports:\n")
		for port in com_ports:
			portn+=1
			print(port)
			# text_box.insert(tk.END, f"port: {port}\n")
			# text_box.insert(tk.END, f"total port: {portn}\n")
			applog(f"port: {port}\n")
			applog(f"total port: {portn}\n")
			if port !="COM1":
				ser = serial.Serial(port, baudrate=9600, timeout=1)  # Replace 'COM3' with your port
				root.title("Serial Reader on " + port)
		if portn ==1:
			port_dropdown.set(com_ports[0]) 
		else:
			port_dropdown.set(com_ports[1]) 

		
		port_dropdown.configure(values=accepted_port)
		if accepted_port:
			port_dropdown.set(accepted_port[0])	
			ser = serial.Serial(accepted_port[0], baudrate=9600, timeout=1)  # Replace 'COM3' with your port
			
		port_dropdown.bind("<<ComboboxSelected>>", on_port_select)
			
	else:
		print("No COM ports found.")
		# text_box.insert(tk.END, "No COM ports found.\n")
		applog("No COM ports found.\n")
else:
	applog( "we in linux\n")
	com_ports = list_com_ports()
	accepted_port=[]
	if com_ports:
		# port_dropdown['values'] = com_ports	
		# port_dropdown.configure(values=com_ports)
		for port in com_ports:
			# scom_ports=str(com_ports)
			if "/dev/ttyACM" in port or  "/dev/ttyUSB" in port:
				port_dropdown['values'] = port	
				accepted_port.append(port)
				# port_dropdown.configure(values=com_ports)
				# port_dropdown.set(port) 
				applog(port+"\n")		
				# ser = serial.Serial(port, baudrate=9600, timeout=1)  # Replace 'COM3' with your port
				root.title("Serial Reader on " + port)
		
		port_dropdown.configure(values=accepted_port)
		if accepted_port:
			port_dropdown.set(accepted_port[0])	
			ser = serial.Serial(accepted_port[0], baudrate=9600, timeout=1)  # Replace 'COM3' with your port
			
		port_dropdown.bind("<<ComboboxSelected>>", on_port_select)

	# for i in range(9):
	# 	# Configure the serial port
	# 	try:
	# 		ser = serial.Serial('/dev/ttyUSB'+str(i), baudrate=9600, timeout=1)  # Replace 'COM3' with your port
	# 		root.title("Serial Reader on " + 'ttyUSB'+str(i))
	# 		break
	# 	except Exception as e:
	# 		text_box.insert(tk.END, f"Error: {e}\n")

# window.geometry(CenterWindowToDisplay(window, 900, 400, window._get_window_scaling()))
# Start the Tkinter event loop
# root.iconbitmap('rc.ico')
root.mainloop()
