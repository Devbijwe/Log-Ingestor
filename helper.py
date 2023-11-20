import sys

def get_data_size(data):
    # Serialize the data to a string and calculate its size using sys.getsizeof()
    serialized_data = str(data)
    size_in_bytes = sys.getsizeof(serialized_data)
    return size_in_bytes
if __name__=="__main__":

    log_data = {
        "level": "info",
        "message": "Sample log messageegdfgrekgverguj",
        "resourceId": "sample_resource_id",
        "timestamp": "2023-01-01T12:00:00Z",
        "traceId": "sample_trace_id",
        "spanId": "sample_span_id",
        "commit": "sample_commit",
        "metadata": {"parentResourceId": "sample_parent_resource_id"}
    }

    data_size = get_data_size(log_data)
    print(f"Size of data: {data_size} bytes")
