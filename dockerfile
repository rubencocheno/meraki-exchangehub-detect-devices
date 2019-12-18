FROM ubuntu 

WORKDIR /usr/src/app
COPY requirements.txt .
RUN apt-get -y update
RUN apt-get -y install python3-pip
RUN pip3 install -r requirements.txt    
COPY . .

CMD [ "python3", "/usr/src/app/main.py", "--credentials=credentials.json"]


# Use the following line when building to have the script send out a message for the initial round of devices detected
# CMD [ "python3", "/usr/src/app/main.py", "--credentials=credentials.json", "--debug"]