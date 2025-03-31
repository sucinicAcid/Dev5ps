from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

def to_kst(dt: datetime):
    return dt.replace(tzinfo=timezone.utc).astimezone(KST)