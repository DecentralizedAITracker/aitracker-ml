import rsa
import json
import base64
from aitracker_oracle import AITrackerOracle

class AITrackerML:

    def __init__(self,public_key_oracle_filename,private_key_ml_filename):
        self.publicKeyOracle = self.__import_public_key(public_key_oracle_filename)
        self.privateKeyML = self.__import_private_key(private_key_ml_filename)

    def encrypt(self,prediction):
        prediction = prediction.encode('utf8')
        prediction_encrypted = rsa.encrypt(prediction,self.publicKeyOracle)
        return base64.b64encode(prediction_encrypted).decode('ascii')

    def sign(self,message):
        message = message.encode()
        signature = rsa.sign(message, self.privateKeyML, 'SHA-1')
        return signature

    def __import_public_key(self,filename):
        f_pub_read = open(filename,'rb')
        publicKeyFromFIle = f_pub_read.read()
        publicKey = rsa.PublicKey.load_pkcs1(publicKeyFromFIle)
        f_pub_read.close()
        return publicKey

    def __import_private_key(self,filename):
        f_read = open(filename,'rb')
        privateKeyFromFIle = f_read.read()
        privateKey = rsa.PrivateKey.load_pkcs1(privateKeyFromFIle)
        f_read.close()
        return privateKey


