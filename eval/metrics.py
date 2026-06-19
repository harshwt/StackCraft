import time

results = []

start = time.time()

# run pipeline

end = time.time()

results.append({
    "latency": end - start,
    "success": True
})