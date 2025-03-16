import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("music player")

def scale_image(image):
    original_width, original_height = image.get_size()
    scale_factor = min(800 / original_width, 600 / original_height)
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    return pygame.transform.scale(image, (new_width, new_height))

play_image = pygame.image.load("play.png")
stop_image = pygame.image.load("stop.png")

play_image = scale_image(play_image)
stop_image = scale_image(stop_image)

current_image = play_image

tracks = ["song1.mp3", "song2.mp3", "song3.mp3"]
track_names = ["JOJOOOOOOOO", "Samurai Champlo", "Riptide"]
current_track_index = 0

def play_track(index):
    """Загружает и начинает воспроизведение трека по заданному индексу."""
    pygame.mixer.music.load(tracks[index])
    pygame.mixer.music.play()

play_track(current_track_index)

# Устанавливаем событие, которое сработает при окончании песни
pygame.mixer.music.set_endevent(pygame.USEREVENT)

paused = False

font = pygame.font.Font(None, 48)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            current_track_index = (current_track_index + 1) % len(tracks)
            play_track(current_track_index)
            paused = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_image == play_image:
                    current_image = stop_image
                else:
                    current_image = play_image
            if event.key == pygame.K_SPACE:
                if not paused:
                    pygame.mixer.music.pause()
                    paused = True
                else:
                    pygame.mixer.music.unpause()
                    paused = False

            elif event.key == pygame.K_RIGHT:
                paused = False
                current_image = play_image
                current_track_index = (current_track_index + 1) % len(tracks)
                play_track(current_track_index)

            elif event.key == pygame.K_LEFT:
                paused = False
                current_image = play_image
                current_track_index = (current_track_index - 1) % len(tracks)
                play_track(current_track_index)

    screen.fill((255, 255, 255))
    
    img_width, img_height = current_image.get_size()
    x = (800 - img_width) // 2
    y = (600 - img_height) // 2
    screen.blit(current_image, (x, y))

    text_box_rect = pygame.Rect((800 - 300) // 2, 50, 300, 100)
    pygame.draw.rect(screen, (50, 50, 50), text_box_rect)
    
    song_name = track_names[current_track_index]
    text_surface = font.render(song_name, True, (255, 255, 255))
    
    text_x = text_box_rect.x + (text_box_rect.width - text_surface.get_width()) // 2
    text_y = text_box_rect.y + (text_box_rect.height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))


    pygame.display.flip()

pygame.quit()

