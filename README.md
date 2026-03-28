# CMPE472 - Computer Networks Spring 2026
## Programming Assignment 1
**Topic:** Country Capital Prediction Using Socket Based Client-Server Programming

---

### 1. Brief Explanation of How the System Works
This project implements a TCP client-server architecture to provide a simple capital city prediction quiz. Both the server and client run on the local machine (`127.0.0.1`) on port `65432`.
1. The **Server** loads a list of countries and their respective capital cities from an Excel file (`country_capital_list.xlsx`) into memory upon startup.
2. The server creates a TCP socket, binds to the defined address, and listens for incoming connections. As clients connect, they are numbered progressively.
3. Once a **Client** connects, the server randomly picks a country and sends a question formatted as: `What is the capital city of <CountryName>?`.
4. The client prompts the user for a prediction and sends it back to the server.
5. The server evaluates the response with the following logic:
   - **Correct Answer**: Server responds with `"Correct! <Capital> is the capital of <Country>."`, cleanly closes the connection, and waits for a new client.
   - **Invalid Answer**: If the string contains numeric values or special characters, it responds with `"Numeric input is not allowed..."` and cuts the connection.
   - **Wrong Answer**: The server checks if the guessed city is the capital of a different country (e.g., `'berlin' is the capital of Germany...`) and prompts `"Wrong answer. Attempts left: <N>. Try again:"`. The client prompts the user again, allowing a maximum of **3 total attempts**.
   - **Program Termination**: If the client sends `"end"`, both programs register the action and immediately terminate their execution.

---

### 2. Explanation of the Server Code (`server.py`)
- **Library Imports**: Uses `socket` for network communication, `pandas` to read the Excel dataset and search for capitals, and `sys` to properly handle system processes.
- **Socket Initialization**: The server initializes with `socket.AF_INET` and `socket.SOCK_STREAM`. `SO_REUSEADDR` is added to prevent binding issues during tests.
- **Data Lookup**: When a wrong answer is received, the script searches the entire dataset `df[df['Capital'].str.lower() == data.lower()]` to provide contextual hints about which country the user's guessed capital actually belongs to.
- **Evaluation Loop**: A `while attempts > 0:` loop manages up to 3 tries. Different error handling blocks verify if input is correctly formatted (no digits), if it's correct, or if it has reached limits.
- **Termination Request**: Checking `if data.lower() == 'end'` terminates the execution synchronously with the client.

---

### 3. Explanation of the Client Code (`client.py`)
- **Connection**: Creates a TCP client socket matching the host `127.0.0.1:65432` and `connect()`s.
- **Question Retrieval & Display**: Wait to receive the prompt, presenting it continuously on the same line as the prompt logic for seamless user experience (`input(f"{question} Your guess...")`).
- **Loop Logic**: A continuous `while True` loop is used to repetitively send inputs until the server deliberately includes a disconnect clause in its message footprint.
- **Response Handling**:
  - Validates if the message from the server contains the keywords `"Closing connection"`, `"Connection will close"`, or `"Goodbye"`. The client successfully disconnects autonomously after receiving them.
  - If the session isn't over, it fetches a fresh prompt asking `Your guess (or 'END' to finish):` and cycles back.
