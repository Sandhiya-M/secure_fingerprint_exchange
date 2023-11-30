
import socket
import pickle  
import ctypes
import random
import cv2
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
    return matrix
    



def client():
    host = socket.gethostname()  
    port = 5000 

    client_socket = socket.socket()  
    client_socket.connect((host, port)) 
   
    p=int(client_socket.recv(1024).decode())
    print("received prime number:",p)
    if p < 255 and check_prime(p):
        l = find_primitive_roots(p)
        print(l)

        alpha_img = receive_image_matrix(client_socket)
        print("Displaying alpha")
        show_image_from_matrix(alpha_img,"alpha")
        
        get_private_key_a = construct_image_array([i for i in range(1, p)])
        print("private key:",get_private_key_a)
        show_image_from_matrix(get_private_key_a,"Privatekey_a")
        

        get_public_a = mod_cal(alpha_img, get_private_key_a, p)
        send_image_matrix(client_socket, get_public_a)
        show_image_from_matrix(get_public_a,"Public_key_a")
        get_public_b = receive_image_matrix(client_socket)
        show_image_from_matrix(get_public_b,"Public_key_b")
       
        get_common_a = mod_cal(get_public_b, get_private_key_a, p)
        show_image_from_matrix(get_common_a,"Common_key")
        print("Converting fingerprint to matrix")
        fp = image_to_matrix("fp.jpg")
        show_image_from_matrix(fp,"Fingerprint")

        encrypted_img = []
        print("Encrypting...")
        for i in range(128):
             temp = [(get_common_a[i][j] + fp[i][j]) % 256 for j in range(128)]
             encrypted_img.append(temp)
        show_image_from_matrix(encrypted_img,"Encrypted_image")
        send_image_matrix(client_socket, encrypted_img)
        
        client_socket.close()




def send_prime_number(socket, p):
    socket.send(str(p).encode())


def receive_prime_number(socket_t):
    p_bytes = socket_t.recv(1024)
    p = int(p_bytes)
    return p


if __name__ == "__main__":
    client()