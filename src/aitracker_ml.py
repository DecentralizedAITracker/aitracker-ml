import rsa
import json
import base64

class AITrackerML:

    def __init__(self,public_key_oracle_filepath,private_key_ml_filepath,public_key_web_filepath):
        self.publicKeyOracle = self.__import_public_key(public_key_oracle_filepath)
        self.publicKeyWeb = self.__import_public_key(public_key_web_filepath)
        self.privateKeyML = self.__import_private_key(private_key_ml_filepath)

    def encrypt(self,prediction):
        prediction = prediction.encode('utf8')
        prediction_encrypted = rsa.encrypt(prediction,self.publicKeyOracle)
        return base64.b64encode(prediction_encrypted).decode('ascii')

    def encrypt_for_user(self,prediction):
        prediction = prediction.encode('utf8')
        prediction_encrypted = rsa.encrypt(prediction,self.publicKeyWeb)
        return base64.b64encode(prediction_encrypted).decode('ascii')

    def sign(self,message):
        message = message.encode()
        signature = rsa.sign(message, self.privateKeyML, 'SHA-1')
        return base64.b64encode(signature).decode('ascii')

    def __import_public_key(self,filepath):
        f_pub_read = open(filepath,'rb')
        publicKeyFromFIle = f_pub_read.read()
        publicKey = rsa.PublicKey.load_pkcs1(publicKeyFromFIle)
        f_pub_read.close()
        return publicKey

    def __import_private_key(self,filepath):
        f_read = open(filepath,'rb')
        privateKeyFromFIle = f_read.read()
        privateKey = rsa.PrivateKey.load_pkcs1(privateKeyFromFIle)
        f_read.close()
        return privateKey


