import tkinter as tk
import customtkinter
import platform

# from customtkinter import CTkButton
# from customtkinter import CTkEntry
# from customtkinter import CTk
# from customtkinter import CTkOptionMenu
from customtkinter import *
from CTkListbox import *
from tkinter import ttk
import serial
import threading
import subprocess
import pyperclip
import os
import serial.tools.list_ports
import json

# import ctkmenu

com_ports = []

# https://www.computerhope.com/htmcolor.htm#color-codes
FIRST_SCANNING = False
BACKGROUND = "#d9d9d9"
FOREGROUND = "black"
BUTTON_BACKGROUND = "#08b19a"
BUTTON_ACTIVE_BACKGROUND = "#1fcaf5"
RED = "#FF0000"
GREEN = "#00AA00"
DARKGREEN = "#005800"
BLUE = "#0000FF"
LIGHTBLUE = "#0384FC"
YELLOW = "#FFFF00"
ORANGE = "#FFA500"
PURPLE = "#800080"
PINK = "#FFC0CB"
BROWN = "#A52A2A"
BLACK = "#000000"
WHITE = "#FFFFFF"
GRAY = "#808080"
CYAN = "#00FFFF"
MAGENTA = "#FF00FF"
LIME = "#44FF00"
TEAL = "#008080"
NAVY = "#000080"
MAROON = "#800000"
OLIVE = "#808000"
CORAL = "#FF7F50"
GOLD = "#FFD700"
SILVER = "#C0C0C0"


BG_LVL_1 = NAVY
BG_LVL_2 = BLUE
BG_LVL_3 = LIGHTBLUE
BG_LVL_4 = CYAN
CORNERRADIUS = 10

POINTER_HISTORY = 0
CMD_HISTORY = []
MAX_HISTORY = 50
OSNAME = ""
POPUP_SUGGESTION = False
LBFOCUS = 0
root = customtkinter.CTk()
root.title("Serialone v 1")


# floating_window = ctkmenu.CTkFloatingWindow(root, corner_radius=15, border_width=1)
# floating_window=ctkmenu.CTkFloatingWindow(root)
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
    activeforeground=FOREGROUND,
):
    btn = CTkButton(
        frame, text=text, fg_color=BUTTON_BACKGROUND, command=command, corner_radius=50
    )
    return btn


def myOptionMenu(frame, values, state="", width=10, corner_radius=20, command=""):
    om = CTkOptionMenu(
        frame,
        state=state,
        values=values,
        button_color=BLACK,
        corner_radius=corner_radius,
        text_color=YELLOW,
        dropdown_fg_color=DARKGREEN,
        width=width,
        dropdown_hover_color=BLACK,
        dropdown_text_color=WHITE,
    )
    return om


def myCheckBox(frame, text="", command=""):
    cb = customtkinter.CTkCheckBox(
        frame,
        text=text,
        fg_color=BLACK,
        border_width=2,
        border_color=WHITE,
        text_color=WHITE,
    )
    return cb


def myframe(frame, level=1, width=0, height=0):
    global CORNERRADIUS
    BGC = [0, BG_LVL_1, BG_LVL_2, BG_LVL_3, BG_LVL_4]
    frm = customtkinter.CTkFrame(
        frame,
        border_color=WHITE,
        border_width=0,
        corner_radius=CORNERRADIUS,
        fg_color=BGC[level],
    )
    return frm


# contex menu
def popup_menu2(event, frame):
    try:
        frame.popup(event.x_root, event.y_root)
    finally:
        frame.grab_release()


def popup_menu(event):
    try:
        menu.post(event.x_root, event.y_root)
    except Exception as e:
        print(f"Error: {e}")


def remove_selected():
    print("remove selected")
    selected = hystory_listbox.curselection()
    if selected:
        hystory_listbox.delete(selected)


def clear_history():
    print("clear history")
    hystory_listbox.delete(0, tk.END)
    CMD_HISTORY.clear()
    POINTER_HISTORY = 0
    applog("History cleared\n")


menu = tk.Menu(root, tearoff=0)
# menu = customtkinter.CTkMenu(root, tearoff=0)
menu.add_command(label="remove selected", command=remove_selected)
menu.add_command(label="Clear history", command=clear_history)
menu.add_separator()
menu.add_command(label="Exit", command=root.quit)
# menu.post(event.x_root, event.y_root)


def mytextbox(frame, height, width, bordercolor, bg, fg):
    global CORNERRADIUS
    ctb = customtkinter.CTkTextbox(
        frame,
        height=height,
        width=width,
        border_color=bordercolor,
        bg_color=bg,
        fg_color=fg,
        corner_radius=CORNERRADIUS,
        border_width=0,
    )
    return ctb


def mylabel(frame, txt, bg, justify, tcolor):
    global CORNERRADIUS
    cl = customtkinter.CTkLabel(
        frame,
        text=txt,
        fg_color=bg,
        justify=justify,
        text_color=tcolor,
        corner_radius=CORNERRADIUS,
    )
    return cl


def list_com_ports():
    ports = serial.tools.list_ports.comports()
    available_ports = []
    for port in ports:
        available_ports.append(port.device)
    return available_ports


ser = serial.Serial(None, baudrate=9600, timeout=1)
if ser.isOpen():
    ser.close()
count = 0


# window=CTk()
# def CenterWindowToDisplay(Screen: root, width: int, height: int, scale_factor: float = 1.0):
#     """Centers the window to the main display/monitor"""
#     screen_width = Screen.winfo_screenwidth()
#     screen_height = Screen.winfo_screenheight()
#     x = int(((screen_width/2) - (width/2)) * scale_factor)
#     y = int(((screen_height/2) - (height/1.5)) * scale_factor)
#     return f"{width}x{height}+{x}+{y}"


# hystory_listbox.bind("<Button-3>", popup_menu)
# Function to read serial data
def read_serial():
    global count
    try:
        while True:
            if ser.in_waiting > 0:  # Check if there is data in the serial buffer
                line = (
                    ser.readline().decode("utf-8").strip()
                )  # Read, decode, and strip the newline
                count += 1
                if count == 1:
                    update_textbox(line)  # Update the textbox with the received data
                    applog(string_to_hex(line) if outout_cb.get() == 1 else line)
                if count > 2:
                    count = 0
                # update_textbox(str(count) + " > "+line)  # Update the textbox with the received data
    except Exception as e:
        update_textbox(f"Error: {e}")

def string_to_hex(string):
    return ' '.join(format(ord(c), '02x') for c in string)

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


def draw_history():
    global ser
    global POINTER_HISTORY
    global CMD_HISTORY
    hystory_listbox.delete(0, tk.END)
    for i in range(0, len(CMD_HISTORY)):
        hystory_listbox.insert(i, CMD_HISTORY[i])
    # hystory_listbox.see(tk.END)  # Scroll to the end
    hystory_listbox.see(POINTER_HISTORY)


def update_history(cmd):
    global MAX_HISTORY
    global hystory_listbox
    print(f"update history: {cmd} {hystory_listbox.size()} {MAX_HISTORY}")
    if hystory_listbox.size() > MAX_HISTORY:
        hystory_listbox.delete(0)
    hystory_listbox.insert(tk.END, cmd)
    hystory_listbox.see(tk.END)  # Scroll to the end


