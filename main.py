import asyncio
import requests
import random
import time
import aiogram
from faker import Faker
from aiogram.types import InputFile
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import live

fake = Faker()

def luhn_algorithm(card_number):
    digits = [int(digit) for digit in card_number]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

async def send_messages():
    # Initialize the bot
    bot = aiogram.Bot(token='7431477906:AAGblI2dxvpOxEGPPI7SEdiHmc0fxWBEM-s') #put Your Bot Token
    chat_id ='-1002225168609' #Put Your Channel Chat Id Here

    # Read the text file
    with open('cards.txt') as file:
        lines = file.readlines()

    # Limit and pause configuration
    requests_limit = 1  # Number of requests per long pause
    pause_duration = 1  # Duration of the long pause in seconds

    # Iterate over the lines of the text file and send each message to the channel
    for i, line in enumerate(lines, start=1):
        # Remove the last 4 digits of the card number
        linea = line[:28]
        card_number = line[:12]

        # Check if the card is valid using the Luhn algorithm
        if not luhn_algorithm(card_number):
            print(f"Invalid card at position {i}: {linea}")
            continue

        # Verify the card's BIN
        BIN = card_number[:6]
        req = requests.get(f"https://bins.antipublic.cc/bins/{BIN}").json()

        # Handle the error if the 'brand' key is not present
        try:
            brand = req['brand']
        except KeyError:
            print("The 'brand' key is not present in the JSON response. This entry will be skipped.")
            continue

        # Capture the values from the JSON response
        country = req['country']
        country_name = req['country_name']
        country_flag = req['country_flag']
        country_currencies = req['country_currencies']
        bank = req['bank']
        level = req['level']
        typea = req['type']

        # Generate a random date in the range of the last 5 years
        month = str(random.randint(1, 12)).zfill(2)

        # Generate a random two-digit year (between 24 and 32)
        year = str(random.randint(24, 32)).zfill(2)

        # Generate a random name
        full_name = fake.name()

        # Generate a random address
        address = fake.address()

        # Path of the photo you want to send
        photo_path = "ruler.jpg"

        # Load the photo using InputFile
        photo = InputFile(photo_path)

        button_consultas = InlineKeyboardButton("About Sam", url="https://t.me/portaltodestroyer")
        # Add the buttons to a list
        keyboard = [[button_consultas]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        message = ""
        message += f"\n"
        message += f" CC FUCKER 🐍"
        message += "━━━━━━━━━━━━━━\n"
        message += f"<b>⌖ 𝗖𝗰 ⤳</b> <code>{linea}</code>\n"
        message += f"⌖ 𝗦𝘁𝗮𝘁𝘂𝘀 ⤳ valid card! ✅\n"
        message += f"⌖ 𝗕𝗶𝗻 ⤳ #Bin{BIN}\n"
        message += "━━━━━━━━━━━━━━\n"
        message += f"<b>⌮ INFO ⤳ </b>  <code>{brand}-{typea}-{level}</code>\n"
        message += f"<b>⌮ Bank Name ⤳ </b>  <code>{bank}</code>\n"
        message += f"<b>⌮ Country ⤳ </b>  <code>{country_name} [{country_flag}]</code>\n"
        message += "━━━━━━━━━━━━━━\n"
        message += f"<b>⌮ 𝐄𝐱𝐭𝐫𝐚 ⤳ </b>  <code>{card_number}xxxx|{month}|{year}|rnd</code>\n"
        message += f"⌖  Created by ⤳ @EthicalGod\n"
        message += "━━━━━━━━━━━━━━\n"

        # Send the message to the channel with parse_mode='HTML'
        try:
            await bot.send_photo(chat_id, photo, caption=message, reply_markup=reply_markup, parse_mode='HTML')
        except Exception as e:
            print(f"Error sending message: {e}")

        # Check if the request limit has been reached
        if i % requests_limit == 0 and i != len(lines):
            print(f"Request limit reached. Pausing for {pause_duration} seconds.")
            time.sleep(pause_duration)

live()
if __name__ == '__main__':
    asyncio.run(send_messages())
