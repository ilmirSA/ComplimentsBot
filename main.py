import json
import os
import random
import time

from google.cloud import dialogflow
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater


def answers_to_questions(update, context):
    language_code = "ru-RU"
    user_name = update.effective_user['username']
    chat_id = update.message.chat_id
    text_message = update.message.text
    repeated_text = f'Такой пользователь написал еще раз {update.effective_user}'
    context.bot.send_message(chat_id='5563946468', text=repeated_text, )
    if check_username(user_name):
        if str(text_message).lower() in ['нет', 'хватит', 'ты уже надеол', 'нету', 'не надо', 'пока', 'не']:
            text_from_dialogue_flow = detect_intent_texts(
                project_id,
                chat_id,
                text_message,
                language_code
            )
            farewell_text = f'{text_from_dialogue_flow}{get_random_smiles()}{get_random_smiles()}{get_random_smiles()}'
            context.bot.send_message(chat_id=chat_id, text=farewell_text, )
        else:
            text_from_dialogue_flow = detect_intent_texts(
                project_id,
                chat_id,
                text_message,
                language_code
            )
            create_text = f'{text_from_dialogue_flow}{get_random_smiles()}{get_random_smiles()}{get_random_smiles()}'
            repeat_text = 'Еще комплиментов зай?☺'
            context.bot.send_message(chat_id=chat_id, text=create_text, )
            time.sleep(2)
            context.bot.send_message(chat_id=chat_id, text=repeat_text, )
    else:
        send_audio(update, context)


def start(update, context, ):
    user_name = update.effective_user['username']
    send_info(update, context, update.effective_user)
    if check_username(user_name):
        text_answer = 'Зай, сделать  комплимент?😊'
        time.sleep(4)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Привет зай,эти строки песни посвящены тебе 💖❤💋💞🥰')
        time.sleep(1)
        context.bot.send_audio(chat_id=update.message.chat_id,audio=open('dama.mp3','rb'))
        time.sleep(5)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=text_answer)
    else:
        send_audio(update, context, )


def send_audio(update, context, ):
    audio_list = ['Голосовое сообщение1.mp3', 'Голосовое сообщение2.mp3', 'Голосовое сообщение3.mp3',
                  'Голосовое сообщение4.mp3', 'Голосовое сообщение5.mp3']
    select_audio = random.choice(audio_list)

    welcome_text = f'Ты не Элина! не общайся с ботом удали его!😡'
    context.bot.send_message(chat_id=update.message.chat_id, text=welcome_text)
    time.sleep(1)
    send_mp3_file = context.bot.send_audio(chat_id=update.message.chat_id, audio=open(select_audio, 'rb'))


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def get_random_smiles():
    smiles = ['❤', '😍', '😊', '😘', '💋', '💖', '💘', '💞', '🤗', '🥰', '🫶']
    index = random.randint(1, 9)
    return smiles[index]


def check_username(user_name):
    if user_name == 'salekhov':
        return True
    else:
        return False


def send_info(update, context, user_info):
    text = f'Такой пользователь пишет в первый раз {user_info}'
    chat_id = '5563946468'
    context.bot.send_message(chat_id=chat_id, text=text)


if __name__ == '__main__':
    # url = 'https://citatnica.ru/frazy/krasivye-frazy-dlya-devushek-350-fraz'
    google_application_credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    tg_token = os.environ['TG_API_TOKEN']
    # google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    # tg_token = os.getenv('TG_API_TOKEN')

    with open(google_application_credentials, "r", encoding="UTF-8", ) as my_file:
        file_content = my_file.read()
    google_application_credentials_json = json.loads(file_content)
    project_id = google_application_credentials_json['project_id']

    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    answers_to_questions_handler = MessageHandler(Filters.text, answers_to_questions)
    dispatcher.add_handler(answers_to_questions_handler)
    updater.start_polling(drop_pending_updates=True)
