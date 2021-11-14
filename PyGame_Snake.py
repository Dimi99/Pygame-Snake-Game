import random
from enum import Enum
from collections import namedtuple
import pygame


pygame.init()

font = pygame.font.SysFont('arial', 25)
clock = pygame.time.Clock()



# document all directions as an Enumeration
class Direction(Enum):
    Right = 1
    Up = 2
    Left = 3
    Down = 4
    
    
Point = namedtuple('Point', 'x, y')

##Constants##
# rgb colors
RED = (255,0,0)
GREEN = (0,255,0)
DARKGREEN = (0, 100,0)
BLACK = (0,0,0)
MAGENTA = (255,0,255)
YELLOW= (255,255,0)

BLOCK_SIZE = 25
SPEED = 18
COLOUR_BORDERS = MAGENTA
COLOUR_SNAKE = GREEN





class Snake:
    
    def __init__(self, width=700, height=700):
        self.width = width
        self.height = height
 
        
        #Initialize the display
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Snake")
        self.score = 0 
        self.game_over = False 
        
     
         #Draw the snake with 4 blocks 
        self.snake = []
        
        for i in range( 4):
            p = Point(int((width/2)/BLOCK_SIZE)*BLOCK_SIZE-(BLOCK_SIZE * i), int((height/2)/BLOCK_SIZE)*BLOCK_SIZE)
            self.snake.append(p)     
      
        self._spawn_food()
        
        #set the initial direction to right 
        self.Direction = Direction.Right  
        

        
    def _spawn_food(self):
        
        # generates 2 random food coordinates, divide and multiply by Block_Size to ensure placement on grid
        random_x = int(random.randint(BLOCK_SIZE,self.width-BLOCK_SIZE-2)/BLOCK_SIZE+0.1) *BLOCK_SIZE
        random_y = int(random.randint(BLOCK_SIZE,self.height-BLOCK_SIZE-2)/BLOCK_SIZE+0.1) *BLOCK_SIZE
        self.food = Point(random_x, random_y) 
        
        
        # Recursively call function again to avoid food placement inside snake or borders
        if self.food in self.snake:
            self._spawn_food
 
    def game_frame(self):

        # 1. collect user input 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.Direction = Direction.Up
                elif event.key == pygame.K_DOWN:
                    self.Direction = Direction.Down
                elif event.key == pygame.K_RIGHT:
                    self.Direction = Direction.Right 
                elif event.key == pygame.K_LEFT:
                    self.Direction = Direction.Left 
                    
        # 2. move (update the head) 
        self._move(self.Direction) 
    
        # 3. check if snake has eaten on this frame
        if self.snake[0] == self.food:
            self._spawn_food()
            self.score += 1 
        else:
            self.snake.pop()
            
        # 4. Update the UI 
        self._draw_ui()
        
        # 5. check if game over & return
        if self._is_collision() :
            self.game_over = True
        return self.game_over, self.score 
        
       
        

        
    def _is_collision(self):
        # check if snake hits boundary / itself
        #
        if  self._collision_with_itself(self.snake) or  self._collision_with_border() :
            return True 
        else:
            return False
        
        
    def _collision_with_itself(self,listOfElems):
   # helper function:
   #if duplicates in list --> snake hit itself 
        if len(listOfElems) == len(set(listOfElems)):
            return False
        else:
            return True
        
    def _collision_with_border(self):
        
        if (self.snake[0].x < BLOCK_SIZE or self.snake[0].x == self.width- BLOCK_SIZE or self.snake[0].y < BLOCK_SIZE or 
            self.snake[0].y == self.height-BLOCK_SIZE):
             
            return True
        else:
            return False

    def _draw_ui(self):
        # Draw Screen, Borders & Score-Text
        self.screen.fill(BLACK)
        self._draw_borders(MAGENTA)
        text = font.render("Score: " + str(self.score), True, YELLOW)
        self.screen.blit(text, [BLOCK_SIZE, BLOCK_SIZE])
   
        #Draw the food 
        food_rec =  pygame.draw.rect(self.screen, RED, pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        
        #Draw the snake 
        for blocks in self.snake:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(blocks.x,blocks.y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.screen, DARKGREEN, pygame.Rect(blocks.x+(BLOCK_SIZE/5),blocks.y+(BLOCK_SIZE/5) ,BLOCK_SIZE/2 ,BLOCK_SIZE/2))
            
            
        pygame.display.flip()
        
  
    #Draw 4 borders around the screen 
    def _draw_borders(self,colour_Borders):
        
        self.border1 = pygame.draw.rect(self.screen, colour_Borders, pygame.Rect(0, 0, BLOCK_SIZE, self.height-BLOCK_SIZE))
        self.border2 = pygame.draw.rect(self.screen, colour_Borders, pygame.Rect(0, 0, self.width-BLOCK_SIZE, BLOCK_SIZE))
        self.border3 = pygame.draw.rect(self.screen, colour_Borders, pygame.Rect(self.width-  
                                                                                 BLOCK_SIZE,0,BLOCK_SIZE,self.height))
        self.border4 = pygame.draw.rect(self.screen, colour_Borders, pygame.Rect(0,self.height-
                                                                                 BLOCK_SIZE,self.width,BLOCK_SIZE))

    def _move(self, direction):
        
        x_head = self.snake[0].x
        y_head = self.snake[0].y
         
        # moves based on direction --> 4 Possible Directions
        if self.Direction == Direction.Right:
            x_head += BLOCK_SIZE
        elif self. Direction == Direction.Left:
            x_head -= BLOCK_SIZE
            
        elif self.Direction == Direction.Up:
            y_head -= BLOCK_SIZE
            
        elif self.Direction == Direction.Down:
            y_head += BLOCK_SIZE 
        
        head = Point(x_head, y_head)
        self.snake.insert(0,head) 
        
            

if __name__ == '__main__':
    game = Snake()

    # game loop
    while True:
        
        game_over, score = game.game_frame()
        
        if game_over == True:
            break
        clock.tick(SPEED) 
        
    print('Final Score', score)
        
