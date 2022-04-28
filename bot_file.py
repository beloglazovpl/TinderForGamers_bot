import random
import os
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tinder.settings")
import django
django.setup()
from django.conf import settings
from tgbot.models import Profile


import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


games = ['FIFA', 'GTA V', 'God of war', 'CS:Go', 'Dota 2', 'World of warcraft', 'Mortal combat', 'NHL']


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data == 'create_profile':
        """
        Начальная функция при создании профиля 
        """
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Выбрать игру', callback_data='change_game')],
        ])
        bot.sendMessage(from_id, f'Для начала выбери игру, чтобы увидеть список игр нажмите на кнопку ниже',
                        reply_markup=keyboard)

    if query_data == 'change_game':
        """
        Выбор игры из списка
        """
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='GTA V', callback_data='GTA V')],
            [InlineKeyboardButton(text='FIFA', callback_data='FIFA')],
            [InlineKeyboardButton(text='God of war', callback_data='God of war')],
            [InlineKeyboardButton(text='CS:Go', callback_data='CS:Go')],
            [InlineKeyboardButton(text='Dota 2', callback_data='Dota 2')],
            [InlineKeyboardButton(text='World of warcraft', callback_data='World of warcraft')],
            [InlineKeyboardButton(text='Mortal combat', callback_data='Mortal combat')],
            [InlineKeyboardButton(text='NHL', callback_data='NHL')],
        ])
        bot.sendMessage(from_id, f'Выбери игру', reply_markup=keyboard)

    if query_data in games:
        global game, status
        game = query_data
        try:
            Profile.objects.get(chat_id=from_id)
            Profile.objects.update_or_create(
                chat_id=from_id,
                defaults={
                    'game': game
                }
            )
            bot.sendMessage(from_id, f'Выбрана игра {game}')
        except:
            bot.sendMessage(from_id, f'Выбрана игра {game}\n\n'
                                     f'Необходимо заполнить раздел "О себе"\n'
                                     f'Отправь в одном сообщении то что ты хочешь указать в данном разделе')
            status = 'description'

    if query_data == 'repeat_search':
        """
        Продолжить поиск напарника
        """
        if len(all_users) == 0:
            bot.sendMessage(from_id, f'Ты просмотрел всех пользователей по игре '
                                     f'{Profile.objects.get(chat_id=from_id).game}\n'
                                     f'Начни поиск заново, либо выбери другую игру')
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Продолжить поиск', callback_data='repeat_search')],
                [InlineKeyboardButton(text='Написать пользователю', callback_data='send_message')],
            ])
            global user_chat_id, search_user_name, search_user_game
            random_user = random.randint(0, len(all_users)-1)
            search_user_name = all_users[random_user].name
            search_user_game = all_users[random_user].game
            search_user_description = all_users[random_user].description
            user_chat_id = all_users[random_user].chat_id
            bot.sendMessage(from_id, f'Посмотри\n'
                                     f'Пользователь: {search_user_name}\n'
                                     f'Игра: {search_user_game}\n'
                                     f'Описание: {search_user_description}', reply_markup=keyboard)
            all_users.remove(all_users[random_user])

    if query_data == 'send_message':
        """
        Отправляет сообщение пользователю выбранной карточки профиля
        """
        bot.sendMessage(user_chat_id,
                        f'Пользователю {Profile.objects.get(chat_id=from_id).name} '
                        f'понравилась ваша карточка по игре {search_user_game}. Напиши ему!')
        bot.sendMessage(from_id, f'Пользователю {search_user_name} отправлено сообщение!')

    if query_data == 'change_description':
        """
        Обновление раздела "О себе"
        """
        bot.sendMessage(from_id, f'Напиши информацию и отправь сообщением')
        status = 'description'

    if query_data == 'change_visibility':
        """
        Смена видимости в поиске
        """
        visibility_now = Profile.objects.get(chat_id=from_id).search
        if visibility_now is True:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Отключить', callback_data='search_off')]
            ])
            bot.sendMessage(from_id, 'Вы включены в поиск', reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Включить', callback_data='search_on')]
            ])
            bot.sendMessage(from_id, 'Вы выключены из поиска', reply_markup=keyboard)

    if query_data == 'search_off':
        """
        Отключает видимость профиля
        """
        bot.sendMessage(from_id, 'Теперь твой профиль не виден другим пользователям')
        Profile.objects.update_or_create(
            chat_id=from_id,
            defaults={'search': False},
        )

    if query_data == 'search_on':
        """
        Включает видимость профиля
        """
        bot.sendMessage(from_id, 'Теперь твой профиль виден другим пользователям')
        Profile.objects.update_or_create(
            chat_id=from_id,
            defaults={'search': True},
        )


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    global status

    if msg['text'] == '/start':
        """
        Стартовая команда, проверяет указн ли username в настройках телеграма
        В случае отсутствия - необходимо указать username в настройках и перезапустить бота
        После уточнения username предлагает создать профиль
        """
        try:
            global name
            name = msg['from']['username']
            try:
                Profile.objects.get(chat_id=chat_id)
                bot.sendMessage(chat_id, 'Профиль есть в системе. Для доступа к командам воспользуйтесь '
                                         'кнопкой "Меню" слева внизу')
            except:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Создать профиль', callback_data='create_profile')],
                ])
                bot.sendMessage(chat_id,
                                f'Привет, {msg["from"]["first_name"]}!\n'
                                f'Это сервис для поиска напарника в твоей любимой игре!\n\n'
                                f'Перед тем как начать давай заполним твой профиль)',
                                reply_markup=keyboard)

        except KeyError:
            bot.sendMessage(chat_id, 'Укажите "Имя пользователя" в настройках профиля Telegram '
                                     'и перезапустите бота командой /start')
        status = None

    elif msg['text'] == '/change_profile':
        """
        Команда для измнения выбранного раздела профиля
        """
        try:
            Profile.objects.get(chat_id=chat_id)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Изменить игру', callback_data='change_game')],
                [InlineKeyboardButton(text='Изменить "О себе"', callback_data='change_description')],
                [InlineKeyboardButton(text='Изменить видимость поиска', callback_data='change_visibility')]
            ])
            bot.sendMessage(chat_id, 'Выбери что хочешь изменить', reply_markup=keyboard)
        except:
            bot.sendMessage(chat_id, 'Профиль не создан. Введите команду /start')

    elif msg['text'] == '/search':
        """
        Команда для поиска напарника в выбранной игре
        """
        global all_users
        try:
            users = Profile.objects.exclude(chat_id=chat_id).exclude(search=False).filter(game=Profile.objects.get(chat_id=chat_id).game)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Продолжить поиск', callback_data='repeat_search')],
                [InlineKeyboardButton(text='Написать игроку', callback_data='send_message')],
            ])
            all_users = [user for user in users]
            random_user = random.randint(0, len(all_users)-1)
            search_user_name, search_user_game, search_user_description = all_users[random_user].name, \
                                                                          all_users[random_user].game, \
                                                                          all_users[random_user].description
            bot.sendMessage(chat_id, f'Посмотри\n'
                                     f'Пользователь: {search_user_name}\n'
                                     f'Игра: {search_user_game}\n'
                                     f'Описание: {search_user_description}', reply_markup=keyboard)
            all_users.remove(all_users[random_user])
        except ValueError:
            bot.sendMessage(chat_id, f'Новые пользователи по игре {Profile.objects.get(chat_id=chat_id).game} не найдены\n'
                                     f'Начни поиск заново, либо выбери другую игру')
        except:
            bot.sendMessage(chat_id, 'Профиль не создан. Введите команду /start')

    elif msg['text'] == '/my_profile':
        """
        Команда выводит сообщение с карточкой пользователя
        """
        try:
            bot.sendMessage(chat_id, f'Мой профиль\n\n'
                                     f'Имя: {Profile.objects.get(chat_id=chat_id).name}\n'
                                     f'Игра: {Profile.objects.get(chat_id=chat_id).game}\n'
                                     f'О себе: {Profile.objects.get(chat_id=chat_id).description}\n'
                                     f'Статус для поиска: {Profile.objects.get(chat_id=chat_id).search}')
        except:
            bot.sendMessage(chat_id, 'Профиль не создан. Введите команду /start')

    else:
        try:
            if status is None:
                bot.sendMessage(chat_id, 'Воспользуйся кнопкой Меню для выбора нужной команды')
            if status == 'description':
                description = msg['text']
                try:
                    Profile.objects.get(chat_id=chat_id)
                    Profile.objects.update_or_create(
                            chat_id=chat_id,
                            defaults={
                                'description': description
                            }
                    )
                    bot.sendMessage(chat_id, 'Раздел "О себе" обновлен')
                    status = None
                except:
                    Profile.objects.update_or_create(
                        chat_id=chat_id,
                        defaults={
                            'name': name,
                            'description': description,
                            'game': game
                        }
                    )
                    bot.sendMessage(chat_id, 'Профиль создан!\n'
                                             'Теперь можешь воспользоваться поиском напарника\n'
                                             'Доступные команды находятся в Меню')
                    status = None
        except NameError:
            bot.sendMessage(chat_id, 'Воспользуйся кнопкой Меню для выбора нужной команды')


bot = telepot.Bot(settings.TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
while 1:
    time.sleep(10)
