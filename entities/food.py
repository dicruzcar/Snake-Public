
import random

class Food():

    def __init__(self, width, height):
        self.rangeX = (0,width-1)
        self.rangeY = (0,height-1)
        self.actual_food = [
            random.randint(self.rangeX[0], self.rangeX[1]),
            random.randint(self.rangeY[0], self.rangeY[1])
        ]

    def generate_food(self, exclude = []):
        tmp_x = random.randint(self.rangeX[0], self.rangeX[1])
        tmp_y = random.randint(self.rangeY[0], self.rangeY[1])

        if [tmp_x, tmp_y] not in exclude:
            self.actual_food = [tmp_x, tmp_y]
        else:
            self.generate_food(exclude)

    def get_food_position(self):
        return self.actual_food
