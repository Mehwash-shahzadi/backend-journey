"""Input validation utilities.""" 
def is_numeric(value) -> bool:
    """Check if value is int or float."""
    return isinstance(value, (int, float))
