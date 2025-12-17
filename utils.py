def parse_time_to_seconds(time_str):
    if ":" in time_str:
        minutes, seconds = time_str.split(":")
        return int(minutes) * 60 + int(seconds)
    return int(time_str)
