import asyncpg
import asyncio
from config import config
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

####################################################################################
# Блок User
####################################################################################


"""Функция возвращающая стаж
@dp.message_handlers(commands='Стаж')"""


async def staj_user(message: types.Message):
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    id_user = message.from_id
    staj = await conn.fetchrow('''
        select * from staj($1)
         ''', id_user)
    await conn.close()
    await message.answer("📋 Ваш стаж работы составляет: | " + str(staj[0]) + " лет 🎉🎊")


# Функция возвращающая zp
async def zp_user(message: types.Message):
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    id_user = message.from_id
    zp = await conn.fetchrow('''
        select * from zp($1)
         ''', id_user)
    await conn.close()
    await message.answer("💸  Ваша текущая заработная плата составляет: | " + str(zp[0]) + "руб  💸")


# Функция возвращающая prize
async def prize_user(message: types.Message):
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    id_user = message.from_id
    prize = await conn.fetchrow('''
        select * from prize($1)
         ''', id_user)
    await conn.close()
    await message.answer("🎉  Ваша премия составляет: | " + str(prize[0]) + "руб  🎉")


# Функция возвращающая tool
async def tool_user(message: types.Message):
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    id_user = message.from_id
    tools = await conn.fetch('''
        select "Название_Оборудования" from "Оборудование"
        join "Сотрудники_Лабораторий" СЛ on СЛ."Номер_Тестировщика" = "Оборудование"."Номер_Тестировщика"      
        where id_tg=$1
         ''', id_user)
    await conn.close()
    str_tools = "🛠  ️Ваше оборудование для работы:\n"
    for tool in tools:
        str_tools += "\n📌  " + str(tool[0])
    await message.answer(str_tools)


####################################################################################
# Блок Admin
####################################################################################

"""Получение списка пользователей по команде Текущий список сотрудников"""


async def get_users(message: types.Message):
    # Вывод таблы Пользователи
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetch('''select * from "Сотрудники_Лабораторий"''')
    await conn.close()
    str_row = "<b>ID | NAME | FAM | PROF </b>"
    for row in rows:
        str_row += "\n" + ("  " + str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]))
    await message.answer(str_row, parse_mode="HTML")


"""Получение списка Оборудования по команде Текущий список Оборудования"""


async def get_equip(message: types.Message):
    # Вывод таблы Оборудования
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetch('''select * from "Оборудование"''')
    await conn.close()
    str_row = "<b>ID_EQUIP | ID_LAB | ID_EMPL | NAME_EQUIP </b>"
    for row in rows:
        str_row += "\n" + ("  " + str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]))
    await message.answer(str_row, parse_mode="HTML")


async def lab_fail(message: types.Message):
    # Вывод таблы lab fail
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetch('''select * from laboratories_fail''')
    await conn.close()
    str_row = "<b>Name LAB </b>"
    for row in rows:
        str_row += "\n" + ("  " + str(row[0]))
    await message.answer("Лаборатории с проваленными испытаниями\n\n" + str_row, parse_mode="HTML")


async def prod_proc(message: types.Message):
    # Вывод таблы product_process
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetch('''select * from "product_process"''')
    await conn.close()
    str_row = "<b>ID_PROD</b>"
    for row in rows:
        str_row += "\n" + ("  " + str(row[0]))
    await message.answer("Изделия в производстве:\n\n" + str_row, parse_mode="HTML")


async def max_prod(message: types.Message):
    # Вывод таблы max_prod
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetchrow('''select max_product()''')
    await conn.close()
    str_row = "<b>ID_УЧ</b>" + " | " + "<b>Count</b>" + f"\n {rows[0][0]}" + "      |        " + f"{rows[0][1]}"
    await message.answer("Участок с самым большим кол-вом изделий:\n\n" + str_row, parse_mode="HTML")


async def good_empl(message: types.Message):
    # Вывод таблы good_employee
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetchrow('''select good_employee()''')
    await conn.close()
    str_row = "<b>ID_УЧ</b>" + "                | " + "<b>Count</b>" + f"\n {rows[0][0]}" + "      |        " + f"{rows[0][1]}"
    await message.answer("Самый продуктивный работник:\n\n" + str_row, parse_mode="HTML")


