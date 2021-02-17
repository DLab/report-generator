FROM python:3.8
WORKDIR /reports
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENV FLASK_APP Report_server.py	
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
