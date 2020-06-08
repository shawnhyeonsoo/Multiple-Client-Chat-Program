# Multiple-Client-Chat-Program

A chat program that allows clients to communicate with multiple clients using socket API in python3. </br>
</br>
Chatting starts with creating a chat room. Once a chat room is created by a client, any other client is able
to join the room. A client is able to create or join a chat room to interactively chat with clients in the room.
Server provides the list of chat rooms to clients and have authority to destroy any chat room.</br>
</br>

1. Specification
There are 2 states for clients, and 1 states for server

* Initial/Waiting State (for both client and server): </br>
  Initial state and waiting state are virtually the same. In these states, both programs stay idle until any command is
  given or environment has changed (i.e., new client entering the network or new chat room created). Program
  enters initial state when executed. The client does not show any changes until command is given.  As the server has to    
  manage chat rooms, it should be executed first; if not, an error message should be thrown on the client side.

* Chatting State (for client): </br>
  Clients in this state share their keyboard inputs with other clients in the room except when below commands are
  entered. When client sends a message, the message is sent to the server, then the server broadcasts
  the message to all clients in the room.
 
</br>
</br>
2. Commands

* /ls (for both client and server): </br>
  The /ls command give the list of existing chat rooms on screen. This command is supported on server and
  client. Once a room is destroyed, the name of the destroyed room is deleted from the list. 

* /create (for client): </br>
  This allows the client to create a new chat room. The command and arguments should be given as following:
  /create [Room_Name] [User_Name]</br>
  If [User_Name] is not given as an argument, a default nickname 'Unknown' is named for the client. When
  a room is created, the server is informed and displays “New room [Room_Name] created” message on
  terminal. If the client is already in another chat room (by joining or creating), an error message is thrown
  for this command and room must not be created.

* /join (for client): </br>
  /join allows the client to enter a specific chat room. The command and arguments should be given as following:
  /join [Room_Name] [User_Name] </br>
  The client joins the chat room [Room_Name] using [User_Name] as a nickname in the room. If [User_Name] is
  not given as an argument, a default nickname 'Unknown' is named for the client. The server does not make
  any action. If the client is already in another chat room (by joining or creating), an error message is thrown
  for this command and must not join the designated room.

* /whisper (for client): </br>
  Client also can send a whisper message that no one but one can hear. The command and arguments should be as
  following: </br>
  /whisper [Member_Name] [Message] </br>
  Only a client with [Member_Name] receives [Message] from client with [Sender_Name], and it throws “(whisper)
  [Sender_Name] : [Message]”. The target client with [Member Name] should be in the same chat room, or else an
  error message is given to the client.

* /kill (for server): </br>
  This forces a room to be close and ejects all participating members, including the creator, from the chat room. The
  command and arguments should be given as following: /kill [Room_Name]. Once participating members are
  ejected from [Room_Name], those members return to waiting state. Only the server can execute /kill.

</br>
</br>
To execute: </br>
run 'python3 server.py' and 'python3 client.py' on separate consoles.(server file should be executed first in order to function properly). 

</br> 
This is a programming project given in Computer Networks class. New to socket programming, this was a great opportunity to get
familiar with socket API, and thread functions as well. Although it took some time to complete the project as specified, it was completed after long thorough reading on sockets and threads. </br>
Please feel free to comment on mistakes or adjustments to be made. 
