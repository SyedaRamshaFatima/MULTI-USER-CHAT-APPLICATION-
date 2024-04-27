import socket

def greatest_common_divisor(a, b):
    while b:
        a, b = b, a % b
    return a

def modular_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(p, q):
    modulus = p * q
    totient = (p - 1) * (q - 1)
    public_exponent = 65537 # Common choice for the public exponent
    private_exponent = modular_inverse(public_exponent, totient)
    return ((modulus, public_exponent), (modulus, private_exponent))

def perform_encryption(message, public_key):
    modulus, public_exponent = public_key
    encrypted_values = [pow(ord(char), public_exponent, modulus) for char in message]
    hex_encrypted = ' '.join(hex(value)[2:] for value in encrypted_values)
    return hex_encrypted

def perform_decryption(encrypted_values, private_key):
    modulus, private_exponent = private_key
    decrypted_message = ''.join([chr(pow(int(value, 16), private_exponent, modulus)) for value in encrypted_values.split()])
    return decrypted_message

if __name__ == "__main__":
    prime1 = 61
    prime2 = 53
    public_key, private_key = generate_keypair(prime1, prime2)
    server_ip = "127.0.0.1"
    server_port = 1234
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    while True:
        user_input = input("[You]: ")
        if user_input.lower() == 'exit':
            client_socket.send(bytes(user_input, "utf-8"))
            break
        encrypted_message = perform_encryption(user_input, public_key)
        client_socket.send(bytes(encrypted_message, "utf-8"))
        buffer = client_socket.recv(1024)
        buffer = buffer.decode("utf-8")
        decrypted_message = perform_decryption(buffer, private_key)
        print(f"[Server] {decrypted_message}")
    print("[*] Client is closing...")
    client_socket.close()
