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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    

    server_socket.bind(('127.0.0.1', 65432))
    server_socket.listen(5)
    print("Server is listening on 127.0.0.1:65432")
    
    client_count = 1
    
    while True:
        print(f"Waiting for client #{client_count} ...")
        try:
            conn, addr = server_socket.accept()
        except OSError:
            break
            
        print(f"Client connected from {addr}")
        
        #Select a random country
        row = df.sample().iloc[0]
        country = row['Country']
        capital = str(row['Capital']).strip()
        
        #Send initial question
        question = f"What is the capital city of {country}?"
        try:
            conn.sendall(question.encode('utf-8'))
        except:
            conn.close()
            continue
            
        attempts = 3
        while attempts > 0:
            try:
                data = conn.recv(1024).decode('utf-8').strip()
            except:
                break
                
            if not data:
                break
                
            #If client sends END
            if data.lower() == 'end':
                conn.sendall("Session ended by client. Goodbye.".encode('utf-8'))
                print("END received. Shutting down server.")
                conn.close()
                server_socket.close()
                sys.exit(0)
                
            #Check for numeric or invalid inputs
            if any(char.isdigit() for char in data) or not data.replace(' ', '').isalpha():
                #Allow spaces for names like "New York", but no numbers or symbols
                conn.sendall("Numeric input is not allowed for capital names. Connection will close.".encode('utf-8'))
                print("Numeric input is not allowed; closing connection.")
                break
                
            #Check correct answer
            if data.lower() == capital.lower():
                conn.sendall(f"Correct! {capital} is the capital of {country}. Closing connection.".encode('utf-8'))
                print("Correct; closing connection.")
                break
            else:
                #Wrong answer handling
                attempts -= 1
                response_lines = []
                
                #Check if the guess is a capital of another country in the list
                match = df[df['Capital'].astype(str).str.lower() == data.lower()]
                if not match.empty:
                    wrong_country = match.iloc[0]['Country']
                    response_lines.append(f"'{data}' is the capital of {wrong_country}, not {country}.")
                else:
                    #Provide generic feedback if it's not a known capital
                    #Actually screenshot exactly showed "'guessed' is the capital ...", if we don't find it
                    #we can omit adding it or just say it's not the capital. 
                    pass
                
                if attempts > 0:
                    response_lines.append(f"Wrong answer. Attempts left: {attempts}. Try again:")
                    conn.sendall("\n".join(response_lines).encode('utf-8'))
                else:
                    response_lines.append(f"Maximum attempts reached (3). The correct answer is {capital}. Closing connection.")
                    conn.sendall("\n".join(response_lines).encode('utf-8'))
                    print("Max attempts reached; closing connection.")
                    break
                    
        conn.close()
        client_count += 1

if __name__ == "__main__":
    start_server()