from fastapi import FastAPI, Query
from typing import Optional
import random
from datetime import datetime, timedelta
import time
from pydantic import BaseModel

app = FastAPI(title="Kubernetes Cluster Monitor API")

# Dummy service names
SERVICES = [
    "auth-service",
    "user-service",
    "payment-service",
    "notification-service",
    "analytics-service",
    "api-gateway"
]

# Log level distribution
LOG_LEVELS = ["INFO", "DEBUG", "WARN", "ERROR"]
LOG_LEVEL_WEIGHTS = [0.6, 0.25, 0.1, 0.05]

# Sample log messages
LOG_MESSAGES = [
    "Request processed successfully",
    "Database connection established",
    "Cache hit for key: {}",
    "Processing batch job",
    "HTTP request received: GET /api/v1/{}",
    "Response sent with status code: {}",
    "Authentication successful for user: {}",
    "Rate limit check passed",
    "Circuit breaker closed",
    "Health check completed",
    "Memory usage: {} MB",
    "Connection timeout, retrying...",
    "Invalid request parameter: {}",
    "Service discovery updated",
    "Background task scheduled"
]

# Commit message types and templates
COMMIT_TYPES = ["feat", "fix", "refactor", "perf", "docs", "test", "chore"]
COMMIT_MESSAGES = [
    "add authentication middleware",
    "fix memory leak in connection pool",
    "update dependencies to latest versions",
    "optimize database query performance",
    "implement rate limiting",
    "add unit tests for API endpoints",
    "refactor error handling logic",
    "improve logging format",
    "fix race condition in cache invalidation",
    "add health check endpoint",
    "update API documentation",
    "implement circuit breaker pattern",
    "optimize memory usage",
    "fix null pointer exception",
    "add integration tests",
    "refactor service discovery logic",
    "improve error messages",
    "add metrics collection",
    "fix timeout handling",
    "implement retry mechanism",
    "update configuration management",
    "add request validation",
    "optimize response time",
    "fix connection leak",
    "add monitoring dashboards",
    "refactor database access layer",
    "implement graceful shutdown",
    "add feature flags support",
    "fix concurrent access issues",
    "improve security headers"
]

# Developer names
DEVELOPERS = [
    "alice.chen",
    "bob.smith",
    "carol.jones",
    "david.kim",
    "emma.wilson",
    "frank.garcia",
    "grace.lee",
    "henry.brown"
]


class ServiceMetrics(BaseModel):
    service_name: str
    cpu_usage_percent: float
    memory_mb: int
    p99_latency_ms: float
    request_rate_per_sec: float
    error_rate_percent: float
    memory_leak_score: float  # 0-100, higher indicates potential leak
    anomaly_detected: bool


class MetricsResponse(BaseModel):
    timestamp: str
    cluster_name: str
    services: list[ServiceMetrics]


class Commit(BaseModel):
    commit_hash: str
    author: str
    date: str
    message: str
    service: str
    files_changed: int
    insertions: int
    deletions: int


class CommitHistoryResponse(BaseModel):
    cluster_name: str
    total_commits: int
    services: list[str]
    time_range: dict
    commits: str  # Concatenated commit history


def generate_log_line(service: str, timestamp: datetime) -> str:
    """Generate a single log line for a service"""
    level = random.choices(LOG_LEVELS, weights=LOG_LEVEL_WEIGHTS)[0]
    message = random.choice(LOG_MESSAGES)
    
    # Add random data to message templates
    if "{}" in message:
        replacements = [
            f"user_{random.randint(1000, 9999)}",
            str(random.randint(200, 500)),
            f"resource_{random.randint(1, 100)}",
            str(random.randint(64, 512))
        ]
        message = message.format(random.choice(replacements))
    
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return f"{timestamp_str} [{level}] [{service}] {message}"


def generate_service_metrics(service: str) -> ServiceMetrics:
    """Generate metrics for a single service"""
    # Base values with some randomization
    cpu_usage = round(random.uniform(5, 95), 2)
    memory_mb = random.randint(128, 2048)
    p99_latency = round(random.uniform(10, 500), 2)
    request_rate = round(random.uniform(10, 1000), 2)
    error_rate = round(random.uniform(0, 5), 2)
    
    # Memory leak score: higher values indicate potential issues
    # Simulate some services with potential leaks
    if random.random() < 0.2:  # 20% chance of elevated leak score
        memory_leak_score = round(random.uniform(60, 95), 2)
    else:
        memory_leak_score = round(random.uniform(0, 40), 2)
    
    # Detect anomalies based on thresholds
    anomaly_detected = (
        cpu_usage > 85 or
        p99_latency > 400 or
        error_rate > 3 or
        memory_leak_score > 70
    )
    
    return ServiceMetrics(
        service_name=service,
        cpu_usage_percent=cpu_usage,
        memory_mb=memory_mb,
        p99_latency_ms=p99_latency,
        request_rate_per_sec=request_rate,
        error_rate_percent=error_rate,
        memory_leak_score=memory_leak_score,
        anomaly_detected=anomaly_detected
    )


