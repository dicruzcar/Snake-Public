
# An apology for my bad English, I hope the code is useful or at least you can enjoy the game

class Snake:

    #Directions
    __NORTH = "N"
    __SOUTH = "S"
    __EAST = "E"
    __WEST = "W"
    
    def __init__(self, pos_x = 2, pos_y = 2, size = 3, direction = __SOUTH):

        self.steps_buffer = []
        self.last_pos = []
        self.body = []
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.direction = direction
        trans_dir = self.__init_translate_dir(self.direction) # Translates de direction in a value to place the body of the snake
        modif_x = trans_dir[0] # Renaming value 1
        modif_y = trans_dir[1] # Renaming value 2
        
        for part in range(size):
            self.body.append([pos_x + (part * modif_x), pos_y + (part * modif_y)])
            # Setting the initial place of the snake
        
        self.steps_buffer = self.body.copy() #Saving to the position history
        self.steps_buffer.reverse()

    def eat(self): #Only works after the update body procces
        self.size = self.size + 1 #Growth the size
        self.grow_body()

    def grow_body(self):
        self.body.append(self.last_pos) # After the body update we restore the last position to grow the body
        self.steps_buffer.insert(0,self.last_pos) # We restory into the buffer to because we need it to

    def change_dir(self, new_dir):
        if (new_dir is not self.direction) and self.check_direction(new_dir): # if the direction is new, then changes it
            self.direction = new_dir

    def update_body(self):
        trans_dir = self.__translate_dir(self.direction) # Translates de direction in a value to place the head of the snake
        modif_x = trans_dir[0] # Values that can modify the directions
        modif_y = trans_dir[1] 
        self.body[0] = [self.body[0][0] + modif_x, self.body[0][1] + modif_y]
        self.steps_buffer.append(self.body[0]) # Saving the new head position
        self.last_pos = self.steps_buffer.pop(0) # Deleting the last body part position and saving temporally

        self.manage_queue(1) #This gona manage the consecuent movements of the rest of the body

    def manage_queue(self, start):
        self.body = self.steps_buffer.copy() #Setting the new head and the concecuent body movements in to the main body
        self.body.reverse() # Restoring the body position

    def get_head_position(self):
        return self.body[0]

    def get_only_body(self):
        tmp_arr = self.body.copy()
        tmp_arr.pop(0)
        return tmp_arr

    def __init_translate_dir(self, direction): # For use in reverse or in the initialization
        if direction == self.__NORTH:
            return (0, 1) 
        elif direction == self.__SOUTH:
            return (0, -1)
        elif direction == self.__EAST:
            return (-1, 0)
        elif direction == self.__WEST:
            return (1, 0)

    def __translate_dir(self, direction): # For use in the game regular cycle
        if direction == self.__NORTH:
            return (0, -1)
        elif direction == self.__SOUTH:
            return (0, 1)
        elif direction == self.__EAST:
            return (1, 0)
        elif direction == self.__WEST:
            return (-1, 0)

    def tick_cycle(self):
        self.update_body()

    def check_direction(self, direction):
        if (direction is self.__NORTH) and (self.direction is not self.__SOUTH):
            return direction
        elif (direction is self.__SOUTH) and (self.direction is not self.__NORTH):
            return direction
        elif (direction is self.__EAST) and (self.direction is not self.__WEST):
            return direction
        elif (direction is self.__WEST) and (self.direction is not self.__EAST):
            return direction
        else:
            return False

    #Get directions
    def get_north(self):
        return self.__NORTH
    
    def get_south(self):
        return self.__SOUTH

    def get_east(self):
        return self.__EAST

    def get_west(self):
        return self.__WEST

    
        



