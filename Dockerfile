FROM python:latest
WORKDIR /app
RUN pip install html-writer iptcinfo3 Pillow filetype
RUN apt-get update
RUN apt-get install -y ffmpeg
CMD ["sh", "-c", "python3 MediaStack.py"] 