####################################################################################
# Машина состояния:
####################################################################################


"""Создание класса Машины состояний и её этапов для добавления Пользователя"""


class FSMAdmin(StatesGroup):
    firstname_empl = State()
    surname_empl = State()
    profession = State()

    id_empl = State()
    del_empl = State()

    id_empl_staj = State()
    upd_staj = State()

    id_empl_prize = State()
    upd_prize_count = State()
    upd_prize = State()

    id_empl_tg = State()
    upd_tg = State()

    id_empl_equip_del = State()
    del_equip = State()

    name_equip = State()
    id_equip_empl_add = State()
    id_equip_lab = State()


####################################################################################
# Машина состояния на AddUser
####################################################################################


"""Отмена машины состояний
@dp.message_handlers(state="*", commands="/Отмена")"""


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Всё ок, продолжай работу!")
        return 0
    await state.finish()
    await message.answer("END!!!")


"""Начало диалога, загрузка нового пункта меню, Спрашиваем Имя
@dp.message_handlers(commands='Добавить пользователя', state=None)"""


async def cm_start_add(message: types.Message):
    await FSMAdmin.firstname_empl.set()
    await message.answer("|...Запуск Диалога...|\n|...Для завершения напишите <b>«Отмена»</b>...|\n\nВведите Имя",
                         parse_mode="HTML")


"""Берём ответ, записываем в словарь и спрашиваем Фамилию
@dp.message_handlers(state=FSMAdmin.firstname_empl)"""


async def load_firstname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstname'] = message.text
    await FSMAdmin.next()
    await message.answer("Введите Фамилию")


"""Берём ответ, записываем в словарь и спрашиваем Профессию
@dp.message_handlers(state=FSMAdmin.surname_empl)"""


async def load_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await FSMAdmin.next()
    await message.answer("Введите профессию")


"""Берём ответ, добавляем пользователя и завершаем машину состояния
@dp.message_handlers(state=FSMAdmin.profession)"""


async def load_profession(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['profession'] = message.text

        try:
            conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                         database=config.database, host=config.host, port=config.port_bd)
        except:
            print("\n========= Не удалось установить соединение с БД =========")
            exit()

        # Добавление User
        try:
            await conn.execute('''call add_employee($1,$2,$3)
            ''', data["firstname"], data["surname"], data["profession"])
            await message.answer(
                f"Данные успешно добавились!!!\n\n"
                f"Имя: {data['firstname']}\n"
                f"Фамилия: {data['surname']}\n"
                f"Профессия: {data['profession']}"
                f"\n\nДобро пожаловать!!!")
        except:
            await message.answer("Данные НЕ добавились")

    await state.finish()


####################################################################################
# Машина состояния на DeleteUser
####################################################################################


"""Начало диалога, загрузка нового пункта меню, Спрашиваем id
@dp.message_handlers(commands='DeleteUser', state=None)"""


async def cm_start_del(message: types.Message):
    await FSMAdmin.id_empl.set()
    await message.answer(
        "|...Запуск Диалога...|\n|...Для завершения напишите <b>«Отмена»</b>...|"
        "\n\nВведите ID Пользователя для Удаления:",
        parse_mode="HTML")

    # Вывод таблы Пользователи
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetch('''select * from "Сотрудники_Лабораторий"''')
    await conn.close()
    str_row = "<b>ID | NAME | FAM | PROF </b>"
    for row in rows:
        str_row += "\n" + ("  " + str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]))
    await message.answer(str_row, parse_mode="HTML")


async def del_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_user'] = message.text
        if data['id_user'] in ['1', '2', '3', '4', '5']:
            await message.answer("Это лучше не удалять :)")
            await state.finish()
            return 0
        else:
            # Удаление пользователя
            try:
                conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                             database=config.database, host=config.host, port=config.port_bd)
            except:
                print("\n========= Не удалось установить соединение с БД =========")
                exit()

            try:
                await conn.execute('''call del_user($1)''', int(data['id_user']))
                await message.answer(f"Пользователь с id = {data['id_user']} удалён!!!")
            except:
                await message.answer(f"Пользователя с id = {data['id_user']} не удалось удалить...")

            await conn.close()
            await state.finish()


