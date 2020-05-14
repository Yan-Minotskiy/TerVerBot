import telebot
import config
import terver
from telebot import types
import codecs

bot = telebot.TeleBot(config.TOKEN)  # создаём бота


@bot.message_handler(commands=['start'])
def welcome(message):  # функция для приветствия польщователя
    bot.send_message(message.chat.id,
                     '*Добро пожаловать, {0.first_name}!*\n'
                     'Это Бот, который поможет тебе решать задачи '
                     'по теории вероятностей!🎲\n'.format(message.from_user),
                     parse_mode='Markdown')
    menu(message)


n, p, k, k2, p_a, x_a = None, None, None, None, None, None


@bot.message_handler(commands=['menu'])
def menu(message):  # главное меню
    global n, p, k, k2, p_a, x_a
    n, p, k, k2, p_a, x_a = None, None, None, None, None, None
    keyboard = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text='Расчёт простой вероятности 🎯', callback_data='simple')
    keyboard.add(key1)
    key2 = types.InlineKeyboardButton(text='Комбинаторика 🎰', callback_data='combinatoric')
    keyboard.add(key2)
    key3 = types.InlineKeyboardButton(text='Повторяющиеся события ♻️', callback_data='ver_count_event')
    keyboard.add(key3)
    key4 = types.InlineKeyboardButton(text='Случайные дискретные величины 🎲', callback_data='discret_random_value')
    keyboard.add(key4)
    key5 = types.InlineKeyboardButton(text='Теория 📚', callback_data='theory')
    keyboard.add(key5)
    key6 = types.InlineKeyboardButton(text='Примеры решений 🚀', callback_data='soon')
    keyboard.add(key6)
    bot.send_message(message.chat.id, '*Список моих возможностей:*\nВведите " / ", '
                                      'чтобы увидеть полный список команд 🤖\n'
                                      '*Место для вашей рекламы*', parse_mode='Markdown', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_msg(message):  # справка
    h = codecs.open("help.txt", encoding='utf-8')
    help = h.read()
    bot.send_message(message.chat.id, help, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):  # функция, вызывающая определённые функции после нажатия кнопок
    if call.data == "simple":
        simple(call.message)
    elif call.data == "combinatoric":
        combinatoric(call.message)
    elif call.data == "comb1":
        comb1(call.message)
    elif call.data == "comb2":
        comb2(call.message)
    elif call.data == "comb3":
        comb3(call.message)
    elif call.data == "ver_count_event":
        ver_count_event(call.message)
    elif call.data == "ver_count_event_step3_1":
        ver_count_event_step3_1(call.message)
    elif call.data == "ver_count_event_step3_2":
        ver_count_event_step3_2(call.message)
    elif call.data == "ver_count_event_step3_3":
        ver_count_event_step3_3(call.message)
    elif call.data == "discret_random_value":
        discret_random_value(call.message)
    elif call.data == "discret_random_value_step3_1":
        discret_random_value_step3_1(call.message)
    elif call.data == "discret_random_value_step3_2":
        discret_random_value_step3_2(call.message)
    elif call.data == "discret_random_value_step3_3":
        discret_random_value_step3_3(call.message)
    elif call.data == "discret_random_value_step3_4":
        discret_random_value_step3_4(call.message)
    elif call.data == "theory":
        theory(call.message)
    else:
        bot.send_message(call.message.chat.id, 'Пока не работает')


def send_error(bot_f, msg):  # отправление сообщения об ошибке
    bot_f.send_message(msg.chat.id,
                       'Что-то пошло не так ☹ '
                       'Возможно вам стоит проверить корректность введённых данных.\n'
                       'Попробуте снова👇')
    menu(msg)


@bot.message_handler(commands=['simple'])
def simple(message):  # подсчёт классической вероятности
    img = open('simple.png', 'rb')
    bot.send_photo(message.chat.id, img, caption='Вот формула простой вероятности👆')
    bot.send_message(message.chat.id, '🎯Введите целое число благоприятных событий:')
    bot.register_next_step_handler(message, simple_step1)


def simple_step1(message):
    global k
    try:
        k = int(message.text)
        if k < 0 or int(k) != k:
            raise ValueError
        bot.send_message(message.chat.id, 'Теперь введите общее количество событий (целое число):')
        bot.register_next_step_handler(message, simple_step2)
    except:
        send_error(bot, message)


def simple_step2(message):
    global n, k
    try:
        n = int(message.text)
        if n < 0 or int(n) != n:
            raise ValueError
        bot.send_message(message.chat.id, '*Результат*\nP = ' + str(k / n) +
                         ' (или P = ' + terver.reduce_fraction(k, n) + ')', parse_mode='Markdown')
        if k > n:
            bot.send_message(message.chat.id,
                             'Ни то чтобы я придираюсь, но число благоприятных '
                             'событий не может быть больше, чем общее число событий. '
                             'Но я всё-равно нашёл результат. '
                             'Его коректность остаётся на вашей совести.')
        menu(message)
    except:
        send_error(bot, message)


@bot.message_handler(commands=['combinatoric'])
def combinatoric(message):  # меню раздела комбинаторика
    img = open('combinatorics.jpg', 'rb')
    bot.send_photo(message.chat.id, img, caption='Основные формулы комбинаторики👆')
    keyboard1 = types.InlineKeyboardMarkup()
    key1_1 = types.InlineKeyboardButton(text='Число перестановок из n элементов', callback_data='comb1')
    keyboard1.add(key1_1)
    key1_2 = types.InlineKeyboardButton(text='Число размещений из n элементов по k элемнтов', callback_data='comb2')
    keyboard1.add(key1_2)
    key1_3 = types.InlineKeyboardButton(text='Число сочетаний из n элементов по k элемнтов', callback_data='comb3')
    keyboard1.add(key1_3)
    bot.send_message(message.chat.id, 'Что будем считать?', reply_markup=keyboard1)


@bot.message_handler(commands=['permutation'])
def comb1(message):  # расчёт числа перестановок
    bot.send_message(message.chat.id, 'Введите целое число n:')
    bot.register_next_step_handler(message, comb1_step1)


def comb1_step1(message):
    try:
        bot.send_message(message.chat.id, '*✅Решение*\nPn = n! = ' +
                         str(terver.count_permutation(int(message.text))), parse_mode='Markdown')
    except:
        send_error(bot, message)


@bot.message_handler(commands=['placement'])
def comb2(message):  # расчёт числа размещений
    bot.send_message(message.chat.id, 'n = ')
    bot.register_next_step_handler(message, comb2_step1)


def comb2_step1(message):
    global n
    try:
        n = int(message.text)
        bot.send_message(message.chat.id, 'k = ')
        bot.register_next_step_handler(message, comb2_step2)
    except:
        send_error(bot, message)


def comb2_step2(message):
    global n, k
    try:
        k = int(message.text)
        bot.send_message(message.chat.id, '*✅Решение*\nAnk = n! / (n - k)! = ' +
                         str(terver.count_placement(n, k)), parse_mode='Markdown')
        menu(message)
    except:
        send_error(bot, message)


@bot.message_handler(commands=['combinations'])
def comb3(message):  # вычисление числа сочетаний
    bot.send_message(message.chat.id, 'n = ')
    bot.register_next_step_handler(message, comb3_step1)


def comb3_step1(message):
    global n
    try:
        n = int(message.text)
        bot.send_message(message.chat.id, 'k = ')
        bot.register_next_step_handler(message, comb3_step2)
    except:
        send_error(bot, message)


def comb3_step2(message):
    global n, k
    try:
        k = int(message.text)
        bot.send_message(message.chat.id, '*✅Решение*\nCnk = n! / (n-k)!k! = ' +
                         str(terver.count_combinations(n, k)), parse_mode='Markdown')
        menu(message)
    except:
        send_error(bot, message)


def ver_count_event(message):  # раздел повторяющихся событий
    img = open('bernulli.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    img = open('laplas.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    img = open('puasson.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    bot.send_message(message.chat.id, 'Методы поиска вероятности повторяющихся событий👆\n\n'
                                      'Введите количество независимых испытаний: ')
    bot.register_next_step_handler(message, ver_count_event_step1)


def ver_count_event_step1(message):
    global n
    try:
        n = int(message.text)
        bot.send_message(message.chat.id,
                         'Укажите вероятность наступления события в каждом исптании'
                         ' (если известна вероятность, при которой случайное событие '
                         'не наступит, введите эту вероятность со знаком минус): ')
        bot.register_next_step_handler(message, ver_count_event_step2)
    except:
        send_error(bot, message)


def ver_count_event_step2(message):  # меню для выбора того, что нам необходимо найти
    global p
    try:
        p = float(message.text)
        if p < -1 or p > 1:
            raise ValueError
        if p < 0:
            bot.send_message(message.chat.id, 'p = 1 - q = ' + str(1 + p))
            p = 1 + p
        keyboard2 = types.InlineKeyboardMarkup()
        key2_1 = types.InlineKeyboardButton(text='Вероятность отдельного значения',
                                            callback_data='ver_count_event_step3_1')
        keyboard2.add(key2_1)
        key2_2 = types.InlineKeyboardButton(text='Вероятность диапазона значений',
                                            callback_data='ver_count_event_step3_2')
        keyboard2.add(key2_2)
        key2_3 = types.InlineKeyboardButton(text='Наивероятнейшее число событий',
                                            callback_data='ver_count_event_step3_3')
        keyboard2.add(key2_3)
        bot.send_message(message.chat.id, 'Вы хотите найти вероятность отдельного значения k'
                                          ', вероятность диапазона значений от k1 до k2 '
                                          'или наивероятнейшее число пройденных испытаний?', reply_markup=keyboard2)
    except:
        send_error(bot, message)


def ver_count_event_step3_1(message):
    bot.send_message(message.chat.id, 'k = ')
    bot.register_next_step_handler(message, ver_count_event_step4_1)


def ver_count_event_step4_1(message):
    global n, p, k
    try:
        k = int(message.text)
        if k < 0 or k > n:
            raise ValueError
        bot.send_message(message.chat.id, terver.ver_count_event_solve(n, p, k), parse_mode='Markdown')
        menu(message)
    except:
        send_error(bot, message)


def ver_count_event_step3_2(message):
    bot.send_message(message.chat.id, 'k1 = ')
    bot.register_next_step_handler(message, ver_count_event_step4_2)


def ver_count_event_step4_2(message):
    global k, n
    try:
        k = int(message.text)
        if k < 0 or k > n:
            raise ValueError
        bot.send_message(message.chat.id, 'k2 = ')
        bot.register_next_step_handler(message, ver_count_event_step5_2)
    except:
        send_error(bot, message)


def ver_count_event_step5_2(message):
    global n, p, k, k2
    try:
        k2 = int(message.text)
        if k2 < 0 or k2 > n:
            raise ValueError
        if k2 < k:
            bot.send_message(message.chat.id, 'Значение k2 не может быть меньше, чем k1.')
            menu(message)
        else:
            bot.s4end_message(message.chat.id, terver.ver_count_event_solve(n, p, k, k2), parse_mode='Markdown')
            menu(message)
    except:
        send_error(bot, message)


def ver_count_event_step3_3(message):
    global n, p
    q = 1 - p
    bot.send_message(message.chat.id, '*✅Решение*\nq = 1 - p = ' + str(q) +
                     '\nНайдём наивероятнейшее число успехов с помощью неравенства:\nnp-q <= k <= np+p\n'
                     + str(n * p - q) + ' <= k <= ' + str(n * p + p) + '\n*Ответ:' +
                     terver.most_probable_count(n, p) + '*', parse_mode='Markdown')
    menu(message)


@bot.message_handler(commands=['discret_random_value', 'math_expectation', 'dispersion', 'mean_square_deviation'])
def discret_random_value(message):
    bot.send_message(message.chat.id, 'Введите значения x одной строкой через пробел:')
    bot.register_next_step_handler(message, discret_random_value_step1)


def discret_random_value_step1(message):
    global x_a
    try:
        x_a = list(map(float, message.text.split()))
        bot.send_message(message.chat.id, 'Введите значения p одной строкой через пробел:')
        bot.register_next_step_handler(message, discret_random_value_step2)
    except:
        send_error(bot, message)


def discret_random_value_step2(message):
    global x_a, p_a
    try:
        p_a = list(map(float, message.text.split()))
        if len(p_a) != len(x_a):
            bot.send_message(message.chat.id, 'Количество значений p и x не совпадает. ')
            raise ValueError
        elif sum(p_a) != 1:
            bot.send_message(message.chat.id, 'Сумма всех вероятностей должна быть равна 1.')
            raise ValueError
        keyboard4 = types.InlineKeyboardMarkup()
        key4_1 = types.InlineKeyboardButton(text='Математическое ожидание',
                                            callback_data='discret_random_value_step3_1')
        keyboard4.add(key4_1)
        key4_2 = types.InlineKeyboardButton(text='Дисперсию',
                                            callback_data='discret_random_value_step3_2')
        keyboard4.add(key4_2)
        key4_3 = types.InlineKeyboardButton(text='Среднее квадратическое отклонение',
                                            callback_data='discret_random_value_step3_3')
        keyboard4.add(key4_3)
        key4_4 = types.InlineKeyboardButton(text='Всё вышеперечисленное👆',
                                            callback_data='discret_random_value_step3_4')
        keyboard4.add(key4_4)
        bot.send_message(message.chat.id, 'Что будем искать?🔎', reply_markup=keyboard4)
    except:
        send_error(bot, message)


def discret_random_value_step3_1(message):
    global x_a, p_a
    bot.send_message(message.chat.id, '*✅Решение*\nM(X) = Σxipi = ' + str(terver.math_expectation(p_a, x_a)))
    menu(message)


def discret_random_value_step3_2(message):
    global x_a, p_a
    x2 = list(map(lambda x: x * x, x_a))
    m = terver.math_expectation(p_a, x_a)
    d = terver.dispersion(p_a, x_a)
    m2 = terver.math_expectation(p_a, x2)
    bot.send_message(message.chat.id, '*✅Решение*\nM(X) = Σxipi = ' + str(m) + '\nM(x)^2 = ∑(xi)^2⋅pi' + str(m * m) +
                     '\nM(x^2) = ' + str(m2) + '\nD(X) = M(X^2)−[M(X)]^2 = ' + str(d) + '\n*Ответ: ' + str(d) + '.*',
                     parse_mode='Markdown')
    menu(message)


def discret_random_value_step3_3(message):
    global x_a, p_a
    x2 = list(map(lambda x: x * x, x_a))
    m = terver.math_expectation(p_a, x_a)
    d = terver.dispersion(p_a, x_a)
    q = terver.mean_square_deviation(p_a, x_a)
    m2 = terver.math_expectation(p_a, x2)
    bot.send_message(message.chat.id, '*✅Решение*\nM(X) = Σxipi = ' + str(m) + '\nM(x)^2 = ∑(xi)^2⋅pi = ' +
                     str(m * m) + '\nM(x^2) = ' + str(m2) + '\nD(X) = M(X^2)−[M(X)]^2 = ' + str(d) +
                     '\nσ(X) = √D(X) = ' + str(q) + '\n*Ответ: ' + str(q) + '.*', parse_mode='Markdown')
    menu(message)


def discret_random_value_step3_4(message):
    global x_a, p_a
    x2 = list(map(lambda x: x * x, x_a))
    m = terver.math_expectation(p_a, x_a)
    d = terver.dispersion(p_a, x_a)
    q = terver.mean_square_deviation(p_a, x_a)
    m2 = terver.math_expectation(p_a, x2)
    bot.send_message(message.chat.id, '*✅Решение*\nM(X) = Σxipi = *' + str(m) + '*\nM(x)^2 = ∑(xi)^2⋅pi = ' +
                     str(m * m) + '\nM(x^2) = ' + str(m2) + '\nD(X) = M(X^2)−[M(X)]^2 = *' + str(d) +
                     '*\nσ(X) = √D(X) = *' + str(q) + '*', parse_mode='Markdown')
    menu(message)


@bot.message_handler(commands=['theory'])
def theory(message):
    t = codecs.open("theory.txt", encoding='utf-8').read().split('%')
    bot.send_message(message.chat.id, t[0], parse_mode='Markdown')
    img = open('simple.png', 'rb')
    bot.send_photo(message.chat.id, img, caption='Вот формула простой вероятности👆')
    bot.send_message(message.chat.id, t[1], parse_mode='Markdown')
    img = open('combinatorics.jpg', 'rb')
    bot.send_photo(message.chat.id, img, caption='Основные формулы комбинаторики👆')
    bot.send_message(message.chat.id, t[2], parse_mode='Markdown')
    bot.send_message(message.chat.id, t[3], parse_mode='Markdown')
    img = open('bernulli.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    img = open('laplas.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    img = open('puasson.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    bot.send_message(message.chat.id, t[4], parse_mode='Markdown')
    menu(message)


@bot.message_handler(commands=['feedback'])
def feedback(message):
    bot.send_message(message.chat.id, 'Оставьте отзыв о работе бота сообщением👇')
    bot.register_next_step_handler(message, feedback_step1)


def feedback_step1(message):
    if message.from_user.username not in config.BLOCK_USER_LIST:
        bot.send_message(config.FEEDBACK_CHAT_ID,
                         'Отзыв от пользователя @{0.username}:\n\n{1}'.format(message.from_user,
                                                                              message.text))
        bot.send_message(message.chat.id, 'Ваш отзыв отправлен. Спасибо за обратную связь❤')
        menu(message)
    else:
        bot.send_message(message.chat.id, 'Администратор ограничил вашу возможность отправлять обратную связь❌')
        menu(message)


@bot.message_handler(commands=['kill'])
def kill(message):
    if message.from_user.username in config.ADMIN_LIST:
        bot.send_message(message.chat.id, 'Введите имя пользователя, которого, хотите заблокировать:')
        bot.register_next_step_handler(message, kill_step1)
    else:
        bot.send_message(message.chat.id, 'Данная команда доступна только администраторам бота!')
        menu(message)


def kill_step1(message):
    config.BLOCK_USER_LIST.append(message.text)
    bot.send_message(message.chat.id, 'Пользователь @' + message.text
                     + ' теперь не может отправлять сообщения обратной связи.')


@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.chat.id, '*ТерВерБот*\nВерсия: ' + config.VERSION + '\nДата релиза: '
                     + config.RELEASE_DATE + '\nРезработчик бота: @yan_minotskiy\nКод и другая информация: '
                                             'https://github.com/Yan-Minotskiy/TerVerBot')


@bot.message_handler(content_types=['text', 'document', 'audio', 'video',
                                    "sticker", "pinned_message", "photo", 'voice'])
def answer(message):
    sti1 = open('sti1.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti1)
    bot.send_message(message.chat.id, 'Я пока не научился понимать это')
    menu(message)


bot.polling(none_stop=True)
