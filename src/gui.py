import pygame
import monopoly
import sys, os
from typing import Union
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

pygame.init()

WINDOW: int = 13 * 75
BORDER: int = 50
DISPLAY_HEIGHT: int = WINDOW + 2 * BORDER
DISPLAY_WIDTH: int = WINDOW + 2 * BORDER
TILE_WIDTH = WINDOW // 13 
TILE_HEIGHT = TILE_WIDTH * 2
BACKGROUND_COLOR = (191, 219, 174)

FONTSIZE = TILE_WIDTH // 6
TILETEXT = pygame.font.Font(size = FONTSIZE)


def draw_property(prop: monopoly.Property) -> pygame.Surface:
    tile_image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    tile_image.fill(BACKGROUND_COLOR)
    
    
    image = pygame.image.load(prop.image)
    tile_image.blit(image, (0,2))
    newnames = prop.name.split()
    addname = ""
    for row, name in enumerate(newnames):
        
        if len(name) <= 3:
            addname = name
            continue
        
        name = addname + name
        addname = ""
        text = TILETEXT.render(name, True, (0,0,0), BACKGROUND_COLOR)
        
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, TILE_HEIGHT // 4 + (row + 1) * FONTSIZE))

        tile_image.blit(text, text_rect)
    
    cost = TILETEXT.render("$" + str(prop.price), True, (0,0,0), BACKGROUND_COLOR)
    cost_rect = cost.get_rect(center=(TILE_WIDTH // 2, 7 * TILE_HEIGHT // 8 ))
    tile_image.blit(cost, cost_rect)
    
    
    pygame.draw.line(tile_image, (0,0,0), (0,1),(TILE_WIDTH - 1, 1))

    pygame.draw.rect(tile_image, color = (0,0,0), rect = (0,0,TILE_WIDTH,TILE_HEIGHT), width = 1)

    return tile_image


def draw_special_property(prop: Union[monopoly.Utility, monopoly.Railroad]) -> pygame.Surface:
    tile_image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    tile_image.fill(BACKGROUND_COLOR)
    
    image = pygame.image.load(prop.image)
    
    image = pygame.transform.scale(image, (TILE_WIDTH // 5 * 3, TILE_HEIGHT // 5 * 2))

    image_rect = image.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 2))
    

    tile_image.blit(image, image_rect)

    newnames = prop.name.split()
    
    for row, name in enumerate(newnames):
        text = TILETEXT.render(name, True, (0,0,0), BACKGROUND_COLOR)
            
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, (row + 1) * FONTSIZE))

        tile_image.blit(text, text_rect)
    
    cost = TILETEXT.render("$" + str(prop.price), True, (0,0,0), BACKGROUND_COLOR)
    cost_rect = cost.get_rect(center=(TILE_WIDTH // 2, 7 * TILE_HEIGHT // 8 ))
    tile_image.blit(cost, cost_rect)
    
    pygame.draw.line(tile_image, (0,0,0), (0,1),(TILE_WIDTH - 1, 1))

    pygame.draw.rect(tile_image, color = (0,0,0), rect = (0,0,TILE_WIDTH,TILE_HEIGHT), width = 1)
    
    
    return tile_image

def draw_chance(ch_tile: monopoly.Chance_Tile) -> pygame.Surface:
    
    tile_image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    
    tile_image.fill(BACKGROUND_COLOR)
    
    image = pygame.image.load(ch_tile.image)
    
    image = pygame.transform.scale(image, (TILE_WIDTH // 5 * 2, TILE_HEIGHT // 5 * 2))

    image_rect = image.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 2))
    

    tile_image.blit(image, image_rect)

    newnames = ch_tile.name.split()
    
    for row, name in enumerate(newnames):
        text = TILETEXT.render(name, True, (0,0,0), BACKGROUND_COLOR)
            
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, (row + 1) * FONTSIZE))

        tile_image.blit(text, text_rect)
    
    pygame.draw.rect(tile_image, color = (0,0,0), rect = (0,0,TILE_WIDTH,TILE_HEIGHT), width = 1)
    
    pygame.draw.line(tile_image, (0,0,0), (0,1),(TILE_WIDTH - 1, 1))


    return tile_image

