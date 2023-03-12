import vk_api
import database
from datetime import date
token = "vk1.a.07rHbbJwwXNuw6G57_fYTPztuM_YDYZAtkJGAUsJClesxa2CagyoMsU8ZSonIefjlQFFpT9nIGxxJQ9rm_TuPDiI3UbdVIY6Zq1TlYiwYCohnVURXXJ2Ul-DdlZSBqQFljPWyKjlZJTVm7C-su6fMPDmY_Ejo1SwUqHPrncH-iB9moew54Hz0WZxv_JtiPQO1pXEugC7qr2VeSdH60-iNQ"  # В ковычки вставляем аккуратно наш ранее взятый из группы токен.
token1 = "vk1.a.DORfAY-ITv15OOeopjNGLpGXe8b93O3NvCqWTKEIFez4emjJ_al1_H6w-HrvQAzVJCSzmpZ3M4_F0RdfR9P5jx6zZfqgIPilx2Fux9ovGOcoAx4osHv2oaxNXIWMmUHvBXkyE5srEhAWPQfCsSKTa2j8t5fS9uqy92fw8N3yjibjF9IIVmJiy5k9gafFI_pRY_0osB8e2wpRfRlOORxx6g"
# Подключаем токен и longpoll
vk = vk_api.VkApi(token=token)
vk1 = vk_api.VkApi(token=token1)
#import time
def bot_write_foto(id, text,url):
    if url == 'none':
        vk.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})
    else:
        vk.method('messages.send', {'user_id': id, 'message': text, "attachment": url, 'random_id': 0})


    #######################################

def photos_partner(id,nomer):
        partner_users = vk1.method("photos.get", {"owner_id": id,"rev": 0 ,"count": 3,"offset" : 0, "extended": 1, "album_id": "wall"})
        phot = partner_users["items"]
       #print(partner_users['count']) # количество фото
        return partner_users['count'], phot # кол-во фото и ссылка на фото






def vvesti_sex_user(message):
    bot_write_foto(id, "Вы мужчина или женщина (2/1)?", 'none')
    input()
    if (int(message) == 1) or (int(message) == 2):
        if int(message) == 2:  # пол пользователя
            sex_user = 1
        elif int(message) == 1:
            sex_user = 2
        return sex_user
    else:
        vvesti_sex_user(message)
        return


def vvesti_city_user(message):
    bot_write_foto(id, "Введите название города", 'none')
    input()
    if not(message.isdigit()):


        city_id = vk.method("database.getCities",{message})
        city_user = city_id
        return city_user  # Проверка существования города ?!?!?!?!?

    else:
        vvesti_city_user(message)

        return




def user_data1(id):

    user = vk.method("users.get", {"user_ids": id, 'fields': 'city,relation, sex,photo_50,bdate'})
    first_name_user = user[0]['first_name']  # имя пользователя

    last_name_user = user[0]['last_name']  # фамилия пользовател


    try:
       current_date = date.today()
       date_of_birth = int(current_date.year) - int(user[0]['bdate'][-4:]) #   Возраст пользователя( вычисляется не точно)
    except:
        date_of_birth = "нет данных"

    try:
        sex_user = user[0]['sex']
    except:
        sex_user = "нет данных"

    try:
        city_user = user[0]['city']['title']                              #user[0]['city']['title']  # город пользователя
    except:
        city_user = "нет данных"

    try:
        relation_user = user[0]['relation']
    except:
        relation_user = "нет данных"


    photo_50_user = user[0]['photo_50']


    return first_name_user, last_name_user, date_of_birth, sex_user, city_user, relation_user, photo_50_user




def partner_search(id,city_user,date_of_birth,sex_user,nomer):           # поиск подходящих людей

    age_from = date_of_birth-5  # возростной диапазон
    age_to = date_of_birth+5
    user_partner = []
    max_reseah_partner = 10
    for nomer in range(0, max_reseah_partner):
        user_partner = vk1.method("users.search", {'age_from': age_from, 'age_to': age_to, 'is_closed': "false",
                                               'count': 1000, 'sex':  sex_user, 'city': city_user, 'offset': nomer })
        print(user_partner)
        if user_partner['items'][0]['is_closed']:
          nomer = nomer +1
        else:
          database.insert_users_partner(int(user_partner['items'][0]['id']), int(0))


def main_function(id,event, nomer, nomer1,status, city_user, date_of_birth, sex_user,status_poisk):

        #qwert = user_data1(id)
        #partner_search(id, city_user, date_of_birth, sex_user, nomer)
        #partner_search(id, qwert[7], qwert[2], qwert[3], nomer)
        new_partners = database.select_users_partner(status_poisk)  ##########################################
        zzzz = photos_partner(new_partners[0][0], nomer)
        print(zzzz)

        if int(zzzz[0]) >= 3:
            number_of_photo = 3
        else:
            number_of_photo = (int(zzzz[0]) - 1)

        qqqq = (user_data1(new_partners[0][0]))

        bot_write_foto(id, f"ЗНАКОМЬТЕСЬ:  {qqqq[0] + '    ' + qqqq[1]}", 'none')
        bot_write_foto(event.user_id, f"ЛЕТ :   {qqqq[2]}", 'none')
        bot_write_foto(event.user_id, f"Город :   {qqqq[4]}", 'none')
        bot_write_foto(event.user_id, f" Семейное положение :   {qqqq[5]}", 'none')
        bot_write_foto(id, f"Адрес страницы:  https://vk.com/id{new_partners[0][0]}", 'none')
        #bot_write(event.user_id, f" Пол:   {qqqq[3]}")

        for j in range(0, number_of_photo):
            zzzz = photos_partner(new_partners[0][0], j)
            try:
               bot_write_foto(id, f"ФОТО № {j + 1}", zzzz[1][j]['sizes'][4]['url'])  # цифра 4 это размер фото
            except(IndexError):
               bot_write_foto(id, f"ФОТО № {j + 1}", zzzz[1][j]['sizes'][1]['url'])   # частая ошибка (размер фото)
        bot_write_foto(event.user_id, "Продолжить : q    В черный список : w     В избранное : e ", 'none')
        #nomer = nomer + 1
        #zzzz = photos_partner(new_partners[0][0], 2)
        #new_partners = database.select_users_partner(status_poisk)
        if nomer1 == 1:
              database.update_users_partner(new_partners[0][0], status)

       # partner_search(id, qwert[7], qwert[2], qwert[3], nomer)
        #partner_search(id, city_user,date_of_birth,sex_user,nomer)


