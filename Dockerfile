FROM tensorflow/tensorflow:latest
### install python dependencies if you have some

RUN pip3 install pandas
RUN pip3 install keras
RUN pip3 install eth_abi
RUN pip3 install numpy
RUN pip3 install rsa

COPY ./src /src


ENTRYPOINT ["python3", "/src/app.py"]