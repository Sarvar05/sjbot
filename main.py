# base requirements
import time
import traceback
import re
from datetime import datetime
import pytz


# telegram methods
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from telegram.ext import (
    CallbackContext,
    Updater,
    CommandHandler,
    ConversationHandler,
    InlineQueryHandler,
    ChosenInlineResultHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)

from telegram.utils import helpers

# configuration
from config.config import *
# get db connect functions
from db.db_helper import DBHelper


def main_buttons(is_author=False):
    if is_author:
        return [
            [InlineKeyboardButton('Test yaratish', callback_data='create')],
            [InlineKeyboardButton('Yaratilgan Testlar', callback_data='my_tests')],
            [InlineKeyboardButton('Javoblarini tekshirish', callback_data='check')]
        ]
    else:
        return [
            [InlineKeyboardButton('Test yaratish', callback_data='create')],
            [InlineKeyboardButton('Javoblarini tekshirish', callback_data='check')]
        ]


def home_button():
    return [
        [InlineKeyboardButton('Bosh menyu', callback_data='home')]
    ]


def my_tests_buttons(tests):
    buttons = []

    for test in tests:
        buttons.append([
            InlineKeyboardButton(test['name'], callback_data='test-' + str(test['id']))
        ])

    buttons.append(
        [
            # InlineKeyboardButton('Ortga', callback_data='back'),
            InlineKeyboardButton('Bosh menyu', callback_data='home')
        ]
    )

    return buttons


def solve_button(url):

    return [
        [InlineKeyboardButton('Testni tekshirish', url=url)]
    ]


def test_buttons(test_id, status=True):
    buttons = [
        [InlineKeyboardButton('Bosh menyu', callback_data='home')],
    ]

    if status:
        buttons.append([InlineKeyboardButton('Yuborish', switch_inline_query='share-' + str(test_id))])

    return buttons

def start(update, context):
    print('start')
    try:
        db = DBHelper()
        query = update.callback_query
        if query is not None:
            telegram_id = query.message.chat.id
            user = db.get('users', telegram_id)

            if user:
                if user.get('full_name') is not None:
                    query.message.reply_html(
                        GREETING_TEXT.format(user['full_name']),
                        reply_markup=InlineKeyboardMarkup(main_buttons(user['is_author']))
                    )
                    return STATE_MAIN
            else:
                db.insert('users', {'id': telegram_id})

            query.message.reply_html(
                ASK_NAME
            )
            return STATE_ASK_NAME

        else:
            telegram_id = update.message.chat.id
            user = db.get('users', telegram_id)

            if user:
                if user.get('full_name') is not None:
                    update.message.reply_html(
                        GREETING_TEXT.format(user['full_name']),
                        reply_markup=InlineKeyboardMarkup(main_buttons(user['is_author']))
                    )
                    return STATE_MAIN
            else:
                db.insert('users', {'id': telegram_id})

            update.message.reply_html(
                ASK_NAME
            )
            return STATE_ASK_NAME

    except Exception as e:
        print(traceback.format_exc())

def home(update, context):
    print('home')
    try:
        db = DBHelper()
        query = update.callback_query
        if query is not None:
            telegram_id = query.message.chat.id
            user = db.get('users', telegram_id)

            if user:
                if user.get('full_name') is not None:
                    query.message.reply_html(
                        GREETING_TEXT.format(user['full_name']),
                        reply_markup=InlineKeyboardMarkup(main_buttons(user['is_author']))
                    )
                    return STATE_MAIN
            else:
                db.insert('users', {'id': telegram_id})

            query.message.reply_html(
                ASK_NAME
            )
            return STATE_ASK_NAME
    except Exception as e:
        print(traceback.format_exc())


def ask_name(update, context):
    print('ask_name')
    try:
        db = DBHelper()
        if update.message.text is not None:

            full_name = " ".join(update.message.text.strip().split())

            if bool(re.fullmatch('[A-Za-z]{3,25}[ ][A-Za-z]{3,25}', full_name)):
                telegram_id = update.message.chat.id
                db.update('users', telegram_id, {'full_name': full_name})
                user = db.get('users', telegram_id)
                update.message.reply_html(
                    GREETING_TEXT.format(full_name),
                    reply_markup=InlineKeyboardMarkup(main_buttons(user['is_author']))
                )
                return STATE_MAIN
            else:
                update.message.reply_html('Iltimos Ism familiyangizni to\'liq kiriting.')
        else:
            update.message.delete()
    except Exception as e:
        print(traceback.format_exc())


