def script_filter(script_name):
    def filter(log_record):
        return log_record['extra'].get('script') == script_name

    return filter