def send_command(event):
    global ser
    global POINTER_HISTORY
    global CMD_HISTORY
    command = command_entry.get()
    if command == "":
        applog("No command entered.\n")
        return
    lastlist = hystory_listbox.get(hystory_listbox.size() - 1)
    # print(f'cmd : -{command}- | lastlist : -{lastlist}-')

    # for i in range(0, len(CMD_HISTORY)):
    # 	if command == CMD_HISTORY[i]:
    # 		print(f"command already in history: {command}")
    # 		break

    if command != lastlist:
        # for i in range(0, hystory_listbox.size()):
        # 	if command == hystory_listbox.get(i):
        # 		print(f"command already in listbox: {command}")
        # 		hystory_listbox.delete(i)
        # 		CMD_HISTORY.pop(i)
        # 		hystory_listbox.insert(tk.End, command)
        # 		CMD_HISTORY.append(command)
        # 		break

        if len(CMD_HISTORY) == MAX_HISTORY:
            CMD_HISTORY.pop(0)
        # hystory_listbox.insert(tk.END, command)
        CMD_HISTORY.append(command)
        POINTER_HISTORY = hystory_listbox.size()
        print(f"POINTER_HISTORY: {POINTER_HISTORY}")
        command_entry.delete(0, tk.END)

        for i in range(0, hystory_listbox.size()):
            if command == hystory_listbox.get(i):
                print(f"command already in listbox: {command} at pos {i}")
                hystory_listbox.delete(i)
                CMD_HISTORY.pop(i)
                POINTER_HISTORY = hystory_listbox.size()
                break

        save_history()
        # draw_history()
        update_history(command)
    else:
        hystory_listbox.see(tk.END)  # Scroll to the end

    crlf = crlf_optionmenu.get()
    # crlf = crlf_dropdown.get()
    if crlf == "CRLF":
        command += "\r\n"
    elif crlf == "LF":
        command += "\n"
    elif crlf == "CR":
        command += "\r"
    else:
        pass

    if ser.isOpen():
        write_serial(command)
        applog(f"Command sent: {command}\n")
    else:
        # command_entry.delete(0, tk.END)
        # hystory_listbox.see(tk.END)  # Scroll to the end
        applog("Serial port is not open.\n")


def send_toserial():
    global ser
    global POINTER_HISTORY
    global CMD_HISTORY
    command = command_entry.get()
    if command == "":
        applog("No command entered.\n")
        return
    lastlist = hystory_listbox.get(hystory_listbox.size() - 1)
    if command != lastlist:
        if len(CMD_HISTORY) == MAX_HISTORY:
            CMD_HISTORY.pop(0)
        # hystory_listbox.insert(tk.END, command)
        CMD_HISTORY.append(command)
        POINTER_HISTORY = hystory_listbox.size()
        print(f"POINTER_HISTORY: {POINTER_HISTORY}")
        command_entry.delete(0, tk.END)

        for i in range(0, hystory_listbox.size()):
            if command == hystory_listbox.get(i):
                print(f"command already in listbox: {command} at pos {i}")
                hystory_listbox.delete(i)
                CMD_HISTORY.pop(i)
                POINTER_HISTORY = hystory_listbox.size()
                break

        save_history()
        # draw_history()
        update_history(command)
    else:
        hystory_listbox.see(tk.END)  # Scroll to the end

    crlf = crlf_optionmenu.get()
    # crlf = crlf_dropdown.get()
    if crlf == "CRLF":
        command += "\r\n"
    elif crlf == "LF":
        command += "\n"
    elif crlf == "CR":
        command += "\r"
    else:
        pass

    if ser.isOpen():
        write_serial(command)
        applog(f"Command sent: {command}\n")
    else:
        applog("Serial port is not open.\n")


def traceBackCommand(event):
    global ser
    global POINTER_HISTORY
    global POPUP_SUGGESTION
    if POPUP_SUGGESTION:
        return  
    # hystory_listbox.selection_set(0)
    # command = hystory_listbox.get(hystory_listbox.curselection(POINTER_HISTORY))
    POINTER_HISTORY = POINTER_HISTORY - 1
    command = hystory_listbox.get(POINTER_HISTORY)
    if POINTER_HISTORY > 1 and POINTER_HISTORY < hystory_listbox.size():
        tmpPH = POINTER_HISTORY - 1
        for i in range(3, 0, -1):
            if (POINTER_HISTORY - i) >= 0:
                tmpPH = POINTER_HISTORY - i
                # hystory_listbox.see(tmpPH)
                break
        hystory_listbox.see(tmpPH)
    # POINTER_HISTORY=POINTER_HISTORY - 1
    if ser.isOpen():
        # write_serial(command)
        # applog(f"Command sent: {command}\n")
        command_entry.delete(0, tk.END)
        command_entry.insert(0, command)
    else:
        command_entry.delete(0, tk.END)
        applog("Serial port is not open.\n")


def traceForwardCommand(event):
    global ser
    global POINTER_HISTORY
    global POPUP_SUGGESTION
    if POPUP_SUGGESTION:
        return  
    POINTER_HISTORY = POINTER_HISTORY + 1
    print(
        f"POINTER HISTORY : {POINTER_HISTORY} | CMD_HISTORY size : {len(CMD_HISTORY)}"
    )
    if POINTER_HISTORY > (len(CMD_HISTORY) - 1):
        POINTER_HISTORY = len(CMD_HISTORY) - 1
    command = hystory_listbox.get(POINTER_HISTORY)
    if POINTER_HISTORY > 1 and POINTER_HISTORY < hystory_listbox.size():
        hystory_listbox.see(POINTER_HISTORY)
    hystory_listbox.see(POINTER_HISTORY + 1)
    # hystory_listbox.bind(("<Button-4>", on_mouse_wheel_listbox))
    # POINTER_HISTORY=POINTER_HISTORY + 1
    if ser.isOpen():
        # write_serial(command)
        # applog(f"Command sent: {command}\n")
        command_entry.delete(0, tk.END)
        command_entry.insert(0, command)
    else:
        command_entry.delete(0, tk.END)
        command_entry.insert(0, command)
        # command_entry.delete(0, tk.END)
        applog("Serial port is not open.\n")


def on_hystory_select(event):
    global POINTER_HISTORY
    """Handle the event when a new item is selected in the listbox."""
    POINTER_HISTORY = hystory_listbox.curselection()
    print(f"POINTER_HISTORY select: {POINTER_HISTORY}")
    selected_item = hystory_listbox.get(hystory_listbox.curselection())
    applog(f"Selected item: {selected_item}\n")
    command_entry.delete(0, tk.END)
    command_entry.insert(0, selected_item)
    command_entry.focus()
    # hystory_listbox.bind("<<ListboxSelect>>", on_hystory_select)
    # hystory_listbox.bind("<Double-Button-1>", traceBackCommand)
    # hystory_listbox.bind("<Button-3>", traceForwardCommand)


def on_hystory_double_click(event):
    """Handle the event when a new item is selected in the listbox."""
    selected_item = hystory_listbox.get(hystory_listbox.curselection())
    applog(f"send item: {selected_item}\n")

    command_entry.delete(0, tk.END)
    command_entry.insert(0, selected_item)
    send_toserial()

    # if ser.is_open():
    # 	ser.write(selected_item.encode("utf-8"))
    # 	command_entry.delete(0, tk.END)
    # hystory_listbox.bind("<<ListboxSelect>>", on_hystory_select)
    # hystory_listbox.bind("<Double-Button-1>", traceBackCommand)
    # hystory_listbox.bind("<Button-3>", traceForwardCommand)


# Function to update the tkinter Text widget
def update_textbox(line):
    # applog(line+"\n")
    filtr = text_filter.get(1.0, "end-1c")
    if filtr != "":
        if filtr in line:
            # print("contain "+ filtr)
            dfn = text_pre_str.get(1.0, "end-1c")
            poststring = text_post_str.get(1.0, "end-1c")
            if dfn != "":
                line = dfn + line
            if poststring != " ":
                line += poststring
            text_box.insert(tk.END, f"{line}\n")
            text_box.see(tk.END)  # Scroll to the end
    if line != "":
        # if datamode_dropdown.get()=="ASCII":
        if datamode_option.get() == "ASCII":
            applog(line + "\n")
        # elif datamode_dropdown.get()=="HEX":
        elif databit_option.get() == "HEX":
            applog(line.encode())
            applog("\n")


def applog(msg):
    # texbox_monitor.delete("1.0", "end")
    texbox_monitor.insert(tk.END, msg)
    if auto_scroll_cb.get() == 1:
        texbox_monitor.see(tk.END)


