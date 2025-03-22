import time

class GameTimer:

    def __init__(self, duration=120):
        # duration — длительность таймера в секундах (по умолчанию 120 = 2 минуты).
        self.duration = duration
        self.start_time = None  # время старта зададим в init_timer

    def init_timer(self):
        # Инициализируем (запускаем) таймер, запоминая текущее время.
        self.start_time = time.time()

    def get_time_left(self):
        if self.start_time is None:
            # Если таймер ещё не был инициализирован — вернём полную длительность.
            return self.duration
        elapsed = time.time() - self.start_time  # сколько прошло секунд
        left = int(self.duration - elapsed)      # сколько осталось (целое число)
        return max(0, left)
    def is_finished(self):
        return self.get_time_left() <= 0