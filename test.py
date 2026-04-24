import os

import pyaes, pbkdf2, binascii, os, secrets
import base64

def getKey(): #generating key with PBKDF2 for AES
    password = "s3cr3t*c0d3"
    passwordSalt = '76895'
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    return key

def encrypt(plaintext): #AES data encryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def decrypt(enc): #AES data decryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    decrypted = aes.decrypt(enc)
    return decrypted

with open("paper.pdf", mode="rb") as file:
    data = file.read()
file.close()

def calculateBlock(filepath):
    length = os.path.getsize(filepath)
    tot_blocks = 0
    size = 0
    if length >= 1000:
        size = length / 10
        tot_blocks = 10
    if length < 1000 and length > 500:
        size = length / 5
        tot_blocks = 5
    if length < 500 and length > 1:
        size = length / 3
        tot_blocks = 3
    return int(size), tot_blocks, length     

size, tot_blocks, length = calculateBlock("paper.pdf")
chunks = []
start = 0
end = size
for i in range(0, tot_blocks):
    chunk = data[start:end]
    chunk = encrypt(chunk)
    print(str(start)+" "+str(size)+" "+str(len(chunk)))
    start = end
    end = end + size
    chunks.append(["block_"+str(i), chunk])

remain =  length - start
if remain > 0:
    chunk = data[start:length]
    chunks.append(["block_"+str(len(chunks)), chunk])
    start = start + remain

if os.path.exists("new.pdf"):
    os.remove("new.pdf")

with open("new.pdf", "wb+") as myfile:
    for i in range(len(chunks)):
        block, content = chunks[i]
        content = decrypt(content)
        print(len(content))
        myfile.write(content)
myfile.close()
