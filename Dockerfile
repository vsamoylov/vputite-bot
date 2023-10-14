FROM python:3.10-alpine
WORKDIR /usr/app/
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt --no-cache 

COPY . .
ENV PYTHONPATH ./
CMD ["python", "bot.py"]
