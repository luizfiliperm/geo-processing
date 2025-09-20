FROM python:3.10-slim

WORKDIR /app/src

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
