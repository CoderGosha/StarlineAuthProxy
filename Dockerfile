FROM python AS runtime
WORKDIR /app
COPY . .

RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install -r requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0"]
