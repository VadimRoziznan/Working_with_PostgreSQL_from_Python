import configparser
import pandas as pd
import sys
import os

sys.path.append(os.path.join('..'))
from Library.MyPSQL import MyPSQL
from Library.help import Help


def commands(com):
    if com == 'add_client' or com == 'a/c':
        user_name = input('Укажите имя и фамилию клиента: ')
        db.add_new_client(user_name)
    elif com == 'exit' or com == 'q':
        global data_checking
        data_checking = False
        return
    elif com == 'add_inf' or com == 'a/i':
        user_name = input('Укажите имя и фамилию клиента: ')
        id_user_name = db.get_id(
            'id', 'personal_datas', 'personal_data', user_name
        )
        if id_user_name == 0:
            return print('Данный пользователь не найден.')
        telephone = input('Укажите телефон: ')
        response = db.get_user_information(id_user_name)
        for el in response:
            if telephone in el:
                print('Данный телефон уже существует воспользуйтесь '
                      'командой "change" или короткой '
                      'командой "c"')
                return
        mail = input('Укажите mail: ')
        response = db.get_user_information(id_user_name)
        for el in response:
            if mail in el:
                print('Данный mail уже существует воспользуйтесь '
                      'командой "change" или короткой '
                      'командой "c"')
                return
        db.add_new_information(id_user_name, telephone, mail)
        return
    elif com == 'change' or com == 'c':
        user_name = input('Укажите имя и фамилию клиента: ')
        id_user_name = db.get_id(
            'id', 'personal_datas', 'personal_data', f'{user_name}'
        )
        if id_user_name == 0:
            return print('Данный пользователь не найден.')
        data_user = db.get_user_information(id_user_name)
        for el in range(len(data_user)):
            if data_user[el][1] is None:
                return print(f"У пользователя {user_name} нет данных.\n"
                             f"Для добавления данных воспользуйтесь "
                             f"командой --> 'добавить информацию'\nили "
                             f"короткой командой --> 'add'")
        print(pd.DataFrame(data=data_user, columns=['Имя', 'id', 'Телефон',
                                                    'Mail']))
        question = input('Вы хотите изменить Ф.И.О Да/Нет: ').lower()
        if question == 'да':
            new_name = input('Укажите новое имя: ')
            db.change(
                'personal_datas', 'personal_data', id_user_name, new_name
            )
        question = input('Вы хотите изменить телефон Да/Нет: ').lower()
        if question == 'да':
            check_id = int(input('Укажите id телефона: '))
            for el in range(len(data_user)):
                if check_id == data_user[el][1]:
                    new_phone = input('Укажите новый телефон: ')
                    db.change(
                        'contact_datas', 'phone_number', check_id, new_phone
                    )
                    break
            else:
                print('Проверьте правильность ввода id телефона и '
                      'повторите попытку.')
        question = input('Вы хотите изменить mail Да/Нет: ').lower()
        if question == 'да':
            check_id = int(input('Укажите id mail: '))
            for el in range(len(data_user)):
                if check_id == data_user[el][1]:
                    new_mail = input('Укажите новый mail: ')
                    db.change(
                        'contact_datas', 'email_address', check_id, new_mail
                    )
                    break
            else:
                print('Проверьте правильность ввода id mail и '
                      'повторите попытку.')
        return
    elif com == 'del_data' or com == 'd/d':
        user_name = input('Укажите имя и фамилию клиента: ')
        id_user_name = db.get_id(
            'id', 'personal_datas', 'personal_data', user_name
        )
        if id_user_name == 0:
            return print('Данный пользователь не найден.')
        data_user = db.get_user_information(id_user_name)
        for el in range(len(data_user)):
            if data_user[el][1] is None:
                return print(f"У пользователя {user_name} нет данных.\n"
                             f"Для добавления данных воспользуйтесь "
                             f"командой --> 'добавить информацию'\nили "
                             f"короткой командой --> 'add'")
        print(pd.DataFrame(data=data_user, columns=['Имя', 'id', 'Телефон',
                                                    'Mail']))
        check_id = input("Для удаления укажите id данных, для возврата в "
                         "меню введите 'Выход': ").lower()
        if check_id == 'выход':
            return
        for el in range(len(data_user)):
            if int(check_id) == data_user[el][1]:
                db.delete('contact_datas', int(check_id))
                print('Данные удалены')
                break
        else:
            print('Проверьте правильность ввода id телефона и '
                  'повторите попытку.')
        return
    elif com == 'del_user' or com == 'd/u':
        user_name = input('Укажите имя и фамилию клиента: ')
        id_user_name = db.get_id(
            'id', 'personal_datas', 'personal_data', user_name
        )
        if id_user_name == 0:
            return print('Данный пользователь не найден.')
        question = input("Для удаления пользователя и всех его данных "
                         "введите Да, для выхода в главное меню введите "
                         "Нет: ").lower()
        if question == 'да':
            data_user = db.get_user_information(id_user_name)
            for el in range(len(data_user)):
                db.delete('contact_datas', data_user[el][1])
            db.delete('personal_datas', id_user_name)
            print('Пользователь удалён')
        else:
            return
    elif com == 'find_user' or com == 'f/u':
        search_user = input('Ведите Имя и Фамилию или данные пользователя: ')
        data_user = db.get_all_information()
        if data_user == 0:
            return print('Совпадений не найдено')
        response = False
        for el in range(len(data_user)):
            for data in data_user[el]:
                if search_user == data:
                    response = data_user[el][0], data_user[el][2:]
                    print(response)
        if response is False:
            return print('Совпадений не найдено')
        else:
            return
    elif com == 'help':
        print(Help.help())
        return
    else:
        return print('Неизвестная команд, для вызова справки введите help')


if __name__ == '__main__':
    data_checking = True
    config = configparser.ConfigParser()
    config.read("settings.ini")
    user = config["settings"]["user"]
    password = config["settings"]["password"]
    print(Help.help())
    name_db = input('Введите имя базы данных: ')
    db = MyPSQL(name_db, user, password, data_checking)
    db.checking_database()
    if (db.__dict__.get('data_checking')) == False:
        print('Проверьте данные в файле settings и повторите попытку.')
        data_checking = False
    while data_checking:
        command = input('Введите команду для дальнейших действий: ').lower()
        commands(command)
