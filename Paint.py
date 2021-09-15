import pygame
from pygame.locals import *
from math import floor
from tkinter import *
from tkinter import filedialog
import pickle
# from ast import literal_eval
import os
pygame.init()

WIDTH,HEIGHT = 800,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Paint")

font = pygame.font.SysFont('Times New Roman',30)
FILL_BUCKET_IMG = pygame.image.load(os.path.join('Assets','Paint_bucket.png'))
PEN_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Pen.png')),(30,30))
ERASER_IMG = pygame.image.load(os.path.join('Assets','Eraser.png'))
EYEDROP_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Eyedropper.png')),(30,30))
EYEDROP_IMG.set_colorkey((255,255,255))


Canvas_Height = HEIGHT-100
Canvas_Width = WIDTH-150
spacing = 10
rows = int(Canvas_Width/spacing)
cols = int(Canvas_Height/spacing)

font1 = pygame.font.Font(None,32)
clear = font.render('Clear',True,(1,2,3))
save = font.render('Save',True,(1,2,3))
load = font.render('Load',True,(1,2,3))

class pixels:
    def __init__(self,x,y,color,width):
        self.x = x
        self.y = y
        self.width = width
        self.color = color

    def show(self):
        pygame.draw.rect(WIN,self.color,(self.x,self.y,self.width,self.width))

    def change_color(self,color):
        self.color = color

class color:
    def __init__(self,x,y,color,width):
        self.x = x
        self.y = y
        self.color = color
        self.width = width

    def show(self):
        pygame.draw.rect(WIN,self.color,(self.x,self.y,self.width,self.width))
    
    def clicked(self,mx,my):
        if mx > self.x and mx < self.x + self.width:
            if my > self.y and my < self.y + self.width:
                return True
        else:
            return False

def floodfill(matrix, x, y,old_color,new_color):
    if matrix[x][y].color != new_color:
        if matrix[x][y].color == old_color:  
            matrix[x][y].change_color(new_color) 
            if x > 0:
                floodfill(matrix,x-1,y,old_color,new_color)
            if x < len(matrix[y]) - 1:
                floodfill(matrix,x+1,y,old_color,new_color)
            if y > 0:
                floodfill(matrix,x,y-1,old_color,new_color)
            if y < len(matrix) - 1:
                floodfill(matrix,x,y+1,old_color,new_color)

            return matrix
    else:
        return matrix

def prompt_file():
    top = Tk()
    top.withdraw()
    filename = filedialog.askopenfilename(parent=top)
    top.destroy()
    return filename

textbox = pygame.Rect(390,HEIGHT-85,170,30)
textbox_passive_color = pygame.Color('gray15')
textbox_active_color = pygame.Color('lightskyblue3')

def draw_window(grid,colors,choosen_color,file_name,textbox_state):
    WIN.fill((255,255,255))
    pygame.draw.rect(WIN,(128,128,128),(Canvas_Width,0,WIDTH-Canvas_Width,HEIGHT))
    pygame.draw.rect(WIN,(128,128,128),(0,Canvas_Height,WIDTH,HEIGHT-Canvas_Height))
    pygame.draw.rect(WIN,(200,200,200),(20,HEIGHT-90,120+20,80))
    pygame.draw.rect(WIN,(200,200,200),(170,HEIGHT-75,50,50))
    pygame.draw.rect(WIN,choosen_color,(180,HEIGHT-65,30,30))

    # Clear button
    pygame.draw.rect(WIN,(200,200,200),(250,HEIGHT-65,80,30))
    WIN.blit(clear,(255,HEIGHT-64))

    # Toolbar
    pygame.draw.rect(WIN,(200,200,200),(Canvas_Width+10,10,130,100))
    WIN.blit(PEN_IMG,(Canvas_Width+30,20))
    WIN.blit(FILL_BUCKET_IMG,(Canvas_Width+90,20))
    WIN.blit(ERASER_IMG,(Canvas_Width+30,70))
    WIN.blit(EYEDROP_IMG,(Canvas_Width+90,70))

    # Save Tools
    if textbox_state:
        textbox_color = textbox_active_color
    else:
        textbox_color = textbox_passive_color
    pygame.draw.rect(WIN,textbox_color,textbox,2)
    file_name_surface = font1.render(file_name,True,(1,2,3))
    WIN.blit(file_name_surface,(395,HEIGHT-80))
    pygame.draw.rect(WIN,(200,200,200),(390,HEIGHT-45,80,30))
    WIN.blit(save,(400,HEIGHT-44))
    pygame.draw.rect(WIN,(200,200,200),(480,HEIGHT-45,80,30))
    WIN.blit(load,(490,HEIGHT-44))

    for i in range(rows):
        for j in range(cols):
            grid[i][j].show()
    for i in colors:
        i.show()
    pygame.display.update()

