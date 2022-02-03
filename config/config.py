TOKEN = '5182163593:AAH-IGm21twRRfXlpZZQcqUC1dKPbC8KRWw'

ADMIN = '@akbarov_dev'

STATE_START = '0'
STATE_ASK_NAME = '1'
STATE_MAIN = '2'
STATE_CREATE_TEST = '3'
STATE_CHECK_TEST = '4'
STATE_MY_TESTS = '5'

ASK_NAME = 'Iltimos ism familiyangizni kiriting'

GREETING_TEXT = '''Assalomu alaykum <b>{}</b>, Xush kelibsiz!
Bu bot online testlar uchun
yaratilgan.

🖊️ Ismingizni uzgartirish uchun
/edit ni bosing.'''

TEST_CREATE_TEXT = '''<b>Yaratish uchun</b>:

misol: <i>fan_nomi*savollar_soni*ajratilganvaqti(minutda)*javob_lar</i>

namuna: Matematika*10*20*abacdcbac....

Shu koʻrinishda yozing.'''

CHECK_TEST_TEXT = '''<b>Javoblarni tekshirish uchun</b>:

misol: <i>test_kodi*javoblar</i>

namuna: 1234*abcabadacb...

Shu koʻrinishda yoʻboring.'''

TEST_CREATED_SUCCESSFULLY = '''<b>Test bazaga qushildi</b>

Fan nomi: <i>{}</i>

Testlar soni: <i>{}</i> ta

Ajratilgan vaqt: <i>{}</i> daqiqa 

Test kodi: <i>{}</i>

Test ishlanishga tayyor!!!'''

TEST_INTRO_VIEW_TEXT = ''' 
Fan nomi: {}

Testlar soni: {} ta

Ajratilgan vaqti: {} daqiqa

Test kodi: {}

Test ishlanishga tayyor!!!'''


TEST_VIEW_TEXT = ''' 
Fan nomi: {}

Test yaratuvchisi: {}

Testlar soni: {} ta

Ajratilgan vaqti: {} daqiqa

Qatnashganlar soni: {} ta
 
Test kodi: {}

Test ishlanishga tayyor!!!'''

MY_TESTS_TEXT = '''
Sizni muallifligingizdagi testlar.
'''

ERROR_TEXT = '''
Xatolik yuz berdi. /start bosib qayta urinib ko'ring yoki {} bilan bog'laning. Rahmat.
'''

TEST_RESULT_TEXT = '''
<b>Testga natijalari</b>
 
Fan nomi: {}
Savollar soni: {} ta 
Sarflangan vaqti: {} daqiqa
Test kodi: {}
Ismi: {}

<b>Natijalari</b>:
{}


Toʻgʻri javob soni {} ta
'''

TOTAL_TEST_RESULTS_TEXT = '''
<b>Testga natijalari</b>
 
Fan nomi: {}
Savollar soni: {} ta 
Qatnashganlar soni: {} ta
Ajratilgan vaqti: {} ta
Test kodi: {}

<b>Natijalari</b>:
{}

'''