import Nextiondisplay
MyNextion=Nextiondisplay.display()
MyNextion.set_port('/dev/ttyUSB0')
#MyNextion.send_command("page page1")
MyNextion.send_command('page page2')#sukses
MyNextion.send_command('dim=10')#sukses
# MyNextion.send_command('t1.bco=BLUE')# sukses
MyNextion.send_command('t0.txt="live score"')
MyNextion.send_command('t1.txt="Puskas FC Academy vs Hammarby\n 24\'"')
MyNextion.send_command('t1.isbr=1')# sukses 1=true 0=false
MyNextion.send_command('t1.xcen=Center')