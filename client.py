import random, sys
from socket import *
import time

def sender(seed1,seed2,seed3,num_of_packets,corrupt_prob,round_trip):
    serverName = 'localhost'
    serverPort = 50007
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect( (serverName, serverPort) )
    print ("connected to: " + str(serverName) + str(serverPort) )
    random.seed(seed1)
    arival_rng = random.getstate()
    random.seed(seed2)
    corrupt_rng = random.getstate()
    random.seed(seed3)
    data_rng = random.getstate()
    seq = 0
    for i in range(num_of_packets):
        random.setstate(data_rng)
        data = random.randint(25,100)
        data_rng = random.getstate()
        packet = str(data)+str(seq)+"0"
        print("A packet with sequence number "+str(seq)+" is about to be sent")
        print("Packet to send contains: data ="+str(data)+" seq = "+str(seq)+" isack= False")
        print("Starting timeout timer for ACK"+str(seq))
        clientSocket.send(packet.encode())
        random.setstate(arival_rng)
        arival = random.uniform(0.0,6.0)
        arival_rng = random.getstate()
        arival_time = arival+time.time()
        recived=0
        while(arival_time>time.time()):
            if recived==0:
                clientSocket.settimeout(round_trip)
                recvedPacket = clientSocket.recv(1024)
                if recvedPacket!=None:
                    ack = recvedPacket.decode()
                    recived=1
                    random.setstate(corrupt_rng)
                    corrupt = random.random()
                    print("The random generated corrupted probabilty is: ",corrupt)
                    corrupt_rng = random.getstate()
                    if corrupt<corrupt_prob:
                        time.sleep(round_trip)
                        print("ACK "+str(seq)+"timeout timer expired")
                        print("A Corrupted ACK packet has just been received")
                        print("A packet with sequence number", seq, "is about to be resent")
                        clientSocket.send(packet.encode())
                        print("The sender is moving back to state WAIT FOR ACK"+str(seq))
                    elif recvedPacket[-2]!=seq:
                        print("An ACK",ack[-2],"packet has just been received")
                        print("A packet with sequence number", seq, "is about to be resent")
                        clientSocket.send(packet.encode())
                        print("The sender is moving to state WAIT FOR ACK"+str(seq))
                    elif recvedPacket[-1]!=0:
                        time.sleep(round_trip)
                        print("ACK "+str(seq)+"timeout timer expired")
                        print("A packet with sequence number", seq, "is about to be resent")
                        clientSocket.send(packet.encode())
                        print("The sender is moving back to state WAIT FOR CALL ",seq," FROM ABOVE")
                    else:
                        print("An ACK",ack[-2],"packet has just been received")
                        print("Packet received contains: data =",ack[0],"seq =",ack[-2],"isack= True")
                        print("Stopping timeout timer for ACK"+str(seq))
                        if seq==0:
                            print("The sender is moving to state WAIT FOR CALL 1 FROM ABOVE")
                        else:
                            print("The sender is moving to state WAIT FOR CALL 0 FROM ABOVE")
                else:
                    pass
        if seq==0:
            seq=1
        elif (seq==1):
            seq=0
    shutdown = "shutdown"
    clientSocket.send(shutdown.encode())
    clientSocket.close


def main():
    seed1 = float(input("Seed for timing arrival of data:"))
    seed2 = float(input("Seed for corruption:"))
    seed3 = float(input("Seed for data:"))
    num_of_packets = int(input("Number of packets:"))
    corrupt_prob = float(input("Probability that an ACK has been corrupted."))
    round_trip = float(input("Round trip time:"))
    sender(seed1,seed2,seed3,num_of_packets,corrupt_prob,round_trip)
    print("Terminating.")

if __name__ == '__main__':
    main()