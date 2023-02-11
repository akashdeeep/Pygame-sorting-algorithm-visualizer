import pygame
import random
import math
pygame.init()

class draw_information:
    black = 0,0,0
    white = 255,255,255
    green = 0,255,0
    blue = 0,0,255
    grey = 128,128,128
    red = 255,0,0
    background_color = white
    side_pad = 100
    top_pad = 150
    gradient = [
        grey,
        (160,160,160),
        (192,192,192)
    ]
    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)
    def set_list(self,lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.side_pad)/ len(lst))
        self.block_height = math.floor((self.height - self.top_pad)/(self.max_val - self.min_val))
        self.start_x = self.side_pad // 2

def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.background_color)

    title = draw_info.FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.blue)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.black)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 35))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.black)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 65))


    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions = {}, clear_bg= False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.side_pad//2, draw_info.top_pad, draw_info.width - draw_info.side_pad, draw_info.height - draw_info.top_pad)
        pygame.draw.rect(draw_info.window, draw_info.background_color, clear_rect)
    
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        color = draw_info.gradient[i%3]
        if i in color_positions:
            color= color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()



def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for  i in range(len(lst)-1):
        for j in range(len(lst) -1 -i):
            num1 = lst[j]
            num2 = lst[j+1] 
            if (( num1 > num2 ) and ascending) or ((num1 < num2) and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j:draw_info.green, j+1: draw_info.red}, True)
                yield True
    return lst

def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for i in range(1,len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i -1] > current and ascending
            descending_sort = i>0 and lst[i-1] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i-1]
            i = i-1
            lst[i] = current
            draw_list(draw_info, {i-1: draw_info.green, i: draw_info.red}, True)
            yield True
    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 100
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val,max_val)
    draw_info = draw_information(800,600,lst)
    sorting = False
    ascending = True
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm = bubble_sort
    sorting_algorithm_gen = None

    while run:
        clock.tick(1000)

        if sorting:
            try:
                next(sorting_algorithm_gen)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name, ascending)

        # pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_gen = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and sorting == False:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
            
            


    pygame.quit()

if __name__ == "__main__":
    main()
