import time

from direction import Direction


class Movement(object):
    def __init__(self, direction, learner):
        # has a 0 < x < 1 and a 0 < y < 1
        self.x: float = 0
        self.y: float = 0
        self.direction = direction
        self.learner = learner

    def update(self):
        if self.direction.value == Direction.LEFT.value:
            self.x = - 1 + ((time.time() - self.learner.last_movement) / self.learner.must_wait)
        elif self.direction.value == Direction.UP.value:
            self.y = - 1 + ((time.time() - self.learner.last_movement) / self.learner.must_wait)

        elif self.direction.value == Direction.RIGHT.value:
            self.x = 1 - ((time.time() - self.learner.last_movement) / self.learner.must_wait)
        elif self.direction.value == Direction.DOWN.value:
            self.y = 1 - ((time.time() - self.learner.last_movement) / self.learner.must_wait)

    def get_offset(self):
        return self.x, self.y
