import os
import requests
import pygame  # Requires at least pygame v2.0.0 & updated dependencies: libsdl2-ttf-2.0-0
from pygame.locals import *
import platform

# Check if platform is raspberry pi
# Load config
try:
    if platform.system() == "Linux" and "raspberrypi" in platform.uname().nodename.lower():
        print("Platform is Raspberry Pi")
        print("Loading config 'config_pi'")
        from Configs.config_pi import *
    else:
        print("Platform is NOT Raspberry Pi")
        print("Loading config 'config_generic'")
        # TODO: Load other platform config (full-screen)
        from Configs.config_generic import *
except Exception as e:
    print("Could not determine platform", e)
    print("Loading config 'config_generic'")
    from Configs.config_generic import *
    # TODO: Load other platform config (full-screen)

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

# Initialize pygame
pygame.init()

# Define screen dimensions and create a window
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)  # can use NOFRAME too

pygame.display.set_caption("BTC TRACKER")

# Define colors
black = (0, 0, 0)
red = (255, 0, 0)
grey = (211,211,211)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
gold = (210,150,30)

# Rectangle sizes
rect_inner_padding_x = 40
rect_inner_padding_y = 5
char_padding_x = 70
char_padding_y = 80
char_spacing = 40
border_thickness = 1

update_time = 120  # time between main API calls

# Alpha value for fading block text by decrementing
alpha = 255

# initialise blank strings
old_block_num = ""
price_integer = ""
block_height = ""

# To be used for API limit queries
change_text = False  # NOT used yet
credits_used = ""  # NOT used yet
monthly_limit = ""  # NOT used yet

do_request = False  # Bool for doing API call after set time
start_run = True  # Runs API calls on initial run

# Font path and size
font_path = os.environ.get('FONT_PATH', 'DS-DIGII.TTF') #not working, always defaults
secondary_font_path = os.environ.get('FONT_PATH', 'DS-DIGII.TTF')
font = pygame.font.Font(None, 10)
font_file = font_path  # "../Fonts/DS-DIGII.TTF"
secondary_font = secondary_font_path

print(f"BTC PRICE")

# coinmarketcap API documentation @ https://coinmarketcap.com/api/documentation/v1/
# Latest Price API endpoint URL
price_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
# Usage of API Key #TODO - not used yet
usage_url = "https://pro-api.coinmarketcap.com/v1/key/info"
block_url = "https://blockchain.info/latestblock"

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


def draw_text_centered(text, font, color, screen):
    # Clear the screen
    screen.fill(black)

    # Calculate the width and height of the text surface
    text_surface = font.render(text, True, color)
    text_width, text_height = text_surface.get_size()

    # Calculate the position to center the text on the screen
    x = ((screen_width - text_width) // 2) - start_pos
    y = (screen_height - text_height) // 2

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


###########
# MAIN
###########
start_time = pygame.time.get_ticks()

running = True
while running:
    # Get the current time in milliseconds
    current_time = pygame.time.get_ticks()

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
            change_text = not change_text  # will be used to print debug/updates if screen clicked/pressed

    # Reduce alpha of block text each loop - looks better with higher frame-rate
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

    block_font = pygame.font.Font(secondary_font, update_size)

    # Send the GET request
    # Block 840,000 - 3.125 BTC - Expected ~May 2024
    block_num = requests.get(block_url, headers=blockchain_headers)

    if block_num.status_code == 200:
        block_data = block_num.json()
        block_height = block_data["height"]
        print(f"new block height: {block_height}  old block height: {old_block_num}")
        if block_height != old_block_num:
            alpha = 255
            old_block_num = block_height
            print(f"ADDING NEW BLOCK")

    # If time to update, hit API
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

        else:
            print(f"Request failed with status code {response.status_code}")

    print(f"price: {price_integer}")

    price_font = pygame.font.Font(font_file, price_size)

    # Clear the screen
    screen.fill(black)

    # Render the price text with digital clock style graphics
    draw_text_centered(str(price_integer), price_font, white, screen)

    # Render block number
    block_text = block_font.render(f"Block #{block_height}", True, grey)
    block_text_width, block_text_height = block_text.get_size()
    block_text.set_alpha(alpha)
    block_pos_x = ((screen_width - block_text_width) // 2)
    block_pos_y = ((screen_height - block_text_height) // 2) + block_padding_y
    screen.blit(block_text, (block_pos_x, block_pos_y))  # Adjust the position as needed

# For testing
#    alpha_text = block_font.render(f"alpha: {alpha}", True, grey)
#    screen.blit(alpha_text, (10, 70))  # Adjust the position as needed

    # Update the display
    pygame.display.flip()
    do_request = False

    # Keep loop running at specified frame-rate
    pygame.time.Clock().tick(frame_rate)

pygame.quit()

