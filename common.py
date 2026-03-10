from datetime import datetime, timezone

def timeNow():
  # Time format '2022-12-28T00:00:01Z' in UTC
  return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def timeStamp():
  # Time format '2025-07-14 18:17:28.538768+00:00' in UTC
  return datetime.now(timezone.utc)

def timeLocal(): # Local
  # Time format '2025-07-14 18:17:28' in Localtime
  now = datetime.now()
  now = now.replace(microsecond=0)
  return now 

