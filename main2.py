import socket  # Import the socket module for network communication
import threading  # Import the threading module to handle multiple threads

class TicTacToe:  # Define the TicTacToe class
    def __init__(self):  # Initialize the game
        # Create a 3x3 board represented by a list of lists
        self.board = [[" "," "," "], [" "," "," "], [" "," "," "]]
        self.turn = "X"  # Set the starting player to "X"
        self.you = "X"  # Set the player's symbol
        self.opponent = "O"  # Set the opponent's symbol
        self.game_over = False  # Flag to track if the game is over
        self.counter = 0  # Counter for the number of moves made

    def host_game(self, host, port):  # Method to host the game
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
        server.bind((host, port))  # Bind the socket to the specified host and port
        server.listen(1)  # Listen for incoming connections

        client, addr = server.accept()  # Accept a connection from a client

        self.you = "X"  # Set the player symbol for the host
        self.opponent = "O"  # Set the opponent symbol
        threading.Thread(target=self.handle_connection, args=(client,)).start()  # Start a new thread for handling the connection
        server.close()  # Close the server socket (optional, as it will be closed after handling the game)

    def connect_to_game(self, host, port):  # Method to connect to a hosted game
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
        client.connect((host, port))  # Connect to the server at the specified host and port

        self.you = 'O'  # Set the player symbol for the client
        self.opponent = 'X'  # Set the opponent symbol
        threading.Thread(target=self.handle_connection, args=(client,)).start()  # Start a new thread for handling the connection

    def handle_connection(self, client):  # Method to handle the player's connection
        while not self.game_over:  # Continue until the game is over
            if self.turn == self.you:  # If it's the player's turn
                move = input("Enter a move (row, column): ")  # Prompt the player for their move
                if self.check_valid_move(move.split(',')):  # Check if the move is valid
                    client.send(move.encode('utf-8'))  # Send the move to the opponent
                    self.apply_move(move.split(','), self.you)  # Apply the player's move
                    self.turn = self.opponent  # Switch turns to the opponent
                else:
                    print("Invalid move!")  # Notify the player of an invalid move
            else:  # If it's the opponent's turn
                data = client.recv(1024)  # Receive the opponent's move
                if not data:  # If no data is received, exit the loop
                    break
                else:
                    self.apply_move(data.decode('utf-8').split(','), self.opponent)  # Apply the opponent's move
                    self.turn = self.you  # Switch turns back to the player
        client.close()  # Close the client socket after the game ends

    def apply_move(self, move, player):  # Method to apply a move to the board
        if self.game_over:  # If the game is over, do nothing
            return
        self.counter += 1  # Increment the move counter
        self.board[int(move[0])][int(move[1])] = player  # Place the player's symbol on the board
        self.print_board()  # Print the current state of the board
        if self.check_if_won():  # Check if the player has won
            if self.winner == self.you:  # If the player is the winner
                print("You win!")  # Notify the player of their victory
                exit()  # Exit the game
            elif self.winner == self.opponent:  # If the opponent is the winner
                print("You lose!")  # Notify the player of their loss
                exit()  # Exit the game
        else:
            if self.counter == 9:  # If all moves have been made
                print("It is a tie!")  # Notify the player of a tie
                exit()  # Exit the game

    def check_valid_move(self, move):  # Method to check if a move is valid
        # Return True if the selected cell is empty
        return self.board[int(move[0])][int(move[1])] == " "

    def check_if_won(self):  # Method to check if a player has won
        for row in range(3):  # Check each row for a win
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]  # Set the winner
                self.game_over = True  # Mark the game as over
                return True  # Return True to indicate a win
        for col in range(3):  # Check each column for a win
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]  # Set the winner
                self.game_over = True  # Mark the game as over
                return True  # Return True to indicate a win
        # Check the two diagonals for a win
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]  # Set the winner
            self.game_over = True  # Mark the game as over
            return True  # Return True to indicate a win
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]  # Set the winner
            self.game_over = True  # Mark the game as over
            return True  # Return True to indicate a win
        return False  # Return False if no win conditions are met

    def print_board(self):  # Method to print the current game board
        for row in range(3):  # Loop through each row
            print(" | ".join(self.board[row]))  # Print the row with separators
            if row != 2:  # If not the last row
                print("-----------")  # Print a separator line

# Create an instance of the TicTacToe class and connect to a game hosted on localhost at port 9999
game = TicTacToe()
game.connect_to_game("localhost", 9999)
game = TicTacToe()
game.connect_to_game("localhost", 9999)