# Start the serial reading in a separate thread
def start_reading():
    print("start reading")
    open_button.configure(text="close", command=close_serial)
    sh_setting_button.configure(text="show setting")
    sh_setting_button.pack_forget()
    bottomTopFrame.pack_forget()
    thread = threading.Thread(target=read_serial, daemon=True)
    thread.start()
    # inputFrame.pack(fill="x", side="top", padx=5, pady=5)
    monitorframe.pack_forget()
    statusFrame.pack_forget()
    middleFrame.pack(fill="x", side="top", pady=2)    
    monitorframe.pack(side="top", expand=True, fill="both", pady=2)
    statusFrame.pack(side="top", fill="x", pady=2)


def close_serial():
    global ser
    if ser.isOpen():
        ser.close()
        open_button.configure(text="open", command=setupserial)
        text_box.insert(tk.END, f"Serial Port: {ser} is closed\n")
        applog(f"Serial Port: {ser} is closed\n")
        sh_setting_button.pack(side="left", padx=5, pady=5)
        # inputFrame.pack_forget()
        middleFrame.pack_forget()
    # else:

    # 	open_button.configure(text="open", command=start_reading)
    # 	text_box.insert(tk.END, f"Serial Port: {ser} is already closed\n")
    # 	applog( f"Serial Port: {ser} is already closed\n")
    status_label.configure(text="Serial closed")


def cleartb():
    text_box.delete("1.0", "end")


def clear_monitor():
    texbox_monitor.delete("1.0", "end")


def copytoclip():
    filtr = text_box.get(1.0, "end-1c")
    pyperclip.copy(filtr)
    # subprocess.run("pbcopy", text=True, input=filtr)


def paste_from_clipboard():
    try:
        clipboard_content = pyperclip.paste()
        command_entry.insert(tk.INSERT, clipboard_content)
    except Exception as e:
        print(f"Error pasting from clipboard: {e}")
def paste_and_send():
    paste_from_clipboard()
    send_toserial()

def clear_and_paste_from_clipboard():
    command_entry.delete(0, tk.END)
    paste_from_clipboard()

def show_context_menu(event):
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Paste", command=paste_from_clipboard)
    context_menu.add_command(label="paste and send", command=paste_and_send)
    context_menu.add_command(label="Clear and Paste", command=clear_and_paste_from_clipboard)
    context_menu.tk_popup(event.x_root, event.y_root)


