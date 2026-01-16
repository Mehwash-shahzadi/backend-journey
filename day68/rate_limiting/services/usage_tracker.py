from models.usage import TokenUsage, UserUsageSummary
import redis
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Redis connection – Docker localhost:6379
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

try:
    r.ping()
    logger.info("Redis connected successfully")
except redis.ConnectionError as e:
    logger.error(f"Redis connection failed: {e}")
    raise

BUDGET_LIMIT_USD = 5.00  # example monthly budget per IP/user

class UsageTracker:
    @staticmethod
    def record_usage(user_key: str, usage: dict):
        entry = TokenUsage(
            user_key=user_key,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            estimated_cost_usd=usage.get("estimated_cost_usd", 0.0),
            timestamp=datetime.utcnow().isoformat()
        )

        key = f"usage:{user_key}"
        history = r.get(key)
        usages = json.loads(history) if history else []
        usages.append(entry.model_dump())
        r.set(key, json.dumps(usages))

    @staticmethod
    def get_summary(user_key: str) -> UserUsageSummary:
        key = f"usage:{user_key}"
        data = r.get(key)
        entries = json.loads(data) if data else []

        if not entries:
            return UserUsageSummary(user_key=user_key)

        total_tokens = sum(e["total_tokens"] for e in entries)
        total_cost = sum(e["estimated_cost_usd"] for e in entries)

        return UserUsageSummary(
            user_key=user_key,
            total_requests=len(entries),
            total_tokens=total_tokens,
            total_cost_usd=round(total_cost, 4),
            last_request=max(e["timestamp"] for e in entries),
            is_blocked=total_cost >= BUDGET_LIMIT_USD
        )

    @staticmethod
    def calculate_cost(prompt_tokens: int, completion_tokens: int) -> float:
        # Gemini 2.5 Flash approx pricing (Jan 2026)
        input_cost = (prompt_tokens / 1_000_000) * 0.35
        output_cost = (completion_tokens / 1_000_000) * 1.05
        return round(input_cost + output_cost, 6)