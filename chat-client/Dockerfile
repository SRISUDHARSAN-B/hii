FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install "python-socketio[client]"
CMD ["python", "app.py"]