# AI Microservice with Vector Search

A FastAPI-based microservice for AI document embeddings and vector similarity search, with full monitoring stack.

## Services

- **FastAPI App** (port 8000) - REST API for document embedding and vector search
- **Redis Stack** (ports 6379, 8001) - Vector database with RediSearch
- **Ollama** (port 11434) - Local LLM inference
- **Prometheus** (port 9090) - Metrics collection
- **Grafana** (port 3000) - Metrics visualization (admin/admin)

## Installation

### Install Docker
```bash
sudo apt install -y docker-compose docker.io docker-buildx
```

### Start Services
```bash
docker-compose up -d
```

### Install Ollama Model
```bash
docker exec ollama ollama pull mistral
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Initialize Vector Index
```bash
curl -X POST http://localhost:8000/vector/index/init
```

### Embed Document
```bash
curl -X POST "http://localhost:8000/vector/embed?id=doc1" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your document text here"}'
```

### Search Documents
```bash
curl "http://localhost:8000/vector/search?q=your%20query&k=5"
```

### Get Metrics
```bash
curl http://localhost:8000/vector/metrics
```

## Monitoring

### Grafana Setup
1. Access Grafana at http://localhost:3000 (admin/admin)
2. Add Prometheus data source: `http://prometheus:9090`
3. Create dashboards using the queries below

### Prometheus Queries for Dashboards

#### Vector Operations Dashboard

**Document Ingestion:**
```promql
# Total documents embedded
vector_upserts_total

# Document ingestion rate (per minute)
rate(vector_upserts_total[1m])

# Document ingestion rate (per hour)
rate(vector_upserts_total[1h]) * 60
```

**Search Performance:**
```promql
# Total search queries
vector_queries_total

# Query rate (queries per second)
rate(vector_queries_total[1m])

# Average query latency (seconds)
rate(vector_query_latency_seconds_sum[5m]) / rate(vector_queries_total[5m])

# Query latency histogram - 95th percentile
histogram_quantile(0.95, rate(vector_query_latency_seconds_bucket[5m]))

# Query latency histogram - 99th percentile
histogram_quantile(0.99, rate(vector_query_latency_seconds_bucket[5m]))
```

#### LLM/Prompt Dashboard

**Prompt Usage:**
```promql
# Total prompts sent
prompts_total

# Prompt rate (per minute)
rate(prompts_total[1m])
```

**Request Performance:**
```promql
# Average request latency
rate(request_latency_seconds_sum[5m]) / rate(request_latency_seconds_count[5m])

# 95th percentile request latency
histogram_quantile(0.95, rate(request_latency_seconds_bucket[5m]))
```

#### System Resources Dashboard

**Memory:**
```promql
# Process memory usage (bytes)
process_resident_memory_bytes

# Virtual memory (bytes)
process_virtual_memory_bytes
```

**CPU:**
```promql
# CPU usage rate
rate(process_cpu_seconds_total[1m])
```

**Python Garbage Collection:**
```promql
# GC objects collected by generation
rate(python_gc_objects_collected_total[5m])

# GC frequency
rate(python_gc_collections_total[5m])
```

#### Health & Availability

**Uptime:**
```promql
# Process uptime (seconds)
time() - process_start_time_seconds
```

**File Descriptors:**
```promql
# Open file descriptors
process_open_fds

# File descriptor usage percentage
(process_open_fds / process_max_fds) * 100
```

### Example Dashboard Panels

**Single Stat Panels:**
- Total Documents: `vector_upserts_total`
- Total Queries: `vector_queries_total`
- Avg Query Latency: `rate(vector_query_latency_seconds_sum[5m]) / rate(vector_queries_total[5m])`

**Graph Panels:**
- Query Rate Over Time: `rate(vector_queries_total[1m])`
- Query Latency Over Time: `histogram_quantile(0.95, rate(vector_query_latency_seconds_bucket[5m]))`

**Gauge Panels:**
- Memory Usage: `process_resident_memory_bytes`
- CPU Usage: `rate(process_cpu_seconds_total[1m]) * 100`

## Manual Vector DB Setup (Optional)

The vector index is created automatically via `/vector/index/init`, but you can also create it manually:

```bash
docker exec -it redis-vector redis-cli
FT.CREATE docs ON HASH PREFIX 1 doc: SCHEMA text TEXT embedding VECTOR FLAT 6 TYPE FLOAT32 DIM 1536 DISTANCE_METRIC COSINE
```