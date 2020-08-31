import random 

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

class PieceContainer:
    def __init__(self, shapes):
        self.bag_inventory = list(shapes)
        self.bag = self.bag_inventory.copy()
        self.current = self.bag.pop() 

    def pop(self):
        if self.remainig_length() == 0:
            self.reset()
        return self.bag.pop()

    def reset(self):
        random.shuffle(self.bag_inventory)
        self.bag = self.bag_inventory.copy()

    def next(self):
        if(len(self.bag)) == 0:
            self.reset_bag()
        
        return self.bag[-1]

    def remainig_length(self):
        return len(self.bag)