def generate_commit(service: str, timestamp: datetime) -> Commit:
    """Generate a single commit for a service"""
    commit_hash = ''.join(random.choices('0123456789abcdef', k=7))
    author = random.choice(DEVELOPERS)
    commit_type = random.choice(COMMIT_TYPES)
    message = random.choice(COMMIT_MESSAGES)
    full_message = f"{commit_type}: {message}"
    
    files_changed = random.randint(1, 15)
    insertions = random.randint(5, 200)
    deletions = random.randint(1, 100)
    
    return Commit(
        commit_hash=commit_hash,
        author=author,
        date=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        message=full_message,
        service=service,
        files_changed=files_changed,
        insertions=insertions,
        deletions=deletions
    )


def format_commit(commit: Commit) -> str:
    """Format a commit as a git log style string"""
    return (
        f"commit {commit.commit_hash}\n"
        f"Author: {commit.author}\n"
        f"Date:   {commit.date}\n"
        f"Service: {commit.service}\n"
        f"\n"
        f"    {commit.message}\n"
        f"\n"
        f"    {commit.files_changed} files changed, "
        f"{commit.insertions} insertions(+), {commit.deletions} deletions(-)\n"
    )

def throw_error():
    time.sleep(3)
    return {"status": 500}

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    # return {
    #     "message": "Kubernetes Cluster Monitor API",
    #     "endpoints": {
    #         "/logs": "Get concatenated service logs",
    #         "/metrics": "Get service performance metrics",
    #         "/commit_history": "Get concatenated commit history of services"
    #     }
    # }
    return random.choice([{"status": 200}, throw_error()])


@app.get("/logs")
def get_logs(num_logs: Optional[int] = Query(default=100, ge=1, le=10000)):
    """
    Get concatenated logs from all services in the cluster
    
    Args:
        num_logs: Number of log lines to return (default: 100, max: 10000)
    
    Returns:
        Dictionary with logs and metadata
    """
    logs = []
    
    # Generate logs across a time range
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    
    # Generate logs for each service
    logs_per_service = num_logs // len(SERVICES)
    remainder = num_logs % len(SERVICES)
    
    for idx, service in enumerate(SERVICES):
        service_log_count = logs_per_service + (1 if idx < remainder else 0)
        
        for i in range(service_log_count):
            # Distribute timestamps across the time range
            timestamp = start_time + timedelta(
                seconds=random.uniform(0, 3600)
            )
            logs.append({
                "timestamp": timestamp,
                "line": generate_log_line(service, timestamp)
            })
    
    # Sort logs by timestamp
    logs.sort(key=lambda x: x["timestamp"])
    
    # Format output
    log_lines = [log["line"] for log in logs]
    
    return {
        "cluster_name": "production-cluster-01",
        "total_services": len(SERVICES),
        "services": SERVICES,
        "log_count": len(log_lines),
        "time_range": {
            "start": start_time.isoformat(),
            "end": end_time.isoformat()
        },
        "logs": "\n".join(log_lines)
    }


@app.get("/commit_history", response_model=CommitHistoryResponse)
def get_commit_history(num_commits: Optional[int] = Query(default=50, ge=1, le=1000)):
    """
    Get concatenated commit history from all services in the cluster
    
    Args:
        num_commits: Number of commits to return (default: 50, max: 1000)
    
    Returns:
        CommitHistoryResponse with concatenated git-style commit history
    """
    commits = []
    
    # Generate commits across a time range (last 30 days)
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)
    
    # Generate commits for each service
    commits_per_service = num_commits // len(SERVICES)
    remainder = num_commits % len(SERVICES)
    
    for idx, service in enumerate(SERVICES):
        service_commit_count = commits_per_service + (1 if idx < remainder else 0)
        
        for i in range(service_commit_count):
            # Distribute timestamps across the time range
            timestamp = start_time + timedelta(
                seconds=random.uniform(0, 30 * 24 * 3600)
            )
            commits.append({
                "timestamp": timestamp,
                "commit": generate_commit(service, timestamp)
            })
    
    # Sort commits by timestamp (most recent first)
    commits.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Format output
    commit_lines = [format_commit(commit["commit"]) for commit in commits]
    
    return CommitHistoryResponse(
        cluster_name="production-cluster-01",
        total_commits=len(commits),
        services=SERVICES,
        time_range={
            "start": start_time.isoformat(),
            "end": end_time.isoformat()
        },
        commits="\n".join(commit_lines)
    )


@app.get("/metrics", response_model=MetricsResponse)
def get_metrics():
    """
    Get performance metrics for all services in the cluster
    
    Returns:
        MetricsResponse with CPU, latency, memory, and anomaly detection data
    """
    service_metrics = [generate_service_metrics(service) for service in SERVICES]
    
    return MetricsResponse(
        timestamp=datetime.now().isoformat(),
        cluster_name="production-cluster-01",
        services=service_metrics
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)