FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY wrapper.py wrapper_demo.py ./

ENV PORT=8888
EXPOSE 8888

CMD ["python3", "wrapper_demo.py"]