def menu(update, context):
    print('menu')
    try:
        query = update.callback_query
        if query is not None:
            data = query.data
            state = STATE_MAIN
            if data == 'create':
                query.message.edit_text(
                    TEST_CREATE_TEXT,
                    reply_markup=InlineKeyboardMarkup(home_button()),
                    parse_mode='html'
                )
                state = STATE_CREATE_TEST

            elif data == 'check':
                query.message.edit_text(
                    CHECK_TEST_TEXT,
                    reply_markup=InlineKeyboardMarkup(home_button()),
                    parse_mode='html'
                )
                state = STATE_CHECK_TEST
            elif data == 'my_tests':
                db = DBHelper()
                telegram_id = query.message.chat.id
                tests = db.get_all('tests', {'author_id': telegram_id})
                if tests:
                    query.message.edit_text(
                        MY_TESTS_TEXT,
                        reply_markup=InlineKeyboardMarkup(my_tests_buttons(tests)),
                        parse_mode='html'
                    )
                    state = STATE_MY_TESTS
                else:
                    query.answer(text="Hali birorta test yaratmagansiz", show_alert=True)
            query.answer()
            return state
        elif update.message is not None:
            update.message.delete()
    except Exception as e:
        print(traceback.format_exc())


def create_test(update, context):
    print('create_test')
    try:
        query = update.callback_query
        db = DBHelper()

        if query is not None:
            data = query.data
            if data == 'home':
                telegram_id = query.message.chat.id
                user = db.get('users', telegram_id)

                query.message.edit_text(
                    GREETING_TEXT.format(user['full_name']),
                    reply_markup=InlineKeyboardMarkup(main_buttons(user['is_author'])),
                    parse_mode='html'
                )
                query.answer()
                return STATE_MAIN
        elif update.message.text is not None:

            telegram_id = update.message.chat.id
            test_data = update.message.text.split('*')

            if len(test_data) == 4:
                test_title = test_data[0]
                test_count = test_data[1]
                test_time = test_data[2]
                test_answers = test_data[3]

                errors = []

                if not test_count.isnumeric():
                    errors.append('Test soni no\'to\'g\'ri kiritildi')

                if not test_time.isnumeric():
                    errors.append('Test vaqti no\'to\'g\'ri kiritildi')

                if not len(test_answers) == int(test_count):
                    errors.append('Test javoblari no\'to\'g\'ri kiritildi')

                if len(errors) != 0:
                    update.message.reply_html(
                        "<b>Quyidagi xatoliklarni bartaraf etib qayta kiriting</b>:\n\n" + "\n".join(errors))
                else:
                    test_id = db.insert('tests', {
                        'name': test_title,
                        'count_tests': int(test_count),
                        'test_time': int(test_time),
                        'answers': test_answers,
                        'created_at': int(time.time()),
                        'author_id': int(telegram_id)
                    })

                    if test_id:
                        db.update('users', telegram_id, {'is_author': True})

                        context.job_queue.run_once(generate_report, int(test_time) * 60, context=test_id)

                        update.message.reply_html(
                            TEST_CREATED_SUCCESSFULLY.format(test_title, test_count, test_time, test_id),
                            reply_markup=InlineKeyboardMarkup(test_buttons(test_id))
                        )
                    else:
                        update.message.reply_html(
                            ERROR_TEXT.format(ADMIN),
                        )
            else:
                update.message.reply_html('Ko\'rsatilgan ko\'rinishda kiriting.')
                update.message.reply_html(
                    TEST_CREATE_TEXT,
                    reply_markup=InlineKeyboardMarkup
                )
        else:
            update.message.delete()
    except Exception as e:
        print(traceback.format_exc())


