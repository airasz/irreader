import Nextiondisplay
import converter
import threading
import random
cconv=converter.color()

MyNextion=Nextiondisplay.display()

MyNextion.set_port('/dev/ttyUSB0')

def pulse():
    #MyNextion.send_command("page page1")
    MyNextion.send_command('page page2')#sukses
    MyNextion.send_command('page 4')#sukses
    MyNextion.send_command('dim=40')#sukses
    # MyNextion.send_command('t1.bco=BLUE')# sukses
    MyNextion.send_command('t0.txt="orange radio"')
    MyNextion.send_command('t1.txt="merdeka FM"')
    MyNextion.send_command('t1.isbr=1')# sukses 1=true 0=false
    MyNextion.send_command('t1.xcen=Center')


    MyNextion.send_command('h0.val=34')#vol
    ct=cconv.percentTo565Color(42)
    MyNextion.send_command(f'h1.bco1={ct}')#cpu temp
    MyNextion.send_command('h1.val=42')#cpu temp
    cpuload=random.randint(0,101)
    cl=cconv.percentTo565Color(cpuload)
    MyNextion.send_command(f'j0.pco={cl}')#cpu temp
    MyNextion.send_command(f'j0.val={cpuload}')#cpu load
    memload=random.randint(0,101)
    ml=cconv.percentTo565Color(memload)
    MyNextion.send_command(f'j1.pco={ml}')#cpu temp
    MyNextion.send_command(f'j1.val={memload}')#memory load
    MyNextion.send_command('t2.txt="play list here"')#log
    MyNextion.send_command('t3.txt="192.168.10.200"')#ip
    MyNextion.send_command('t4.txt="3"')#station index
    threading.Timer(1, pulse).start()  
pulse()