import tracemalloc


def track_memory_usage():
    # Start tracing memory allocations
    tracemalloc.start()

    # Your code here
    # Example: instance = YourClass()

    # Take a snapshot and display the top statistics
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)
