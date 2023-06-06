import pygame
import monopoly
import sys, os
from typing import Union, Tuple, Callable, List, Set
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"



BUYABLE_TILE = Union[monopoly.Property, monopoly.Utility, monopoly.Railroad]
RGBTYPE = Tuple[int, int, int]

pygame.init()
DISPLAY = pygame.display.Info()
DISPLAY_HEIGHT: int = DISPLAY.current_h
DISPLAY_WIDTH: int = DISPLAY.current_w
BORDER: int = 50

TILE_WIDTH = (DISPLAY_HEIGHT - 2 * BORDER) // 13 
TILE_HEIGHT = TILE_WIDTH * 2
BOARD_WINDOW = 13 * TILE_WIDTH

BACKGROUND_COLOR: RGBTYPE = (191, 219, 174)
HOUSECOLOR: RGBTYPE = (0,255,0)
HOTELCOLOR: RGBTYPE = (255, 0, 0)
TEXT_COLOR: RGBTYPE = (0, 0, 0)
BUTTON_TEXT_COLOR: RGBTYPE = (0, 0, 0)
MORGAGE_WARNING_COLOR: RGBTYPE = (255, 0, 0)
PROPERTY_CARD_COLOR: RGBTYPE = (255, 255, 255)
LINE_BORDER_COLOR: RGBTYPE = (0, 0, 0)
HIGHLIGHT_COLOR: RGBTYPE = (255, 255, 0)
ACTIVE_BUTTON_BACKGROUND: RGBTYPE =  (170, 255, 190)
INACTIVE_BUTTON_BACKGROUND: RGBTYPE =  (120, 120, 120)

PROPCARD_Y_PADDING: int = 5
PROPCARD_X_PADDING: int = 5
PROPCARD_TEXT_SPACING: int = 4
PROPCARD_XPOS = 2 * BORDER + BOARD_WINDOW
PROPCARD_YPOS = 2 * BORDER
PROPCARD_POS = (PROPCARD_XPOS, PROPCARD_YPOS)
PROPCARD_HEIGHT = 2 * TILE_HEIGHT
PROPCARD_WIDTH = 2 * TILE_WIDTH

HOUSE_SPACING: int = 2

BUTTON_HEIGHT = TILE_WIDTH // 2
BUTTON_FONTSIZE = TILE_WIDTH // 3 - 1
BUTTON_FONT = pygame.font.Font(None, size = BUTTON_FONTSIZE)
BUTTON_PADDING = 5
BUTTON_WIDTH = PROPCARD_WIDTH - 2 * BUTTON_PADDING
SMALL_BUTTON_WIDTH = (BUTTON_WIDTH - BUTTON_PADDING) // 2
SMALLBUTTON_FONT = pygame.font.Font(None, size = round(BUTTON_FONTSIZE * .7)) 
FONTSIZE = TILE_WIDTH // 6 + 2
TILETEXT = pygame.font.Font(None, size = FONTSIZE)
LABELFONTSIZE = TILE_WIDTH // 2
LABELFONT = pygame.font.Font(None, size = LABELFONTSIZE)



DICE_IMAGES = {
    1: "images/dice1.png",
    2: "images/dice2.png",
    3: "images/dice3.png",
    4: "images/dice4.png",
    5: "images/dice5.png",
    6: "images/dice6.png"
}

PLAYER_PIECES = {
    1: "images/RACECAR.png",
    2: "images/DOG.png"

}



def empty_tile() -> pygame.Surface:
    
    tile_image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    tile_image.fill(BACKGROUND_COLOR)
    

    
    return tile_image

def tile_finish(tile_image: pygame.Surface):
    
    pygame.draw.line(tile_image, LINE_BORDER_COLOR, (0,1),(TILE_WIDTH - 1, 1))
    
    pygame.draw.line(tile_image, LINE_BORDER_COLOR, (0, TILE_HEIGHT - 2),(TILE_WIDTH, TILE_HEIGHT - 2))

    pygame.draw.rect(tile_image, color = LINE_BORDER_COLOR, rect = (0,0,TILE_WIDTH,TILE_HEIGHT), width = 1)

