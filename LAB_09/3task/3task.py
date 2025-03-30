import pygame
import math

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

#Calculates position and size of a square
def calculate_square(x1,y1,x2,y2):
    size=min(abs(x1-x2),abs(y1-y2))
    return pygame.Rect(min(x1,x2),min(y1,y2),size,size)

#Calculates vertices of an equilateral triangle given two points (base endpoints)
def calculate_triangle(x1,y1,x2,y2):
    dx=x2-x1
    dy=y2-y1
    angle=math.radians(60)
    cos_angle=math.cos(angle)
    sin_angle=math.sin(angle)
    x3=x1+dx*cos_angle-dy*sin_angle
    y3=y1+dx*sin_angle+dy*cos_angle
    return [(x1,y1),(x2,y2),(int(x3),int(y3))]

#Calculates vertices of a right triangle
def calculate_right_triangle(x1,y1,x2,y2):
    return [(x1,y1),(x2,y1),(x1,y2)]

#Calculates vertices of a rhombus inscribed in the rectangle defined by (x1,y1) and (x2,y2)
def calculate_rhombus(x1,y1,x2,y2):
    mid_x=(x1+x2)//2
    mid_y=(y1+y2)//2
    return [(mid_x,y1),(x2,mid_y),(mid_x,y2),(x1,mid_y)]

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
            if event.key == pygame.K_s: 
                current_tool = 'square'
            if event.key==pygame.K_t:
                current_tool='triangle'
            if event.key==pygame.K_g:
                current_tool='right_triangle'
            if event.key==pygame.K_p:
                current_tool='rhombus'
            
            if event.key == pygame.K_z:  # Detect "Z" key press
                screen.fill(colorBLACK)  # Fill the entire screen with black
                base_layer.fill(colorBLACK)  # Clear the base layer as well

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
                #Drawing a square
                if current_tool=='square':
                    screen.blit(base_layer,(0,0))
                    pygame.draw.rect(screen,cur_color,calculate_square(prev_x,prev_y,cur_x,cur_y))
                #Drawing a right triangle
                if current_tool=='right_triangle':
                    screen.blit(base_layer,(0,0))
                    vertices=calculate_right_triangle(prev_x,prev_y,cur_x,cur_y)
                    pygame.draw.polygon(screen,cur_color,vertices)
                #Drawing a triangle
                if current_tool=='triangle':
                    screen.blit(base_layer,(0,0))
                    vertices=calculate_triangle(prev_x,prev_y,cur_x,cur_y)
                    pygame.draw.polygon(screen,cur_color,vertices)
                #Drawing a rhombus
                if current_tool=='rhombus':
                    screen.blit(base_layer,(0,0))
                    vertices=calculate_rhombus(prev_x,prev_y,cur_x,cur_y)
                    pygame.draw.polygon(screen,cur_color,vertices)
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
            if current_tool=='square':
                pygame.draw.rect(base_layer,cur_color,calculate_square(prev_x,prev_y,cur_x,cur_y))
            if current_tool=='right_triangle':
                vertices=calculate_right_triangle(prev_x,prev_y,cur_x,cur_y)
                pygame.draw.polygon(base_layer,cur_color,vertices)
            if current_tool=='triangle':
                vertices=calculate_triangle(prev_x,prev_y,cur_x,cur_y)
                pygame.draw.polygon(base_layer,cur_color,vertices)
            if current_tool=='rhombus':
                vertices=calculate_rhombus(prev_x,prev_y,cur_x,cur_y)
                pygame.draw.polygon(base_layer,cur_color,vertices)
        
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