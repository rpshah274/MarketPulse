from prometheus_client import Counter, Histogram, Gauge

# Total trades processed
trades_processed = Counter(
    'marketpulse_trades_processed_total',
    'Total number of trades processed',
    ['symbol']
)

# Trade processing latency
processing_latency = Histogram(
    'marketpulse_processing_seconds',
    'Time to process a trade',
    ['symbol']
)

# WebSocket connection status
websocket_connected = Gauge(
    'marketpulse_websocket_connected',
    'WebSocket connection status (1=connected, 0=disconnected)'
)

# Redis write errors
redis_errors = Counter(
    'marketpulse_redis_errors_total',
    'Total Redis write errors'
)