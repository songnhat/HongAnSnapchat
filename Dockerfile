FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get install -y libglib2.0-0 libnss3 libxcb1

WORKDIR /hongansnapchat

COPY requirements requirements

RUN python3 -m pip install wheel

RUN pip3 install -r requirements/base.txt

COPY . .

CMD [ "python3", "-m" , "flask", "--app", "HongAnSnapchat_app", "run", "--host=0.0.0.0", "--port=5000"]
