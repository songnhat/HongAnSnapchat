FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip

ENV CHROMEDRIVER_VERSION=131.0.6778.87

### install chrome
RUN apt-get update && apt-get install -y wget && apt-get install -y zip
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

### install chromedriver
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip \
  && unzip chromedriver-linux64.zip && rm -dfr chromedriver_linux64.zip \
  && mv /chromedriver-linux64/chromedriver /usr/bin/chromedriver \
  && chmod +x /usr/bin/chromedriver

WORKDIR /hongansnapchat

COPY requirements requirements

RUN python3 -m pip install wheel

RUN pip3 install -r requirements/base.txt

COPY . .

CMD [ "python3", "-m" , "flask", "--app", "HongAnSnapchat_app", "run", "--host=0.0.0.0", "--port=5000"]
