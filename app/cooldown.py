import time
class Cooldown:
    def __init__(self, seconds: int):
        self.seconds = seconds
        self._last = {}
    def allow(self, key: str) -> bool:
        now = time.time(); last = self._last.get(key, 0.0)
        if now - last >= self.seconds:
            self._last[key] = now; return True
        return False
    def remaining(self, key: str) -> int:
        now = time.time(); last = self._last.get(key, 0.0)
        rem = self.seconds - (now - last)
        return int(rem) if rem > 0 else 0
