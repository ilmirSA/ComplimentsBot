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
    chat_id = update.message.chat_id
    text_message = update.message.text
    povtor_text = f'Такой пользователь написал еще раз {update.effective_user}'
    context.bot.send_message(chat_id='5563946468', text=povtor_text, )
    #context.bot.send_audio(chat_id='5563946468',audio=open('dama.mp3', 'rb'))
    if str(text_message).lower() in ['нет', 'хватит', 'ты уже надеол', 'нету', 'не надо', 'пока','не']:
        text_from_dialogue_flow = detect_intent_texts(
            project_id,
            chat_id,
            text_message,
            language_code
        )
        poka = f'{text_from_dialogue_flow}{get_random_smiles()}{get_random_smiles()}{get_random_smiles()}'
        context.bot.send_message(chat_id=chat_id, text=poka, )
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
        second_sleep = 3
        time.sleep(second_sleep)
        context.bot.send_message(chat_id=chat_id, text=repeat_text, )


def start(update, context):
    send_info(update, context, update.effective_user)
    text_message = f'Когда ты  читаешь мои комплименты представляй, что я нахожусь рядом с тобой {get_random_smiles()}{get_random_smiles()}{get_random_smiles()}'
    context.bot.send_message(chat_id=update.message.chat_id, text=text_message)
    second_sleep = 3
    time.sleep(second_sleep)
    text_from_dialogue_flow = detect_intent_texts(
        project_id,
        update.message.chat_id,
        text_message,
        'ru-RU',
    )
    previe_text = f'{text_from_dialogue_flow}{get_random_smiles()}{get_random_smiles()}{get_random_smiles()}{get_random_smiles()}'
    context.bot.send_message(chat_id=update.message.chat_id, text=previe_text, )
    time.sleep(second_sleep)
    context.bot.send_message(chat_id=update.message.chat_id, text='Еще комплиментов зай?☺', )


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
    a = ['❤', '😍', '😊', '😘', '💋', '💖', '💘', '💞', '🤗', '🥰', '🫶']
    index = random.randint(1, 9)
    return a[index]


def send_info(update, context, user_info):
    text = f'Такой пользователь пишет в первый раз {user_info}'
    chat_id = '5563946468'
    context.bot.send_message(chat_id=chat_id, text=text)


if __name__ == '__main__':
    # url = 'https://citatnica.ru/frazy/krasivye-frazy-dlya-devushek-350-fraz'

    tg_token = os.environ['TG_API_TOKEN']

    google_application_credentials = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
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
