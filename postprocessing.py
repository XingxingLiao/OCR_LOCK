import re
import math

def extract_numbers(text, region_id):
    results = []
    numbers = re.findall(r'\d+\.\d+|\d+', text)

    if numbers:
        num = numbers[0]
        if '.' in num:
            results.append(f"Region {region_id} - {num}")
        else:
            num = int(num)
            if region_id == 1:
                results.append(f"Region {region_id} - {math.floor(num / 10) * 10 / 10:.1f}")
            elif region_id == 2:
                results.append(f"Region {region_id} - {math.floor(num / 100) * 100 / 100:.2f}")
    else:
        first_line = text.split("\n")[0].strip() if text else ""
        match = re.search(r'\b(OUT|OFF)\b', first_line, re.IGNORECASE)
        results.append(f"Region {region_id} - {match.group(1).upper() if match else first_line or 'No Text'}")
    return results

def extract_on_off(text, region_id):
    matches = re.findall(r'\b(ON|OFF)\b', text, flags=re.IGNORECASE)
    return [f"Region {region_id} - {state.upper()} #{i+1}" for i, state in enumerate(matches)]
