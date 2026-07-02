import pygame

FINISH_RECT = pygame.Rect(50, 420, 145, 35)
CHECKPOINTS = [
    pygame.Rect(740, 175, 30, 160),
    pygame.Rect(1395, 335, 160, 30),
    pygame.Rect(790, 710, 30, 155),
]
MESSAGE_FRAMES = 30


class GameState:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.checkpoints_passed = [False, False, False]
        self.message = ""
        self.message_timer = 0


def update_lap_progress(car, state):
    on_finish_line = FINISH_RECT.collidepoint(car.x, car.y)
    on_checkpoint_1 = CHECKPOINTS[0].collidepoint(car.x, car.y)
    on_checkpoint_2 = CHECKPOINTS[1].collidepoint(car.x, car.y)
    on_checkpoint_3 = CHECKPOINTS[2].collidepoint(car.x, car.y)

    if on_checkpoint_1:
        if state.checkpoints_passed[1]:
            state.checkpoints_passed[1] = False
        elif not any(state.checkpoints_passed):
            state.checkpoints_passed[0] = True

    if on_checkpoint_2:
        if state.checkpoints_passed[2]:
            state.checkpoints_passed[2] = False
        elif state.checkpoints_passed[0] and not state.checkpoints_passed[1]:
            state.checkpoints_passed[1] = True

    if (
        on_checkpoint_3
        and state.checkpoints_passed[1]
        and not state.checkpoints_passed[2]
    ):
        state.checkpoints_passed[2] = True

    if on_finish_line and state.checkpoints_passed[2]:
        state.score += 1
        for i in range(3):
            state.checkpoints_passed[i] = False
        state.message = "+1 Lap!"
        state.message_timer = MESSAGE_FRAMES


def update_high_score(state):
    if state.score > state.high_score:
        state.high_score = state.score
