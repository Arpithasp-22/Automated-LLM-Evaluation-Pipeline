from scoring.refusal import is_refusal

def is_hallucination(response: str, allow_refusal: bool) -> bool:
    if allow_refusal:
        return not is_refusal(response)
    return False
