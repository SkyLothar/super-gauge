import socket

HOSTNAME = socket.gethostname()

SUPERVISOR_STOPPED = (
    0,  # STOPPED
    100,  # EXITED
    200,  # FATAL
    1000  # UNKNOWN
)

SUPERVISOR_RUNNING = (
    10,  # STARTING
    20,  # RUNNING,
    30,  # BACKOFF,
)

RUNNING = "RUNNING"
