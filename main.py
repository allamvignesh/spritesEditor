import pygame
from pygame.locals import *
from convertImagesTransperent import convertImage

pygame.init()

size = (600, 600)
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("Sprite Animation")
display = pygame.Surface([600, 600])

clock = pygame.time.Clock()
done = False

resolution = 50
Pad = [[(0, 0, 0, 0) for _ in range(500+resolution)[::resolution]] for _ in range(500+resolution)[::resolution]]
images = [pygame.Surface([500, 500])]
canvasPads = [[list(i) for i in Pad], ]
activeCanvas = 0
offset = 0
drawingColor = (255, 255, 0)

activeAnimation = 0
triggerAnimation = False

def drawGrid():
    grid = pygame.Surface([510, 510])

    for i in range(500+resolution)[::resolution]:
        pygame.draw.line(grid, (201, 201, 201), (i, 0), (i, 500))
    for i in range(500+resolution)[::resolution]:
        pygame.draw.line(grid, (201, 201, 201), (0, i), (500, i))
    
    grid.set_colorkey((0, 0, 0))
    display.blit(grid, (0, 0))

def newCanvas():
    canvasPads.append([list(i) for i in Pad])
    return pygame.Surface([500, 500])

def drawCanvas(image):
    display.blit(image, (0, 0))

def drawing(canva):

    l = [i for i in range(500+resolution)[::resolution]]
    length = l[1] - l[0]
    mouse = pygame.mouse.get_pos()
    canvasPad = canvasPads[activeCanvas]

    for i in range(len(canvasPad)):
        for j in range(len(canvasPad[i])):
            pygame.draw.rect(canva, canvasPad[i][j], ((i*length), (j*length), length, length))
            if (i*length) < mouse[0] < (i*length)+length and (j*length) < mouse[1] < (j*length)+length:
                pygame.draw.rect(canva, drawingColor, ((i*length), (j*length), length, length))
                if pygame.mouse.get_pressed()[0]:
                    canvasPad[i][j] = drawingColor
                elif pygame.mouse.get_pressed()[2]:
                    canvasPad[i][j] = (0, 0, 0, 0)

    canva.set_colorkey((0,0,0))
    display.blit(canva, (0, 0))

    return canva

def moreImages():
    global activeCanvas

    plus = pygame.image.load("plus.png")
    mouse = pygame.mouse.get_pos()
    end = len(images)

    for i, image in enumerate(images):
        display.blit(pygame.transform.scale(image, (80, 80)), (i+(80*i)-offset, 510))
        color = (148, 148, 148)
        if i == activeCanvas:
            color = (66, 233, 255)
        pygame.draw.rect(display, color, pygame.Rect(i+(80*i)-offset, 505, 85, 90),  4, 3)
        if i+(80*i) < mouse[0]+offset < i+(80*i)+85 and 505 < mouse[1] < 505+90:
            if pygame.mouse.get_pressed()[0]:
                activeCanvas = i
    
    pygame.draw.rect(display, (148, 148, 148), pygame.Rect(len(images)+(80*len(images))-offset, 505, 85, 90),  4, 3)
    
    if end+(80*end) < mouse[0]+offset < end+(80*end)+85 and 505 < mouse[1] < 505+90:
        plus = pygame.transform.scale(plus, (35, 35))
        if pygame.mouse.get_pressed()[0]:
            images.append(newCanvas())
    else:
        plus = pygame.transform.scale(plus, (30, 30))
    
    rect = plus.get_rect()
    rect.center = (len(images)+(80*len(images))+40-offset, 550)
    
    display.blit(plus, rect)

def changeColor():
    global drawingColor

    picker = pygame.image.load("color wheel.png")
    picker = pygame.transform.scale(picker, (550, 550))
    color = picker.get_at(pygame.mouse.get_pos())
    rect = picker.get_rect()
    rect.center = [i//2 for i in size]

    display.blit(picker, rect)
    if color[3] != 0:
        drawingColor = color
        pygame.draw.circle(display, (255, 255, 255), pygame.mouse.get_pos(), 5)

def exitCode():
    font = pygame.font.Font('freesansbold.ttf', 18)

    while True:
        screen.fill(0)

        display.set_alpha(100)
        screen.blit(display, (0, 0))
        mouse = pygame.mouse.get_pos()

        saveAndExit = font.render("Do you want to save before exit?", True, (0,0,0))
        save = font.render("Save", True, (0,0,0))
        exitOut = font.render("Exit", True, (0,0,0))

        pygame.draw.rect(screen, (235, 235, 235), pygame.Rect(150, 200, 300, 100),  0, 15)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(175, 250, 100, 30),  2, 10)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(325, 250, 100, 30),  2, 10)
        
        screen.blit(saveAndExit, (160, 218))
        screen.blit(save, (200, 256))
        screen.blit(exitOut, (360, 256))
        
        if pygame.mouse.get_pressed()[0]:
            if 200 < mouse[0] < 200+100 and 256 < mouse[1] < 256+30:
                for i, image in enumerate(images):
                    pygame.image.save(image, f"saves/{i}.png")
                    convertImage(f"saves/{i}.png")
                return True
            elif 360 < mouse[0] < 360+100 and 256 < mouse[1] < 256+30:
                return True
            else:
                return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        
        pygame.display.flip()
        clock.tick(60)

while not done:
    display.fill((255, 255, 255))
    
    if activeCanvas != 0 and not triggerAnimation:
        blank = pygame.Surface([500, 500])
        blank.blit(images[activeCanvas-1], (0,0))
        blank.set_colorkey((0,0,0))
        blank.set_alpha(100)
        display.blit(blank, (0,0))
    
    drawGrid()

    if not triggerAnimation:
        image = drawing(images[activeCanvas])
    else:
        try:
            drawCanvas(images[activeAnimation])
        except:
            activeAnimation = 0
        activeAnimation += 1
    moreImages()

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()

    pygame.draw.rect(display, (0, 0, 0), (590, offset, 10, 80))
    if mouse[0] > 580:
        if pygame.mouse.get_pressed()[0]:
            offset = mouse[1]-40
        
    if keys[K_c]:
        changeColor()

    if keys[K_t]:
        newEvent = pygame.event.Event(pygame.locals.KEYDOWN, unicode=' ', key=32, mod=4096, scancode=44, window=None)
        pygame.event.post(newEvent)

    screen.blit(display, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = exitCode()
        if event.type == pygame.KEYDOWN:
            if event.unicode == ' ':
                activeAnimation = 0
                triggerAnimation = not triggerAnimation

    pygame.display.flip()
    clock.tick(40)
