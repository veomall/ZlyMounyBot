class CheckResult:
    def __init__(self, is_flagged=False, reason=None):
        self.is_flagged = is_flagged
        self.reason = reason

def check_text_stub(text: str) -> CheckResult:
    """
    Заглушка: проверяет, больше ли 15 слов в тексте.
    """
    word_count = len(text.split())
    if word_count > 15:
        return CheckResult(is_flagged=True, reason=f"В твите {word_count} слов (>15).")
    
    return CheckResult(is_flagged=False)