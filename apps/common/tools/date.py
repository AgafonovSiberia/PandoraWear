from datetime import datetime, UTC, date


def utc_now():
    return datetime.now(UTC)


def json_serializer(obj):
    if isinstance(obj, datetime | date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")
