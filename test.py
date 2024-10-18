import enum

class JobStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"
    RESUMED = "resumed"
    QUEUED = "queued"
    RETRYING = "retrying"
    SKIPPED = "skipped"
    TERMINATED = "terminated"
