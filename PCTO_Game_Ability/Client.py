# final client version to command the alphabot through the muse 2
# go ahead if you are focused
#If you are focused and you turn your head, the robot turns in the direction the subject turned their head
#if you are not focused the alphabot stands still

import logging
import socket
import threading as thr
import Movement_Concentration
# import subprocess library to open a .exe file

registered = False
nickname = ""
SERVER=('192.168.1.119', 3450) # IP address alphabot
class Receiver(thr.Thread):
    def __init__(self, s): #Thread constructor, self is like this, s is the socket
        thr.Thread.__init__(self)  #constructor 
        self.running = True   #as long as it exists
        self.s = s 

    def stop_run(self): #if it stops
        self.running = False

    def run(self): #Inside it all actions are performed
        global registered

        while self.running:
            data = self.s.recv(4096).decode()   #reception
            
            if data == "OK":    #If it receives OK, the connection is successful
                registered = True
                logging.info(f"\nConnection established")
            
            else:
                logging.info(f"\n{data}")

def main():
    global registered
    global nickname
    #file = "./Windows/Pcto.exe" # file to open
    #subprocess.Popen(file) # command to open the file
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #I create a TCP / IPv4 socket, first it sends, I create the base that does everything
    s.connect(SERVER)  #connection to the server

    ricev = Receiver(s) #receives messages, so that when the server sends the message back to clients, it reaches everyone
    ricev.start()

    command = None
    while True:

        concentration = Movement_Concentration.museConcentration() #function that calculates the concentration level
        #Movement_Concentration.simulationPressionKeys(Movement_Concentration.museDxSx(), Movement_Concentration.museConcentration()) 
        if(concentration == "GO"): #concentrated subject
            command = Movement_Concentration.museDxSx() #control of where and if the subject turns his head
            print("concentration command: ", command)
            s.sendall(command.encode()) #send the message to the server
      
        else:
            command = concentration #alphabot stopped (FERMO) cause unconcentrated subject
            print("concentration command: ", concentration)
            s.sendall(command.encode()) #send the message to the server

            if 'exit' in command:   #In case the connection should be interrupted
                ricev.stop_run()    #breaks the connection
                 
    ricev.join()
    s.close()

if __name__ == "__main__":
    main()
