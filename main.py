import bot
from datetime import date
# Импортируем библиотеку vk_api
import vk_api
# Достаём из неё longpoll
from vk_api.longpoll import VkLongPoll, VkEventType

token = "vk1.a.07rHbbJwwXNuw6G57_fYTPztuM_YDYZAtkJGAUsJClesxa2CagyoMsU8ZSonIefjlQFFpT9nIGxxJQ9rm_TuPDiI3UbdVIY6Zq1TlYiwYCohnVURXXJ2Ul-DdlZSBqQFljPWyKjlZJTVm7C-su6fMPDmY_Ejo1SwUqHPrncH-iB9moew54Hz0WZxv_JtiPQO1pXEugC7qr2VeSdH60-iNQ"  # В ковычки вставляем аккуратно наш ранее взятый из группы токен.
token1 = "vk1.a.DORfAY-ITv15OOeopjNGLpGXe8b93O3NvCqWTKEIFez4emjJ_al1_H6w-HrvQAzVJCSzmpZ3M4_F0RdfR9P5jx6zZfqgIPilx2Fux9ovGOcoAx4osHv2oaxNXIWMmUHvBXkyE5srEhAWPQfCsSKTa2j8t5fS9uqy92fw8N3yjibjF9IIVmJiy5k9gafFI_pRY_0osB8e2wpRfRlOORxx6g"

vk = vk_api.VkApi(token=token)
vk1 = vk_api.VkApi(token=token1)
nomer = 0
nomer_marker = 0
longpoll = VkLongPoll(vk)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        message = event.text.lower()
        nomer1 = 0

        if event.to_me:
            message = event.text.lower()
            id = event.user_id



            pfoto1 = bot.photos_partner(id, nomer1)
            if (event.to_me) and (nomer_marker == 0):

                nomer_marker = 0
                qqqq = vk.method("users.get", {"user_ids": id, 'fields': 'city,relation, sex,photo_50,bdate'})
               # qqqq = (bot.user_data(id))
                bot.bot_write_foto(id, f"Здравствуйте, {qqqq[0]['first_name']}", 'none')
                try:
                       current_date = date.today()
                       date_of_birth = int(current_date.year) - int(qqqq[0]['bdate'][-4:]) #   Возраст пользователя( вычисляется не точно)
                       nomer_marker = nomer_marker + 1


                except:
                       nomer_marker = 0
                       bot.bot_write_foto(id, f"Ваш возраст ?", 'none')
                       if message.isdigit():
                            if (int(message) >= 16) and (int(message) < 100):
                                 date_of_birth = int(message)
                                 nomer_marker = nomer_marker + 1
                                 print(nomer_marker)
                                 print('marker2')

            if (event.to_me) and (nomer_marker == 1):
                try:
                       if (qqqq[0]['sex'] == 2) :  # пол пользователя
                           sex_user = 1
                           nomer_marker = nomer_marker + 1
                       elif (qqqq[0]['sex'] == 1) :
                           sex_user = 2
                           nomer_marker = nomer_marker + 1
                       else:
                            nomer_marker = 0
                            if message.isdigit():
                               bot.bot_write_foto(id, "Вы мужчина или женщина (2/1)?", 'none')
                               if (qqqq[0]['sex'] == 2) :  # пол пользователя
                                  sex_user = 1
                                  nomer_marker = nomer_marker + 1
                               elif (qqqq[0]['sex'] == 1) :
                                  sex_user = 2
                                  nomer_marker = nomer_marker + 1
                except :
                        nomer_marker = 0
                        bot.bot_write_foto(id, "Вы мужчина или женщина (2/1)?", 'none')
                        if message.isdigit():
                           if message == 2 :  # пол пользователя
                              sex_user = 1
                              nomer_marker = nomer_marker + 1
                           elif message == 1 :
                              sex_user = 2
                              nomer_marker = nomer_marker + 1

            if (event.to_me) and (nomer_marker == 2):
                try:
                         city_user = qqqq[0]['city']['id']
                         nomer_marker = nomer_marker + 1
                except:
                        nomer_marker = 0
                        bot.bot_write_foto(id, "Введите название города", 'none')
                        xcdx = message
                        city_user11 = vk1.method("database.getCities",{"q": xcdx, "count": 1, 'country_id': 1})
                        if city_user11['count'] != 0:
                            city_user = city_user11['items'][0]['id']
                            nomer_marker = nomer_marker + 1
                        else:
                             bot.bot_write_foto(id, "Город с таким названием не найден ", 'none')

                        

            if (event.to_me) and (nomer_marker == 3):


               if message == "привет":
                    bot.bot_write_foto(event.user_id, f"Хай, {event.user_id}", 'none')
               elif message == "пока":
                    bot.bot_write_foto(event.user_id, "Пока((", 'none')
               elif message == "избранное":
                    print('ppppppppppppppppppppppppppppppppppppppppppppppp')
                    #izban_partners = database.select_users_partner(0)
                    #print(izban_partners)
                    bot.main_function(id, event, 1, 0, 3, city_user, date_of_birth, sex_user,3)
                   
 ##################################################################################################
               elif message == 'w': #   ЧЕРНЫЙ СПИСОК':
                   if (1 > nomer) and (nomer <= 100):                            # Не корректно
                      bot.partner_search(id, city_user, date_of_birth, sex_user, nomer,0)
                   bot.main_function(id, event, nomer, 1, 2, city_user, date_of_birth, sex_user,0)
                   nomer = nomer + 1
               elif message == 'e':     # ИЗБРАННОЕ'
                   bot.main_function(id, event, nomer, 1, 3, city_user, date_of_birth, sex_user, 0 )
                   nomer = nomer + 1
               elif message == "q":  # НОВЫЕ ВАРИАНТЫ":
                    bot.main_function(id, event, nomer, 1, 1, city_user, date_of_birth, sex_user,0)
                    nomer = nomer + 1                             
####################################################################################################



               else:
                     bot.bot_write_foto(event.user_id, "Не поняла вашего ответа... Нажмите 'q' для поиска пары", 'none')
