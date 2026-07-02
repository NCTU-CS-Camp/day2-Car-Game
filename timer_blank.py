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
        lap()  →  lap() × N  →  reset()  →  lap() ...
    """

    def __init__(self) -> None:
        self.is_running: bool = False
        self.best_lap: float | None = None   # 歷史最快圈，reset 也不清
        self._lap_start: int | None = None   # 本圈起始 ticks
        self._laps: list[float] = []         # 本次跑的各圈時間

    def lap(self) -> float | None:
        """
        --------------------------------------------------------
        #### 功能 : 按下計時鍵時呼叫，啟動碼表 / 記錄圈速 共用同一個按鍵
        --------------------------------------------------------
        #### 回傳值
        - 第一次按下（啟動碼表）：回傳 None
        - 之後每次過終點：回傳這圈花了幾秒（float）
        --------------------------------------------------------
        """
        """
        --------------------------------------------------------
        Q6. 完成 lap() 在 running 狀態下的邏輯（idle 那段已經寫好了）
        Todo : 碼表已在計時時：
                1. 把 lap_time 算出來：(now - self._lap_start) / 1000.0
                   （now 跟 self._lap_start 都是毫秒，除以 1000 換成秒）
                2. 如果 self.best_lap 是 None，或 lap_time 比 self.best_lap 小，
                   就把 self.best_lap 更新成 lap_time
        Hint : - 第 1 格：(now - self._lap_start) / 1000.0
               - 第 2 格（if 條件）：lap_time < self.best_lap
               - 第 3 格（if 內容）：self.best_lap = lap_time
        --------------------------------------------------------
        """
        # Q6 begin
        now = pygame.time.get_ticks()          # 1. 取得目前時間（毫秒）

        if not self.is_running:      # 碼表還沒啟動（idle 狀態）
            self._lap_start = now    # 重要：記錄這圈的起點時間，起點時間從這裡找
            self._laps = []          # 清空本次圈速紀錄
            self.is_running = True   # 啟動碼表
            return None              # 第一次按下不算一圈，直接回傳 None

        lap_time = "__fill_in__"     # 計算這圈花了幾秒（目前時間 - 起點時間，再把毫秒換算成秒）
        self._laps.append(lap_time)  # 把這圈時間加進紀錄 list
        self._lap_start = now        # 重設下一圈的起點為現在

        if self.best_lap is None or "__fill_in__":   # 還沒有最快圈、或這圈更快？
            "__fill_in__"                 #     更新最快圈紀錄

        return lap_time              # 回傳這圈的秒數
        # Q6 end

    def reset(self) -> None:
        """
        撞牆時呼叫。
        - 從本次所有圈中取最快的更新 best_lap
        - 清空本次資料，碼表回到 idle
        """
        if self._laps:
            try:
                run_best = min(self._laps)
            except TypeError:
                run_best = None  # Q6 未完成時 _laps 可能含非數字
            if run_best is not None and (self.best_lap is None or run_best < self.best_lap):
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
