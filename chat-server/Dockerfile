FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install flask flask-socketio eventlet
CMD ["python", "server.py"]