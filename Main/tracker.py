import os
import requests
import time
import pygame #Requires at least pygame v2.0.0 & updated dependencies: libsdl2-ttf-2.0-0
from pygame.locals import *

#xdg_runtime_dir = os.environ.get('XDG_RUNTIME_DIR')
#print(xdg_runtime_dir)

# Set XDG_RUNTIME_DIR if not already set for sudo cron
#if 'XDG_RUNTIME_DIR' not in os.environ:
#    os.environ['XDG_RUNTIME_DIR'] = str(xdg_runtime_dir)

# TODO: Pass in API key
# TODO: separate API calls from pygame display
# TODO: Fix Font path

#for attempts at cronjob - not yet working
current_directory = os.path.dirname(os.path.realpath(__file__))
# Set the working directory to the script's directory
os.chdir(current_directory)

font_path = os.environ.get('FONT_PATH', 'DS-DIGII.TTF') #not working, always defaults
secondary_font_path = os.environ.get('FONT_PATH', 'DS-DIGII.TTF')

# Initialize pygame
pygame.init()

# Define screen dimensions and create a window
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
#screen = pygame.display.set_mode((screen_width, screen_height), NOFRAME)
screen = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)

pygame.display.set_caption("LED Display")

# Define colors
black = (0, 0, 0)
red = (255, 0, 0)
grey = (211,211,211)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
gold = (210,150,30)

# Font sizes
price_size = 100
update_size = 60
start_pos = 260

# Rectangle sizes
rect_inner_padding_x = 40
rect_inner_padding_y = 5
char_padding_x = 70
char_padding_y = 80
char_spacing = 40
border_thickness = 1

frame_rate = 30 #60 for laptop?
update_time = 120  # seconds

alpha = 255

# initialise blank strings
old_block_num = ""
price_integer = ""

# Define the font and font size
font = pygame.font.Font(None, 10)

print(f"BTC PRICE")
# api key: b4de8a18-e523-457a-917b-78f8e6093bd9
# curl -H "X-CMC_PRO_API_KEY: b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c" -H "Accept: application/json" -d "start=1&limit=5000&convert=USD" -G https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest

# Latest Price API endpoint URL
price_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
# Usage of API Key
usage_url = "https://pro-api.coinmarketcap.com/v1/key/info"

# Define the headers
headers = {
    "X-CMC_PRO_API_KEY": "b4de8a18-e523-457a-917b-78f8e6093bd9",
    "Accept": "application/json"
}

blockchain_headers = {
    "Accept": "application/json"
}

# Define the query parameters
params = {
    "id": 1  # BTC
}


#def draw_text_centered(text, font, color, screen):
#    text_surface = font.render(text, True, color)
#    text_rect = text_surface.get_rect()
#    text_rect.center = (screen_width // 2, screen_height // 2)  # Center text on the screen
#    screen.blit(text_surface, text_rect)

