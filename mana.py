# @kingsofpy - please subscripe this channel
# Author - Firdavs Yorkulov
# Username - @MrYorkulov
import asyncio
import wikipedia
from aiogram import Bot, Dispatcher, executor, types
import openai

TOKEN = 'Your bot token here from @botfather'
openai.api_key = "Your openai api key"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
]

promptHis = []

def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages



@dp.message_handler(commands=['wiki'])
async def send_wiki(message: types.Message):
 text = message.text.split("/wiki ", maxsplit=1)[1]
 try:
  result = wikipedia.summary(text)
  await message.reply(f'<b>{result}</b>', parse_mode="html")
 except IndexError:
  await message.reply("Не хватает аргументов!\nПример:<code> /wiki wikipedia</code>", parse_mode="html")
 except:
  await message.reply("⚠️Ошибка: Не удалось найти информацию")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global access
    global messages
    await message.answer("Привет, в этом боте ты можешь использовать <b>GPT 3.5</b>, просто отправь свой запрос", parse_mode=types.ParseMode.HTML)

@dp.message_handler(commands=['clear'])
async def start(message: types.Message):
    global messages
    messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
]
    await message.answer("История очищена", parse_mode=types.ParseMode.HTML)

@dp.message_handler(commands=['re'])
async def start(message: types.Message):
    sent_message = await message.answer("<b>ChatGPT регенерирует ответ...</b>", parse_mode=types.ParseMode.HTML)
    update(messages, "user", promptHis[len(promptHis) - 1])
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
    )
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    await message.answer(response['choices'][0]['message']['content'], parse_mode="Markdown")

# Chatgpt uchun komanda
# Command for generate request from chatgpt
@dp.message_handler(commands=['gpt'])
async def prompt(message: types.Message):
    text_matn = message.text.replace("/gpt ", "")
    if message.text != "/start" or "/clear" or "/re":
        promptHis.append(message.text)
        sent_message = await message.answer("<b>ChatGPT генерирует ответ...</b>", parse_mode=types.ParseMode.HTML)
        update(messages, "user", text_matn)
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages,
        )
        await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
        await message.answer(response['choices'][0]['message']['content'], parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())