def main():
    
    grid = []
    for i in range(rows):
        t = []
        for j in range(cols):
            x = pixels(i*spacing,j*spacing,(255,255,255),spacing)
            t.append(x)
        grid.append(t)

    colors_width = 30
    colors = [color(colors_width,HEIGHT-80,(0,0,0),colors_width),\
            color(colors_width*2,HEIGHT-80,(255,0,0),colors_width),\
            color(colors_width*3,HEIGHT-80,(0,255,0),colors_width),\
            color(colors_width*4,HEIGHT-80,(0,0,255),colors_width),\
            color(colors_width,HEIGHT-50,(255,0,255),colors_width),\
            color(colors_width*2,HEIGHT-50,(255,255,0),colors_width),\
            color(colors_width*3,HEIGHT-50,(143,76,198),colors_width),\
            color(colors_width*4,HEIGHT-50,(255,255,255),colors_width)]

# Color Changing from text file
    # color_names = []
    # with open('change_colors.txt') as f:
        # for line in f:
            # color_names.append(literal_eval(line.strip()))

    # colors_width = 30
    # colors = [color(colors_width,HEIGHT-80,color_names[0],colors_width),\
            # color(colors_width*2,HEIGHT-80,color_names[1],colors_width),\
            # color(colors_width*3,HEIGHT-80,color_names[2],colors_width),\
            # color(colors_width*4,HEIGHT-80,color_names[3],colors_width),\
            # color(colors_width,HEIGHT-50,color_names[4],colors_width),\
            # color(colors_width*2,HEIGHT-50,color_names[5],colors_width),\
            # color(colors_width*3,HEIGHT-50,color_names[6],colors_width),\
            # color(colors_width*4,HEIGHT-50,color_names[7],colors_width)]
    
    file_name = 'New Draw1'
    textbox_state = False

    pen_color = (0,0,0)
    pen_state = 0                   # 0-Brush  1-Fill    2-Eyedropper

    run = True
    while run:
        
        mx,my = pygame.mouse.get_pos()
        choosen_color = pen_color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if pygame.mouse.get_pressed()[0]:
                if my < Canvas_Height and mx < Canvas_Width:
                    if pen_state == 0:
                        grid[floor(mx/spacing)][floor(my/spacing)].change_color(pen_color)
                    # elif event.button == 3:
                        # grid[floor(mx/spacing)][floor(my/spacing)].change_color((255,255,255))

                    if pen_state == 1:
                        grid = floodfill(grid,floor(mx/spacing),floor(my/spacing),grid[floor(mx/spacing)][floor(my/spacing)].color,pen_color)
                    
                    if pen_state == 2:
                        pen_color = grid[floor(mx/spacing)][floor(my/spacing)].color
                        pen_state = 0

                elif mx > 255 and mx < 255 + 80:
                    if my > HEIGHT-65 and my < HEIGHT-65 + 30:
                        for i in range(rows):
                            for j in range(cols):
                                grid[i][j].change_color((255,255,255))
                
                elif mx > 480 and mx < 480 + 80:
                    if my > HEIGHT-45 and my < HEIGHT-45 + 30:
                        load_file_name = prompt_file()
                        file1 = open(load_file_name,'rb')
                        try:
                            while True:
                                grid = pickle.load(file1)
                        except EOFError:
                            file1.close()
                elif mx > 390 and mx < 390 + 80:
                    if my > HEIGHT-45 and my < HEIGHT-45 + 30:
                        if len(file_name) != 0:
                            file2 = open(f"./Saves/{file_name}.dat",'wb')
                            print('Saved!')
                            pickle.dump(grid,file2)
                            file2.close()

                elif mx > Canvas_Width+90 and mx < Canvas_Width+120:
                    if my > 20 and my < 50:
                        pen_state = 1
                    if my > 70 and my < 100:
                        pen_state = 2

                elif mx > Canvas_Width+30 and mx < Canvas_Width+60:
                    if my > 20 and my < 50:
                        pen_state = 0
                    if my > 70 and my < 100:
                        pen_color = (255,255,255)
                        pen_state = 0
                else:
                    for i in colors:
                        if i.clicked(mx,my):
                            pen_color = i.color

            if event.type == pygame.MOUSEBUTTONDOWN:
                if textbox.collidepoint(event.pos):
                    textbox_state = True
                else:
                    textbox_state = False

            if event.type == pygame.KEYDOWN:
                if textbox_state:
                    if event.key == pygame.K_BACKSPACE:
                        file_name = file_name[:-1]
                    else:
                        file_name += event.unicode

        draw_window(grid,colors,choosen_color,file_name,textbox_state)


    pygame.quit()

if __name__ == '__main__':
    main()
