from socket import *
import random

serverHost = ''
serverPort = 50007
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(( serverHost, serverPort))
serverSocket.listen(1)
seed = float(input("Seed of corruption:"))
corrupt_prob = float(input("Chance of corruption:"))
random.seed(seed)
while True:
    connectionID, addr = serverSocket.accept()
    seq = 0
    while True:
        data = connectionID.recv(1024).decode()
        if( data == "shutdown" ): break
        corrupt = random.random()
        if corrupt<corrupt_prob:
            print("A Corrupted packet has just been received")
            if seq==0:
                ack ="011"
            elif seq==1:
                ack ="001"
            print("An ACK",ack[1],"is about to be sent")
            print("Packet to send contains: data =",ack[0],"seq =",ack[1],"isack = True")
            connectionID.send(ack.encode())
            print("The receiver is moving back to state WAIT FOR",seq,"FROM BELOW")
        elif str(seq)==data[-2]:
            print ("A packet with sequence number",data[-2],"has been received")
            print("Packet received contains: data",data[0:-2], "seq =",data[-2],"isack = False")
            ack = "0"+str(seq)+"1"
            if seq==0:
                seq=1
            elif (seq==1):
                seq=0
            print("An ACK",ack[1],"is about to be sent")
            print("Packet to send contains: data =",ack[0],"seq =",ack[1],"isack = True")
            connectionID.send(ack.encode())
            print("The receiver is moving to state WAIT FOR",seq,"FROM BELOW")
        else:
            print ("A duplicate packet with sequence number",data[-2],"has been received ")
            print("Packet received contains: data",data[0:-2], "seq =",data[-2],"isack = False")
            if seq==0:
                ack ="011"
            elif seq==1:
                ack ="001"
            print("An ACK",ack[1],"is about to be sent")
            print("Packet to send contains: data =",ack[0],"seq =",ack[1],"isack = True")
            connectionID.send(ack.encode())
            print("The receiver is moving back to state WAIT FOR",seq,"FROM BELOW")
    connectionID.close()
    print("Connection closed, shutting down")
    break
serverSocket.close()