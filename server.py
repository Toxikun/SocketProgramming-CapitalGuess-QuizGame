import socket
import pandas as pd
import sys

def start_server():
    #Load the excel dataset
    try:
        df = pd.read_excel('country_capital_list.xlsx')
    except Exception as e:
        print(f"Error reading excel file: {e}")
        return

    #Initialize TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Initialize TCP socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#Allow the socket to be reused
    

    server_socket.bind(('127.0.0.1', 65432))#Bind the socket to the IP address and port number
    server_socket.listen(5)#Listen for incoming connections
    print("Server is listening on 127.0.0.1:65432")
    
    client_count = 1
    
    while True:#Loop for accepting connections
        print(f"Waiting for client #{client_count} ...")
        try:
            conn, addr = server_socket.accept()#Accepts the connection
        except OSError:
            break
            
        print(f"Client connected from {addr}")
        
        #Select a random country
        row = df.sample().iloc[0]#Selects a random row from the dataframe
        country = row['Country']#Gets the country name
        capital = str(row['Capital']).strip()#Gets the capital name
        
        #Send initial question
        question = f"What is the capital city of {country}?"#Sends the question to the client
        try:
            conn.sendall(question.encode('utf-8'))#Sends the question to the client
        except:
            conn.close()
            continue
            
        attempts = 3
        while attempts > 0:#Loop for attempts
            try:
                data = conn.recv(1024).decode('utf-8').strip()#Receives the data from the client
            except:
                break
                
            if not data:#Checks if the data is empty
                break
                
            #If client sends END
            if data.lower() == 'end':
                conn.sendall("Session ended by client. Goodbye.".encode('utf-8'))#Sends the response to the client
                print("END received. Shutting down server.")
                conn.close()
                server_socket.close()
                sys.exit(0)
                
            #Check for numeric or invalid inputs
            if any(char.isdigit() for char in data) or not data.replace(' ', '').isalpha():#Checks if the data is numeric or invalid
                conn.sendall("Numeric input is not allowed for capital names. Connection will close.".encode('utf-8'))#Sends the response to the client
                print("Numeric input is not allowed; closing connection.")
                break
                
            #Check correct answer
            if data.lower() == capital.lower():
                conn.sendall(f"Correct! {capital} is the capital of {country}. Closing connection.".encode('utf-8'))#Sends the response to the client
                print("Correct; closing connection.")
                break
            else:
                #Wrong answer handling
                attempts -= 1
                response_lines = []
                
                #Check if the guess is a capital of another country in the list
                match = df[df['Capital'].astype(str).str.lower() == data.lower()]#Checks if the guess is a capital of another country in the list
                #This part is not listed in the homework pdf but it was in the example video of the project so I added that
                if not match.empty:
                    wrong_country = match.iloc[0]['Country']#Gets the country name
                    response_lines.append(f"'{data}' is the capital of {wrong_country}, not {country}.")#Appends the response to the response lines
                else:
                    pass
                
                if attempts > 0:
                    response_lines.append(f"Wrong answer. Attempts left: {attempts}. Try again:")#Appends the response to the response lines
                    conn.sendall("\n".join(response_lines).encode('utf-8'))#Sends the response to the client
                else:
                    response_lines.append(f"Maximum attempts reached (3). The correct answer is {capital}. Closing connection.")#Appends the response to the response lines
                    conn.sendall("\n".join(response_lines).encode('utf-8'))#Sends the response to the client
                    print("Max attempts reached; closing connection.")
                    break
                    
        conn.close()
        client_count += 1

if __name__ == "__main__":#Run the server
    start_server()