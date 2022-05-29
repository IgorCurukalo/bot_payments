from main import bot, dp, anti_flood, user_db
from aiogram.types import Message

def seconds_to_words(second: int) -> str:
    intervals = ['пользователь','пользователя','пользователей']
    result = []
    listday = list(str(second).split())
    if (len(listday) > 1 and listday[len(listday)-1] == 1 and listday[len(listday)-2] != 1) or (second == 1):
        name_ = intervals[0]
    if (len(listday) > 1 and listday[len(listday)-1] not in (0,1,5,6,7,8,9)) or (second not in (0,1,5,6,7,8,9)):
        name_ = intervals[1]
    if (len(listday) > 1 and listday[len(listday)-1] not in (1,2,3,4)) or (second not in (1,2,3,4)):
        name_ = intervals[2]
    result.append("{} {}".format(second, name_))
    return ' '.join(result)

@dp.message_handler(commands=['start'])
async def menu_command(m: Message):
    user_ref = 0 if len(m.text.split()) < 2 else m.text.split()[1]
    print(m.text)
    count = user_db.count_ref(user_ref=user_ref)
    end = seconds_to_words(count)
    if user_db.add_new_user(user_id=m.from_user.id, user_name=m.from_user.first_name, user_ref=user_ref):
        return await m.answer(f'Добро пожаловать, вы пригласили №: {end}')
    return await m.answer(f'Вы тут уже были, всего приглашенных по данной ссылке: {end}')

@dp.message_handler(commands=['ref'])
async def ref_func(m: Message):
    link = "https://t.me/cingcingbotbot?start=" + str(m.from_user.id)
    return await m.answer("Ваша реф ссылка"+link)