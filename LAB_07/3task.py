import pygame

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Red ball")

ball_radius = 25
ball_color = (255, 0, 0)
ball_x = screen_width // 2
ball_y = screen_height // 2

move_step = 20

pygame.key.set_repeat(50, 25)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            new_x, new_y = ball_x, ball_y

            if event.key == pygame.K_UP:
                new_y -= move_step
            elif event.key == pygame.K_DOWN:
                new_y += move_step
            elif event.key == pygame.K_LEFT:
                new_x -= move_step
            elif event.key == pygame.K_RIGHT:
                new_x += move_step

            if new_x - ball_radius < 0 or new_x + ball_radius > screen_width:
                new_x = ball_x
            if new_y - ball_radius < 0 or new_y + ball_radius > screen_height:
                new_y = ball_y

            ball_x, ball_y = new_x, new_y

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
