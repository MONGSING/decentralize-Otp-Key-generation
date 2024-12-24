import socket
import RSA_encrypt_decrypt
import Response_Phrase_Generator

private_key,public_key = RSA_encrypt_decrypt.loadKeys()

public_key_bytes = public_key.save_pkcs1(format='PEM')
private_key_bytes = private_key.save_pkcs1(format='PEM')

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind(('127.0.0.1',12345))
server_socket.listen(5)

while True:
    print("Waiting for Connections from Trusted Authorities...........")
    connection,client_address = server_socket.accept()
    print(f"Connected to {client_address}")

    print("Connected to the Trusted Authority!")

    connection.sendall(public_key_bytes)
    received_encrypted_data = connection.recv(4096)
    print("This is the received encrypted secret phrase:")
    print(received_encrypted_data)

    # This is X
    decrypted_secret_phrase = RSA_encrypt_decrypt.decrypt(received_encrypted_data,private_key)

    print("The decrypted secret data:")
    print(decrypted_secret_phrase)

    # This is the y
    response_secret_phrase = Response_Phrase_Generator.generate_int_from_random(decrypted_secret_phrase)

    with open("key_store.txt",'a') as file:
        file.write(str(response_secret_phrase) + "\n")

    connection.close()






