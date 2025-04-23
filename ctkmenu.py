from customtkinter import *
import customtkinter
import sys

class CTkFloatingWindow(CTkToplevel):
    """
    On-screen popup window class for customtkinter
    Author: Akascape
    """
    def __init__(self,
                 master=None,
                 corner_radius=15,
                 border_width=1,
                 **kwargs):
        
        super().__init__(takefocus=1)
        
        self.focus()
        self.master_window = master
        self.corner = corner_radius
        self.border = border_width
        self.hidden = True

        # add transparency to suitable platforms
        if sys.platform.startswith("win"):
            self.after(100, lambda: self.overrideredirect(True))
            self.transparent_color = self._apply_appearance_mode(self._fg_color)
            self.attributes("-transparentcolor", self.transparent_color)
        elif sys.platform.startswith("darwin"):
            self.overrideredirect(True)
            self.transparent_color = 'systemTransparent'
            self.attributes("-transparent", True)
        else:
            self.attributes("-type", "splash")
            self.transparent_color = '#000001'
            self.corner = 0
            self.withdraw()
             
        self.frame = customtkinter.CTkFrame(self, bg_color=self.transparent_color, corner_radius=self.corner,
                              border_width=self.border, **kwargs)
        self.frame.pack(expand=True, fill="both")
        
        self.master.bind("<Button-1>", lambda event: self._withdraw_off(), add="+") # hide menu when clicked outside
        self.bind("<Button-1>", lambda event: self._withdraw()) # hide menu when clicked inside
        self.master.bind("<Configure>", lambda event: self._withdraw()) # hide menu when master window is changed
        
        self.resizable(width=False, height=False)
        self.transient(self.master_window)
         
        self.update_idletasks()
        
        self.withdraw()
        
    def _withdraw(self):
        self.withdraw()
        self.hidden = True

    def _withdraw_off(self):
        if self.hidden:
            self.withdraw()
        self.hidden = True
        
    def popup(self, x=None, y=None):
        self.x = x
        self.y = y
        self.deiconify()
        self.focus()
        self.geometry('+{}+{}'.format(self.x, self.y))
        self.hidden = False


"""
Usage
"""

def do_popup(event, frame):
    """ open the popup menu """
    try: frame.popup(event.x_root, event.y_root)
    finally: frame.grab_release()
    
# root = CTk()
root= customtkinter.CTk()
float_window = CTkFloatingWindow(root) # our popup menu

widget = customtkinter.CTkLabel(root, text="Right Click Here")
widget.pack(padx=20, pady=20)

widget.bind("<Button-3>", lambda event: do_popup(event, float_window)) # right click mouse bind
widget.bind("<Button-2>", lambda event: do_popup(event, float_window)) # mac os right click (optional)

# Add menu buttons in float_window.frame

menu_button = customtkinter.CTkButton(float_window.frame, text="Click Here 1", fg_color="transparent", command=lambda: print("Hello"))
menu_button.pack(expand=True, fill="x", padx=10, pady=(10,0))

menu_button2 = customtkinter.CTkButton(float_window.frame, text="Click Here 2", fg_color="transparent", command=lambda: print("Hello"))
menu_button2.pack(expand=True, fill="x", padx=10, pady=(5,0))

menu_button3 = customtkinter.CTkButton(float_window.frame, text="Click Here 3", fg_color="transparent", command=lambda: print("Hello"))
menu_button3.pack(expand=True, fill="x", padx=10, pady=(5,10))

root.mainloop()