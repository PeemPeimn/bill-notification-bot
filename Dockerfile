FROM selenium/node-chrome

WORKDIR /app

RUN sudo apt-get -y update
RUN sudo apt-get install -y python3.12-venv

ENV PATH="/app/venv/bin:$PATH"
RUN python3 -m venv ./venv

COPY . /app/
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install --upgrade --force-reinstall chromedriver-binary-auto

CMD ["python3", "facebook_messenger.py", "--headless"]