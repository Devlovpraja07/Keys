# Python Flask Application
FROM python:3.9

# Working Directory Set Karein
WORKDIR /app

# Dependencies Install Karein
COPY requirements.txt .
RUN pip install -r requirements.txt

# Application Code Copy Karein
COPY . .

# Flask App Run Karein
CMD ["python", "app.py"]
