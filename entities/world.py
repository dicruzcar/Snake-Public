
class World:

    __world = []

    def __init__(self, width = 20, height = 20, snake_value = 1, food_value = 2):
        self.width = width
        self.height = height
        self.clear_world()
        self.snake_value = snake_value
        self.food_value = food_value

    def __render(self, array):
        for y in array:
            for x in y:
                if y[x] == 0:
                    print(x, end ="")
                elif y[x] == 1:
                    print(x, end ="")
            print("")

    def set_world(self, world):
        self.__world = world
    
    def get_world(self):
        return self.__world

    def insert_snake(self, array):
        for elem in array:
            self.__world[elem[1]][elem[0]] = self.snake_value

    def insert_food(self, array):
        self.__world[array[1]][array[0]] = self.food_value

    def clear_world(self):
        self.__world.clear()
        tmp_array = []
        for y in range(self.height):
            for x in range(self.width):
                tmp_array.append(0)
            self.__world.append(tmp_array.copy())
            tmp_array.clear()

    def _win_game(self):
        self.__world.clear()
        tmp_array = []
        for y in range(self.height):
            for x in range(self.width):
                tmp_array.append(1)
            self.__world.append(tmp_array.copy())
            tmp_array.clear()

    