import pygame
import monopoly
import sys, os
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
    prop_tile = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    prop_tile.fill(BACKGROUND_COLOR)
    
    
    image = pygame.image.load(prop.image)
    prop_tile.blit(image, (0,2))
    newnames = prop.name.split()
    
    for row, name in enumerate(newnames):
        text = TILETEXT.render(name, True, (0,0,0), BACKGROUND_COLOR)
            
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, TILE_HEIGHT // 4 + (row + 1) * FONTSIZE))

        prop_tile.blit(text, text_rect)
    
    cost = TILETEXT.render("$" + str(prop.price), True, (0,0,0), BACKGROUND_COLOR)
    cost_rect = cost.get_rect(center=(TILE_WIDTH // 2, 7 * TILE_HEIGHT // 8 ))
    prop_tile.blit(cost, cost_rect)
    pygame.draw.rect(prop_tile, color = (0,0,0), rect = (0,0,TILE_WIDTH,TILE_HEIGHT), width = 2)

    return prop_tile


def draw_special_property(prop: Union[monopoly.Utility, monopoly.Railroad]) -> pygame.Surface
    prop_tile = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    prop_tile.fill(BACKGROUND_COLOR)
    
    image = pygame.image.load(prop.image)
    image_rect = image.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 2))
    prop_tile.blit(image, image_rect)

    newnames = prop.name.split()
    
    for row, name in enumerate(newnames):
        text = TILETEXT.render(name, True, (0,0,0), BACKGROUND_COLOR)
            
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, (row + 1) * FONTSIZE))

        prop_tile.blit(text, text_rect)
    
    cost = TILETEXT.render("$" + str(prop.price), True, (0,0,0), BACKGROUND_COLOR)
    cost_rect = cost.get_rect(center=(TILE_WIDTH // 2, 7 * TILE_HEIGHT // 8 ))
    prop_tile.blit(cost, cost_rect)
    pygame.draw.rect(prop_tile, color = (0,0,0), rect = (0,0,TILE_WIDTH,TILE_HEIGHT), width = 2)
    
    
    return prop_tile





def draw_tile(surface: pygame.Surface, tile: monopoly.GameTileType):
    newnames = tile.name.split()

    quad, dist = tile.pos

    if dist == 9:
        
        draw_special(surface, tile)
        return
    
    if quad == 0:
        rect = ((WINDOW + BORDER) - (3 + dist) * TILE_WIDTH, 
                (WINDOW + BORDER) - TILE_HEIGHT, 
                TILE_WIDTH, 
                TILE_HEIGHT)
        
        pygame.draw.rect(surface, color = (100,100,100),rect = rect, width = 1)
        pygame.display.update()
        
        for row, name in enumerate(newnames):
            text = TILETEXT.render(name, True, (0,0,0), BACKGROUND_COLOR)
            text_rect = text.get_rect(center=(((WINDOW + BORDER) - (3 + dist) * TILE_WIDTH + TILE_WIDTH // 2), (WINDOW + BORDER) - (TILE_HEIGHT - (row + 2) * FONTSIZE) ))

            surface.blit(text, text_rect)
        
        pygame.display.update()

        


    if quad == 1:
        rect = (BORDER + (3 + dist) * TILE_WIDTH, 
                BORDER + TILE_HEIGHT, 
                TILE_WIDTH, 
                TILE_HEIGHT)
        
        pygame.draw.rect(surface, color = (0,0,0),rect = rect, width = 3)
        pygame.display.update()
        text = TILETEXT.render(tile.name, True, (0,0,0), BACKGROUND_COLOR)
        surface.blit(text, (50, 50))
        pygame.display.update()



    if quad == 2:
        pass
    

    if quad == 3:
        pass
    

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
s.blit(draw_property(a.prop_dict[1]), (50,50))
pygame.display.update()