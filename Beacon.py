import blescan
import sys
import bluetooth._bluetooth as bluez
import threading
import time
from Tkinter import*

global User1Exist
global User1Distance

global User2Exist
global User2Distance

global yazFlag

global User1ExistCnt  
global User2ExistCnt

def Scan():
    
    global User1Exist
    global User1Distance

    global User2Exist
    global User2Distance
    
    global yazFlag
    
    User1Exist = 0
    User1Distance = 0
    
    User2Exist = 0
    User2Distance = 0
    
    yazFlag = 0
    
    dev_id = 0

    try:
            sock = bluez.hci_open_dev(dev_id)	
            print "Personel tarama basladi...\r\n"
    except:
            print "Hata: Bluetooth modulune erisilemedi..."
            sys.exit(1)                 
      
      
    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)


    while True:
        
            returnedList = blescan.parse_events(sock, 10)            
            
            for beacon in returnedList:
                mylist = beacon.split(",")

                if mylist[2] == "4660" and mylist[3] == "64001":
                    
                    #accuracy = calculateAccuracy(mylist[4], mylist[5])
                    distance = pow(10,((float(mylist[4]) - float(mylist[5]))/20))                   
                    print ("MAC: "+mylist[0])
                    print ("UUID: "+mylist[1])
                    print ("MINOR: "+mylist[2])
                    print ("MAJOR: "+mylist[3])
                    print ("TX POWER: "+mylist[4])
                    print ("RSSI: "+mylist[5])
                    print ("DISTANCE: "+str(distance_filtered))

                    if mylist[0] == "f4:84:4c:4d:dc:50":#Personel-1
                        User1Exist = 1
                        User1Distance = distance
                        
                    if mylist[0] == "f0:45:da:f6:5b:51":#Personel-2
                        User2Exist = 1
                        User2Distance = distance
            yazFlag = 1
                    
                    print ("\r\n***************************\r\n")
           

def Update():
    global User1Exist
    global User1Distance

    global User2Exist
    global User2Distance
    
    global yazFlag
    
    global User1ExistCnt  
    global User2ExistCnt
    global button1
    global button2
    
    User1Exist = 0
    User1Distance = 0

    User2Exist = 0
    User2Distance = 0
    
    yazFlag = 0
    
    time1 = 0
    time2 = 0
    timeout = 0
    
    User1ExistCnt = 0   
    User2ExistCnt = 0
    
    root = Tk()
    frame = Frame(root)
    frame.pack()
     
    root.title("Personel Takip Sistemi")
    
    topframe = Frame(root)
    topframe.pack(side = TOP)
    button1 = Button(topframe, padx=128, bd=64, text="Personel-1: VAR", fg="black", command=1)
    button1.pack(side = LEFT)
    
    button2 = Button(topframe, padx=128, bd=64, text="Personel-2: VAR", fg="black", command=1)
    button2.pack(side = LEFT)
  
    
    while True:
        
        if yazFlag == 1:            
        
            if User1Exist == 1 and User1Distance <= 1:
                User1ExistCnt = 6
                User1Exist = 0
            else:
                User1ExistCnt -=1
                if User1ExistCnt <= 0:
                    User1ExistCnt = 0
                
                
            if User1ExistCnt > 2:
                print("PERSONEL-1: VAR, "+"Mesafe: "+ str(User1Distance))
                button1["bg"]="green"
                button1["text"]="Personel-1: VAR"
            else:
                print("PERSONEL-1: YOK, "+"Mesafe: -")
                button1["bg"]="red"
                button1["text"]="Personel-1: YOK"
            
                
            if User2Exist == 1 and User2Distance <= 1:
                User2ExistCnt = 6                
                User2Exist = 0
            else:
                User2ExistCnt -=1
                if User2ExistCnt <= 0:
                    User2ExistCnt = 0
                
                
            if User2ExistCnt > 2: 
                print("PERSONEL-2: VAR, "+"Mesafe: "+ str(User2Distance))
                button2["bg"]="green"
                button2["text"]="Personel-2: VAR"
            else:
                print("PERSONEL-2: YOK, "+"Mesafe: -")
                button2["bg"]="red"
                button2["text"]="Personel-2: YOK"
                
            print""
            
            yazFlag = 0
            time1 = time.time()
        else:
            time2 = time.time()
            timeout = time2-time1
            if timeout > 15:
                print "Timeout"
                yazFlag = 1
            
def gui():
     
    global User1ExistCnt  
    global User2ExistCnt
    global button1
    global button2
     
    root = Tk()
    frame = Frame(root)
    frame.pack()
     
    root.title("Personel Takip Sistemi")     
       
    topframe = Frame(root)
    topframe.pack(side = TOP)
    button1 = Button(topframe, padx=128, bd=64, text="Personel-1: VAR", fg="black", command=1)
    button1.pack(side = LEFT)
    
    button2 = Button(topframe, padx=128, bd=64, text="Personel-2: VAR", fg="black", command=1)
    button2.pack(side = LEFT)
  
         
    root.mainloop()
       

t1=threading.Thread(target = Scan)
t1.start()

t2=threading.Thread(target = Update)
t2.start()

t3=threading.Thread(target = gui)
t3.start()
