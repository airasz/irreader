import Nextiondisplay
MyNextion=Nextiondisplay.display()
MyNextion.set_port('/dev/ttyUSB0')
MyNextion.send_command("page page1")