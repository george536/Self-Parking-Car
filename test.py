import cv2
import numpy as np
import pygame
import os

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bird's Eye View")


class ImageWarp():
    
    def __init__(self,offset=80):
        h, w, _ = image.shape
        src=[[0, h//2.5], [w, h//2.5], [w, h], [0, h]]
        w = 300
        h = 240
        dst=[[0, 0], [w, 0], [(w//2)+(w//4), h], [(w//2)-(w//4), h]]
        self.img_h = h
        self.img_w = w
        self.warp_offset = offset
        self.src = np.float32(src)
        self.dst = np.float32(dst)
        self.wmat = cv2.getPerspectiveTransform(self.src, self.dst)
        self.wmat_inv = cv2.getPerspectiveTransform(self.dst,self.src)
    
    def img_warp(self, iimg,inv=False, offset=False,offset_val=80):
        """
        Warps an image based on the input parameters

        Args:
            iimg ([type]): RGB / Gray image
            inv (bool, optional): invers transformation. Defaults to False.
            offset (bool, optional): use offset for warping the image. Defaults to False.

        Returns:
            [type]: warped image
        """
        
        ret = []
        timg = None

        if offset == True:
            self.warp_offset = offset_val
        
        if offset == True:
            timg = iimg[self.warp_offset:self.warp_offset+self.img_h, 0:self.img_w]
        else:
            timg = iimg
        
        if inv == False:
            ret = cv2.warpPerspective(timg,self.wmat , (self.img_w, self.img_h),flags=cv2.INTER_LANCZOS4)
        else:
            ret = cv2.warpPerspective(timg,self.wmat_inv , (self.img_w, self.img_h), flags=cv2.INTER_LANCZOS4)
        return ret

image = cv2.imread("car images/front.jpg")
wrap = ImageWarp()
wrapped = wrap.img_warp(image,False,False)

# image_folder = "car images"
# front_pos = (screen_width // 4, 0)
# back_pos = (screen_width // 4, screen_height // 2)
# left_pos = (0, screen_height // 4)
# right_pos = (screen_width // 2, screen_height // 4)
# birdseye_view = pygame.Surface((screen_width, screen_height))
# birdseye_view.blit(pygame.surfarray.make_surface(wrapped), front_pos)  # front image
# birdseye_view.blit(pygame.surfarray.make_surface(wrapped), right_pos)  # back image

w = 300
h = 240
dst=[[0, 0], [w, 0], [(w//2)+(w//4), h], [(w//2)-(w//4), h]]
pts = np.array(dst, np.int32)
pts = pts.reshape((-1, 1, 2))
mask = np.zeros_like(wrapped)
cv2.fillPoly(mask, [pts], (255, 255, 255))
cropped_image = cv2.bitwise_and(wrapped, mask)


from pygame.locals import *

pygame.init()
window_size = (800, 600)  # Set your desired window size
window = pygame.display.set_mode(window_size)

combined_surface = pygame.Surface(window_size, pygame.SRCALPHA)
pygame_img = pygame.image.frombuffer(wrapped.tostring(), wrapped.shape[1::-1], "BGR")
pygame_img.set_colorkey((0,0,0))
pygame_img.set_alpha(255)
combined_surface.blit(pygame_img, (0, 0))
combined_surface.blit(pygame_img, (30, 50))

rotation_matrix = cv2.getRotationMatrix2D((w/2, h/2), -(3-1)*90, 1)
rotation_matrix2 = cv2.getRotationMatrix2D((w/2, h/2), 90, 1)

# Apply the rotation to the image
down = cv2.warpAffine(wrapped, rotation_matrix, (w, h))
left = cv2.warpAffine(wrapped, rotation_matrix, (w, h))

# Determine the dimensions of the images
height1, width1, _ = wrapped.shape
height2, width2, _ = down.shape
height3, width3, _ = left.shape

# Calculate the width and height of the combined image
combined_width = width1 + width2
combined_height = h*2

# Create an empty canvas for the combined image
combined_image = np.zeros((combined_height, combined_width, 3), dtype=np.uint8)

# Copy the first image onto the canvas
combined_image[:height1, width1:width1*2] = wrapped

# Copy the second image onto the canvas, starting from the end of the first image
combined_image[height2:, width1:width1*2] = down

middle_y = combined_height // 2 - h // 2
combined_image[middle_y:middle_y+h, :width1] = left


# right image
while True:
    cv2.imshow("Bird's eye view", combined_image)
    cv2.waitKey(10)
    
    window.blit(combined_surface, (0, 0))
    pygame.display.update()

    # screen.blit(birdseye_view, (screen_width, 0))
    # pygame.display.update()