####################################################################################
# Машина состояния на +Стаж
####################################################################################


async def cm_start_staj(message: types.Message):
    await FSMAdmin.id_empl_staj.set()
    await message.answer(
        "|...Запуск Диалога...|\n|...Для завершения напишите <b>«Отмена»</b>..."
        "|\n\nВведите ID Пользователя для добавления стажа:",
        parse_mode="HTML")

    # Вывод таблы Пользователи
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetch('''select * from "Сотрудники_Лабораторий"''')
    await conn.close()
    str_row = "<b>ID | NAME | FAM | PROF </b>"
    for row in rows:
        str_row += "\n" + ("  " + str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]))
    await message.answer(str_row, parse_mode="HTML")


async def update_staj(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_user'] = message.text

    # Добавление стажа пользователю
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    try:
        await conn.execute('''call updating_experience($1)''', int(data['id_user']))
        await message.answer(f"Пользователь с id = {data['id_user']} постарел!!!")
    except:
        await message.answer(f"Пользователь с id = {data['id_user']} не смог постареть...")

    await conn.close()
    await state.finish()


####################################################################################
# Машина состояния на +Премия
####################################################################################


async def cm_start_prize_upd(message: types.Message):
    await FSMAdmin.id_empl_prize.set()
    await message.answer(
        "|...Запуск Диалога...|\n|...Для завершения напишите <b>«Отмена»"
        "</b>...|\n\nВведите ID Пользователя для добавления премии:",
        parse_mode="HTML")

    # Вывод таблы Пользователи
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetch('''select * from "Сотрудники_Лабораторий"''')
    await conn.close()
    str_row = "<b>ID | NAME | FAM | PROF </b>"
    for row in rows:
        str_row += "\n" + ("  " + str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]))
    await message.answer(str_row, parse_mode="HTML")


async def update_prize_coun(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_user'] = message.text
    await FSMAdmin.next()
    await message.answer("Сколько добавить к премии?")


async def upd_prize_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['prize'] = message.text
    # Добавление Премии пользователю
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    try:
        await conn.execute('''call updating_prize($1, $2)''', int(data['id_user']), int(data['prize']))
        await message.answer(f"Пользователь с id = {data['id_user']} получил премию = {data['prize']} !!!")
    except:
        await message.answer(f"Пользователь с id = {data['id_user']} не получил премию = {data['prize']}...")

    await conn.close()
    await state.finish()


####################################################################################
# Машина состояния на UPD_TG
####################################################################################


async def cm_start_tg_id(message: types.Message):
    await FSMAdmin.id_empl_tg.set()
    await message.answer(
        "|...Запуск Диалога...|\n|...Для завершения напишите <b>«Отмена»</b>...|"
        "\n\nВведите ID Пользователя для добавления TG_ID:",
        parse_mode="HTML")

    # Вывод таблы Пользователи
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetch('''select "Номер_Тестировщика", "Фамилия", id_tg from "Сотрудники_Лабораторий"''')
    await conn.close()
    str_row = "<b>ID | FAM | TG_ID</b>"
    for row in rows:
        str_row += "\n" + ("  " + str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]))
    await message.answer(str_row, parse_mode="HTML")
    await conn.close()


