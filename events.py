class SpawnNewPieceEvent:
    pass 

class BoundaryHitEvent:
    def __init__(self, side):
        self.side = side