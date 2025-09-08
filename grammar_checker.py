class CheckResult:
    def __init__(self, is_flagged=False, reason=None):
        self.is_flagged = is_flagged # bool: нужно ли отправить на модерацию
        self.reason = reason       # str: причина (пока просто для информации)

def check_text_stub(text: str) -> CheckResult:
    """
    Заглушка: проверяет, больше ли 5 слов в тексте.
    """
    word_count = len(text.split())
    if word_count > 5:
        return CheckResult(is_flagged=True, reason=f"В твите {word_count} слов (>5).")
    
    return CheckResult(is_flagged=False)