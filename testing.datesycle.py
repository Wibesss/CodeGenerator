import time
from datetime import datetime, timezone

end_time = time.time()
start_time = end_time - 86400

for i in range(5):
    start_time_str = datetime.fromtimestamp(start_time, tz=timezone.utc).strftime('%Y-%m-%d')
    end_time_str = datetime.fromtimestamp(end_time, tz=timezone.utc).strftime('%Y-%m-%d')
    query = f"flast languag:python created:{start_time_str}..{end_time_str}"
    print(query)
    end_time -= 86400
    start_time -= 86400

