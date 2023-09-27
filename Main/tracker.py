import os
import requests
import time
import pygame
from pygame.locals import *

font_path = os.environ.get('FONT_PATH', 'DS-DIGII.TTF') #not working, always defaults?
print(font_path)

# Initialize pygame
pygame.init()

# Define screen dimensions and create a window
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), NOFRAME)


pygame.display.set_caption("LED Display")

# Define colors
black = (0, 0, 0)
red = (255, 0, 0)

# Define the font and font size
font = pygame.font.Font(None, 10)

print(f"BTC PRICE")
# api key: b4de8a18-e523-457a-917b-78f8e6093bd9
# curl -H "X-CMC_PRO_API_KEY: b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c" -H "Accept: application/json" -d "start=1&limit=5000&convert=USD" -G https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest

# Define the API endpoint URL
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

# Define the headers
headers = {
    "X-CMC_PRO_API_KEY": "b4de8a18-e523-457a-917b-78f8e6093bd9",
    "Accept": "application/json"
}

# Define the query parameters
params = {
    "id": 1 #BTC
}

def draw_text_centered(text, font, color, screen):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)  # Center text on the screen
    screen.blit(text_surface, text_rect)

# Initialize the update count
update_count = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Send the GET request
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Access the price in USD
        price_usd = data["data"]["1"]["quote"]["USD"]["price"]

        # Convert the price to an integer
        price_integer = int(price_usd)

        # Increment the update count
        update_count += 1

        # Clear the screen
        screen.fill(black)

        #font
        # font = pygame.font.Font('../Fonts/DS-DIGII.TTF', 400)
        font_file = font_path #"../Fonts/DS-DIGII.TTF"
        price_size = 400
        update_size = 100
        price_font = pygame.font.Font(font_file, price_size)
        updates_font = pygame.font.Font(font_file, update_size)

        # Render the price text with digital clock style graphics
        draw_text_centered(str(price_integer), price_font, (255,255,255), screen)

        # Render the update count
        count_text = updates_font.render(f"Updates: {update_count}", True, red)
        screen.blit(count_text, (10, 70))  # Adjust the position as needed
        # draw_text_centered(count_text, font, (0, 0, 0), screen)  # Draw centered text in black

        # Update the display
        pygame.display.flip()

    else:
        print(f"Request failed with status code {response.status_code}")

    # Wait for a minute (60 seconds)
    time.sleep(10)

pygame.quit()

