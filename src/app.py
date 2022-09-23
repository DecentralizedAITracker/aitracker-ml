import requests
import json
import os
import sys
import eth_abi
import pandas as pd
import numpy as np
import time
from ml import ML
from scaler import Scaler
from aitracker_ml import AITrackerML

iexec_out = os.environ['IEXEC_OUT']
iexec_in = os.environ['IEXEC_IN']
iexec_in_filename = os.environ['IEXEC_INPUT_FILE_NAME_1']

class Utils:
   
    def ensureDeterministicOutput(response_json,unix_timestamp):
        for x in range(len(response_json)):
            if(int(response_json[x][6]) > unix_timestamp):
                del response_json[x]
        return response_json

    def parser(klines):
        seq_x = list()
        for row in klines:
            row[0] = int(row[0])    #open time
            row[1] = float(row[1])  #open
            row[2] = float(row[2])  #high
            row[3] = float(row[3])  #low
            row[4] = float(row[4])  #close
            row[5] = float(row[5])  #volume
            row[6] = int(row[6])    #close time
            row[7] = float(row[7])  #quote asset volume
            row[8] = int(row[8])    #number of trades
            row[9] = float(row[9])  #taker buy base asset volume
            row[10] = float(row[10])#taker buy quote asset volume
            row[11] = float(row[11])#ignore
            seq_x.append(row)
        return np.array(seq_x)
        
class Binance:

    def fetchCandlesticks(symbol):
        url = 'https://api.binance.com/api/v3/klines'
        params = {
            'symbol': symbol,
            'interval': "1h",
            'limit': '500',
            'endTime' : unix_timestamp
        }
        json_data = requests.get(url, params=params).json()
        json_data = Utils.ensureDeterministicOutput(json_data,unix_timestamp)
        seq_x = Utils.parser(json_data)
        return seq_x


if __name__ == '__main__':
    print("oracle started")
    prediction = 0  # default returned value to avoid attack on scheduler
    prediction_with_signature = 0 # default returned value to avoid attack on scheduler
    try:
        milliseconds = int(round(time.time() * 1000))
        unix_timestamp = milliseconds
        symbol = "BTCUSDT"
        #fetch data
        seq_x = Binance.fetchCandlesticks(symbol)

        #hold value for reference
        last_value = seq_x[-1]
        last_value= last_value[1]

        #edit data
        seq_x = seq_x[-240:,[2,3,7]]
        scaler = Scaler()
        seq_x_scaled = scaler.fit_transform(seq_x)
        seq_x_scaled_reshaped = np.reshape(seq_x_scaled,(1,240,2))

        #load model
        ml = ML("test.h5")

        #predict
        prediction_scaled = ml.predict(seq_x_scaled_reshaped)

        #prepare result
        prediction = scaler.inverse(prediction_scaled)
        prediction = float(prediction)

        #compare from reference
        if(prediction > last_value):
            print("UP")
            prediction = "UP"
        else:
            print("DOWN")
            prediction = "DOWN"
        
        #AITracker code
        public_key_web_filepath = iexec_in + "/" + iexec_in_filename
        ait_ml = AITrackerML('./src/' + 'public_key_oracle.pem','./src/' + 'private_key_ml.pem',public_key_web_filepath)

        #encrypt
        prediction_encrypted = ait_ml.encrypt(prediction)
        prediction_encrypted_for_user = ait_ml.encrypt_for_user(prediction)

        #prepare prediction
        prediction_for_oracle = {
            
            'prediction_encrypted' : prediction_encrypted,
            'timestamp' : unix_timestamp,
        }

        prediction_for_oracle_string = json.dumps(prediction_for_oracle)
        #sign
        signature = ait_ml.sign(prediction_for_oracle_string)

        prediction = {
            'prediction_for_user' : prediction_encrypted_for_user,
            'prediction_for_oracle' : prediction_for_oracle,
            'signature_for_oracle' : signature
        }
        
        

    except Exception as e:
        print('Execution Failure: {}'.format(e))

    print(iexec_out)
    print('prediction: {}'.format(prediction))
    with open(iexec_out + '/result.json', 'w+') as fout:
        json.dump({"prediction" : prediction}, fout)

    with open(iexec_out + '/computed.json', 'w+') as f:
        json.dump({"deterministic-output-path" : iexec_out + '/result.json'}, f)
