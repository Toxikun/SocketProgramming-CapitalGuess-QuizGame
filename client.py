import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:#Connect to the server
        client_socket.connect(('127.0.0.1', 65432))#IP address and port number
    except Exception as e:
        print("Connection error:", e)
        return

    #Receive the initial question from the server
    try:
        question = client_socket.recv(1024).decode('utf-8')#Receive the question from the server
    except:
        return

    if not question:
        return
        
    #First prompt asks question AND the guess instruction on same line
    guess = input(f"{question} Your guess (or 'END' to finish): ")
    
    while True:
        try:
            client_socket.sendall(guess.encode('utf-8'))#Send the guess to the server
            response = client_socket.recv(1024).decode('utf-8')#Receive the response from the server
        except:
            break
            
        if not response:
            break
            
        print(response)#Print the response from the server
        
        #Check termination keywords seen in the screenshot output
        if ("Closing connection" in response or 
            "Connection will close" in response or 
            "Goodbye" in response):
            break
            
        #Subsequent prompts just ask for the guess
        guess = input("Your guess (or 'END' to finish): ")#Ask for the guess

    client_socket.close()#Close the connection

if __name__ == "__main__":#Run the client
    start_client()