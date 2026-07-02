"""
--------------------------------------------------------
#### 這個檔案負責「碼表 / 圈速紀錄」功能
--------------------------------------------------------
#### 使用流程
1. 建立物件：lap_timer = LapTimer()
2. 每一幀呼叫 lap_timer.update_key(any_key_pressed)
3. 玩家通過終點線時呼叫 lap_timer.lap_completed()
4. 玩家撞牆時呼叫 lap_timer.crash()
5. 用 lap_timer.current_lap_str() / best_lap_str() 顯示資訊
--------------------------------------------------------
"""

import pygame


def _fmt(seconds: float) -> str:
    """把秒數格式化成 M:SS.mmm 或 S.mmm 字串（F1 風格，三位毫秒）。"""
    minutes = int(seconds // 60)
    secs = seconds % 60
    if minutes > 0:
        return f"{minutes}:{secs:06.3f}"
    return f"{secs:.3f}"


class LapTimer:
    """
    --------------------------------------------------------
    #### 物件 : 碼表，支援多圈記錄與最快圈紀錄
    --------------------------------------------------------
    #### 狀態
    - idle（等待中）：還沒按任何鍵，碼表不計時
    - running（計時中）：已按鍵，碼表持續跑，每圈會記錄圈速
    --------------------------------------------------------
    #### 函式
    - update_key(any_key_pressed) : 每幀呼叫；偵測第一個按鍵以啟動計時
    - lap_completed()             : 通過終點線時呼叫；記錄這圈時間，重設圈計時起點
    - crash()                     : 撞牆時呼叫；從本次所有圈取最快的更新最佳紀錄，然後全部重置
    - current_lap_seconds()       : 目前這圈已跑幾秒
    - total_run_seconds()         : 這次按鍵後總共跑了幾秒
    - current_lap_str()           : 目前圈計時的格式化字串
    - best_lap_str()              : 最快圈的格式化字串（無紀錄時顯示 "--"）
    --------------------------------------------------------
    #### 屬性
    - is_running  : 目前是否在計時中
    - best_lap    : 最快圈秒數（float），尚無紀錄時為 None
    - laps        : 本次跑的所有圈速紀錄 list（唯讀）
    --------------------------------------------------------
    """

    def __init__(self) -> None:
        self.is_running: bool = False
        self.best_lap: float | None = None   # 歷史最快圈，撞牆也不清
        self._run_start_ticks: int | None = None   # 本次按鍵後的起始時間
        self._lap_start_ticks: int | None = None   # 本圈的起始時間
        self._laps: list[float] = []               # 本次跑的各圈時間

    # ── 公開函式 ──────────────────────────────────────────

    def update_key(self, any_key_pressed: bool) -> None:
        """每幀呼叫。若碼表在 idle 且偵測到任何按鍵，啟動計時。"""
        if not self.is_running and any_key_pressed:
            self.is_running = True
            now = pygame.time.get_ticks()
            self._run_start_ticks = now
            self._lap_start_ticks = now
            self._laps = []

    def lap_completed(self) -> float | None:
        """
        通過終點線時呼叫。
        記錄這圈時間、把圈計時起點重設成現在（準備下一圈）。
        回傳這圈的秒數；碼表未啟動時回傳 None。
        """
        if not self.is_running or self._lap_start_ticks is None:
            return None

        now = pygame.time.get_ticks()
        lap_time = (now - self._lap_start_ticks) / 1000.0
        self._laps.append(lap_time)
        self._lap_start_ticks = now   # 重設圈計時起點
        if self.best_lap is None or lap_time < self.best_lap:
            self.best_lap = lap_time
        return lap_time

    def crash(self) -> None:
        """
        撞牆時呼叫。
        從本次所有圈中取最快的那圈更新歷史最佳紀錄，
        其他資料全部清除，碼表回到 idle（等待下一次按鍵）。
        """
        if self._laps:
            run_best = min(self._laps)
            if self.best_lap is None or run_best < self.best_lap:
                self.best_lap = run_best

        self.is_running = False
        self._run_start_ticks = None
        self._lap_start_ticks = None
        self._laps = []

    def current_lap_seconds(self) -> float:
        """目前這圈已跑幾秒。碼表未啟動時回傳 0。"""
        if not self.is_running or self._lap_start_ticks is None:
            return 0.0
        return (pygame.time.get_ticks() - self._lap_start_ticks) / 1000.0

    def total_run_seconds(self) -> float:
        """這次按鍵後總共跑了幾秒（跨多圈持續累積）。碼表未啟動時回傳 0。"""
        if not self.is_running or self._run_start_ticks is None:
            return 0.0
        return (pygame.time.get_ticks() - self._run_start_ticks) / 1000.0

    def current_lap_str(self) -> str:
        """目前圈計時的格式化字串。idle 時回傳 'Press key...'。"""
        if not self.is_running:
            return "Press key..."
        return _fmt(self.current_lap_seconds())

    def best_lap_str(self) -> str:
        """最快圈的格式化字串。尚無紀錄時回傳 '--'。"""
        if self.best_lap is None:
            return "--"
        return _fmt(self.best_lap)

    @property
    def laps(self) -> list[float]:
        """本次跑的各圈時間（唯讀副本）。"""
        return list(self._laps)
