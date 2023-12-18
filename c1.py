import socket
import re

def send_message():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 1234))

    try:
        # Receive and process the initial message from the server
        initial_message = client.recv(1024).decode('utf-8')
        #print(f"Received initial message: {initial_message}")
        
        # Using regular expression to extract the port number
        match = re.search(r"Echo:\('.*?', (\d+)\)", initial_message)
        if match:
            port_number = match.group(1)
            print(f"your port number: {port_number}")
        else:
            print("No port number found in the echo message.")

        
        while True:
            im =input("Enter 's' for sender and 'r' for recever :: ")

            if im == 's':
                recipient = input("Enter recipient ( port numbe): ")
                message = input("Enter your message: ")

                if message.lower() == 'stop':
                    client.send(bytes("stop", 'utf-8'))
                    break
            
                full_message = f"to:{recipient}:{message}"
                client.send(bytes(full_message, 'utf-8'))
                

            if im == 'r':
                # Receive and process incoming messages
                received_data = client.recv(1024).decode('utf-8')
                
                #print(f"Received message>>>>>>>: {received_data}-------------")
                if received_data:
                    massage = re.search(r":(\w+)$", received_data)
                    port_resv = re.search(r"to:(\d+):", received_data) #pnr
                    match = re.search(r"from \('.*?', (\d+)\):", received_data) #
                    
                    if massage and port_resv :
                        fa = massage.group(1)
                        pnr = port_resv.group(1)
                        if match:
                            sender = match.group(1)
                            #print(f"Sender port: {sender}")
                            #print(f"Sender port:pnr= {pnr} port_number ={port_number} ")
                        
                            if  pnr == port_number:
                                print(f"Received message:- {fa}")
                                if fa == 'hello':
                                    client.send(bytes(f"to:{sender}:i_am_online", 'utf-8'))
                                    print("-----response sent successfully-----")
                            else:
                                if fa == "i_am_online":
                                    print(f"Received message:- {fa}")
                        else:
                            print(f"No sender information found.")
                    else:
                        print("No massage for you")
                else:
                    print("No data received")
                    
                    
                
                
    except KeyboardInterrupt:
        print("Client shutting down.")
    finally:
        client.close()
        
if __name__ == "__main__":
    send_message()
