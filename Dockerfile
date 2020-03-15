FROM python:latest
RUN apt-get update
RUN apt-get install -y ffmpeg
ADD . /app
WORKDIR /app
RUN python3 -m venv .venv
RUN . .venv/bin/activate
RUN pip install -r requirements.txt
CMD ["sh", "-c", "python3 MediaStack.py"] 
