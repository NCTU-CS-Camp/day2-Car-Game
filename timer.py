"""
碼表 / 圈速紀錄
"""

import pygame


def _fmt(seconds: float) -> str:
    """把秒數格式化成 M:SS.mmm 或 S.mmm 字串。"""
    minutes = int(seconds // 60)
    secs = seconds % 60
    if minutes > 0:
        return f"{minutes}:{secs:06.3f}"
    return f"{secs:.3f}"


class LapTimer:
    """
    狀態：idle（未啟動）→ running（計時中）

    呼叫順序：
        start()  →  lap() × N  →  reset()  →  start() ...
    """

    def __init__(self) -> None:
        self.is_running: bool = False
        self.best_lap: float | None = None   # 歷史最快圈，reset 也不清
        self._lap_start: int | None = None   # 本圈起始 ticks
        self._laps: list[float] = []         # 本次跑的各圈時間

    # ── 主要三個 method ───────────────────────────────────

    def lap(self) -> float | None:
        """
        按下計時鍵時呼叫（啟動 / 過終點線 共用同一個按鍵）。
        - idle 狀態：啟動計時，回傳 None
        - running 狀態：記錄這圈、重設圈計時起點、更新最快圈，回傳這圈秒數
        """
        now = pygame.time.get_ticks()

        if not self.is_running:
            self._lap_start = now
            self._laps = []
            self.is_running = True
            return None

        lap_time = (now - self._lap_start) / 1000.0
        self._laps.append(lap_time)
        self._lap_start = now

        if self.best_lap is None or lap_time < self.best_lap:
            self.best_lap = lap_time

        return lap_time

    def reset(self) -> None:
        """
        撞牆時呼叫。
        - 從本次所有圈中取最快的更新 best_lap
        - 清空本次資料，碼表回到 idle
        """
        if self._laps:
            run_best = min(self._laps)
            if self.best_lap is None or run_best < self.best_lap:
                self.best_lap = run_best

        self.is_running = False
        self._lap_start = None
        self._laps = []

    # ── 顯示用 ────────────────────────────────────────────

    def current_lap_seconds(self) -> float:
        """目前這圈已跑幾秒。idle 時回傳 0。"""
        if not self.is_running or self._lap_start is None:
            return 0.0
        return (pygame.time.get_ticks() - self._lap_start) / 1000.0

    def current_lap_str(self) -> str:
        if not self.is_running:
            return "Press key..."
        return _fmt(self.current_lap_seconds())

    def best_lap_str(self) -> str:
        if self.best_lap is None:
            return "--"
        return _fmt(self.best_lap)

    @property
    def laps(self) -> list[float]:
        return list(self._laps)
