import asyncio
import logging
import sys
from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

def get_gemini_respone(inpute):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(inpute
                                    )
    return response.text


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`

    print(message.text)


    # respone= get_gemini_respone(Message)
    await message.answer("respone")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        print(message.text)
        respone= get_gemini_respone(message.text)
        print(respone)
        # Send a copy of the received message
        await message.answer(respone)
        
        
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

# @dp.message_handler()
# async def chatgpt(message: types.Message):
#     """
#     A handler to process the user's input and generate a response using the Google gemini-pro API.
#     """
#     print(f">>> USER: \n\t{message.text}")
#     response = get_gemini_respone(message.text)
#     #reference.response = response
#     print(f">>> chatGPT: \n\t{response}")
#     await Bot.send_message(chat_id = message.chat.id, text = response)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    # print(message.text)
    # response = get_gemini_respone(message.text)
    # print(f">>> chatGPT: \n\t{response}")
    # # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())