async def update_tg_id_get(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_user'] = message.text
        if data['id_user'] not in ['1', '2', '3', '4', '5']:
            await FSMAdmin.next()
            await message.answer("Какой ID_TG задать?")
        else:
            await message.answer("Это лучше не менять :)")
            await state.finish()
            return 0


async def upd_tg_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tg_id'] = message.text
    # Добавление TG_ID пользователю
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    try:
        await conn.execute('''call add_id_tg($2, $1)''', int(data['id_user']), int(data['tg_id']))
        await message.answer(f"Пользователь с id = {data['id_user']} получил TG_ID = {data['tg_id']} !!!")
    except:
        await message.answer(f"Пользователь с id = {data['id_user']} не получил TG_ID = {data['tg_id']}...")

    await conn.close()
    await state.finish()


####################################################################################
# Машина состояния на AddEquip
####################################################################################


"""Начало диалога Спрашиваем Имя Оборудование
@dp.message_handlers(commands='AddEquip', state=None)"""


async def cm_start_add_equip(message: types.Message):
    await FSMAdmin.name_equip.set()
    await message.answer("|...Запуск Диалога...|\n|...Для завершения напишите "
                         "<b>«Отмена»</b>...|\n\nВведите название Оборудования",
                         parse_mode="HTML")


"""Берём ответ, записываем в словарь и спрашиваем какому сотруднику дать
@dp.message_handlers(state=FSMAdmin.name_equip)"""


async def load_name_equip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_equip'] = message.text
        await FSMAdmin.next()
        await message.answer(f"Какому сотруднику присвоить {data['name_equip']}")
        # Вывод таблы Польз
        try:
            conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                         database=config.database, host=config.host, port=config.port_bd)
        except:
            print("\n========= Не удалось установить соединение с БД =========")
            exit()

        rows = await conn.fetch(
            '''select "Номер_Тестировщика", "Фамилия", "Специализация" from "Сотрудники_Лабораторий"''')
        await conn.close()
        str_row = "<b>ID_EMPL | FAM_EMPL | PROF </b>"
        for row in rows:
            str_row += "\n" + ("  " + str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]))
        await message.answer(str_row, parse_mode="HTML")


"""Берём ответ, записываем в словарь и спрашиваем Номер Лабы
@dp.message_handlers(state=FSMAdmin.id_equip_empl)"""


async def load_id_equip_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_empl'] = message.text
    await FSMAdmin.next()
    await message.answer(f"Введите Номер Лаборатории в которой требуется {data['name_equip']}")
    # Вывод таблы Лабы
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetch('''select * from "Лаборатории"''')
    await conn.close()
    str_row = "<b>ID_LAB | NAME_LAB </b>"
    for row in rows:
        str_row += "\n" + ("  " + str(row[0]) + " | " + str(row[1]))
    await message.answer(str_row, parse_mode="HTML")


"""Берём ответ, добавляем пользователя и завершаем машину состояния
@dp.message_handlers(state=FSMAdmin.profession)"""


async def load_equip_lab(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lab'] = message.text

        try:
            conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                         database=config.database, host=config.host, port=config.port_bd)
        except:
            print("\n========= Не удалось установить соединение с БД =========")
            exit()

        # Добавление Оборудования
        try:
            await conn.execute('''call add_equipment($1,$2,$3)
                ''', data["name_equip"], int(data["id_empl"]), int(data["lab"]))
            await message.answer(
                f"Оборудование успешно добавилось!!!\n\n"
                f"Название: {data['name_equip']}\n"
                f"Номер тестировщика: {data['id_empl']}\n"
                f"Лаба: {data['lab']}"
                f"\n\nПродолжаем работать!!!")
        except:
            await message.answer("Оборудование НЕ добавилось")

    await state.finish()


####################################################################################
# Машина состояния на DeleteEquip
####################################################################################


"""Начало диалога, загрузка нового пункта меню, Спрашиваем id
@dp.message_handlers(commands='DeleteEquip', state=None)"""


async def cm_start_del_equip(message: types.Message):
    await FSMAdmin.id_empl_equip_del.set()
    await message.answer(
        "|...Запуск Диалога...|\n|...Для завершения напишите <b>«Отмена»</b>...|"
        "\n\nВведите название Оборудования:",
        parse_mode="HTML")

    # Вывод таблы Оборудование
    try:
        conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                     database=config.database, host=config.host, port=config.port_bd)
    except:
        print("\n========= Не удалось установить соединение с БД =========")
        exit()

    rows = await conn.fetch('''select * from "Оборудование"''')
    await conn.close()
    str_row = "<b>ID_EQUIP | ID_LAB | ID_EMPL | NAME_EQUIP </b>"
    for row in rows:
        str_row += "\n" + (
                "     " + str(row[0]) + "     |       " + str(row[1]) + "    |    " + str(
            row[2]) + "     |       " + str(row[3]))
    await message.answer(str_row, parse_mode="HTML")


