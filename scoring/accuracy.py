import json
import re

def extract_number(text):
    match = re.search(r"\d+", text)
    return match.group(0) if match else None

def normalize_json(text):
    try:
        return json.loads(text)
    except Exception:
        return None

def score_accuracy(response, expected, scoring):
    if scoring == "exact_match":
        return expected.lower() in response.lower()

    if scoring == "numeric":
        return extract_number(response) == expected

    if scoring == "keyword":
        return expected.lower() in response.lower()

    if scoring == "json_match":
        return normalize_json(response) == normalize_json(expected)

    return None
