"""
--------------------------------------------------------
#### 這個檔案負責「把按鍵變成車子的動作」(Q2、Q3)
--------------------------------------------------------
"""

import pygame

from car import ACCEL, ROTATE_SPEED


def handle_movement(keys, car):
    """
    --------------------------------------------------------
    #### 功能 : 根據目前按住的鍵，控制車子前進/後退/轉向
    --------------------------------------------------------
    #### 回傳值
    - 無(直接呼叫 car 的方法讓車子動)
    --------------------------------------------------------
    """
    """
    --------------------------------------------------------
    Q2. 完成 W、S 前進/後退的判斷
    Todo : 按 W 呼叫 car.set_accel(ACCEL) 前進
           按 S 呼叫 car.set_accel(-ACCEL) 後退
           兩個都沒按，呼叫 car.set_accel(0)
    Hint : 用 if / elif / else，三種情況只會發生一種
    ####參數：
    - keys : pygame.key.get_pressed() 的結果，
             可以用 keys[pygame.K_w] 這種方式查詢某個鍵有沒有被按住
    - car : 車子物件
    --------------------------------------------------------
    """
    # Q2 begin
    if "__fill_in__": #如果按下W
        "__fill_in__" #車子前進
    elif "__fill_in__": #如果按下S
        "__fill_in__" #車子後退
    else: #如果兩個都沒按
        "__fill_in__" #車子不動
    
    # 參考答案：
    # if keys[pygame.K_w]:
    #     car.set_accel(ACCEL)
    # elif keys[pygame.K_s]:
    #     car.set_accel(-ACCEL)
    # else:
    #     car.set_accel(0)
    # Q2 end

    """
    --------------------------------------------------------
    Q3. 完成 J、K 轉向的判斷
    Todo : 按 J 呼叫 car.rotate(-ROTATE_SPEED) 左轉
           按 K 呼叫 car.rotate(ROTATE_SPEED) 右轉
    Hint : 用兩個獨立的 if(不要用 elif)，因為兩個鍵理論上互不影響
    --------------------------------------------------------
    """
    # Q3 begin
    if "__fill_in__": #如果按下J
        "__fill_in__" #車子左轉
    if "__fill_in__": #如果按下K
        "__fill_in__" #車子右轉
    # 參考答案：
    # if keys[pygame.K_j]:
    #     car.rotate(-ROTATE_SPEED)
    # if keys[pygame.K_k]:
    #     car.rotate(ROTATE_SPEED)
    # Q3 end
