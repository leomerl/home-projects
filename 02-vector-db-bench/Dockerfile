FROM python:3.11-slim

WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas-dev g++ \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY bench/ ./bench

ENTRYPOINT ["python", "-m", "bench.run_bench"]