def draw_house() -> pygame.Surface:
    house_img = pygame.Surface((TILE_WIDTH // 5, TILE_HEIGHT // 10))
    house_img.fill(HOUSECOLOR)
    return house_img

def draw_hotel() -> pygame.Surface:
    hotel_img = pygame.Surface((2 * (TILE_HEIGHT // 5), TILE_HEIGHT // 5))
    hotel_img.fill(HOTELCOLOR)
    return hotel_img

def draw_property_tile(prop: monopoly.Property) -> pygame.Surface:
    tile_image = empty_tile()
    
    
    image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT // 4))
    image.fill(prop.color)

    tile_image.blit(image, (0,2))
    
    if 1 <= prop.houses <= 4:
        houserow = pygame.Surface(((TILE_WIDTH // 5 + HOUSE_SPACING) * prop.houses, TILE_HEIGHT // 10))
        
        for house in range(prop.houses):
            houserow.blit(draw_house(), (house * (TILE_WIDTH // 5 + HOUSE_SPACING) + HOUSE_SPACING, 0))
    
        tile_image.blit(houserow, houserow.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 8)))
    if prop.houses == 5:
        hotel = draw_hotel()
        tile_image.blit(hotel, hotel.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 8)))


    
    
    newnames = prop.name.split()
    addname = ""
    row = 0
    
    for name in newnames:
        
        if len(name) <= 3:
            addname = name + " "
            continue
        
        name = addname + name
        addname = ""
        text = TILETEXT.render(name, True, TEXT_COLOR, BACKGROUND_COLOR)
        
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, TILE_HEIGHT // 4 + (row + 1) * FONTSIZE))

        tile_image.blit(text, text_rect)
        row += 1
    
    cost = TILETEXT.render("$" + str(prop.price), True, TEXT_COLOR, BACKGROUND_COLOR)
    cost_rect = cost.get_rect(center=(TILE_WIDTH // 2, 7 * TILE_HEIGHT // 8 ))
    tile_image.blit(cost, cost_rect)

    tile_finish(tile_image)
    
    return tile_image

def draw_special_property_tile(prop: Union[monopoly.Utility, monopoly.Railroad]) -> pygame.Surface:
    tile_image = empty_tile()

    
    image = pygame.image.load(prop.image)
    
    image = pygame.transform.scale(image, (TILE_WIDTH // 5 * 3, TILE_HEIGHT // 5 * 2))

    image_rect = image.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 2))
    

    tile_image.blit(image, image_rect)

    newnames = prop.name.split()
    
    for row, name in enumerate(newnames):
        text = TILETEXT.render(name, True, TEXT_COLOR, BACKGROUND_COLOR)
            
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, (row + 1) * FONTSIZE))

        tile_image.blit(text, text_rect)
    
    cost = TILETEXT.render("$" + str(prop.price), True, TEXT_COLOR, BACKGROUND_COLOR)
    cost_rect = cost.get_rect(center=(TILE_WIDTH // 2, 7 * TILE_HEIGHT // 8 ))
    tile_image.blit(cost, cost_rect)

    tile_finish(tile_image)
    
    return tile_image

def draw_chance_tile(ch_tile: monopoly.Chance_Tile) -> pygame.Surface:
    
    tile_image = empty_tile()
    
    image = pygame.image.load(ch_tile.image)
    
    image = pygame.transform.scale(image, (TILE_WIDTH // 5 * 2, TILE_HEIGHT // 5 * 2))

    image_rect = image.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 2))
    

    tile_image.blit(image, image_rect)

    newnames = ch_tile.name.split()
    
    for row, name in enumerate(newnames):
        text = TILETEXT.render(name, True, TEXT_COLOR, BACKGROUND_COLOR)
            
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, (row + 1) * FONTSIZE))

        tile_image.blit(text, text_rect)
    
    tile_finish(tile_image)
    return tile_image

def draw_community_tile(c_tile: monopoly.Community_Chest_Tile) -> pygame.Surface:
    
    tile_image = empty_tile()
    
    image = pygame.image.load(c_tile.image)
    
    image = pygame.transform.scale(image, (TILE_WIDTH - TILE_WIDTH // 8, TILE_HEIGHT // 2))

    image_rect = image.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 2))
    

    tile_image.blit(image, image_rect)

    newnames = c_tile.name.split()
    
    for row, name in enumerate(newnames):
        text = TILETEXT.render(name, True, TEXT_COLOR, BACKGROUND_COLOR)
        
        if row == 0:
            text_rect = text.get_rect(center=(TILE_WIDTH // 2, 2 * (FONTSIZE)))
        if row == 1:
            text_rect = text.get_rect(center=(TILE_WIDTH // 2, (TILE_HEIGHT - 2 * FONTSIZE)))

        tile_image.blit(text, text_rect)

    tile_finish(tile_image)
    
    return tile_image

def draw_event_tile(e_tile: monopoly.Event_Tile):
    tile_image = empty_tile()
    
    
    image = pygame.image.load(e_tile.image)
    
    image = pygame.transform.scale(image, (TILE_WIDTH // 4 * 3, TILE_HEIGHT // 4 * 3))

    image_rect = image.get_rect(center = (TILE_WIDTH // 2, TILE_HEIGHT // 2))
    

    tile_image.blit(image, image_rect)

    newnames = e_tile.name.split()
    
    for row, name in enumerate(newnames):
        text = TILETEXT.render(name, True, TEXT_COLOR, BACKGROUND_COLOR)
            
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, (row + 1) * FONTSIZE))


        tile_image.blit(text, text_rect)

    tile_finish(tile_image)
    
    return tile_image

def draw_corner_tile(se_tile: monopoly.Event_Tile) -> pygame.Surface:
    tile_image = pygame.Surface((TILE_HEIGHT, TILE_HEIGHT))
    
    tile_image.fill(BACKGROUND_COLOR)
    
    image = pygame.image.load(se_tile.image)
    
    image = pygame.transform.scale(image, (TILE_HEIGHT, TILE_HEIGHT))

    image_rect = image.get_rect(center = (TILE_HEIGHT // 2, TILE_HEIGHT // 2))
    

    tile_image.blit(image, image_rect)
    
    pygame.draw.rect(tile_image, color = LINE_BORDER_COLOR, rect = (0,0,TILE_HEIGHT,TILE_HEIGHT), width = 1)
    
    pygame.draw.line(tile_image, LINE_BORDER_COLOR, (0, TILE_HEIGHT - 2),(TILE_HEIGHT, TILE_HEIGHT - 2))
    pygame.draw.line(tile_image, LINE_BORDER_COLOR, (TILE_HEIGHT - 2, 0),(TILE_HEIGHT - 2, TILE_HEIGHT))


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
    
    else:
        raise ValueError("Something is wrong")
        return

def draw_tile_onto_display(surface: pygame.Surface, tile: monopoly.GameTileType) -> None:

    loc = tile_loc(tile)
    
    quad, dist = tile.pos

    if dist == 9:
        assert isinstance(tile, monopoly.Event_Tile)
        drawn = draw_corner_tile(tile)
        quad = (quad + 1) % 4 #Change for rots bcs rot deps on rot of pngs

    elif isinstance(tile, monopoly.Property):
        drawn = draw_property_tile(tile)
    elif isinstance(tile, monopoly.Railroad) or isinstance(tile, monopoly.Utility):
        drawn = draw_special_property_tile(tile)
    elif isinstance(tile, monopoly.Community_Chest_Tile):
        drawn = draw_community_tile(tile)
    elif isinstance(tile, monopoly.Chance_Tile):
        drawn = draw_chance_tile(tile)
        
    elif isinstance(tile, monopoly.Event_Tile):
        drawn = draw_event_tile(tile)

    if quad == 1:
        drawn = pygame.transform.rotate(drawn, 270)

    if quad == 2:
        drawn = pygame.transform.rotate(drawn, 180)    

    if quad == 3:
        drawn = pygame.transform.rotate(drawn, 90)
    
    surface.blit(drawn, loc)

def draw_utility_card(prop: monopoly.Utility) -> pygame.Surface:
    
    small_text = pygame.font.Font(None, size = FONTSIZE - FONTSIZE // 6)
    small_spacing = PROPCARD_TEXT_SPACING // 2
    
    height = PROPCARD_HEIGHT
    width = PROPCARD_WIDTH

    prop_card = pygame.Surface((width, height))
    prop_card.fill(PROPERTY_CARD_COLOR)

    image = pygame.image.load(prop.image)
    
    image = pygame.transform.scale(image, ((width - 2 * PROPCARD_X_PADDING) // 3, height // 3))
    
    prop_card.blit(image, (image.get_rect(center = (width // 2, PROPCARD_Y_PADDING + height // 6))))

    line_width = 2

    pygame.draw.line(prop_card, LINE_BORDER_COLOR, (PROPCARD_X_PADDING,height // 3 + PROPCARD_TEXT_SPACING), 
        (width - PROPCARD_X_PADDING, height // 3 + PROPCARD_TEXT_SPACING), 
        width = line_width)
    
    TILETEXT.set_bold(True)
    

    proptext = TEXT_COLOR
    
    name_text = TILETEXT.render(prop.name, True, proptext)
    
    name_rect = name_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING 
        + height // 3 + PROPCARD_TEXT_SPACING 
        + line_width + PROPCARD_TEXT_SPACING 
        + FONTSIZE // 2))
    
    prop_card.blit(name_text, name_rect)
    
    TILETEXT.set_bold(False)


    pygame.draw.line(prop_card, LINE_BORDER_COLOR, (PROPCARD_X_PADDING, PROPCARD_Y_PADDING 
        + height // 3 + PROPCARD_TEXT_SPACING + line_width 
        + PROPCARD_TEXT_SPACING + FONTSIZE + PROPCARD_TEXT_SPACING),
        (width - PROPCARD_X_PADDING, PROPCARD_Y_PADDING 
        + height // 3 + PROPCARD_TEXT_SPACING + line_width 
        + PROPCARD_TEXT_SPACING + FONTSIZE + PROPCARD_TEXT_SPACING),
        width = line_width)
    

    for row in range(1,9):
        
        if row == 1:
            text = small_text.render('   If one "Utility" is owned', True, TEXT_COLOR)
        if row == 2:
            text = small_text.render('rent is 4 times the amount shown', True, TEXT_COLOR)
        if row == 3:
            text = small_text.render('on dice', True, TEXT_COLOR)
        if row == 4:
            text = small_text.render('   If both "Utilities" are owned', True, TEXT_COLOR)
        if row == 5:
            text = small_text.render('rent is 10 times the amount shown', True, TEXT_COLOR)
        if row == 6:
            text = small_text.render('on dice', True, TEXT_COLOR)
        if row == 7:
            text = small_text.render(f'Morgage Value:       ${prop.morgage_price}', True, TEXT_COLOR)
        if row == 8:
            text = small_text.render(f'              Owner: {str(prop.owner)}', True, TEXT_COLOR)
        
        prop_card.blit(text, (PROPCARD_X_PADDING, PROPCARD_Y_PADDING 
            + height // 3 + PROPCARD_TEXT_SPACING + line_width 
            + PROPCARD_TEXT_SPACING + FONTSIZE + PROPCARD_TEXT_SPACING + line_width + 
            (small_spacing + FONTSIZE) * row))
    
    if prop.morgaged:
        morgage_text = small_text.render(f"MORGAGED, PAY ${prop.morgage_price + prop.morgage_price // 10}", True, MORGAGE_WARNING_COLOR)
        
        rect = morgage_text.get_rect(center = (PROPCARD_WIDTH // 2, PROPCARD_Y_PADDING 
            + height // 3 + PROPCARD_TEXT_SPACING + line_width 
            + PROPCARD_TEXT_SPACING + FONTSIZE + PROPCARD_TEXT_SPACING + line_width + 
            (small_spacing + FONTSIZE) * 9))
        
        prop_card.blit(morgage_text, rect)

        morgage_text = small_text.render(f"TO UNMORGAGE", True, MORGAGE_WARNING_COLOR)
        
        rect = morgage_text.get_rect(center = (PROPCARD_WIDTH // 2, PROPCARD_Y_PADDING 
            + height // 3 + PROPCARD_TEXT_SPACING + line_width 
            + PROPCARD_TEXT_SPACING + FONTSIZE + line_width + 
            (small_spacing + FONTSIZE) * 10))
        
        prop_card.blit(morgage_text, rect)

    pygame.draw.rect(prop_card, color = LINE_BORDER_COLOR, rect = (0,0,width,height), width = 2)

    return prop_card

def draw_railroad_card(prop: monopoly.Railroad) -> pygame.Surface:
    
    small_text = pygame.font.Font(None, size = FONTSIZE)

    height = PROPCARD_HEIGHT
    width = PROPCARD_WIDTH

    prop_card = pygame.Surface((width, height))
    prop_card.fill(PROPERTY_CARD_COLOR)

    image = pygame.image.load(prop.image)
    
    image = pygame.transform.scale(image, ((width - 2 * PROPCARD_X_PADDING) // 3, height // 3))
    
    prop_card.blit(image, (image.get_rect(center = (width // 2, PROPCARD_Y_PADDING + height // 6))))

    line_width = 2

    pygame.draw.line(prop_card, LINE_BORDER_COLOR, (PROPCARD_X_PADDING,height // 3 + PROPCARD_TEXT_SPACING), 
        (width - PROPCARD_X_PADDING, height // 3 + PROPCARD_TEXT_SPACING), 
        width = line_width)
    
    TILETEXT.set_bold(True)
    

    proptext = TEXT_COLOR
    
    name_text = TILETEXT.render(prop.name, True, proptext)
    
    name_rect = name_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING 
        + height // 3 + PROPCARD_TEXT_SPACING 
        + line_width + PROPCARD_TEXT_SPACING 
        + FONTSIZE // 2))
    
    prop_card.blit(name_text, name_rect)
    
    TILETEXT.set_bold(False)


    pygame.draw.line(prop_card, LINE_BORDER_COLOR, (PROPCARD_X_PADDING, PROPCARD_Y_PADDING 
        + height // 3 + PROPCARD_TEXT_SPACING + line_width 
        + PROPCARD_TEXT_SPACING + FONTSIZE + PROPCARD_TEXT_SPACING),
        (width - PROPCARD_X_PADDING, PROPCARD_Y_PADDING 
        + height // 3 + PROPCARD_TEXT_SPACING + line_width 
        + PROPCARD_TEXT_SPACING + FONTSIZE + PROPCARD_TEXT_SPACING),
        width = line_width)
    

    for row in range(1,7):
        
        if row == 1:
            text = small_text.render(f'Rent                                 ${prop.rents[row]}', True, TEXT_COLOR)
        if row == 2:
            text = small_text.render(f"If 2 R.R.'s are owned     {prop.rents[row]}", True, TEXT_COLOR)
        if row == 3:
            text = small_text.render(f'If 3    "     "     "                {prop.rents[row]}', True, TEXT_COLOR)
        if row == 4:
            text = small_text.render(f'If 4    "     "     "                {prop.rents[row]}', True, TEXT_COLOR)
        if row == 5:
            text = small_text.render(f'Morgage Value                ${prop.morgage_price}', True, TEXT_COLOR)
        if row == 6:
            text = small_text.render(f'Owner: {str(prop.owner)}', True, TEXT_COLOR)
        
        prop_card.blit(text, (PROPCARD_X_PADDING, PROPCARD_Y_PADDING 
            + height // 3 + PROPCARD_TEXT_SPACING + line_width 
            + PROPCARD_TEXT_SPACING + FONTSIZE + PROPCARD_TEXT_SPACING + line_width + 
            (2 * PROPCARD_TEXT_SPACING + FONTSIZE) * row))

        if prop.morgaged:
            
            morgage_text = TILETEXT.render(f"MORGAGED, PAY ${prop.morgage_price + prop.morgage_price // 10}", True, MORGAGE_WARNING_COLOR)
            
            
            prop_card.blit(morgage_text,  (PROPCARD_X_PADDING, PROPCARD_Y_PADDING 
                + height // 3 + PROPCARD_TEXT_SPACING 
                + PROPCARD_TEXT_SPACING + FONTSIZE + line_width + 
                (2 * PROPCARD_TEXT_SPACING + FONTSIZE) * 7))

            morgage_text = TILETEXT.render(f"TO UNMORGAGE", True, MORGAGE_WARNING_COLOR)

            prop_card.blit(morgage_text,   (PROPCARD_X_PADDING, PROPCARD_Y_PADDING 
                + height // 3 
                + FONTSIZE + line_width + 
                (2 * PROPCARD_TEXT_SPACING + FONTSIZE) * 8 - PROPCARD_TEXT_SPACING))

        pygame.draw.rect(prop_card, color = LINE_BORDER_COLOR, rect = (0,0,width,height), width = 2)


    return prop_card

def draw_property_card(prop: monopoly.Property) -> pygame.Surface:
    

    height = PROPCARD_HEIGHT
    width = PROPCARD_WIDTH

    prop_card = pygame.Surface((width, height))
    

    prop_card.fill(PROPERTY_CARD_COLOR)
    
    
    image = pygame.image.load(prop.image)
    
    image = pygame.transform.scale(image, (width - 2 * PROPCARD_X_PADDING, height // 5))

    prop_card.blit(image, (PROPCARD_X_PADDING,PROPCARD_Y_PADDING))
    
    SMALLBUTTON_FONT.set_bold(True)
    
    if 1 <= prop.propnum <= 2 or 21 <= prop.propnum <= 22:
        proptext = (255,255,255)
    else:
        proptext = TEXT_COLOR
    name_text = SMALLBUTTON_FONT.render(prop.name, True, proptext)
    name_rect = name_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING + height // 10))
    prop_card.blit(name_text, name_rect)
    
    SMALLBUTTON_FONT.set_bold(False)
    
    
    for row, cost in prop.rents.items():
        if row == prop.houses:
            TILETEXT.set_underline(True)
            TILETEXT.set_bold(True)
            if prop.morgaged:
                TILETEXT.set_strikethrough(True)
        
        if row == 0:
            cost_text = TILETEXT.render("RENT $" + str(cost), True, TEXT_COLOR)
        if 0 < row < 5:
            cost_text = TILETEXT.render(f"With {row} House(s)    ${str(cost)}", True, TEXT_COLOR)
        if row == 5:
            cost_text = TILETEXT.render(f"With HOTEL ${str(cost)}", True, TEXT_COLOR)

        cost_rect = cost_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING 
            + height // 5 + PROPCARD_TEXT_SPACING + FONTSIZE
            + row * (PROPCARD_TEXT_SPACING + FONTSIZE)))
       
        prop_card.blit(cost_text, cost_rect)

        if row == prop.houses:
            TILETEXT.set_underline(False)
            TILETEXT.set_bold(False)
            if prop.morgaged:
                TILETEXT.set_strikethrough(False)


    for i in range(6,10):
        
        if i == 6:
            addin_text = TILETEXT.render(f"Morgage Value ${prop.morgage_price}", True, TEXT_COLOR)
        if i == 7:
            addin_text = TILETEXT.render(f"Houses Cost ${prop.house_price} each", True, TEXT_COLOR)
        if i == 8:
            addin_text = TILETEXT.render(f"Hotels, ${prop.house_price} plus 4 houses", True, TEXT_COLOR)

        if i == 9:
            addin_text = TILETEXT.render(f"Owner: {str(prop.owner)}", True, TEXT_COLOR)
        
        addin_rect = addin_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING 
            + height // 5 + PROPCARD_TEXT_SPACING + FONTSIZE
            + i * (PROPCARD_TEXT_SPACING + FONTSIZE)))
        
        prop_card.blit(addin_text, addin_rect)

    if prop.morgaged:
        morgage_text = TILETEXT.render(f"MORGAGED, PAY ${prop.morgage_price + prop.morgage_price // 10}", True, MORGAGE_WARNING_COLOR)
        
        morgage_rect = morgage_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING 
            + height // 5 + PROPCARD_TEXT_SPACING + FONTSIZE
            + 10 * (PROPCARD_TEXT_SPACING + FONTSIZE)))
        
        prop_card.blit(morgage_text, morgage_rect)

        morgage_text = TILETEXT.render(f"TO UNMORGAGE", True, MORGAGE_WARNING_COLOR)

        
        morgage_rect = morgage_text.get_rect(center = (width // 2, PROPCARD_Y_PADDING 
            + height // 5 + PROPCARD_TEXT_SPACING + FONTSIZE
            + 11 * (PROPCARD_TEXT_SPACING + FONTSIZE)))
        
        prop_card.blit(morgage_text, morgage_rect)

    pygame.draw.rect(prop_card, color = LINE_BORDER_COLOR, rect = (0,0,width,height), width = 2)

    return prop_card

def select_tile(surface: pygame.Surface, prop: Union[monopoly.Property, monopoly.Utility, monopoly.Railroad]):
    if isinstance(prop, monopoly.Property):
        prop_card = draw_property_card(prop)
    if isinstance(prop, monopoly.Utility):
        prop_card = draw_utility_card(prop)
    if isinstance(prop, monopoly.Railroad):
        prop_card = draw_railroad_card(prop)
    
    surface.blit(prop_card, PROPCARD_POS)

    x, y = tile_loc(prop)
    quad, dist = prop.pos
    
    if quad == 0 or quad == 2:
        pygame.draw.rect(surface, color = HIGHLIGHT_COLOR, rect = (x, y, TILE_WIDTH, TILE_HEIGHT), width = 1)
    if quad == 1 or quad == 3:
        pygame.draw.rect(surface, color = HIGHLIGHT_COLOR, rect = (x, y, TILE_HEIGHT, TILE_WIDTH), width = 1)

def de_select_tile(surface: pygame.Surface, prop: Union[monopoly.Property, monopoly.Utility, monopoly.Railroad]):
    
    x, y = tile_loc(prop)
    quad, dist = prop.pos

    cover = pygame.Surface((PROPCARD_WIDTH, PROPCARD_HEIGHT))
    cover.fill((BACKGROUND_COLOR))
    surface.blit(cover, PROPCARD_POS)
    
    if quad == 0 or quad == 2:
        pygame.draw.rect(surface, color = LINE_BORDER_COLOR, rect = (x, y, TILE_WIDTH, TILE_HEIGHT), width = 1)
    if quad == 1 or quad == 3:
        pygame.draw.rect(surface, color = LINE_BORDER_COLOR, rect = (x, y, TILE_HEIGHT, TILE_WIDTH), width = 1)

def draw_button_on_display(surface: pygame.Surface, button: "Button", game: monopoly.Monopoly, prop: monopoly.GameTileType):
    if button.active(game, prop):
        surface.blit(button.active_image, button.pos)
    else:
        surface.blit(button.inactive_image, button.pos)

def draw_buttons_onto_display(surface: pygame.Surface, buttons: Set["Button"], game: monopoly.Monopoly, prop: monopoly.GameTileType):
    for button in buttons:
        draw_button_on_display(surface, button, game, prop)


def draw_dice(surface: pygame.Surface, game: monopoly.Monopoly):
    d1img = pygame.image.load(DICE_IMAGES[game.d1])
    d2img = pygame.image.load(DICE_IMAGES[game.d2])
    
    d1img = pygame.transform.scale(d1img, (SMALL_BUTTON_WIDTH, 2 * BUTTON_HEIGHT))
    d2img = pygame.transform.scale(d2img, (SMALL_BUTTON_WIDTH, 2 * BUTTON_HEIGHT))

    d1img_rect = d1img.get_rect(topleft = (PROPCARD_XPOS, DISPLAY_HEIGHT - BORDER - TILE_WIDTH + BUTTON_PADDING))
    d2img_rect = d2img.get_rect(topleft = (PROPCARD_XPOS + BUTTON_PADDING + SMALL_BUTTON_WIDTH, DISPLAY_HEIGHT - BORDER - TILE_WIDTH + BUTTON_PADDING))

    surface.blit(d1img, d1img_rect)
    surface.blit(d2img, d2img_rect)

def draw_pieces(surface: pygame.Surface, game: monopoly.Monopoly):

    pcount = {}

    for pnum in range(1, game.num_players + 1):
        quad, dist = game.ploc[pnum]
        if quad in pcount:
            if dist in pcount[quad]:
                pcount[quad][dist].append(pnum)
            else:
                pcount[quad][dist] = [pnum]
        else:
            pcount[quad] = {}
            pcount[quad][dist] = [pnum]
    
    for quad, distdict in pcount.items():
        for dist, plist in distdict.items():
            draw_player_piece(surface, game, plist, (quad, dist))

def draw_player_piece(surface: pygame.Surface, game: monopoly.Monopoly, plist: List[int], loc: Tuple[int, int]):


    num_same_loc = len(plist)
    pquad, pdist = loc
    tilex, tiley = tile_loc(game.board[pquad][pdist])

    row = 0
    
    for pnum in plist:

        image_load = pygame.image.load(PLAYER_PIECES[pnum])
        tile_image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
        image_load = pygame.transform.scale(image_load, (TILE_WIDTH // num_same_loc, TILE_HEIGHT // num_same_loc))


        tile_image.blit(image_load, (row * (TILE_WIDTH // num_same_loc), TILE_HEIGHT - (TILE_HEIGHT // num_same_loc)))

        if pdist == 9:
            pass
        
        if pquad == 0: 
            pass
        if pquad == 1:
            tile_image = pygame.transform.rotate(tile_image, 90)
            tile_image = pygame.transform.flip(tile_image, True, True)
        if pquad == 2:
            tile_image = pygame.transform.rotate(image_load, 180)
        if pquad == 3:
            tile_image = pygame.transform.rotate(tile_image, 270)
            tile_image = pygame.transform.flip(tile_image, True, True)

        surface.blit(tile_image, (tilex, tiley))
        row += 1 

    
    
    
    
    



def print_error_message(surface: pygame.Surface, emessage: str):
    error_words = emessage.split()
    
    error_line = ""
    
    error_img = pygame.Surface((PROPCARD_WIDTH, PROPCARD_WIDTH))
    error_img.fill(BACKGROUND_COLOR)
    row = 0

    for word in error_words:
        error_line += " " + word
        if len(error_line) >= 20:
            errortxt = TILETEXT.render(error_line, True, MORGAGE_WARNING_COLOR)
            errortxtrect = errortxt.get_rect(center = (PROPCARD_WIDTH // 2, (row + 1) * (FONTSIZE + PROPCARD_TEXT_SPACING)))
            error_img.blit(errortxt, errortxtrect)
            error_line = ""
            row += 1
    if len(error_line) > 0:
        errortxt = TILETEXT.render(error_line, True, MORGAGE_WARNING_COLOR)
        errortxtrect = errortxt.get_rect(center = (PROPCARD_WIDTH // 2, (row + 1) * (FONTSIZE + PROPCARD_TEXT_SPACING)))
        error_img.blit(errortxt, errortxtrect)
    
    surface.blit(error_img, (PROPCARD_XPOS, BORDER + BOARD_WINDOW // 2 + BUTTON_PADDING))


def locate_tile(game: monopoly.Monopoly, loc: Tuple[int, int], quadrant: int) -> monopoly.GameTileType:
    x, y = loc

    if quadrant == 0:
        xboard = BORDER + BOARD_WINDOW - TILE_HEIGHT - x
        tile = xboard // TILE_WIDTH
        if tile == 10:
            tile = 9
        return game.board[0][tile]
    
    if quadrant == 1:
        yboard = BORDER + BOARD_WINDOW - y - TILE_HEIGHT
        
        tile = yboard // TILE_WIDTH
        if tile == 10:
            tile = 9
        return game.board[1][tile]
    if quadrant == 2:
        tile = (x - BORDER - TILE_HEIGHT) // TILE_WIDTH
        if tile == 10:
            tile = 9
        return game.board[2][tile]    
    if quadrant == 3:
        tile = (y - BORDER - TILE_HEIGHT) // TILE_WIDTH
        if tile == 10:
            tile = 9
        return game.board[3][tile]

def play_monopoly(game: monopoly.Monopoly):
    start_display()
    draw_board(game)
    surface = pygame.display.get_surface()

    done = False
    clock = pygame.time.Clock()
    pygame.display.update()
    
    active_buttons = []

    selected_tile = game.prop_dict[1]
    
    active_buttons = {PLUS_ONE_HOUSE, MINUS_ONE_HOUSE, MORGAGE_PROPERTY, BUY_PROPERTY, START_AUCTION,ROLL_DICE}


    while not done:

        if selected_tile.morgaged:
            active_buttons.discard(MORGAGE_PROPERTY)
            active_buttons.add(UNMORGAGE_PROPERTY)
        if not selected_tile.morgaged:
            active_buttons.add(MORGAGE_PROPERTY)
            active_buttons.discard(UNMORGAGE_PROPERTY)
        if game.turn_taken:
            active_buttons.discard(ROLL_DICE)
            active_buttons.add(END_TURN)
        if not game.turn_taken:
            active_buttons.add(ROLL_DICE)
            active_buttons.discard(END_TURN)
        
        draw_buttons_onto_display(surface, active_buttons, game, selected_tile)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                
                mouse_x, mouse_y = pygame.mouse.get_pos()
                poss_tile = None

                for button in active_buttons:
                    if button.in_button((mouse_x, mouse_y)):
                        try:
                            affected_tiles = button.apply_effect(game, selected_tile)
                            
                            if button.effect is take_turn_effect:

                                poss_tile = game.current_tile()

                            for tile in affected_tiles:
                                draw_tile_onto_display(surface, tile)
                            

                        except AssertionError as emessage:
                            print_error_message(surface, str(emessage))

                # Check if in quadrant 0 
                if ((BORDER < mouse_x < BORDER + BOARD_WINDOW - TILE_HEIGHT) and (DISPLAY_HEIGHT - BORDER - TILE_HEIGHT < mouse_y < DISPLAY_HEIGHT - BORDER)):
                    poss_tile = locate_tile(game, (mouse_x, mouse_y), 0)
                    
                
                # Check if in quadrant 1
                if ((BORDER < mouse_x < BORDER + TILE_HEIGHT) and (BORDER < mouse_y < BORDER + BOARD_WINDOW - TILE_HEIGHT)):
                    poss_tile = locate_tile(game, (mouse_x, mouse_y), 1)
                
                # Check if in quadrant 2

                if ((BORDER + TILE_HEIGHT < mouse_x < BORDER + BOARD_WINDOW) and (BORDER < mouse_y < BORDER + TILE_HEIGHT)):
                    poss_tile = locate_tile(game, (mouse_x, mouse_y), 2)


                
                # Check if in quadrant 3
                if ((BORDER + BOARD_WINDOW - TILE_HEIGHT < mouse_x < BORDER + BOARD_WINDOW) and (BORDER + TILE_HEIGHT < mouse_y < BORDER + BOARD_WINDOW)):
                    poss_tile = locate_tile(game, (mouse_x, mouse_y), 3)

                if poss_tile is None:
                    pass
                else:
                    if isinstance(poss_tile, monopoly.Property) or isinstance(poss_tile, monopoly.Utility) or isinstance(poss_tile, monopoly.Railroad):
                        de_select_tile(surface, selected_tile)
                        selected_tile = poss_tile
                        print_error_message(surface, "")



        
        select_tile(surface, selected_tile)
        draw_dice(surface, game)
        draw_pieces(surface, game)
        pygame.display.update()
        clock.tick(12)

def start_display():
    # Filling Background
    s = pygame.display.set_mode()
    s.fill(BACKGROUND_COLOR)

    # Text to indicate position of selected card
    selectedtext = LABELFONT.render("Selected Tile", True, TEXT_COLOR)
    xpos, ypos = PROPCARD_POS
    selected_rect = selectedtext.get_rect(
        center = (xpos + PROPCARD_WIDTH // 2, ypos - BORDER // 2))
    s.blit(selectedtext, selected_rect)

def draw_board(monopoly: monopoly.Monopoly):
    
    surface = pygame.display.get_surface()
    
    # Drawing all the tiles onfo the surface
    for row in monopoly.board:
        for tile in row:
            draw_tile_onto_display(surface, tile)


class Button():

    def __init__(self, pos: Tuple[int, int], active_image: pygame.Surface, 
        inactive_image: pygame.Surface,
        effect: Callable[[monopoly.Monopoly, BUYABLE_TILE], List[BUYABLE_TILE]],
        isactive: Callable[[monopoly.Monopoly, monopoly.GameTileType], bool]):
        
        self.pos = pos
        self.active_image = active_image
        self.inactive_image = inactive_image
        self.effect = effect
        self.isactive = isactive

    
    def in_button(self, loc: Tuple[int, int]) -> bool:
        
        width = self.active_image.get_width()
        height = self.active_image.get_height()
        
        xpos, ypos = loc
        x1, y1 = self.pos

        return (x1 <= xpos <= x1 + width) and (y1 <= ypos <= y1 + height)
    
    def apply_effect(self, game: monopoly.Monopoly, prop: BUYABLE_TILE) -> List[BUYABLE_TILE]:
        return self.effect(game, prop)
    def active(self, game: monopoly.Monopoly, prop: monopoly.GameTileType) -> bool:
        return self.isactive(game, prop)
def draw_button(width: int, height: int, text: str, background: RGBTYPE) -> pygame.Surface:
    surface = pygame.Surface((width, height))
    surface.fill(background)
    
    if width == SMALL_BUTTON_WIDTH:
        txtrender = SMALLBUTTON_FONT.render(text, True, BUTTON_TEXT_COLOR)
        
    else:
        txtrender = BUTTON_FONT.render(text, True, BUTTON_TEXT_COLOR)
    
    text_rect = txtrender.get_rect(center = (width // 2, height // 2))
    surface.blit(txtrender, text_rect)
    return surface

# +1 House Button
def plus_one_house_effect(game: monopoly.Monopoly, prop: BUYABLE_TILE):
    game.build_house(prop)
    return [prop]
def plus_one_house_legal(game: monopoly.Monopoly, prop: monopoly.GameTileType) -> bool:
    return game.can_build(prop)
PLUS_ONE_HOUSE = Button(
    (PROPCARD_XPOS + BUTTON_PADDING, PROPCARD_YPOS + PROPCARD_HEIGHT + BUTTON_PADDING),
    draw_button(SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, "+1 House", ACTIVE_BUTTON_BACKGROUND),
    draw_button(SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, "+1 House", INACTIVE_BUTTON_BACKGROUND),
    plus_one_house_effect, plus_one_house_legal)

# -1 House Button
def minus_one_house_effect(game: monopoly.Monopoly, prop: BUYABLE_TILE):
    game.sell_house(prop)
    return [prop]
def minus_one_house_legal(game: monopoly.Monopoly, prop: monopoly.GameTileType):
    return game.can_sell(prop)
MINUS_ONE_HOUSE = Button(
    (PROPCARD_XPOS + (PROPCARD_WIDTH // 2 + BUTTON_PADDING), PROPCARD_YPOS + PROPCARD_HEIGHT + BUTTON_PADDING),
    draw_button(SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, "-1 House", ACTIVE_BUTTON_BACKGROUND),
    draw_button(SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, "-1 House", INACTIVE_BUTTON_BACKGROUND),
    minus_one_house_effect, minus_one_house_legal)

# Buy Property Button
def buy_property_effect(game: monopoly.Monopoly, prop: BUYABLE_TILE):
    game.buy_property(prop)
    return [prop]
def buy_property_legal(game: monopoly.Monopoly, prop: monopoly.GameTileType):
    return game.can_buy(prop)
BUY_PROPERTY = Button(
    (PROPCARD_XPOS + BUTTON_PADDING, 
    PROPCARD_YPOS + PROPCARD_HEIGHT + BUTTON_PADDING + BUTTON_HEIGHT + BUTTON_PADDING),
    draw_button(SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, "Buy", ACTIVE_BUTTON_BACKGROUND),
    draw_button(SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, "Buy", INACTIVE_BUTTON_BACKGROUND),
    buy_property_effect, buy_property_legal)

# Start Auction Button
def start_auction_effect(game: monopoly.Monopoly, prop: BUYABLE_TILE):
    game.start_auction()
    return []
def start_auction_legal(game: monopoly.Monopoly, prop: monopoly.GameTileType):
    return game.can_start_auction(prop)
START_AUCTION = Button(
    (PROPCARD_XPOS + (PROPCARD_WIDTH // 2) + BUTTON_PADDING, 
    PROPCARD_YPOS + PROPCARD_HEIGHT + BUTTON_PADDING + BUTTON_HEIGHT + BUTTON_PADDING),
    draw_button(SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, "Auction", ACTIVE_BUTTON_BACKGROUND),
    draw_button(SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, "Auction", INACTIVE_BUTTON_BACKGROUND),
    start_auction_effect, start_auction_legal)

# Morgage Property Button
def morgage_property_effect(game: monopoly.Monopoly, prop: BUYABLE_TILE):
    game.morgage_property(prop)
    return [prop]
def morgage_property_legal(game: monopoly.Monopoly, prop: monopoly.GameTileType):
    
    return game.can_morgage(prop)
MORGAGE_PROPERTY = Button(
    (PROPCARD_XPOS + BUTTON_PADDING, 
    PROPCARD_YPOS + PROPCARD_HEIGHT + 3 * BUTTON_PADDING + 2 * BUTTON_HEIGHT),
    draw_button(BUTTON_WIDTH, BUTTON_HEIGHT, "Morgage", ACTIVE_BUTTON_BACKGROUND),
    draw_button(BUTTON_WIDTH, BUTTON_HEIGHT, "Morgage", INACTIVE_BUTTON_BACKGROUND),
    morgage_property_effect, morgage_property_legal)

# Unmorgage Property Button
def unmorgage_property_effect(game: monopoly.Monopoly, prop: BUYABLE_TILE):
    game.unmorgage_property(prop)
    return [prop]
def unmorgage_property_legal(game: monopoly.Monopoly, prop: monopoly.GameTileType):
    
    return game.can_unmorgage(prop)
UNMORGAGE_PROPERTY = Button(
    (PROPCARD_XPOS + BUTTON_PADDING, 
    PROPCARD_YPOS + PROPCARD_HEIGHT + 3 * BUTTON_PADDING + 2 * BUTTON_HEIGHT),
    draw_button(BUTTON_WIDTH, BUTTON_HEIGHT, "Unmorgage", ACTIVE_BUTTON_BACKGROUND),
    draw_button(BUTTON_WIDTH, BUTTON_HEIGHT, "Unmorgage", INACTIVE_BUTTON_BACKGROUND),
    unmorgage_property_effect, unmorgage_property_legal)

# Take Turn Button (Roll Dice + Move)
def take_turn_effect(game: monopoly.Monopoly, prop: BUYABLE_TILE) -> List[monopoly.GameTileType]:
    affected_tiles = [game.current_tile()]
    
    game.take_turn()

    affected_tiles.append(game.current_tile())
    return affected_tiles
def take_turn_legal(game: monopoly.Monopoly, prop: monopoly.GameTileType) -> List[monopoly.GameTileType]:
    return game.can_take_turn()
ROLL_DICE = Button(
    (PROPCARD_XPOS, 
    DISPLAY_HEIGHT - BORDER - TILE_HEIGHT),
    draw_button(BUTTON_WIDTH, BUTTON_HEIGHT * 2, "ROLL", ACTIVE_BUTTON_BACKGROUND),
    draw_button(BUTTON_WIDTH, BUTTON_HEIGHT * 2, "ROLL", INACTIVE_BUTTON_BACKGROUND),
    take_turn_effect, take_turn_legal)

# End Turn Button
def end_turn_effect(game: monopoly.Monopoly, prop: BUYABLE_TILE) -> List[monopoly.GameTileType]:
    game.end_turn()
    return []
def end_turn_legal(game: monopoly.Monopoly, prop: monopoly.GameTileType) -> List[monopoly.GameTileType]:
    return game.can_end_turn()
END_TURN = Button(
    (PROPCARD_XPOS, 
    DISPLAY_HEIGHT - BORDER - TILE_HEIGHT),
    draw_button(BUTTON_WIDTH, BUTTON_HEIGHT * 2, "END TURN", ACTIVE_BUTTON_BACKGROUND),
    draw_button(BUTTON_WIDTH, BUTTON_HEIGHT * 2, "END TURN", INACTIVE_BUTTON_BACKGROUND),
    end_turn_effect, end_turn_legal)