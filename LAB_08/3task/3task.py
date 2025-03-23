import pygame

#Pygame initialization
pygame.init()

WIDTH = 800
HEIGHT = 600

#Colors
colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorBLACK = (0, 0, 0)
colorWHITE = (255, 255, 255)
colorPURPLE = (147, 112, 219)

#1, 2, 3, 4 stand for these colors
colors = {
    pygame.K_1: colorWHITE,
    pygame.K_2: colorRED,
    pygame.K_3: colorBLUE,
    pygame.K_4: colorPURPLE

}

#Default color
cur_color = colorWHITE 

#Setting up our screen and base layer
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(colorBLACK)
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(colorBLACK)


#For FPS
clock = pygame.time.Clock()

#If the left button pressed button
LMBpressed = False
THICKNESS = 5

#Current and previous positions variables
cur_x = cur_y = prev_x = prev_y = 0

running = True

current_tool = 'line'

#Calculates position and size of a rectangle 
def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            

        if event.type == pygame.KEYDOWN:
            #Selecting Color
            if event.key in colors:
                cur_color = colors[event.key]

            #Picking drawing tool
            if event.key == pygame.K_l:
                current_tool = 'line'
            if event.key == pygame.K_r:
                current_tool = 'rectangle'
            if event.key == pygame.K_e:
                current_tool = 'eraser'
            if event.key == pygame.K_c:
                current_tool = 'circle'

            #Regulating thickness
            if event.key == pygame.K_EQUALS:
                print("increased thickness")
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                print("reduced thickness")
                THICKNESS -= 1

        #Updating the variables after pressing the left button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            cur_x = event.pos[0]
            cur_y = event.pos[1]
            prev_x = event.pos[0]
            prev_y = event.pos[1]
        #Drawing based on a tool if the mouse is in the motion
        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                cur_x, cur_y = event.pos
                #Drawing a rectangle
                if current_tool == 'rectangle':
                    screen.blit(base_layer, (0, 0))
                    pygame.draw.rect(screen, cur_color, calculate_rect(prev_x, prev_y, cur_x, cur_y))
                #Drawing a circle
                if current_tool == 'circle':
                    screen.blit(base_layer, (0, 0))
                    radius = int(((cur_x - prev_x) ** 2 + (cur_y - prev_y) ** 2) ** 0.5)
                    pygame.draw.circle(screen, cur_color, (prev_x, prev_y), radius)
        #Updating the variables after letting the left button go
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            cur_x, cur_y = event.pos
            #Fixing our figures
            if current_tool == 'rectangle':
                pygame.draw.rect(base_layer, cur_color, calculate_rect(prev_x, prev_y, cur_x, cur_y))  
            if current_tool == 'circle':
                radius = int(((cur_x - prev_x) ** 2 + (cur_y - prev_y) ** 2) ** 0.5)
                pygame.draw.circle(base_layer, cur_color, (prev_x, prev_y), radius)
        
        #Drawing a line with current color or the background color based on a tool
        if current_tool == 'line' and LMBpressed:
            pygame.draw.line(screen, cur_color, (prev_x, prev_y), (cur_x, cur_y), THICKNESS)
            pygame.draw.line(base_layer, cur_color, (prev_x, prev_y), (cur_x, cur_y), THICKNESS) 
        if current_tool == 'eraser' and LMBpressed:
            pygame.draw.line(screen, colorBLACK, (prev_x, prev_y), (cur_x, cur_y), THICKNESS)
            pygame.draw.line(base_layer, colorBLACK, (prev_x, prev_y), (cur_x, cur_y), THICKNESS)
        

    #Updating the variables if we are drawing lines 
    if current_tool == 'line' or current_tool == 'eraser':
        prev_x = cur_x
        prev_y = cur_y


    #Our palette of colors
    pygame.draw.circle(screen, colorWHITE, (550, 570), 20)
    pygame.draw.circle(screen, colorRED, (600, 570), 20)
    pygame.draw.circle(screen, colorBLUE, (650, 570), 20)
    pygame.draw.circle(screen, colorPURPLE, (700, 570), 20)

    #Updating the screen
    pygame.display.flip()
    clock.tick(60)