def draw_text_centered(text, font, color, screen):
    # Clear the screen
    screen.fill(black)

    # Calculate the width and height of the text surface
    text_surface = font.render(text, True, color)
    text_width, text_height = text_surface.get_size()

    # Calculate the position to center the text on the screen
    x = ((screen_width - text_width) // 2) - start_pos
    y = (screen_height - text_height) // 2

    # Calculate the spacing between characters
    #char_spacing = 60  # Adjust this value to increase or decrease the spacing

    # Iterate through each character in the text and draw a rectangle around it
    for char in text:
        char_surface = font.render(char, True, color)
        char_width, char_height = char_surface.get_size()

        # Define the dimensions of the rectangle
        rect_width, rect_height = char_width + char_padding_x, char_height + char_padding_y  # Add padding around the character

        # Draw the rectangle around the character
        pygame.draw.rect(screen, gold, (x, y - 50, rect_width, rect_height), border_thickness, 2, 10, 10, 10, 10)  # 2 is the border thickness

        # Blit the character surface onto the screen
        screen.blit(char_surface, (x + rect_inner_padding_x, y + rect_inner_padding_y))  # Add padding inside the rectangle

        # Move the x-coordinate to the right for the next character
        x += rect_width + char_spacing  # Add spacing between characters

    # Update the display
    pygame.display.flip()

# Initialize the update count
update_count = 0
change_text = False
credits_used = ""
monthly_limit = ""

do_request = False

start_time = pygame.time.get_ticks()
start_run = True

running = True
while running:
    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds

    # Calculate the elapsed time in seconds since the last API request
    elapsed_time = (current_time - start_time) / 1000  # Convert milliseconds to seconds

    if start_run:
        do_request = True
        start_run = False

    if elapsed_time >= update_time:
        # Reset the start time for the next interval
        start_time = current_time
        do_request = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse click here
            change_text = not change_text

    print(f"alpha: {alpha}")
    alpha -= 15
    if alpha < 0:
        alpha = 0

# WHY IS THIS FAILING SOMETIMES ON RPI?
#    api_usage = requests.get(usage_url, headers=headers)
#    if api_usage.status_code == 200:
#        data = api_usage.json()
#        credits_used = data["data"]["usage"]["current_month"]["credits_used"]
#        monthly_limit = data["data"]["plan"]["credit_limit_monthly"]
#        print(credits_used)
#        print(monthly_limit)

    font_file = font_path  # "../Fonts/DS-DIGII.TTF"
    secondary_font = secondary_font_path
    updates_font = pygame.font.Font(secondary_font, update_size)


    # Send the GET request
    # Block 840,000 - 3.125 BTC - Expected ~May 2024
    block_num = requests.get("https://blockchain.info/latestblock", headers=blockchain_headers)

    if block_num.status_code == 200:
        block_data = block_num.json()
        block_height = block_data["height"]
        print(f"new block height: {block_height}  old block height: {old_block_num}")
        if block_height != old_block_num:
            alpha = 255
            old_block_num = block_height
            print(f"ADDING NEW BLOCK")
            #print(f"new block: {block_height}")
        # print(f"Request failed with status code {response.status_code}")

    # Clear the screen
    screen.fill(black)

    # block_text = updates_font.render(f"Block #{block_height}", True, grey)
    # block_text.set_alpha(alpha)
    # screen.blit(block_text, (10, 540))  # Adjust the position as needed

    if do_request:
        print("Doing update")
        response = requests.get(price_url, headers=headers, params=params)


        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Access the price in USD
            price_usd = data["data"]["1"]["quote"]["USD"]["price"]

            # Convert the price to an integer
            price_integer = int(price_usd)

            # Increment the update count
            #update_count += 1

            # Clear the screen
            #screen.fill(black)

            #font
            # font = pygame.font.Font('../Fonts/DS-DIGII.TTF', 400)
            #secondary_font = secondary_font_path
            #price_font = pygame.font.Font(font_file, price_size)
            #updates_font = pygame.font.Font(secondary_font, update_size)

            # Render the price text with digital clock style graphics
            #draw_text_centered(str(price_integer), price_font, white, screen)

            #block_text = updates_font.render(f"Block #{block_height}", True, grey)
            #block_text.set_alpha(alpha)
#            screen.blit(block_text, (470, 540))  # Adjust the position as needed

            # block_text = updates_font.render(f"Block #{block_height}", True, grey)
            #
            # # Create a new transparent surface with the same size as block_text
            # faded_block_text = pygame.Surface(block_text.get_size(), pygame.SRCALPHA)
            #
            # # Set the alpha value of the new surface
            # faded_block_text.set_alpha(alpha)
            #
            # # Blit the text onto the faded text surface
            # faded_block_text.blit(block_text, (0, 0))
            #
            # # Blit the faded text surface onto the screen
            # screen.blit(faded_block_text, (10, 540))  # Adjust the position as needed

            # Blit the transparent text surface onto the screen
#            screen.blit(block_text_background, (470, 540))

            # Render the update count
#            if change_text:
#                #alpha = 255
#                count_text = updates_font.render(f"Updates: {update_count}", True, grey)
#                screen.blit(count_text, (10, 70))  # Adjust the position as needed

#                if block_height:
#                    block_text = updates_font.render(f"Block #{block_height}", True, grey)
#                    block_text.set_alpha(alpha)
#                    screen.blit(block_text, (10, 540))  # Adjust the position as needed

#                if credits_used:
#                    credits_used_text = updates_font.render(f"Credits used: {credits_used}/{monthly_limit}", True, grey)
#                    screen.blit(credits_used_text, (10, 700))  # Adjust the position as needed

            # Update the display
            #pygame.display.flip()

        else:
            print(f"Request failed with status code {response.status_code}")


    print(f"price: {price_integer}")

    price_font = pygame.font.Font(font_file, price_size)

    # Render the price text with digital clock style graphics
    draw_text_centered(str(price_integer), price_font, white, screen)

    block_text = updates_font.render(f"Block #{block_height}", True, grey)
    block_text_width, block_text_height = block_text.get_size()
    block_text.set_alpha(alpha)
    block_pos_x = ((screen_width - block_text_width) // 2)
    block_pos_y = ((screen_height - block_text_height) // 2) + 150
    screen.blit(block_text, (block_pos_x, block_pos_y))  # Adjust the position as needed

#    alpha_text = updates_font.render(f"alpha: {alpha}", True, grey)
#    screen.blit(alpha_text, (10, 70))  # Adjust the position as needed

    pygame.display.flip()
    do_request = False

    pygame.time.Clock().tick(frame_rate)

    # Wait for a minute (60 seconds)
    #time.sleep(update_time)

pygame.quit()