async def del_equip_funk(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_equip'] = message.text
        if data['id_equip'] in ['1', '2', '3', '4', '5', '6', '7', "8", "9", "10"]:
            await message.answer("Это лучше не удалять :)")
            await state.finish()
            return 0
        else:
            # Удаление Оборудования
            try:
                conn = await asyncpg.connect(user=config.user_bd, password=config.password_bd,
                                             database=config.database, host=config.host, port=config.port_bd)
            except:
                print("\n========= Не удалось установить соединение с БД =========")
                exit()

            try:
                await conn.execute('''call del_equip($1)''', int(data['id_equip']))
                await message.answer(f"Оборудование с id = {data['id_equip']} удалено!!!")
            except:
                await message.answer(f"Оборудование с id = {data['id_equip']} не удалось удалить...")

            await conn.close()
            await state.finish()


####################################################################################
# Блок регистрации хэндлеров
####################################################################################


def register_handlers_db(dp: Dispatcher):
    dp.register_message_handler(staj_user, Text(equals="Стаж", ignore_case=True))
    dp.register_message_handler(zp_user, Text(equals="ЗП", ignore_case=True))
    dp.register_message_handler(tool_user, Text(equals="Моё Оборудование", ignore_case=True))
    dp.register_message_handler(prize_user, Text(equals="Премия", ignore_case=True))

    dp.register_message_handler(get_users, Text(equals="Текущий список Сотрудников", ignore_case=True))
    dp.register_message_handler(get_equip, Text(equals="Текущий список Оборудования", ignore_case=True))
    dp.register_message_handler(lab_fail, Text(equals="Провал Лабы", ignore_case=True))
    dp.register_message_handler(prod_proc, Text(equals="Собираемые изд", ignore_case=True))
    dp.register_message_handler(max_prod, Text(equals="MAX PROD", ignore_case=True))
    dp.register_message_handler(good_empl, Text(equals="Good empl", ignore_case=True))

    dp.register_message_handler(cancel_handler, Text(equals="Отмена", ignore_case=True), state="*")

    dp.register_message_handler(cm_start_add, Text(equals="AddUser", ignore_case=True), state=None)
    dp.register_message_handler(load_firstname, state=FSMAdmin.firstname_empl)
    dp.register_message_handler(load_surname, state=FSMAdmin.surname_empl)
    dp.register_message_handler(load_profession, state=FSMAdmin.profession)

    dp.register_message_handler(cm_start_add_equip, Text(equals="AddEquip", ignore_case=True), state=None)
    dp.register_message_handler(load_name_equip, state=FSMAdmin.name_equip)
    dp.register_message_handler(load_id_equip_name, state=FSMAdmin.id_equip_empl_add)
    dp.register_message_handler(load_equip_lab, state=FSMAdmin.id_equip_lab)

    dp.register_message_handler(cm_start_del, Text(equals="DeleteUser", ignore_case=True), state=None)
    dp.register_message_handler(del_user, state=FSMAdmin.id_empl)

    dp.register_message_handler(cm_start_del_equip, Text(equals="DeleteEquip", ignore_case=True), state=None)
    dp.register_message_handler(del_equip_funk, state=FSMAdmin.id_empl_equip_del)

    dp.register_message_handler(cm_start_staj, Text(equals="+Стаж", ignore_case=True), state=None)
    dp.register_message_handler(update_staj, state=FSMAdmin.id_empl_staj)

    dp.register_message_handler(cm_start_prize_upd, Text(equals="+Премия", ignore_case=True), state=None)
    dp.register_message_handler(update_prize_coun, state=FSMAdmin.id_empl_prize)
    dp.register_message_handler(upd_prize_user, state=FSMAdmin.upd_prize_count)

    dp.register_message_handler(cm_start_tg_id, Text(equals="UPD_TG", ignore_case=True), state=None)
    dp.register_message_handler(update_tg_id_get, state=FSMAdmin.id_empl_tg)
    dp.register_message_handler(upd_tg_id, state=FSMAdmin.upd_tg)
