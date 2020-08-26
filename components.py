class Shape:
    def __init__(self,rotations):
        self.rotations = rotations
        self.current_rotation = 0
        self.number_rotations = len(self.rotations)

    def rotate_right(shape):
        self.current_rotation += 1
        if self.current_rotation >= self.number_rotations:
            self.current_rotation = 0

    def rotate_left(shape):
        self.current_rotation -= 1
        if self.current_rotation < 0:
            self.current_rotation = self.number_rotations-1