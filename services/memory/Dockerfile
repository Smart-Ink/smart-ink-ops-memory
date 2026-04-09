FROM python:3.12-slim
WORKDIR /app
COPY services/memory/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY services/memory/src ./src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8102"]
