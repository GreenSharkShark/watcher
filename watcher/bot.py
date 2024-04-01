from telebot import types
from config.settings import Session, SUPPORTED_SITES, bot
from models import User, Serial, Site
from functions import save_user_data, parse_url, Menu, how_to_use_bot
from sqlalchemy.exc import IntegrityError


@bot.message_handler(commands=['start'])
def start_bot(message):
    """ Запускается при первом старте бота, сохраняет данные пользователя """

    save_user_data(message)
    Menu().main_menu(message)


@bot.callback_query_handler(func=lambda callback: not callback.data.startswith('delete'))
def handle_callback_data(callback):
    """ Обрабатывает кнопки главного меню """

    if callback.data == 'tracking':
        sent = bot.send_message(text='Отправьте ссылку на страницу с сериалом', chat_id=callback.message.chat.id)
        bot.register_next_step_handler(sent, track)
    elif callback.data == 'how_to_use':
        how_to_use_bot(callback.message)
    elif callback.data == 'tracking_list':
        tracking_list(callback.message)
    elif callback.data == 'menu':
        Menu().main_menu(callback.message)
    elif callback.data == 'send_report':
        sent = bot.send_message(text='Опишите вашу проблем или предложение. В данный момент'
                                     'поддерживается отправка только текстовых сообщений.',
                                chat_id=callback.message.chat.id)
        bot.register_next_step_handler(sent, send_report)
    bot.answer_callback_query(callback.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete'))
def handle_delete(call):
    serial_id = int(call.data.split('_')[1])
    with Session() as session:
        serial_to_delete = session.query(Serial).filter_by(id=serial_id).first()
        if not serial_to_delete:
            bot.answer_callback_query(call.id, text='Не удалось найти сериал для удаления', show_alert=True)
            return
        session.delete(serial_to_delete)
        session.commit()
        bot.answer_callback_query(call.id, text='Сериал удален из списка отслеживаемых')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Сериал удален')


def track(message):
    """ Парсит ссылку полученную из def tracking(message) и отмечает сериал как отслеживаемый """

    website = parse_url(message.text)
    try:
        if website['site'] in SUPPORTED_SITES.keys():
            with Session() as session:
                user_object = session.query(User).filter_by(tg_user_id=message.from_user.id).first()
                new_serial = Serial()
                new_serial.url = message.text
                new_serial.site = session.query(Site).filter_by(name=website['site']).first()
                new_serial.watching_users.append(user_object)
                session.add(new_serial)
                session.commit()
                bot.send_message(text=f"Сериал добавлен в список отслеживаемых", chat_id=message.chat.id)
    except KeyError:
        bot.send_message(text=f"Сайт не поддерживается, либо {website['error']}", chat_id=message.chat.id)
    except IntegrityError:
        bot.send_message(text='Этот сериал уже есть в вашем списке отслеживаемых', chat_id=message.chat.id)
    finally:
        Menu().btn_return_to_menu(message)


def tracking_list(message):
    with Session() as session:
        tracked_list = session.query(Serial).all()
        if not tracked_list:
            bot.send_message(text='У вас нет отслеживаемых сериалов', chat_id=message.chat.id)
            Menu().btn_return_to_menu(message)
            return
        bot.send_message(text='Ваш список отслеживаемых сериалов:', chat_id=message.chat.id)
        for item in tracked_list:
            markup = types.InlineKeyboardMarkup()
            btn_delete = types.InlineKeyboardButton('Удалить', callback_data=f"delete_{item.id}")
            markup.add(btn_delete)
            bot.send_message(text=item.url, chat_id=message.chat.id, reply_markup=markup)
        Menu().btn_return_to_menu(message)


def send_report(message) -> None:
    """ Отправляет сообщение с кнопки "Проблемы и предложения" """
    bot.send_message(chat_id=1276508620, text=f'Сообщение от @{message.from_user.username}:\n'
                                              f'{message.text}')
    Menu().btn_return_to_menu(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