def check_test(update, context):
    print('check_test')
    try:
        query = update.callback_query
        db = DBHelper()

        if query is not None:
            data = query.data
            if data == 'home':
                telegram_id = query.message.chat.id
                user = db.get('users', telegram_id)
                query.message.edit_text(
                    GREETING_TEXT.format(user['full_name']),
                    reply_markup=InlineKeyboardMarkup(main_buttons(user['is_author'])),
                    parse_mode='html'
                )
                query.answer()
                return STATE_MAIN
        elif update.message.text is not None:
            test_data = update.message.text.split('*')

            if len(test_data) == 2:
                telegram_id = update.message.chat.id
                user = db.get('users', telegram_id)

                test_id = test_data[0]
                test_answers = test_data[1]

                errors = []

                if not test_id.isnumeric():
                    errors.append('Test soni no\'to\'g\'ri kiritildi')

                if len(errors) == 0:
                    test = db.get('tests', test_id)
                    result = db.check_result_exists(telegram_id, test_id)
                    if not test:
                        update.message.reply_html(
                            "Kiritilgan {} ID li test aniqlanmadi!".format(test_id)
                        )
                    elif test['created_at'] + 60 * test['test_time'] < int(time.time()):
                        update.message.reply_html(
                            "Ushbu test allaqachon yakunlangan!"
                        )
                    elif result:
                        update.message.reply_html(
                            "Siz allaqachon ushbu testda qatnashgansiz!"
                        )
                    elif test['count_tests'] != len(test_answers):
                        update.message.reply_html(
                            "<b>Quyidagi xatoliklarni bartaraf etib qayta kiriting</b>:\n\n" + "Javoblar to\'liq kiritilmadi!"
                        )
                    else:

                        count = 0

                        for i in range(0, len(test_answers)):
                            if test_answers[i] == test['answers'][i]:
                                count = count + 1

                        result_id = db.insert('results', {
                            'test_id': int(test_id),
                            'user_id': int(telegram_id),
                            'result_str': test['answers'] + '|' + test_answers,
                            'correct_answers_count': count,
                            'test_time': int(time.time()) - int(test['created_at'])
                        })

                        if result_id:
                            context.bot.send_message(
                                chat_id=test['author_id'],
                                parse_mode='html',
                                text=TEST_RESULT_TEXT.format(
                                    result['test_name'],
                                    result['count_tests'],
                                    str(round(result['test_time'] / 60)) + ' daqiqa ' + str(
                                        round(result['test_time'] % 60)) + ' soniya',
                                    result['test_id'],
                                    result['full_name'],
                                    generate_user_result(test_answers, test['answers']),
                                    result['correct_answers_count']
                                )
                            )

                            at_time = test['created_at'] + test['test_time'] * 60

                            utc_moment_naive = datetime.utcfromtimestamp(at_time)
                            utc_moment = utc_moment_naive.replace(tzinfo=pytz.utc)
                            finished_time = utc_moment.astimezone(pytz.timezone('Asia/Tashkent')).strftime("%H:%M:%S %m/%d/%Y")

                            update.message.reply_html(
                                "Natijalarni {} dan keyin ko'rishingiz mumkin.".format(finished_time)
                            )

                            context.job_queue.run_once(send_results, at_time - time.time(), context=result_id)
                        else:
                            update.message.reply_html(
                                ERROR_TEXT.format(ADMIN),
                            )
                else:
                    update.message.reply_html(
                        "<b>Quyidagi xatoliklarni bartaraf etib qayta kiriting</b>:\n\n" + "\n".join(errors))

            else:
                update.message.reply_html('Ko\'rsatilgan ko\'rinishda kiriting.')
                update.message.reply_html(
                    CHECK_TEST_TEXT,
                    reply_markup=InlineKeyboardMarkup(home_button()),
                )
        else:
            update.message.delete()
    except Exception as e:
        print(traceback.format_exc())


def my_tests(update, context):
    print('my_tests')
    try:
        query = update.callback_query
        if query is not None:
            data = query.data.split('-')
            db = DBHelper()
            state = STATE_MY_TESTS
            if data[0] == 'home':
                telegram_id = query.message.chat.id
                user = db.get('users', telegram_id)
                query.message.edit_text(
                    GREETING_TEXT.format(user['full_name']),
                    reply_markup=InlineKeyboardMarkup(main_buttons(user['is_author'])),
                    parse_mode='html'
                )
                state = STATE_MAIN
            elif data[0] == 'back':
                telegram_id = query.message.chat.id
                tests = db.get_all('tests', {'author_id': telegram_id})
                query.message.edit_text(
                    MY_TESTS_TEXT,
                    reply_markup=InlineKeyboardMarkup(my_tests_buttons(tests)),
                    parse_mode='html'
                )
                state = STATE_MY_TESTS
            elif data[0] == 'test':
                test = db.get_test(data[1])
                query.message.edit_text(
                    TEST_VIEW_TEXT.format(
                        test['name'],
                        test['author'],
                        test['count_tests'],
                        test['test_time'],
                        test['participants_count'],
                        test['id']
                    ),
                    reply_markup=InlineKeyboardMarkup(test_buttons(data[1], test['status']))
                )

            query.answer()
            return state
        elif update.message is not None:
            update.message.delete()
    except Exception as e:
        print(traceback.format_exc())


