class Shape:
    def __init__(self, rotations):
        self.rotations = rotations
        self.current_rotation = 0
        self.number_rotations = len(self.rotations)

    def get_height(self):
        return len(self.get_current_rotation())

    def get_width(self):
        return len(self.get_current_rotation()[0])

    def get_current_rotation(self):
        return self.rotations[self.current_rotation]

    def rotate_right(self):
        self.current_rotation += 1
        if self.current_rotation >= self.number_rotations:
            self.current_rotation = 0

    def rotate_left(self):
        self.current_rotation -= 1
        if self.current_rotation < 0:
            self.current_rotation = self.number_rotations-1


class Input:
    def __init__(self, bindings):
        self.bindings = bindings
        self.actions = []


class GridPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class DeltaPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rotation:
    def __init__(self, index):
        self.index = index


class Speed:
    def __init__(self, amount):
        self.amount = amount
