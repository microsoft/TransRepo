def format_percentage(value, total):
    """Format percentage value"""
    if total == 0:
        return "0%"
    return f"{(value / total * 100):.1f}%"

def validate_path(path):
    """Validate if path exists"""
    return os.path.exists(path)