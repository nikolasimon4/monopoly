import pygame
import monopoly
import sys, os
from typing import Union, Tuple
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

pygame.init()
DISPLAY = pygame.display.Info()
DISPLAY_HEIGHT: int = DISPLAY.current_h
DISPLAY_WIDTH: int = DISPLAY.current_w
BORDER: int = 50


print(DISPLAY_HEIGHT)
print(DISPLAY_WIDTH)
TILE_WIDTH = (DISPLAY_HEIGHT - 2 * BORDER) // 13 
TILE_HEIGHT = TILE_WIDTH * 2
BOARD_WINDOW: int = 13 * TILE_WIDTH
BACKGROUND_COLOR = (191, 219, 174)
PROPCARD_Y_PADDING: int = 5
PROPCARD_X_PADDONG: int = 5
PROPCARD_TEXT_SPACING: int = 4

FONTSIZE = TILE_WIDTH // 6 + 2
TILETEXT = pygame.font.Font(size = FONTSIZE)


def draw_property(prop: monopoly.Property) -> pygame.Surface:
    tile_image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    tile_image.fill(BACKGROUND_COLOR)
    
    
    image = pygame.image.load(prop.image)
    
    image = pygame.transform.scale(image, (TILE_WIDTH, TILE_HEIGHT // 4))

    tile_image.blit(image, (0,2))
    newnames = prop.name.split()
    addname = ""
    row = 0
    for name in newnames:
        
        if len(name) <= 3:
            addname = name + " "
            continue
        
        name = addname + name
        addname = ""
        text = TILETEXT.render(name, True, (0,0,0), BACKGROUND_COLOR)
        
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, TILE_HEIGHT // 4 + (row + 1) * FONTSIZE))

        tile_image.blit(text, text_rect)
        row += 1
    
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
    
    image = pygame.image.load(se_tile.image)
    
    image = pygame.transform.scale(image, (TILE_HEIGHT, TILE_HEIGHT))

    image_rect = image.get_rect(center = (TILE_HEIGHT // 2, TILE_HEIGHT // 2))
    

    tile_image.blit(image, image_rect)
    
    pygame.draw.rect(tile_image, color = (0,0,0), rect = (0,0,TILE_HEIGHT,TILE_HEIGHT), width = 1)
    
    return tile_image

def tile_loc(tile: monopoly.GameTileType) -> Tuple[int, int]:
    
    quad, dist = tile.pos
    if dist == 9:
        if quad == 0:
            return(BORDER, BORDER + BOARD_WINDOW - TILE_HEIGHT)
            

        if quad == 1:
            return (BORDER, BORDER)
    
            
        if quad == 2:
            return (BORDER + BOARD_WINDOW - TILE_HEIGHT, BORDER)
        

        if quad == 3:
            return (BORDER + BOARD_WINDOW - TILE_HEIGHT, BORDER + BOARD_WINDOW - TILE_HEIGHT)

    if quad == 0:
        return (BOARD_WINDOW + BORDER - (3 * TILE_WIDTH + TILE_WIDTH * dist), BOARD_WINDOW + BORDER - TILE_HEIGHT)

    if quad == 1:
        return (BORDER, BOARD_WINDOW + BORDER  - (3 * TILE_WIDTH + dist * TILE_WIDTH))


    if quad == 2:
        return (BORDER + TILE_WIDTH * 2 + TILE_WIDTH * dist, BORDER)
    

    if quad == 3:
        return (BOARD_WINDOW + BORDER - TILE_HEIGHT, BORDER + 2 * TILE_WIDTH + dist * TILE_WIDTH)


def draw_tile(surface: pygame.Surface, tile: monopoly.GameTileType) -> None:

    loc = tile_loc(tile)
    
    quad, dist = tile.pos

    if dist == 9:
        drawn = draw_special_event(tile)
        surface.blit(drawn, loc)
        return



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

    if quad == 1:
        drawn = pygame.transform.rotate(drawn, 270)

    if quad == 2:
        drawn = pygame.transform.rotate(drawn, 180)    

    if quad == 3:
        drawn = pygame.transform.rotate(drawn, 90)
    
    surface.blit(drawn, loc)


def draw_property_card(prop: monopoly.Property) -> pygame.Surface:
    

    height = 2 * TILE_HEIGHT
    width = 2 * TILE_WIDTH

    prop_card = pygame.Surface((width, height))
    

    prop_card.fill((255,255,255))
    
    
    image = pygame.image.load(prop.image)
    
    image = pygame.transform.scale(image, (width - 2 * PROPCARD_X_PADDONG, height // 5))

    prop_card.blit(image, (PROPCARD_X_PADDONG,PROPCARD_Y_PADDING))
    
    TILETEXT.set_bold(True)
    
    if 1 <= prop.propnum <= 2 or 22 <= prop.propnum <= 23:
        proptext = (255,255,255)
    else:
        proptext = (0,0,0)
    name_text = TILETEXT.render(prop.name, True, proptext)
    name_rect = name_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING + height // 10))
    prop_card.blit(name_text, name_rect)
    
    TILETEXT.set_bold(False)
    
    
    for row, cost in prop.rents.items():
        if row == prop.houses:
            TILETEXT.set_underline(True)
            TILETEXT.set_bold(True)
            if prop.morgaged:
                TILETEXT.set_strikethrough(True)
        
        if row == 0:
            cost_text = TILETEXT.render("RENT $" + str(cost), True, (0,0,0))
        if 0 < row < 5:
            cost_text = TILETEXT.render(f"With {row} House(s)    ${str(cost)}", True, (0,0,0))
        if row == 5:
            cost_text = TILETEXT.render(f"With HOTEL ${str(cost)}", True, (0,0,0))

        cost_rect = cost_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING 
            + height // 5 + PROPCARD_TEXT_SPACING + FONTSIZE
            + row * (PROPCARD_TEXT_SPACING + FONTSIZE)))
       
        prop_card.blit(cost_text, cost_rect)

        if row == prop.houses:
            TILETEXT.set_underline(False)
            TILETEXT.set_bold(False)
            if prop.morgaged:
                TILETEXT.set_strikethrough(False)


    for i in range(6,9):
        
        if i == 6:
            addin_text = TILETEXT.render(f"Morgage Value ${prop.morgage_price}", True, (0,0,0))
        if i == 7:
            addin_text = TILETEXT.render(f"Houses Cost ${prop.house_price} each", True, (0,0,0))
        if i == 8:
            addin_text = TILETEXT.render(f"Hotels, ${prop.house_price} plus 4 houses", True, (0,0,0))

        addin_rect = addin_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING 
            + height // 5 + PROPCARD_TEXT_SPACING + FONTSIZE
            + i * (PROPCARD_TEXT_SPACING + FONTSIZE)))
        
        prop_card.blit(addin_text, addin_rect)

    if prop.morgaged:
        morgage_text = TILETEXT.render(f"MORGAGED, PAY ${prop.morgage_price + prop.morgage_price // 10}", True, (255, 0, 0))
        
        morgage_rect = morgage_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING 
            + height // 5 + PROPCARD_TEXT_SPACING + FONTSIZE
            + 10 * (PROPCARD_TEXT_SPACING + FONTSIZE)))
        
        prop_card.blit(morgage_text, morgage_rect)

        morgage_text = TILETEXT.render(f"TO UNMORGAGE", True, (255, 0, 0))

        
        morgage_rect = morgage_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING 
            + height // 5 + PROPCARD_TEXT_SPACING + FONTSIZE
            + 11 * (PROPCARD_TEXT_SPACING + FONTSIZE)))
        
        prop_card.blit(morgage_text, morgage_rect)

    pygame.draw.rect(prop_card, color = (0,0,0), rect = (0,0,width,height), width = 2)

    return prop_card