class SuggestionPopup:
    def __init__(self, entry_widget, history_list):
        self.entry = entry_widget
        self.history = history_list
        self.popup = None
        self.listbox = None
        
        self.entry.bind("<KeyRelease>", self.on_key_release)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.entry.bind("<Down>", self.on_arrow_down)
        self.entry.bind("<Up>", self.on_arrow_up)
        self.entry.bind("<Return>", self.on_return)

    def on_key_release(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return

        typed_text = self.entry.get()
        if not typed_text:
            self.hide_popup()
            return

        matches = [item for item in self.history if typed_text.lower() in item.lower()]
        if matches:
            self.show_popup(matches)
        else:
            self.hide_popup()

    def show_popup(self, matches):
        if not self.popup:
            # unbind_command_entry()
            global POPUP_SUGGESTION
            POPUP_SUGGESTION = True
            self.popup = tk.Toplevel(self.entry)
            self.popup.wm_overrideredirect(True)
            self.popup.wm_geometry(f"+{self.entry.winfo_rootx()}+{self.entry.winfo_rooty() + self.entry.winfo_height()}")
            
            self.listbox = tk.Listbox(self.popup, height=5)
            self.listbox.pack(fill="both", expand=True)
            self.listbox.bind("<Button-1>", self.on_selection)
            self.listbox.bind("<Return>", self.on_selection)
            
        self.listbox.delete(0, tk.END)
        for item in matches:
            self.listbox.insert(tk.END, item)
        self.listbox.select_set(0)

    def hide_popup(self):
        if self.popup:
            # bind_command_entry()
            global POPUP_SUGGESTION
            POPUP_SUGGESTION = False
            self.popup.destroy()
            self.popup = None
            self.listbox = None

    def on_focus_out(self, event):
        # Delay hiding to allow click event on listbox to register
        self.entry.after(100, self.hide_popup)

    def on_selection(self, event=None):
        if self.listbox:
            selection = self.listbox.curselection()
            if selection:
                selected_text = self.listbox.get(selection[0])
                self.entry.delete(0, tk.END)
                self.entry.insert(0, selected_text)
                self.hide_popup()
                self.entry.focus_set()
                send_command(None)

    def on_arrow_down(self, event):
        if self.listbox:
            current_selection = self.listbox.curselection()
            if current_selection:
                next_index = min(current_selection[0] + 1, self.listbox.size() - 1)
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(next_index)
                self.listbox.see(next_index)
                
                selected_text = self.listbox.get(next_index)
                self.entry.delete(0, tk.END)
                print(f"selected_text: {selected_text}")
                self.entry.insert(0, selected_text)
            else:
                 self.listbox.select_set(0)
                 selected_text = self.listbox.get(0)
                 self.entry.delete(0, tk.END)
                 self.entry.insert(0, selected_text)

    def on_arrow_up(self, event):
        if self.listbox:
            current_selection = self.listbox.curselection()
            if current_selection:
                prev_index = max(current_selection[0] - 1, 0)
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(prev_index)
                self.listbox.see(prev_index)
                
                selected_text = self.listbox.get(prev_index)
                self.entry.delete(0, tk.END)
                print(f"selected_text: {selected_text}")
                self.entry.insert(0, selected_text)

    def on_return(self, event):
        if self.popup:
            self.on_selection()
            return "break" # Prevent default return behavior if popup is open


# Main Tkinter window


def on_baudrate_select(event):
    """Handle the event when a new item is selected in the combobox."""
    # selected_baudrate = baudrate_dropdown.get()
    selected_baudrate = baudrate_option.get()
    applog(f"Selected Baudrate: {selected_baudrate}\n")
    if selected_baudrate != "custom":
        if ser and ser.isOpen():
            text_box.insert(tk.END, f"Serial Port: {ser} is open, try to close\n")
            ser.close()
        # ser = serial.Serial(device_dropdown.get(), baudrate=int(selected_baudrate), timeout=1)
        setupserial()  # Replace 'COM3' with your port
    else:
        pass


def show_setting():
    global ser
    print("show setting")
    if ser.isOpen() == False:
        if sh_setting_button.cget("text") == "show setting":
            print("show setting")
            sh_setting_button.configure(text="hide setting")
            bottomTopFrame.pack(after=topTopFrame, side="top", padx=5, pady=5, fill="x")
        else:
            print("hide setting")
            sh_setting_button.configure(text="show setting")
            bottomTopFrame.pack_forget()


def on_flowrate_select(event):
    global ser
    """Handle the event when a new item is selected in the combobox."""
    # print(f"Selected Flow Control: {selected_flowrate}")
    # selected_flowrate = flowrate_dropdown.get()
    selected_flowrate = flowrate_option.get()
    applog(f"Selected Flow Control: {selected_flowrate}\n")
    if selected_flowrate == "none":
        if ser and ser.isOpen():
            text_box.insert(tk.END, f"Serial Port: {ser} is open, try to close\n")
            cb_rts.pack(after=device_dropdown, side="left")  # show the RTS checkbox
            cb_dtr.pack(after=cb_rts, side="left")
        # 	ser.close()
        # ser = serial.Serial(device_dropdown.get(), baudrate=int(selected_baudrate), timeout=1)  # Replace 'COM3' with your port
    elif selected_flowrate == "Hardware":
        if ser and ser.isOpen():
            text_box.insert(tk.END, f"Serial Port: {ser} is open, try to close\n")
            cb_rts.pack_forget()  # hide the RTS checkbox
            cb_dtr.pack_forget()
        # 	ser.close()
        # ser = serial.Serial(device_dropdown.get(), baudrate=int(selected_baudrate), timeout=1)
    elif selected_flowrate == "Software":
        if ser and ser.isOpen():
            text_box.insert(tk.END, f"Serial Port: {ser} is open, try to close\n")
            cb_rts.pack(side="left")  # show the RTS checkbox
            cb_dtr.pack(side="left")
        # 	ser.close()
        # ser = serial.Serial(device_dropdown.get(), baudrate=int(selected_baudrate), timeout=1)
    else:
        pass


def on_parity_select(event):
    global ser
    """Handle the event when a new item is selected in the combobox."""
    selected_parity = parity_dropdown.get()
    applog(f"Selected Parity: {selected_parity}\n")
    if selected_parity != "none":
        if ser and (ser.isOpen() == True):
            text_box.insert(tk.END, f"Serial Port: {ser} is open, try to close\n")
            ser.close()
        setupserial
        # ser = serial.Serial(device_dropdown.get(), baudrate=int(baudrate_dropdown.get()), parity=getParity(selected_parity), timeout=1)  # Replace 'COM3' with your port
    else:
        pass


def on_port_select(event):
    global ser
    """Handle the event when a new item is selected in the combobox."""
    selected_port = device_dropdown.get()
    print(f"Selected Port: {selected_port}")
    # text_box.insert(tk.END, f"Selected Port: {selected_port}\n")
    applog(f"Selected Port: {selected_port}\n")

    if selected_port != "COM1":
        if ser and ser.isOpen():
            text_box.insert(tk.END, f"Serial Port: {ser} is open, try to close\n")
            ser.close()
        # ser = serial.Serial(selected_port, baudrate=9600, timeout=1)  # Replace 'COM3' with your port

        # pass
    else:
        pass
    root.title("Serial Readerdrop on " + port)


def on_mouse_wheel_listbox(event):
    global LBFOCUS
    """Handle the event when the mouse wheel is scrolled."""
    print(f"Mouse wheel scrolled: {event.delta}")
    if event.delta > 0:
        LBFOCUS -= 1
        # hystory_listbox.yview_scroll(-1, "units")
        # hystory_listbox.
    else:
        LBFOCUS += 1
        # hystory_listbox.yview_scroll(1, "units")

    hystory_listbox.select(LBFOCUS)
    hystory_listbox.see(LBFOCUS)


def on_mouse_wheel_listbox_up(event):
    global LBFOCUS
    LBFOCUS -= 1
    hystory_listbox.select(LBFOCUS)
    hystory_listbox.see(LBFOCUS)


def on_mouse_wheel_listbox_down(event):
    global LBFOCUS
    LBFOCUS += 1
    hystory_listbox.select(LBFOCUS)
    hystory_listbox.see(LBFOCUS)


def on_mouse_wheel_entry(event):
    """Handle the event when the mouse wheel is scrolled."""
    print(f"Mouse wheel scrolled: {event.delta}")

    global LBFOCUS
    """Handle the event when the mouse wheel is scrolled."""
    print(f"Mouse wheel scrolled: {event.delta}")
    if event.delta > 0:
        LBFOCUS -= 1
        # hystory_listbox.yview_scroll(-1, "units")
        # hystory_listbox.
    else:
        LBFOCUS += 1
        # hystory_listbox.yview_scroll(1, "units")

    hystory_listbox.select(LBFOCUS)
    hystory_listbox.see(LBFOCUS)
    # if event.delta > 0:
    # 	# hystory_listbox.yview_scroll(-1, "units")
    # 	traceBackCommand
    # else:
    # 	# hystory_listbox.yview_scroll(1, "units")
    # 	traceForwardCommand


def on_cb_ar_change(event):
    print("ar cb check box changed")
    save_config()


# topFrame = tk.Frame(root, padx=0, bg="#ffff44")
# ====level 1 frame=========
# topFrame=customtkinter.CTkFrame(root,border_width=0,border_color="#000000",fg_color=BG_LVL_1, width=300, height=100,corner_radius=10)
topFrame = myframe(root, level=1, height=100)
topFrame.pack(side="top", fill="x", pady=2)
# middleFrame= customtkinter.CTkFrame(root, width=300, height=100, border_width=0, border_color="#aaff00", fg_color=BG_LVL_1)
middleFrame = myframe(root, level=1)
# middleFrame.pack(fill="x", side="top", pady=2)

# monitorframe= customtkinter.CTkFrame(root, width=300, height=100, border_width=0, border_color="#aaff00", fg_color=BG_LVL_1)
monitorframe = myframe(root, level=1)
monitorframe.pack(side="top", expand=True, fill="both", pady=2)
# statusFrame= customtkinter.CTkFrame(root, width=300, height=100, border_width=0, border_color="#aaff00", fg_color=BG_LVL_1)
statusFrame = myframe(root, level=1)
statusFrame.pack(side="top", fill="x", pady=2)
# ===========level 2 frame=========
# topTopFrame= customtkinter.CTkFrame(topFrame, width=300, height=100, border_width=0, border_color="#aaff00", fg_color=BG_LVL_2)
topTopFrame = myframe(topFrame, level=2, height=100)
topTopFrame.pack(side="top", padx=5, pady=5, fill="x")
# bottomTopFrame= customtkinter.CTkFrame(topFrame, width=300, height=100, border_width=0, border_color="#aaff00", fg_color=BG_LVL_2)
bottomTopFrame = myframe(topFrame, level=2)
# bottomTopFrame.pack(after=topTopFrame, side="top", padx=5, pady=5, fill="x")

# topLeftFrame= customtkinter.CTkFrame(bottomTopFrame, width=300,  border_width=0, border_color="#aaff00", fg_color=BG_LVL_3)
topLeftFrame = myframe(bottomTopFrame, level=3)
topLeftFrame.pack(side="left", padx=5, pady=5)
# topRightFrame= customtkinter.CTkFrame(bottomTopFrame, width=300, border_width=0, border_color="#aaff00", fg_color=BG_LVL_3)
topRightFrame = myframe(bottomTopFrame, level=3)
topRightFrame.pack(side="left", padx=5, pady=5)
# topNextFrame= customtkinter.CTkFrame(bottomTopFrame, width=300, border_width=0, border_color="#aaff00", fg_color=BG_LVL_3)
topNextFrame = myframe(bottomTopFrame, level=3)
topNextFrame.pack(side="left", padx=5, pady=5, fill="both", expand=True)

# subTopLeftFrame1= customtkinter.CTkFrame(topLeftFrame, width=300, height=100, border_width=0, border_color="#aaff00", fg_color=BG_LVL_4)
subTopLeftFrame1 = myframe(topLeftFrame, level=4)
subTopLeftFrame1.pack(side="top", padx=5, pady=5, expand=True, fill="x")
subTopLeftFrame2 = customtkinter.CTkFrame(
    topLeftFrame,
    width=300,
    height=100,
    border_width=0,
    border_color="#aaff00",
    fg_color=BG_LVL_4,
)
subTopLeftFrame2.pack(side="bottom", padx=5, pady=5, expand=True, fill="x")
subTopLeftFrame3 = customtkinter.CTkFrame(
    topLeftFrame,
    width=300,
    height=100,
    border_width=0,
    border_color="#aaff00",
    fg_color=BG_LVL_4,
)
subTopLeftFrame3.pack(side="bottom", padx=5, pady=5, expand=True, fill="x")
subTopRightFrame1 = customtkinter.CTkFrame(
    topRightFrame,
    width=300,
    height=100,
    border_width=0,
    border_color="#aaff00",
    fg_color=BG_LVL_4,
)
subTopRightFrame1.pack(side="top", padx=5, pady=5, expand=True, fill="x")
subTopRightFrame2 = customtkinter.CTkFrame(
    topRightFrame,
    width=300,
    height=100,
    border_width=0,
    border_color="#aaff00",
    fg_color=BG_LVL_4,
)
subTopRightFrame2.pack(side="bottom", padx=5, pady=5, expand=True, fill="x")
subTopRightFrame3 = customtkinter.CTkFrame(
    topRightFrame,
    width=300,
    height=100,
    border_width=0,
    border_color="#aaff00",
    fg_color=BG_LVL_4,
)
subTopRightFrame3.pack(side="bottom", padx=5, pady=5, expand=True, fill="x")

historyFrame = customtkinter.CTkFrame(
    middleFrame, height=200, border_width=2, border_color=RED, fg_color=BG_LVL_1
)
# historyFrame.pack(pady=1, padx=1, expand=True, side="top", fill="x")
hystory_listbox = CTkListbox(
    middleFrame,
    label_text="history",
    label_fg_color=BLACK,
    label_text_color=WHITE,
    height=200,
    border_width=1,
    border_color="#01595a",
    bg_color=NAVY,
    fg_color=CYAN,
    hover_color=LIME,
    highlight_color=WHITE,
    text_color=NAVY,
    scrollbar_button_color=BLACK,
    corner_radius=CORNERRADIUS,
)
hystory_listbox.pack(padx=5, pady=5, expand=True, side="top", fill="x")
hystory_listbox.insert(0, "Hystory here..")
# inputFrame= customtkinter.CTkFrame(middleFrame, width=300, height=100, border_width=0, border_color="#aaff00", fg_color=BG_LVL_2)
inputFrame = myframe(middleFrame, level=2)
inputFrame.pack(fill="x", side="top", padx=5, pady=5)
# inputFrame.visible = False

status_label = mylabel(
    statusFrame, txt="Status", bg="transparent", justify="left", tcolor=YELLOW
)
# status_label=customtkinter.CTkLabel(statusFrame, wraplength=100, text="Status", fg_color="transparent", justify="right", text_color=NAVY)
# status_label.configure(wraplength=300)
status_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")

command_entry = customtkinter.CTkEntry(
    inputFrame,
    width=220,
    height=30,
    border_width=0,
    border_color="#aaff00",
    fg_color=CYAN,
    text_color=BROWN,
    corner_radius=CORNERRADIUS,
)
command_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
command_entry.bind("<Button-3>", show_context_menu)
suggestion_popup = SuggestionPopup(command_entry, CMD_HISTORY)

send_button = customtkinter.CTkButton(
    inputFrame,
    text="Send",
    command=send_toserial,
    width=100,
    height=30,
    border_width=0,
    border_color="#aaff00",
    fg_color=CYAN,
    text_color=BROWN,
    corner_radius=CORNERRADIUS,
)
send_button.pack(side="left", padx=5, pady=5)
crlf_dropdown = customtkinter.CTkComboBox(
    inputFrame,
    state="readonly",
    values=["CRLF", "LF", "CR"],
    width=100,
    border_width=2,
    border_color="#01595a",
)
# crlf_dropdown.pack(pady=5, padx=3,side="left")
crlf_optionmenu = myOptionMenu(inputFrame, values=["CRLF", "CR", "LF"], width=50)
crlf_optionmenu.pack(pady=5, padx=3, side="left")
chr_del_label = mylabel(
    inputFrame, txt="chr del", bg="transparent", justify="right", tcolor=WHITE
)
chr_del_label.pack(side="left", padx=10)
chr_del_dropdown = customtkinter.CTkComboBox(
    inputFrame,
    state="readonly",
    values=["off", "1 MS", "2MS"],
    width=100,
    border_width=2,
    border_color="#01595a",
)
chr_del_dropdown.pack(pady=5, padx=3, side="left")
sendfile_button = mybutton(
    inputFrame,
    text="send file",
    bg=BUTTON_BACKGROUND,
    activebackground=BUTTON_ACTIVE_BACKGROUND,
    command=start_reading,
)
sendfile_button.pack(pady=5, padx=3, side="left")
datamode_dropdown = customtkinter.CTkComboBox(
    inputFrame,
    state="readonly",
    values=["ASCII", "HEX", "BINARY"],
    width=100,
    border_width=2,
    border_color="#01595a",
)
# datamode_dropdown.pack(pady=5, padx=3,side="left")
datamode_option = myOptionMenu(
    inputFrame, state="readonly", values=["ASCII", "HEX", "BINARY"], width=100
)
datamode_option.pack(pady=5, padx=3, side="left")
# resultFrame = tk.Frame(topFrame, padx=20, pady=4, bg="#2266ff")
# ===========#monitor

texbox_monitor = mytextbox(
    monitorframe,
    height=200,
    width=500,
    bordercolor="#ffff00",
    fg=YELLOW,
    bg="transparent",
)
texbox_monitor.configure(text_color=BLACK)
texbox_monitor.pack(padx=5, fill="both", expand=True, pady=5)

# resultControlFrame= customtkinter.CTkFrame(monitorframe,  border_width=0, border_color="#aaff00", fg_color=BG_LVL_2)
resultControlFrame = myframe(monitorframe, level=2)
resultControlFrame.pack(fill="x", pady=5, side="top", padx=5)

resultFrame = customtkinter.CTkFrame(
    middleFrame,
    width=300,
    height=100,
    border_width=0,
    border_color="#aaff00",
    fg_color=BG_LVL_2,
)
# resultFrame.pack(fill="x",side="bottom")

filterFrame = customtkinter.CTkFrame(
    middleFrame,
    width=300,
    height=100,
    border_width=0,
    border_color="#aaff00",
    fg_color="#00a6a0",
)
# filterFrame.pack(fill="x",side="top")

postreadFrame = customtkinter.CTkFrame(
    filterFrame, border_width=0, border_color="#aaff00", fg_color="#00b8cc"
)
# postreadFrame.pack(fill="x",side="right")
clear_button2 = mybutton(
    resultControlFrame,
    text="clear",
    bg=BUTTON_BACKGROUND,
    activebackground=BUTTON_ACTIVE_BACKGROUND,
    command=clear_monitor,
)
clear_button2.pack(pady=5, padx=3, side="left")

auto_scroll_cb = myCheckBox(resultControlFrame, text="Auto scroll")
auto_scroll_cb.pack(pady=5, padx=3, side="left")
# outout_cb= customtkinter.CTkCheckBox(resultControlFrame, text="Output", fg_color="#01595a", border_width=2, border_color="#01595a")
outout_cb = myCheckBox(resultControlFrame, text="Hex Output")
outout_cb.pack(pady=5, padx=3, side="left")
# logging_to_file_cb= customtkinter.CTkCheckBox(resultControlFrame, text="Log to file", fg_color="#01595a", border_width=2, border_color="#01595a")
logging_to_file_cb = myCheckBox(resultControlFrame, text="Log to file")
logging_to_file_cb.pack(pady=5, padx=3, side="left")
logpath_button = mybutton(
    resultControlFrame,
    text="log path",
    bg=BUTTON_BACKGROUND,
    activebackground=BUTTON_ACTIVE_BACKGROUND,
    command=start_reading,
)
logpath_button.pack(pady=5, padx=3, side="left")
logPath_textbox = customtkinter.CTkTextbox(
    resultControlFrame,
    height=1,
    width=100,
    border_width=0,
    border_color="#aaff00",
    fg_color="#00b8cc",
)
logPath_textbox.pack(pady=5, padx=3, side="left")


# Text box to display data
# text_box = tk.Text(resultFrame, height=20, width=50)
text_box = mytextbox(
    resultFrame,
    height=300,
    width=500,
    bordercolor="#ffff00",
    fg="transparent",
    bg="transparent",
)
text_box.pack(padx=1, pady=1, fill="x")

buttonFrame = customtkinter.CTkFrame(
    resultFrame,
    width=300,
    height=100,
    border_width=0,
    border_color="#aaff00",
    fg_color="#b85f07",
)
# buttonFrame.pack(fill="x", side="bottom")

# Button to clear text area
clear_button = CTkButton(buttonFrame, text="clear", command=cleartb, corner_radius=50)
clear_button.pack(side="left", pady=2, padx=5)

# Button copy to clipboard
# ctc_button = ttk.Button(buttonFrame, text="copy to clipboard", command=copytoclip)
ctc_button = mybutton(
    buttonFrame,
    text="copy to clipboard",
    bg=BUTTON_BACKGROUND,
    activebackground=BUTTON_ACTIVE_BACKGROUND,
    command=copytoclip,
)
ctc_button.pack(side="left", pady=2, padx=5)

clr_btn = mybutton(
    buttonFrame,
    text="clear text",
    bg=BUTTON_BACKGROUND,
    activebackground=BUTTON_ACTIVE_BACKGROUND,
    command=cleartb,
)
clr_btn.pack(side="left", pady=2, padx=5)
# Text box to display data

# flbel=tk.Label(filterFrame,text="result filter")
flbel = mylabel(
    filterFrame, txt="result filter", bg="transparent", justify="right", tcolor=NAVY
)
flbel.pack(side="left", padx=10)
# Text box to display data
# text_filter = tk.Text(filterFrame, height=1, width=30 )
text_filter = mytextbox(
    filterFrame,
    height=1,
    width=100,
    bordercolor="#ffff00",
    fg="transparent",
    bg="transparent",
)
text_filter.pack(side="left", padx=0, pady=10)
text_filter.insert(tk.END, "FD")


# fldfn=tk.Label(postreadFrame,text="pre string", bg="#222222", fg="#ffffff")
fldfn = mylabel(
    postreadFrame, txt="pre string", bg="transparent", justify="right", tcolor=NAVY
)
fldfn.pack(side="left", padx=3)

# Text box to display data
# text_pre_str = tk.Text(postreadFrame, height=1, width=20)
text_pre_str = mytextbox(
    postreadFrame,
    height=1,
    width=200,
    bordercolor="#ffff00",
    fg="transparent",
    bg="transparent",
)
text_pre_str.pack(padx=3, pady=10, side="left")
text_pre_str.insert(tk.END, 'KEY_ = "')
# Text box to display data

# fldfn=tk.Label(postreadFrame,text="post string", bg="#222222", fg="#ffffff")
fldfnn = mylabel(
    postreadFrame, txt="post string", bg="transparent", justify="right", tcolor=NAVY
)
fldfnn.pack(side="left", padx=4)

# text_post_str = tk.Text(postreadFrame, height=1, width=20)
text_post_str = mytextbox(
    postreadFrame,
    height=1,
    width=100,
    bordercolor="#ffff00",
    fg="transparent",
    bg="transparent",
)
text_post_str.pack(side="left", padx=4, pady=10)
text_post_str.insert(tk.END, '"')

# Create a dropdown list (combobox)
# port_dropdown = ttk.Combobox(monitorframe, state="readonly", width=30)
port_dropdown = customtkinter.CTkComboBox(
    buttonFrame,
    state="readonly",
    values=["sapi", "kebo", "babi"],
    width=100,
    border_width=2,
    border_color="#01595a",
)
port_dropdown.pack(pady=5, padx=3, side="left")


# Button to start reading
# start_button = ttk.Button(monitorframe, text="Start Reading", command=start_reading)
start_button = mybutton(
    buttonFrame,
    text="Start Reading",
    bg=BUTTON_BACKGROUND,
    activebackground=BUTTON_ACTIVE_BACKGROUND,
    command=start_reading,
)
start_button.pack(pady=10)

open_button = mybutton(
    topTopFrame,
    text="open",
    bg=BUTTON_BACKGROUND,
    activebackground=BUTTON_ACTIVE_BACKGROUND,
    command=start_reading,
)
open_button.pack(pady=10, padx=5, side="left")

label_device = mylabel(
    topTopFrame, txt="Serial Port", bg="transparent", justify="right", tcolor=YELLOW
)
label_device.pack(side="left", padx=10)
device_dropdown = customtkinter.CTkComboBox(
    topTopFrame,
    state="readonly",
    values=["/ttyUSB0", "/ttyUSB2", "/ttyUSB1"],
    width=100,
    border_width=2,
    border_color="#01595a",
    command=on_port_select,
)
# device_dropdown.pack(pady=5, padx=3,side="left")
device_option = myOptionMenu(
    topTopFrame,
    values=["serial port"],
    width=100,
    corner_radius=8,
    command=on_port_select,
)
device_option.pack(pady=5, padx=3, side="left")

# The OptionMenu is a button with a menu attached. The menu typically grows in height until it reaches the edge of the screen. The choices are fixed, and the user can't type in their own value.

# A Combobox is in effect an Entry widget with a dropdown listbox. The user has the ability (if properly configured) to type into the combobox or pick from the dropdown list. The dropdown list is typically constrained to a handful of rows, with a scrollbar when the list gets to long to fit.

# The Combobox is also a bit easier to add and remove items after the widget has been created. The OptionMenu was designed to have a static number of items that are set when the widget is created.

# cb_rts= customtkinter.CTkCheckBox(topTopFrame, text="RTS", fg_color=RED, border_width=2, border_color=YELLOW, text_color=GREEN)
cb_rts = myCheckBox(topTopFrame, text="RTS")
cb_rts.pack(pady=5, padx=3, side="left")
# cb_dtr= customtkinter.CTkCheckBox(topTopFrame, text="DTR", fg_color=RED, border_width=2, border_color=YELLOW, text_color=GREEN)
cb_dtr = myCheckBox(topTopFrame, text="DTR")
cb_dtr.pack(pady=5, padx=3, side="left")
# cb_ar= customtkinter.CTkCheckBox(topTopFrame, text="Auto Reconnect", fg_color=RED, border_width=2, border_color=YELLOW, text_color=GREEN)
cb_ar = myCheckBox(topTopFrame, text="Auto reconnect", command=on_cb_ar_change)
# cb_ar.configure(onvalue="on",offvalue="off")
cb_ar.pack(pady=5, padx=3, side="left")


sh_setting_button = mybutton(
    topTopFrame,
    text="show setting",
    bg=BUTTON_BACKGROUND,
    activebackground=BUTTON_ACTIVE_BACKGROUND,
    command=show_setting,
)
sh_setting_button.pack(pady=10, padx=5, side="left")

label_baud = mylabel(
    subTopLeftFrame1, txt="Baudrate", bg="transparent", justify="right", tcolor=NAVY
)
label_baud.pack(side="left", padx=10)
baudrate_dropdown = customtkinter.CTkComboBox(
    subTopLeftFrame1,
    state="readonly",
    values=[
        "1200",
        "4800",
        "9600",
        "19100",
        "38400",
        "57600",
        "115200",
        "230400",
        "custom",
    ],
    width=100,
    border_width=2,
    border_color="#01595a",
    command=on_baudrate_select,
)
# baudrate_dropdown.pack(pady=5, padx=3,side="right")
baudrate_option = myOptionMenu(
    subTopLeftFrame1,
    values=[
        "1200",
        "4800",
        "9600",
        "19100",
        "38400",
        "57600",
        "115200",
        "230400",
        "custom",
    ],
    width=100,
    command=on_baudrate_select,
)
baudrate_option.pack(pady=5, padx=3, side="right")
label_flow = mylabel(
    subTopLeftFrame2, txt="Flow Control", bg="transparent", justify="right", tcolor=NAVY
)
label_flow.pack(side="left", padx=10)
flowrate_dropdown = customtkinter.CTkComboBox(
    subTopLeftFrame2,
    state="readonly",
    values=["none", "Hardware", "Software"],
    width=100,
    border_width=2,
    border_color="#01595a",
    command=on_flowrate_select,
)
# flowrate_dropdown.pack(pady=5, padx=3,side="right")
flowrate_option = myOptionMenu(
    subTopLeftFrame2,
    state="readonly",
    values=["none", "Hardware", "Software"],
    width=100,
    command=on_flowrate_select,
)
flowrate_option.pack(pady=5, padx=3, side="right")
label_openmode = mylabel(
    subTopLeftFrame3, txt="Open Mode", bg="transparent", justify="right", tcolor=NAVY
)
label_openmode.pack(side="left", padx=10)
openmode_dropdown = customtkinter.CTkComboBox(
    subTopLeftFrame3,
    state="readonly",
    values=["Read Only", "Write Only", "Read/Write"],
    width=100,
    border_width=2,
    border_color="#01595a",
)
# openmode_dropdown.pack(pady=5, padx=3,side="right")
openmode_option = myOptionMenu(
    subTopLeftFrame3,
    state="readonly",
    values=["Read Only", "Write Only", "Read/Write"],
    width=100,
)
openmode_option.pack(pady=5, padx=3, side="right")
label_databit = mylabel(
    subTopRightFrame1, txt="Data Bit", bg="transparent", justify="right", tcolor=NAVY
)
label_databit.pack(side="left", padx=10)
databit_dropdown = customtkinter.CTkComboBox(
    subTopRightFrame1,
    state="readonly",
    values=["5", "6", "7", "8"],
    width=100,
    border_width=2,
    border_color="#01595a",
)
# databit_dropdown.pack(pady=5, padx=3,side="right")
databit_option = myOptionMenu(
    subTopRightFrame1, state="readonly", values=["5", "6", "7", "8"], width=100
)
databit_option.pack(side="left", padx=3, pady=5)
label_parity = mylabel(
    subTopRightFrame2, txt="Parity", bg="transparent", justify="right", tcolor=NAVY
)
label_parity.pack(side="left", padx=10)
parity_dropdown = customtkinter.CTkComboBox(
    subTopRightFrame2,
    state="readonly",
    values=["none", "Even", "Odd", "Space", "Mark"],
    width=100,
    border_width=2,
    border_color="#01595a",
    command=on_parity_select,
)
# parity_dropdown.pack(pady=5, padx=3,side="right")
parity_option = myOptionMenu(
    subTopRightFrame2,
    state="readonly",
    values=["none", "Even", "Odd", "Space", "Mark"],
    width=100,
    command=on_parity_select,
)
parity_option.pack(pady=5, padx=3, side="right")
label_stopbit = mylabel(
    subTopRightFrame3, txt="Stop Bit", bg="transparent", justify="right", tcolor=NAVY
)
label_stopbit.pack(side="left", padx=10)
stopbit_dropdown = customtkinter.CTkComboBox(
    subTopRightFrame3,
    state="readonly",
    values=["1", "2"],
    width=100,
    border_width=2,
    border_color="#01595a",
)
# stopbit_dropdown.pack(pady=5, padx=3,side="right")
stopbit_option = myOptionMenu(
    subTopRightFrame3, state="readonly", values=["1", "2"], width=100
)
stopbit_option.pack(pady=5, padx=3, side="right")

cb_ctrl_char = myCheckBox(topNextFrame, text="Display CTRL Character")
cb_ctrl_char.pack(pady=5, padx=3, side="top", anchor="w")
cb_show_timestamp = myCheckBox(topNextFrame, text="Show Timestamp")
cb_show_timestamp.pack(pady=5, padx=3, side="top", anchor="w")
setlogFrame = customtkinter.CTkFrame(
    topNextFrame,
    width=300,
    height=100,
    border_width=0,
    border_color="#aaff00",
    fg_color=CYAN,
)
setlogFrame.pack(fill="x", expand=True, side="bottom", padx=5, pady=5)
savelog_label = mylabel(
    setlogFrame, txt="Save Log", bg="transparent", justify="right", tcolor=NAVY
)
savelog_label.pack(side="left", padx=10)
logPath_textbox2 = customtkinter.CTkTextbox(
    setlogFrame,
    height=1,
    width=100,
    border_width=1,
    border_color="#aaff00",
    fg_color="#00b8cc",
)
logPath_textbox2.pack(pady=5, padx=3, side="left", fill="x", expand=True)
cb_appendlog = customtkinter.CTkCheckBox(
    setlogFrame,
    text="Append Log",
    fg_color="#01595a",
    border_width=2,
    border_color="#01595a",
)
cb_appendlog.pack(pady=5, padx=3, side="left")
# label_baud=mylabel(topTopFrame, txt="Baudrate", bg="transparent", justify="right", tcolor=NAVY)


# menu1_button = customtkinter.CTkButton(floating_window.frame, text="remove selected", fg_color="transparent", text_color=NAVY, command=lambda: remove_selected)
# menu1_button.pack(pady=5, padx=3,fill="x", expand=True)
# menu2_button = customtkinter.CTkButton(floating_window.frame, text="remove all", fg_color="transparent", text_color=NAVY, command=lambda: clear_history)
# menu2_button.pack(pady=5, padx=3,fill="x", expand=True)

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
OSNAME = os.name
def bind_command_entry():
    global command_entry
    command_entry.bind("<Return>", send_command)
    command_entry.bind("<Up>", traceBackCommand)
    command_entry.bind("<Down>", traceForwardCommand)

def unbind_command_entry():
    global command_entry
    command_entry.unbind("<Return>")
    command_entry.unbind("<Up>")
    command_entry.unbind("<Down>")

if OSNAME == "nt":
    print("we in windows")
    applog("we in windows\n")
    hystory_listbox.bind(
        "<MouseWheel>", on_mouse_wheel_listbox
    )  # only work on windows os
else:
    applog("we in linux\n")
    hystory_listbox.bind("<Button-4>", on_mouse_wheel_listbox_up)
    hystory_listbox.bind("<Button-5>", on_mouse_wheel_listbox_down)
    # bind_command_entry()
    command_entry.bind("<Button-4>", traceBackCommand)
    command_entry.bind("<Button-5>", traceForwardCommand)


def list_ser_ports():
    global ser
    global FIRST_SCANNING
    # print(f'os name: {os.name }')
    # print(f'platform : {platform.system()}') # return Linux , Windows
    if os.name == "nt":
        com_ports = list_com_ports()
        accepted_port = []
        portn = 0
        if com_ports:
            # print("Available COM ports:")
            # port_dropdown['values'] = com_ports
            device_dropdown.configure(values=com_ports)
            device_option.configure(values=com_ports)
            # accepted_port.append(port)

            # text_box.insert(tk.END, "Available COM ports:\n")
            # applog( "Available COM ports:\n")
            for port in com_ports:
                portn += 1
                print(port)
                # text_box.insert(tk.END, f"port: {port}\n")
                # text_box.insert(tk.END, f"total port: {portn}\n")
                # applog(f"port: {port}\n")
                # applog(f"total port: {portn}\n")
                if port != "COM1":
                    accepted_port.append(port)
                    # ser = serial.Serial(port, baudrate=9600, timeout=1)  # Replace 'COM3' with your port
                    root.title("Serialone on " + port)
            print(f"total port: {portn}")
            if portn == 1:
                device_dropdown.set(com_ports[0])
                device_option.set(com_ports[0])
                # applog("No COM ports found.\n")
            else:
                device_dropdown.set(com_ports[1])
                device_option.set(com_ports[1])

            device_dropdown.configure(values=accepted_port)
            device_option.configure(accepted_port)
            if accepted_port:
                device_dropdown.set(accepted_port[0])
                device_option.set(accepted_port[0])
                if cb_ar.get() is True:
                    if ser.isOpen() is False:
                        ser = serial.Serial(
                            accepted_port[0], baudrate=9600, timeout=1
                        )  # Replace 'COM3' with your port

            # device_dropdown.bind("<<ComboboxSelected>>", on_port_select)
            device_option.bind("<<ComboboxSelected>>", on_port_select)
            # item
    else:
        com_ports = list_com_ports()
        accepted_port = []
        if com_ports:
            # port_dropdown['values'] = com_ports
            # port_dropdown.configure(values=com_ports)
            for port in com_ports:
                # scom_ports=str(com_ports)
                if "/dev/ttyACM" in port or "/dev/ttyUSB" in port:
                    device_dropdown["values"] = port
                    device_option["values"] = port
                    accepted_port.append(port)
                    # port_dropdown.configure(values=com_ports)item
                    # port_dropdown.set(port)
                    # applog(port+"\n")
                    # ser = serial.Serial(port, baudrate=9600, timeout=1)  # Replace 'COM3' with your port
                    root.title("Serialone on " + port)

            device_dropdown.configure(values=accepted_port)
            device_option.configure(values=accepted_port)
            if accepted_port:
                device_dropdown.set(accepted_port[0])
                device_option.set(accepted_port[0])
                if cb_ar.get() == 1:
                    # print("auto connect")
                    if ser.isOpen() is False:
                        setupserial()
                    # ser = serial.Serial(accepted_port[0], baudrate=9600, timeout=1)  # Replace 'COM3' with your port

            device_dropdown.bind("<<ComboboxSelected>>", on_port_select)
            device_option.bind("<<ComboboxSelected>>", on_port_select)

        # for i in range(9):
        # 	# Configure the serial port
        # 	try:
        # 		ser = serial.Serial('/dev/ttyUSB'+str(i), baudrate=9600, timeout=1)  # Replace 'COM3' with your port
        # 		root.title("Serial Reader on " + 'ttyUSB'+str(i))
        # 		break
        # 	except Exception as e:
        # 		text_box.insert(tk.END, f"Error: {e}\n")
    if FIRST_SCANNING is False:
        FIRST_SCANNING = True


# list_ser_ports()
# window.geometry(CenterWindowToDisplay(window, 900, 400, window._get_window_scaling()))
# Start the Tkinter event loop
# root.iconbitmap('rc.ico')


# device_dropdown.bind("<<ComboboxSelected>>", on_port_select)
def getParity(parity):
    print(f"parity > {parity}")
    if "Even" in parity:
        return serial.PARITY_EVEN
    elif "Odd" in parity:
        return serial.PARITY_ODD
    elif "Space" in parity:
        return serial.PARITY_SPACE
    elif "Mark" in parity:
        return serial.PARITY_MARK
    elif "none" in parity:
        return serial.PARITY_NONE


def getStopBit(stopbit):
    if stopbit == "1":
        return serial.STOPBITS_ONE
    elif stopbit == "2":
        return serial.STOPBITS_TWO
    else:
        return serial.STOPBITS_ONE


def setupserial():
    global ser
    try:
        ser = serial.Serial(
            # port=device_dropdown.get(),
            port=device_option.get(),
            # baudrate=int(baudrate_dropdown.get()),
            baudrate=int(baudrate_option.get()),
            # parity=getParity(parity_dropdown.get()),
            parity=getParity(parity_option.get()),
            # stopbits=getStopBit(stopbit_dropdown.get()),
            stopbits=getStopBit(stopbit_option.get()),
            # bytesize=int(databit_dropdown.get()),
            bytesize=int(databit_option.get()),
            timeout=0,
        )
        sser = str(ser)
        sser = sser.replace(",", ", ")
        wl = root.winfo_width()
        status_label.configure(wraplength=wl)
        status_label.configure(text=f"Serial Port: {sser} ")
        start_reading()
    except serial.SerialException:
        print(f"Error: {ser.port} is not available")
        applog(f"Error: {ser.port}\n")


def load_config():
    # print(f'ar : {cb_ar.get()}')
    try:
        with open("srwconfig.json", "r") as f:
            config = json.load(f)
            # device_dropdown.set(config['port'])
            # baudrate_dropdown.set(config['baudrate'])
            baudrate_option.set(config["baudrate"])
            # flowrate_dropdown.set(config['flowrate'])
            flowrate_option.set(config["flowrate"])
            # openmode_dropdown.set(config['openmode'])
            openmode_option.set(config["openmode"])
            # openmode_option.set(config['opnmode'])
            # databit_dropdown.set(config['databit'])
            databit_option.set(config["databit"])
            # parity_dropdown.set(config['parity'])
            parity_option.set(config["parity"])
            # print(f'parity > {config['parity']}')
            # stopbit_dropdown.set(config['stopbit'])
            stopbit_option.set(config["stopbit"])
            # crlf_dropdown.set(config['crlf'])
            crlf_optionmenu.set(config["crlf"])
            chr_del_dropdown.set(config["chr_del"])
            # datamode_dropdown.set(config['datamode'])
            datamode_option.set(config["datamode"])
            if config["autoreconnect"]:
                cb_ar.select()
            else:
                cb_ar.deselect()
            # cb_ar.StringVar(config['autoreconnect'])
    except FileNotFoundError:
        print("Config file not found, using default settings.")


load_config()


def load_history():
    global CMD_HISTORY
    global POINTER_HISTORY
    try:
        with open("cmd_history.json", "r") as f:
            history = json.load(f)
            hystory_listbox.delete(0, tk.END)
            for cmd in history:
                hystory_listbox.insert(tk.END, cmd)
                CMD_HISTORY.append(cmd)
            POINTER_HISTORY = len(CMD_HISTORY)
            hystory_listbox.see(POINTER_HISTORY)
    except FileNotFoundError:
        print("History file not found, using empty history.")


load_history()


def save_history():
    global CMD_HISTORY
    with open("cmd_history.json", "w") as f:
        json.dump(CMD_HISTORY, f, indent=4)


def save_config():
    print(f"ar : {cb_ar.get()}")
    config = {
        # 'port': device_dropdown.get(),
        # 'baudrate': baudrate_dropdown.get(),
        "baudrate": baudrate_option.get(),
        # 'flowrate': flowrate_dropdown.get(),
        "flowrate": flowrate_option.get(),
        # 'openmode': openmode_dropdown.get(),
        "openmode": openmode_option.get(),
        # 'databit': databit_dropdown.get(),
        "databit": databit_option.get(),
        # 'parity': parity_dropdown.get(),
        "parity": parity_option.get(),
        # 'stopbit': stopbit_dropdown.get(),
        "stopbit": stopbit_option.get(),
        # 'crlf': crlf_dropdown.get(),
        "crlf": crlf_optionmenu.get(),
        "chr_del": chr_del_dropdown.get(),
        # 'chr_del': chr_del_o.get(),
        # 'datamode': datamode_dropdown.get(),
        "datamode": datamode_option.get(),
        "autoreconnect": cb_ar.get(),
    }
    with open("srwconfig.json", "w") as f:
        json.dump(config, f, indent=4)


save_config()

# setupserial()

# baudrate_dropdown.bind("<<ComboboxSelected>>", on_baudrate_select)
command_entry.bind("<Return>", send_command)
command_entry.bind("<Up>", traceBackCommand)
command_entry.bind("<Down>", traceForwardCommand)
command_entry.bind("<MouseWheel>", on_mouse_wheel_entry)
hystory_listbox.bind("<<ListboxSelect>>", on_hystory_select)
hystory_listbox.bind("<Double-Button-1>", on_hystory_double_click)
# hystory_listbox.bind_all("<MouseWheel>", on_mouse_wheel_listbox)
# hystory_listbox.bind("<MouseWheel>", on_mouse_wheel_listbox) # only work on windows os
hystory_listbox.bind("<Button-3>", popup_menu)
# hystory_listbox.bind("<Button-4>", on_mouse_wheel_listbox_up)
# hystory_listbox.bind("<Button-5>", on_mouse_wheel_listbox_down)
# hystory_listbox.bind("<Button-3>", popup_menu2(event, floating_window))
# hystory_listbox.bind("<Button-3>", lambda event: popup_menu2(event, floating_window))
# hystory_listbox.bind("<Button-3>", lambda event: popup_menu(event, floating_window))
# flowrate_dropdown.bind("<<ComboboxSelected>>", on_flowrate_select)
# device_dropdown.bind("<<ComboboxSelected>>", on_port_select)
print("Serial Reader is running...")


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    # y = (screen_height - (height / 2)) // 2

    window.geometry(f"{width}x{height+200}+{x}+{y}")


# center_window(root)

if ser.isOpen():
    open_button.configure(text="close", command=close_serial)
    sh_setting_button.pack_forget()
else:
    open_button.configure(text="open", command=setupserial)
    ser.close()
    # text_box.insert(tk.END, f"Serial Port: {ser} is closed\n")
    applog(f"Serial Port: {ser} is closed\n")


def on_closing():
    if ser.isOpen():
        ser.close()
        print("Serial port closed.")
        applog("Serial port closed.\n")
    save_config()
    root.destroy()


def scan_ports():
    global ser
    # print("Scanning for COM ports...")
    list_ser_ports()
    threading.Timer(5, scan_ports).start()


scan_ports()
# if ser.isOpen():
# 	ser.close()
# 	print("Serial port closed.")
# 	applog("Serial port closed.\n")
# # scan_ports()
# # root.after(1000, scan_ports)
# root.after(1000, scan_ports)


root.protocol("WM_DELETE_WINDOW", on_closing)
# root.iconbitmap("yrem.ico")
# root.iconphoto(False, customtkinter.CTkImage("mon.png"))
root.mainloop()