def draw_community(c_tile: monopoly.Community_Chest_Tile) -> pygame.Surface:
    
    tile_image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    
    tile_image.fill(BACKGROUND_COLOR)
    
    image = pygame.image.load(c_tile.image)
    
    image = pygame.transform.scale(image, (TILE_WIDTH - TILE_WIDTH // 8, TILE_HEIGHT // 2))

    image_rect = image.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 2))
    

    tile_image.blit(image, image_rect)

    newnames = c_tile.name.split()
    
    for row, name in enumerate(newnames):
        text = TILETEXT.render(name, True, (0,0,0), BACKGROUND_COLOR)
        
        if row == 0:
            text_rect = text.get_rect(center=(TILE_WIDTH // 2, 2 * (FONTSIZE)))
        if row == 1:
            text_rect = text.get_rect(center=(TILE_WIDTH // 2, (TILE_HEIGHT - 2 * FONTSIZE)))

        tile_image.blit(text, text_rect)
    
    pygame.draw.rect(tile_image, color = (0,0,0), rect = (0,0,TILE_WIDTH,TILE_HEIGHT), width = 1)
    pygame.draw.line(tile_image, (0,0,0), (0,1),(TILE_WIDTH - 1, 1))

    return tile_image

def draw_event(e_tile: monopoly.Event_Tile):
    tile_image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    
    tile_image.fill(BACKGROUND_COLOR)
    
    image = pygame.image.load(e_tile.image)
    
    image = pygame.transform.scale(image, (TILE_WIDTH // 4 * 3, TILE_HEIGHT // 4 * 3))

    image_rect = image.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 2))
    

    tile_image.blit(image, image_rect)

    newnames = e_tile.name.split()
    
    for row, name in enumerate(newnames):
        text = TILETEXT.render(name, True, (0,0,0), BACKGROUND_COLOR)
            
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, (row + 1) * FONTSIZE))


        tile_image.blit(text, text_rect)
    
    pygame.draw.rect(tile_image, color = (0,0,0), rect = (0,0,TILE_WIDTH,TILE_HEIGHT), width = 1)
    pygame.draw.line(tile_image, (0,0,0), (0,1),(TILE_WIDTH - 1, 1))

    return tile_image

def draw_special_event(se_tile: monopoly.Event_Tile) -> pygame.Surface:
    tile_image = pygame.Surface((TILE_HEIGHT, TILE_HEIGHT))
    
    tile_image.fill(BACKGROUND_COLOR)
    
    image = pygame.image.load(e_tile.image)
    
    image = pygame.transform.scale(image, (TILE_HEIGHT, TILE_HEIGHT))

    image_rect = image.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 2))
    

    tile_image.blit(image, image_rect)
    
    pygame.draw.rect(tile_image, color = (0,0,0), rect = (0,0,TILE_WIDTH,TILE_HEIGHT), width = 1)
    pygame.draw.line(tile_image, (0,0,0), (0,1),(TILE_WIDTH - 1, 1))
    
    return tile_image


def draw_tile(surface: pygame.Surface, tile: monopoly.GameTileType) -> None:
    newnames = tile.name.split()

    quad, dist = tile.pos

    if dist == 9:
        return
        drawn = draw_special_event(tile)

    elif isinstance(tile, monopoly.Property):
        drawn = draw_property(tile)
    elif isinstance(tile, monopoly.Railroad) or isinstance(tile, monopoly.Utility):
        drawn = draw_special_property(tile)
    elif isinstance(tile, monopoly.Community_Chest_Tile):
        drawn = draw_community(tile)
    elif isinstance(tile, monopoly.Chance_Tile):
        drawn = draw_chance(tile)
        
    elif isinstance(tile, monopoly.Event_Tile):
        drawn = draw_event(tile)


    if quad == 0:
        surface.blit(drawn, (DISPLAY_WIDTH - BORDER - (3 * TILE_WIDTH + TILE_WIDTH * dist), DISPLAY_HEIGHT - BORDER - TILE_HEIGHT))

    if quad == 1:
        drawn = pygame.transform.rotate(drawn, 270)
        surface.blit(drawn, (BORDER, DISPLAY_HEIGHT - BORDER  - (3 * TILE_WIDTH + dist * TILE_WIDTH)))


    if quad == 2:
        drawn = pygame.transform.rotate(drawn, 180)
        surface.blit(drawn, (BORDER + TILE_WIDTH * 2 + TILE_WIDTH * dist, BORDER))
    

    if quad == 3:
        drawn = pygame.transform.rotate(drawn, 90)
        surface.blit(drawn, (DISPLAY_WIDTH - BORDER - TILE_HEIGHT, BORDER + 2 * TILE_WIDTH + dist * TILE_WIDTH))
        

def play_monopoly(monopoly):

    surface = pygame.display.set_mode((DISPLAY_HEIGHT, DISPLAY_WIDTH))
    surface.fill(BACKGROUND_COLOR)
    pygame.display.update()
    mediterranean_ave = monopoly.prop_dict[1]
    print(mediterranean_ave.name)
    print(mediterranean_ave.pos)

    draw_tile(surface, mediterranean_ave)
    
    pygame.display.update()


a = monopoly.Monopoly(2, 1500)
s = pygame.display.set_mode((DISPLAY_HEIGHT, DISPLAY_WIDTH))
s.fill(BACKGROUND_COLOR)

pygame.display.update()

for row in a.board:
    for tile in row:
        draw_tile(s, tile)

pygame.display.update()

while False:

    for row in a.board:
        for tile in row:
            draw_tile(s, tile)

    pygame.display.update()