def select_tile(surface: pygame.Surface, prop: Union[monopoly.Property, monopoly.Utility, monopoly.Railroad]):
    prop_card = draw_property_card(prop)
    surface.blit(prop_card, (2 * BORDER + BOARD_WINDOW, BORDER))

    x, y = tile_loc(prop)
    quad, dist = prop.pos
    
    if quad == 0 or quad == 2:
        pygame.draw.rect(surface, color = (255, 255, 0), rect = (x, y, TILE_WIDTH, TILE_HEIGHT), width = 1)
    if quad == 1 or quad == 3:
        pygame.draw.rect(surface, color = (255, 255, 0), rect = (x, y, TILE_HEIGHT, TILE_WIDTH), width = 1)
def de_select_tile(surface: pygame.Surface, prop: Union[monopoly.Property, monopoly.Utility, monopoly.Railroad]):
    
    x, y = tile_loc(prop)
    quad, dist = prop.pos

    cover = pygame.Surface((2 * TILE_WIDTH, 2 * TILE_HEIGHT))
    cover.fill((BACKGROUND_COLOR))
    surface.blit(cover, (2 * BORDER + BOARD_WINDOW, BORDER))
    
    if quad == 0 or quad == 2:
        pygame.draw.rect(surface, color = (0,0, 0), rect = (x, y, TILE_WIDTH, TILE_HEIGHT), width = 1)
    if quad == 1 or quad == 3:
        pygame.draw.rect(surface, color = (0,0, 0), rect = (x, y, TILE_HEIGHT, TILE_WIDTH), width = 1)



def play_monopoly(monopoly):

    surface = pygame.display.set_mode((200000, DISPLAY_HEIGHT))
    surface.fill(BACKGROUND_COLOR)
    pygame.display.update()
    mediterranean_ave = monopoly.prop_dict[1]
    print(mediterranean_ave.name)
    print(mediterranean_ave.pos)

    draw_tile(surface, mediterranean_ave)
    
    pygame.display.update()

def start_display():
    s = pygame.display.set_mode()
    s.fill(BACKGROUND_COLOR)
    pygame.display.update()


def draw_board(monopoly: monopoly.Monopoly):
    surface = pygame.display.get_surface()
    for row in monopoly.board:
        for tile in row:
            draw_tile(surface, tile)
    
    select_tile(surface, monopoly.prop_dict[5])
    pygame.display.update()

