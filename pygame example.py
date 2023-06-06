import pygame
import os

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bird's Eye View")

image_folder = "car images"
car_images = []

for side in ["front", "back", "left", "right"]:
    image_path = os.path.join(image_folder, side + ".jpg")
    car_image = pygame.image.load(image_path).convert_alpha()
    car_image = pygame.transform.scale(car_image, (screen_width // 4, screen_height // 2))
    car_images.append(car_image)

birdseye_view = pygame.Surface((screen_width // 2, screen_height))

# Calculate the positions for blitting the images
front_pos = (screen_width // 4, 0)
back_pos = (screen_width // 4, screen_height // 2)
left_pos = (0, screen_height // 4)
right_pos = (screen_width // 2, screen_height // 4)

birdseye_view.blit(car_images[0], front_pos)  # front image
birdseye_view.blit(car_images[1], back_pos)  # back image
birdseye_view.blit(car_images[2], left_pos)  # left image
birdseye_view.blit(car_images[3], right_pos)  # right image

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(birdseye_view, (screen_width // 4, 0))
    pygame.display.flip()

pygame.quit()