def inlinequery(update, context):
    print('inlinequery')
    try:
        """Handle the inline query."""
        query = update.inline_query.query

        db = DBHelper()
        split = query.split('-')
        results = []

        test = db.get('tests', int(split[1]))

        url = helpers.create_deep_linked_url(context.bot.username, 'check-test')

        results.append(InlineQueryResultArticle(
            id=split[1],
            title=test['name'],
            # description='shifr: ' + department['code'],
            input_message_content=InputTextMessageContent(
                message_text=TEST_INTRO_VIEW_TEXT.format(
                        test['name'],
                        test['count_tests'],
                        test['test_time'],
                        test['id']
                    ),
            ),
            reply_markup=InlineKeyboardMarkup(solve_button(url))
        ))
        update.inline_query.answer(results=results, next_offset=None, cache_time=5)

    except Exception as e:
        print(traceback.format_exc())


def catch_query(update, context):
    print('catch_query')
    try:
        # print(update)
        from_user = update.chosen_inline_result.from_user
        inline_result = update.chosen_inline_result
        result_id = str(inline_result.result_id)
        query = inline_result.query
        db = DBHelper()

        split = query.split('-')

        return CHECK_TEST_TEXT

    except Exception as e:
        print(traceback.format_exc())


def generate_user_result(user_answers, correct_answers):
    text = ''
    for i in range(0, len(user_answers)):
        if user_answers[i] == correct_answers[i]:
            text = text + "\n" + str(i + 1) + ".  " + user_answers[i] + "  ✅"
        else:
            text = text + "\n" + str(i + 1) + ".  " + user_answers[i] + "  ❓"

    return text


def send_results(context: CallbackContext):
    db = DBHelper()
    result = db.get_result(context.job.context)

    if result:
        answers = result['result_str'].split('|')

        correct_answers = answers[0]
        user_answers = answers[1]

        text = generate_user_result(user_answers, correct_answers)

        context.bot.send_message(
            chat_id=result['user_id'],
            parse_mode='html',
            text=TEST_RESULT_TEXT.format(
                result['test_name'],
                result['count_tests'],
                str(round(result['test_time'] / 60)) + ' daqiqa ' + str(round(result['test_time'] % 60)) + ' soniya',
                result['test_id'],
                result['full_name'],
                text,
                result['correct_answers_count']
            )
        )


def generate_report(context: CallbackContext):
    db = DBHelper()
    test_id = context.job.context
    db.update('tests', test_id, {'status': 0})

    test = db.get('tests', test_id)
    results = db.get_results(test_id)

    text = ''

    if results:
        for i in range(0, len(results)):
            text = text + "\n" + str(i + 1) + ". " + str(results[i]['full_name']) + "\t" + str(results[i]['correct_answers_count']) + "\t" + str(round(results[i]['test_time'] / 60)) + ' daqiqa ' + str(round(results[i]['test_time'] % 60)) + ' soniya'

        context.bot.send_message(
            chat_id=test['author_id'],
            parse_mode='html',
            text=TOTAL_TEST_RESULTS_TEXT.format(
                test['name'],
                test['count_tests'],
                len(results),
                test['test_time'],
                test['id'],
                text,
            )
        )


def main():
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CallbackQueryHandler(start), MessageHandler(Filters.all, start)],
        states={
            STATE_START: [
                CommandHandler('start', start)
            ],
            STATE_ASK_NAME: [
                CommandHandler('start', start),
                MessageHandler(Filters.text, ask_name)
            ],
            STATE_MAIN: [
                CommandHandler('start', start),
                MessageHandler(Filters.text, menu),
                CallbackQueryHandler(menu)
            ],
            STATE_CHECK_TEST: [
                CommandHandler('start', start),
                CallbackQueryHandler(check_test),
                MessageHandler(Filters.text, check_test)
            ],
            STATE_CREATE_TEST: [
                CommandHandler('start', start),
                CallbackQueryHandler(create_test),
                MessageHandler(Filters.text, create_test)
            ],
            STATE_MY_TESTS: [
                CommandHandler('start', start),
                CallbackQueryHandler(my_tests),
                MessageHandler(Filters.text, my_tests)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", home, Filters.regex('check-test')))
    dispatcher.add_handler(conversation_handler)

    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    dispatcher.add_handler(ChosenInlineResultHandler(catch_query))

    updater.start_polling(drop_pending_updates=True)
    updater.idle()


if __name__ == '__main__':
    main()
