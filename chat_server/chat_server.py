import socket
import threading

victim_list = []

def broadcast_message_to_victims(sender, message):
    # Send the message to all connected clients
    for victim, _ in victim_list:
        try:
            if victim != sender:
                victim.send(bytes(message, "utf-8"))
        except Exception as e:
            print(f"Error broadcasting message to a client: {e}")

def remove_client(client):
    for c, _ in victim_list:
        if c == client:
            victim_list.remove((c, _))
            break

recent_messages = []
def show_recent_messages(client):
    global recent_messages
    for recent_message in recent_messages:
        client.send(bytes(recent_message, "utf-8"))


def handle_client(client, address):
    global recent_messages
    print(f"Connection established - {address[0]}:{address[1]}")
    
    victim_list.append((client, address))
    
    while True:
        try:
            string = client.recv(1024)
            if not string:
                break
            string = string.decode("utf-8")
            print(f"[client:{address[1]}] {string}")
            
            if string == "show":
                show_recent_messages(client)
            elif string == "exit":
                print(f"[*] Bye bye: {address[1]}")
                remove_client(client)
                break
            else:
                broadcast_message_to_victims(client, string)
                recent_messages.append(f"[client:{address[1]}] {string}")
                recent_messages = recent_messages[-10:]
        except Exception as e:
            print(f"Error handling client {address[1]}: {e}")
            remove_client(client)
            break
        
        
    client.close()
    print(f"Connection closed - {address[0]}:{address[1]}")

if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port_number = 1234
    sniffer_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sniffer_server.bind((ip_address, port_number))
    sniffer_server.listen(5)
    
    print(f"listening on {ip_address}:{port_number}")
    
    while True:
        victim, address = sniffer_server.accept()
        client_handler = threading.Thread(target=handle_client, args=(victim, address))
        client_handler.start()