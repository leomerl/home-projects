from prometheus_client import Counter, Histogram

prompt_count = Counter("prompts_total", "Total number of prompts")
req_latency = Histogram("request_latency_seconds", "Latency of /ask requests (s)")

vec_upserts_total = Counter("vector_upserts_total", "Total number of vector upserts")
vec_queries_total = Counter("vector_queries_total", "Total number of vector queries")
vec_query_latency = Histogram("vector_query_latency_seconds", "Latency of vector search (s)")