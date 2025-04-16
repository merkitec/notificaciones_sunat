FROM python:3.12-slim
EXPOSE 8080

WORKDIR /app

COPY requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update && apt-get install -y wget unzip && \
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
   apt install -y ./google-chrome-stable_current_amd64.deb && \
   apt-get clean

COPY . .
#ENV PORT=8080
# CMD ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
