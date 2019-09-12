import pygame, sys, os
from pathlib import Path 
from entities.snake import Snake
from entities.food import Food
from entities.world import World

class Game():

    def __init__(self, width = 400, height = 400, background = "background.png", snake_value = 1, food_value = 2):
        os.environ['SDL_VIDEO_CENTERED'] = "1"
        pygame.init()                           #The main pygame init
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake")

        #World attributes
        self.width = width
        self.height = height
        self.background = (255,255,255)
        self.basic_pixel_unit = 20
        self.world_width = width / self.basic_pixel_unit
        self.world_height = height / self.basic_pixel_unit
        self.snake_body_unit_size = self.basic_pixel_unit
        self.snake_body_color = (0,0,0)
        self.snake_value = snake_value
        self.food_value = food_value
        self.food_color = (203,203,203)

        #Game attributes
        self.restart_key = "SPACE"
        self.true_game_frames = 6
        self.reaction_frames = 60
        self.true_frames_and_reaction_coeficent = int(self.reaction_frames/self.true_game_frames)
        self.win = False
        self.h1_font = pygame.font.Font(self.fonts("Blinker-Regular.ttf"), 40)
        self.h2_font = pygame.font.Font(self.fonts("Blinker-Regular.ttf"), 20)
        self.win_text = "¡Felicidades!, ganaste"
        self.win_surface = self.h1_font.render(self.win_text, True, (110,193,229))
        self.dead_text = "Has muerto :("
        self.dead_surface = self.h1_font.render(self.dead_text, True, (228,82,50))
        self.restart_text = f"Presiona [{self.restart_key}] para reiniciar"
        self.restart_surface = self.h2_font.render(self.restart_text, True, (0,0,0))
        self.game_text_margins = 10

        #World objects
        self.world = World(int(self.world_width), int(self.world_height))
        self.snake = Snake()
        self.food = Food(self.world_width,self.world_height)
        self.food.generate_food(self.snake.body)

        self.alive = True
        
        self.main_thread()
        
    def main_thread(self):

        clock = pygame.time.Clock()
        counter = 0
        key_buffer = [self.snake.direction]

        while True:

            for events in pygame.event.get():
                self.events_manager(events.type)

            key_buffer = self.keyboard_events(key_buffer)

            if counter == self.true_frames_and_reaction_coeficent:
                key_buffer = self.keyboard_buffer(key_buffer)
                self.load_world()
                counter = 0

            clock.tick(self.reaction_frames)
            counter = counter + 1

        return 0

    def load_image(self, filename, transparent=False):
        try: image = pygame.image.load(filename) #Try to load the image
        except pygame.error:                     #Manage the exception
            print("Error al cargar la Imagen", pygame.get_error())
            raise (SystemExit)
        image = image.convert()                 #Convert to pygame friendly format
        if transparent:                         #Manage transparency
                color = image.get_at((0,0))
                image.set_colorkey(color, pygame.RLEACCEL)
        return image

    def fonts(self, name):
        base_path = Path.cwd()
        final_path = str(base_path / f"src/fonts/{name}")
        return final_path

    def events_manager(self, event):
            if event == pygame.QUIT:
                sys.exit(0)

    def load_world(self):

        self.screen.fill(self.background)
        self.die_event()
        self.win_event()
        if self.alive and not self.win:
            self.snake.tick_cycle()
            self.world.clear_world()

            self.eat_event()

            self.draw_game(self.world.get_world())
            pygame.display.update()
        elif self.win:
            self.set_win_screen()
        elif not self.alive:
            self.set_dead_screen()
        else:
            pass

    def translate_to_game_unit(self, value):
        return value * self.basic_pixel_unit

    def draw_game(self, array):
        for index_y, y in enumerate(array):
            for index_x, x in enumerate(y):
                tmp_x = self.translate_to_game_unit(index_x)
                tmp_y = self.translate_to_game_unit(index_y)
                if x == self.snake_value:
                    pygame.draw.rect(self.screen, self.snake_body_color, pygame.Rect(tmp_x,tmp_y,self.basic_pixel_unit,self.basic_pixel_unit))
                elif x == self.food_value:
                    pygame.draw.rect(self.screen, self.food_color, pygame.Rect(tmp_x,tmp_y,self.basic_pixel_unit,self.basic_pixel_unit))

    def update_world(self, array):
        self.world = array
    
    def keyboard_events(self, key_array = []):
        key_counter = key_array.copy()
        keys = pygame.key.get_pressed()

        if len(key_counter) < 1:
            key_counter.append(self.snake.direction)

        actual_key = key_counter[len(key_counter)-1]

        if keys[pygame.K_UP] and (self.snake.get_north() != self.snake.direction) and (self.snake.get_north() != actual_key):
            key_counter.append(self.snake.get_north())

        elif keys[pygame.K_DOWN] and (self.snake.get_south() != self.snake.direction) and (self.snake.get_south() != actual_key):
            key_counter.append(self.snake.get_south())

        elif keys[pygame.K_RIGHT] and (self.snake.get_east() != self.snake.direction) and (self.snake.get_east() != actual_key):
            key_counter.append(self.snake.get_east())

        elif keys[pygame.K_LEFT] and (self.snake.get_west() != self.snake.direction) and (self.snake.get_west() != actual_key):
            key_counter.append(self.snake.get_west())

        elif keys[pygame.K_SPACE]:
            self.alive = True
            self.win = False
            self.__init__()


        return key_counter
    
    def keyboard_buffer(self, keys_arr = []):
        keys = keys_arr.copy()
        if keys[0] == self.snake.get_north():
            self.snake.change_dir(self.snake.get_north())
        elif keys[0] == self.snake.get_south():
            self.snake.change_dir(self.snake.get_south())
        elif keys[0] == self.snake.get_east():
            self.snake.change_dir(self.snake.get_east())
        elif keys[0] == self.snake.get_west():
            self.snake.change_dir(self.snake.get_west())
        keys.pop(0)
        return keys
    
    def eat_event(self):
        if self.snake.get_head_position() != self.food.get_food_position():
            self.world.insert_snake(self.snake.body)
            self.world.insert_food(self.food.get_food_position())
        else:
            self.snake.eat()
            self.food.generate_food(self.snake.body)
            self.world.insert_snake(self.snake.body)
            self.world.insert_food(self.food.get_food_position())

    def die_event(self):
        self.wall_collition()
        self.i_have_bit_myself()
        
    def wall_collition(self):
        min_x = 0
        max_x = self.world.width - 1
        min_y = 0
        max_y = self.world.height - 1
        if self.snake.get_head_position()[0] == min_x and self.snake.direction == self.snake.get_west():
            self.alive = False
        elif self.snake.get_head_position()[0] == max_x and self.snake.direction == self.snake.get_east():
            self.alive = False
        elif self.snake.get_head_position()[1] == min_y and self.snake.direction == self.snake.get_north():
            self.alive = False
        elif self.snake.get_head_position()[1] == max_y and self.snake.direction == self.snake.get_south():
            self.alive = False
    
    def i_have_bit_myself(self):
        if self.snake.get_head_position() in self.snake.get_only_body():
            self.alive = False
    
    def win_event(self):
        tmp_counter  = 0
        max_cells = self.world_width * self.world_height
        for y in self.world.get_world():
            for x in y:
                if x == 1:
                    tmp_counter = tmp_counter + 1
        if tmp_counter == max_cells:
            self.win = True

    def set_win_screen(self):
        win_surface_size = self.h1_font.size(self.win_text)
        restart_surface_size = self.h2_font.size(self.restart_text)
        self.screen.blit(self.win_surface,(
            self.width/2 - win_surface_size[0]/2,
            (self.height/2 - win_surface_size[1]/2) - win_surface_size[1]/2)
            )
        self.screen.blit(self.restart_surface,(
            self.width/2 - restart_surface_size[0]/2,
            (self.height/2 + win_surface_size[1] + self.game_text_margins) -  restart_surface_size[1]/2)
            )
        pygame.display.update()

    def set_dead_screen(self):
        dead_surface_size = self.h1_font.size(self.dead_text)
        restart_surface_size = self.h2_font.size(self.restart_text)
        self.screen.blit(self.dead_surface,(
            self.width/2 - dead_surface_size[0]/2,
            (self.height/2 - dead_surface_size[1]/2) - dead_surface_size[1]/2)
            )
        self.screen.blit(self.restart_surface,(
            self.width/2 - restart_surface_size[0]/2,
            (self.height/2 + dead_surface_size[1] + self.game_text_margins) -  restart_surface_size[1]/2)
            )
        pygame.display.update()


