class SpawnNewPieceEvent:
    pass


class BoundaryHitEvent:
    def __init__(self, side):
        self.side = side

class LineCleared:
    pass

class SaveScoreEvent:
    pass

class QuitGameEvent:
    pass

class RotatePieceEvent:
    pass

class MovePieceDownEvent:
    pass

class MovePieceLeftEvent:
    pass

class MovePieceRightEvent:
    pass