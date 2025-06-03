def format_currency(value, default_na=True):
    """
    Simple currency formatter (example utility).
    """
    if value is None:
        return "N/A" if default_na else "$0.00"
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return "N/A" if default_na else "$0.00"

def format_percentage(value, default_na=True):
    """
    Simple percentage formatter.
    """
    if value is None:
        return "N/A" if default_na else "0.00%"
    try:
        return f"{float(value):.2f}%"
    except (ValueError, TypeError):
        return "N/A" if default_na else "0.00%"


if __name__ == "__main__":
    print(f"Currency of 12345.678: {format_currency(12345.678)}")
    print(f"Currency of None: {format_currency(None)}")
    print(f"Percentage of 25.5: {format_percentage(25.5)}")
    print(f"Percentage of None: {format_percentage(None)}")