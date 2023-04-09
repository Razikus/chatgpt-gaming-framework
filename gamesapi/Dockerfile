FROM python:3.11
COPY requirements.txt /reqs.txt
RUN pip3 install -r /reqs.txt && rm -f /reqs.txt

COPY src /app/src
WORKDIR /app
EXPOSE 8000
ENV APIKEY=none
ENV REDISURL=redis
ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0"]