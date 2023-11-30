import socket
import pickle  
import random
import cv2
import ctypes
from PIL import Image
import numpy as np
def check_prime(p):
    for i in range(2,p//2):
        if(p%i==0):
            return False
    return True
def is_root(i,p):
    s=set()  
    t=0
    for j in range(1,p):
         t=pow(i,j)%p
         s.add(t)
         
    if(len(s)==p-1):
        return True
    return False
def find_primitive_roots(p):
    l=[]
    for i in range(2,p):
        if( is_root(i,p)):
            l.append(i)
    return l
def construct_image_array(l):
    a=[]
    for i in range(0,128):
        row=[]
        for j in range(0,128):
            row.append(random.choice(l))
        a.append(row)
    return a
def show_image(a):
    a=np.array(a)
    img=Image.fromarray(a,'RGB')
    img.show()
def mod_cal(a,b,p):
    ans=[]
    for i in range(0,128):
        row=[]
        for j in range(0,128):
            row.append(pow(a[i][j],b[i][j])%p)
        ans.append(row)
    return ans




def image_to_matrix(image_path, target_size=(128, 128)):
    original_image = Image.open(image_path)
    resized_image = original_image.resize(target_size)
    grayscale_image = resized_image.convert('L')
    image_matrix = np.array(grayscale_image)
    matrix_as_list = image_matrix.tolist()
    return matrix_as_list


def show_image_from_matrix(matrix,name="temp"):
    matrix_array = np.array(matrix, dtype=np.uint8)
    img = Image.fromarray(matrix_array, 'L')  
    img.save(name+".jpg")
    img.show(title=name)


def send_image_matrix(socket, matrix):
    serialized_matrix = pickle.dumps(matrix)
    socket.send(serialized_matrix)


def receive_image_matrix(socket):
    serialized_matrix=socket.recv(50000)
    matrix = pickle.loads(serialized_matrix)
    print(matrix)
    return matrix
    
    

def send_prime_number(socket_t, p):
    socket_t.send(p.encode())


def server():
    host = socket.gethostname()
    port = 5000  

    server_socket = socket.socket() 
    server_socket.bind((host, port))  
    server_socket.listen(2)
    conn, address = server_socket.accept() 
    print(f"Connection established with {address}")

    p = int(input("Enter prime number (p): "))
  
    if p < 255 and check_prime(p):
        conn.send(str(p).encode())


        l = find_primitive_roots(p)
        print(l)

        alpha_img = construct_image_array(l)
        send_image_matrix(conn, alpha_img)
    
        get_public_a = receive_image_matrix(conn)
        print("publlic a:\n",get_public_a)

        
        get_private_key_b = construct_image_array([i for i in range(1, p)])
        show_image_from_matrix(get_private_key_b,"Private_key_b")
        get_public_b = mod_cal(alpha_img, get_private_key_b, p)
        send_image_matrix(conn, get_public_b)

        

        get_common_b = mod_cal(get_public_a, get_private_key_b, p)


        print("Receiving encrypted image...")
        encrypted_img = receive_image_matrix(conn)

        decrypted_img = []
        for i in range(128):
             temp = [(encrypted_img[i][j] - get_common_b[i][j] + 256) % 256 for j in range(128)]
             decrypted_img.append(temp)

        print("Displaying decrypted image")
        show_image_from_matrix(decrypted_img,"decrypted fp")
        
        conn.close()
        server_socket.close()




if __name__ == "__main__":
    server()