# Secure Fingerprint Exchange
Symmetric key encryption with Deffie-Hellman(DH) Key Exchange mechanism with Vignere Cipher encryption



# Algorithm
Server:
1. Getting a 'q' value which is prime number.
2. Generate all the primitive roots of 'q'.
3. With generated primitive roots develop alpha(A) of 128 X 128 image in which each cell contains the random value from the primitive roots of q.
4. Now send this alpha and q (public factor) to client.
5. Generate a private key(X) for server of 128 X 128 image in which each cell contains the random value from 1 to q-1.
6. Compute the public component of DH using the fomula:
                    Y[i]= pow(A[i],X[i]) mod q
7. Send this public component to client.
8. Receive the public component of client Y' and compute the common key by
                    K[i]= pow(Y'[i],X[i]) mod q
9. Get the encrypted fingerprint from client E.
10. Decrypt the image with following formula:
                    D[i]=E[i]-K[i]

    
Client:
1. Getting a 'q' value which is prime number from server.
2. Generate all the primitive roots of 'q'.
3. With generated primitive roots develop alpha(A) of 128 X 128 image in which each cell contains the random value from the primitive roots of q.
4. Generate a private key(X) for server of 128 X 128 image in which each cell contains the random value from 1 to q-1.
5. Compute the public component of DH using the fomula:
                    Y[i]= pow(A[i],X[i]) mod q
6. Send this public component to server.
7. Receive the public component of server Y' and compute the common key by
                    K[i]= pow(Y'[i],X[i]) mod q
8.Encrypt the fingerprint(FP) by
                    E[i]=FP[i]+K[i]
9. Send the encrypted fingerprint to Server.
