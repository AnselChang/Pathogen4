def formatDegrees(radians: float, roundDigits: int) -> str:
    deg = round(radians * 180 / 3.1415, roundDigits)
    return f"{deg}\u00b0"