import psycopg2
from psycopg2 import Error

try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="210978",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="users_partner")

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # Распечатать сведения о PostgreSQL
    print("Информация о сервере PostgreSQL")
    print(connection.get_dsn_parameters(), "\n")
    cursor = connection.cursor()


    def insert_users_partner(vk_id1,status1):
        cursor = connection.cursor()
        insert_query = """INSERT INTO users_partner (vk_id,status)
                          VALUES (%s,%s)
                          """
        record_to_insert = (vk_id1,status1)
        cursor.execute(insert_query, record_to_insert)
        connection.commit()

        return


    def update_users_partner(id, status):
        cursor = connection.cursor()
        insert_query = """UPDATE users_partner
                          SET status = %s
                          WHERE vk_id = %s
                       """
        record_to_update = (status, id)
        cursor.execute(insert_query, record_to_update)
        connection.commit()
        return




    def select_users_partner(status1):

         cursor = connection.cursor()
         select_query = """SELECT  vk_id
                           FROM users_partner
                           WHERE status = 0
                           """
         cursor.execute(select_query, status1)
         rows = cursor.fetchmany()
         connection.commit()
         #print(rows)
         return rows



###########################################################################
    try:
       select_users_partner(1)
       print('Таблица существует')                  #     ПРОВЕРКА СУЩЕСТВОВАНИЯ ТАБЛИЦЫ
    except:
       cursor.execute("""DROP TABLE users_partner""");

       cursor.execute("""CREATE TABLE  users_partner (
                Id SERIAL ,
               vk_id INTEGER,
              status INTEGER
               )"""
                      );
       connection.commit()
       print('Таблица создана')

############################################################################

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
#finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
