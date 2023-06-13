# -*- coding: utf-8 -*-
import hashlib
import random
import string
import time

import mysql.connector

id = ""
connection_string = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "goslingskyways",
}

connection_string_for_db_create = {"user": "root", "password": "", "host": "localhost"}

# проверка подключения к базе данных
def db_connection_check():
    try:
        connection = mysql.connector.connect(**connection_string)
        connection.close()
        return True
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        return False


def create_db():
    connection = mysql.connector.connect(**connection_string_for_db_create)
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE aviacompany; USE aviacompany;")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def create_aircraft_table():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE aircraft (
                    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    model varchar(50) NOT NULL,
                    capacity int(11) NOT NULL);"""
        )
        print("[Успех] Создана таблица aircraft")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def create_city_table():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE city (
                id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name varchar(50) NOT NULL);"""
        )
        print("[Успех] Создана таблица city")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def create_user_table():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE user (
                    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    first_name varchar(100) NOT NULL,
                    middle_name varchar(100) DEFAULT NULL,
                    last_name varchar(100) NOT NULL,
                    email varchar(100) NOT NULL,
                    password_hash varchar(64) NOT NULL,
                    role enum('user','admin') NOT NULL);"""
        )
        print("[Успех] Создана таблица user")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def create_airport_table():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE airport (
                    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    city_id int(11) NOT NULL,
                    name varchar(8) NOT NULL,
                    KEY airport_FK (city_id),
                    FOREIGN KEY (city_id) REFERENCES city (id));"""
        )
        print("[Успех] Создана таблица airport")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def create_flight_table():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE flight (
                    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    flight_number varchar(10) NOT NULL,
                    departure_airport_id int(11) NOT NULL,
                    arrival_airport_id int(11) NOT NULL,
                    aircraft_id int(11) NOT NULL,
                    departure_time datetime NOT NULL,
                    arrival_time datetime NOT NULL,
                    ticket_available int(11) NOT NULL,
                    econom_price int(11) NOT NULL,
                    business_price int(11) NOT NULL,
                    FOREIGN KEY (departure_airport_id) REFERENCES airport (id),
                    FOREIGN KEY (arrival_airport_id) REFERENCES airport (id),
                    FOREIGN KEY (aircraft_id) REFERENCES aircraft (id));"""
        )
        print("[Успех] Создана таблица flight")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def create_reservation_table():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE reservation (
                    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    user_id int(11) NOT NULL,
                    flight_id int(11) NOT NULL,
                    class enum('econom','business') NOT NULL,
                    status enum('paid','cancelled') NOT NULL,
                    price int(11) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user (id),
                    FOREIGN KEY (flight_id) REFERENCES flight (id));"""
        )
        print("[Успех] Создана таблица reservation")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def create_tables():
    create_aircraft_table()
    create_city_table()
    create_user_table()
    create_airport_table()
    create_flight_table()
    create_reservation_table()


def insert_aircraft_data():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO aircraft (id, model, capacity) VALUES (1, 'Boeing 737-800', 189), (2, 'Airbus A320', 180);"
        )
        connection.commit()
        print("[Успех] Добавлены модели самолетов")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def insert_airport_data():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO airport (id, city_id, name) VALUES(1, 1, 'DME'), (2, 2, 'AER'), (3, 3, 'LED');"
        )
        connection.commit()
        print("[Успех] Добавлены аэропорты")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def insert_city_data():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO city (id, name) VALUES (1, 'Москва'), (2, 'Сочи'), (3, 'Санкт-Петербург');"
        )
        connection.commit()
        print("[Успех] Добавлены города")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def insert_flight_data():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO flight (id, flight_number, departure_airport_id, arrival_airport_id, aircraft_id, departure_time, arrival_time, ticket_available, econom_price, business_price)
VALUES(1, 'G-1115', 1, 2, 2, '2023-05-16 02:00:00.000', '2023-05-16 04:40:00.000', 180, 35244, 88108),
(2, 'G-3650', 1, 3, 2, '2023-05-15 20:20:00.000', '2023-05-15 22:10:00.000', 178, 26412, 66030),
(3, 'G-6169', 2, 1, 1, '2023-05-16 05:30:00.000', '2023-05-16 09:20:00.000', 0, 27341, 68353),
(4, 'G-4375', 2, 3, 1, '2023-05-17 20:20:00.000', '2023-05-18 00:40:00.000', 189, 34998, 87495),
(5, 'G-6491', 3, 1, 2, '2023-05-16 06:30:00.000', '2023-05-16 08:20:00.000', 178, 37533, 56300),
(6, 'G-1115', 1, 2, 2, '2023-05-18 02:00:00.000', '2023-05-18 04:40:00.000', 180, 24560, 61400),
(7, 'G-4375', 2, 3, 1, '2023-05-19 20:20:00.000', '2023-05-20 00:40:00.000', 189, 38504, 57756);"""
        )
        connection.commit()
        print("[Успех] Добавлены рейсы")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def insert_user_data():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO user (id, first_name, middle_name, last_name, email, password_hash, `role`)
VALUES(1, 'admin', NULL, 'admin', 'admin@gosling.com', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin'),
(2, 'user', NULL, 'user', 'user@gosling.com', '04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb', 'user');"""
        )
        connection.commit()
        print("[Успех] Добавлены базовые пользователи")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def insert_data():
    insert_aircraft_data()
    insert_city_data()
    insert_airport_data()
    insert_flight_data()
    insert_user_data()


def delete_aircraft_data():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM aircraft")
        connection.commit()
        print("[Успех] Удалены данные о самолетах")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def delete_city_data():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM city")
        connection.commit()
        print("[Успех] Удалены данные о городах")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def delete_airport_data():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM airport")
        connection.commit()
        print("[Успех] Удалены данные об аэропортах")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def delete_flight_data():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM flight")
        connection.commit()
        print("[Успех] Удалены данные о рейсах")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def delete_user_data():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM user")
        connection.commit()
        print("[Успех] Удалены данные о пользователях")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def delete_reservation_data():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM reservation")
        connection.commit()
        print("[Успех] Удалены данные о бронированиях")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def delete_data():
    delete_reservation_data()
    delete_user_data()
    delete_flight_data()
    delete_airport_data()
    delete_city_data()
    delete_aircraft_data()


def delete_db():
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE aviacompany")
        connection.commit()
        print("[Успех] База данных удалена полностью")
    except mysql.connector.Error as error:
        print(f"[Ошибка] {error}")
    finally:
        connection.close()


def delete_data_prompt():
    while True:
        print(
            "Желаете удалить только данные или всю базу данных?\n\t(1) Только данные таблиц\n\t(2) База данных\n\t(3) Выход из приложения"
        )
        input_str = input("> ")
        if input_str == "1":
            delete_data()
            print("[Успех] Все данные удалены из базы данных")
            return
        elif input_str == "2":
            delete_db()
            return
        elif input_str == "3":
            print("------------------------------------------")
            print("До свидания. Нажмите любую кнопку, чтобы закрыть окно приложения.")
            input()
            return
        else:
            print("Мы не поняли, что вы хотите сделать, попробуйте снова")
            print("------------------")


def admin_register():
    print("------------------")
    inputLastName = input("Введите фамилию: ")
    inputFirstName = input("Введите имя: ")
    inputMiddleName = input("Введите отчество (при наличии): ")
    inputEmail = input("Введите адрес электронной почты: ")
    password = generate_password()
    add_user(
        inputFirstName,
        inputMiddleName,
        inputLastName,
        inputEmail,
        compute_sha256_hash(password),
        "admin",
    )
    print("[Успех] Регистрация прошла успешно")
    print(f"Пароль нового администратора: {password}")
    admin_home()


def admin_home():
    while True:
        print("Выберите действие:")
        print(
            "\t(1) Купить авиабилет\n\t(2) Посмотреть купленные авиабилеты\n\t(3) Добавить администратора\n\t(4) Выход из приложения"
        )
        input_str = input("> ")
        if input_str == "1":
            buy_ticket()
            admin_home()
            return
        elif input_str == "2":
            print_all_reservations(id)
            admin_home()
            return
        elif input_str == "3":
            admin_register()
            return
        elif input_str == "4":
            print("------------------------------------------")
            print("До свидания. Нажмите любую кнопку, чтобы закрыть окно приложения.")
            input()
            return
        else:
            print("Мы не поняли, что вы хотите сделать, попробуйте снова")
            print("------------------")


def user_home():
    while True:
        print("Выберите действие:")
        print(
            "\t(1) Купить авиабилет\n\t(2) Посмотреть купленные авиабилеты\n\t(3) Выход из приложения"
        )
        input_str = input("> ")
        if input_str == "1":
            buy_ticket()
            user_home()
            return
        elif input_str == "2":
            print_all_reservations(id)
            user_home()
            return
        elif input_str == "3":
            print("------------------------------------------")
            print("До свидания. Нажмите любую кнопку, чтобы закрыть окно приложения.")
            input()
            return
        else:
            print("Мы не поняли, что вы хотите сделать, попробуйте снова")
            print("------------------")


def check_user_role(email, password):
    pwd_hash = compute_sha256_hash(password)
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        query = "SELECT role FROM user WHERE email=%s AND password_hash=%s"
        cursor.execute(query, (email, pwd_hash))

        row = cursor.fetchone()
        if row is not None:
            role = row[0]
            return role
        return "user"
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        return "Error"
    finally:
        connection.close()


def compute_sha256_hash(input_str):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_str.encode("utf-8"))
    return sha256_hash.hexdigest()


def generate_password():
    valid_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    buffer = [random.choice(valid_chars) for i in range(17)]
    return "".join(buffer)


def check_credentials(email, password):
    pwd_hash = compute_sha256_hash(password)
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        query = (
            "SELECT email, password_hash FROM user WHERE email=%s AND password_hash=%s"
        )
        cursor.execute(query, (email, pwd_hash))
        row = cursor.fetchone()
        if row is not None:
            found_email, found_password = row
            if found_email == email and found_password == pwd_hash:
                return True
            else:
                return False
        else:
            return False
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        return False
    finally:
        connection.close()


def get_user_id(email, password):
    pwd_hash = compute_sha256_hash(password)
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        query = "SELECT id FROM user WHERE email=%s AND password_hash=%s"
        cursor.execute(query, (email, pwd_hash))
        row = cursor.fetchone()
        if row is not None:
            user_id = row[0]
            return user_id
        return "Error"
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        return "Error"
    finally:
        connection.close()


def authenticate():
    global id
    is_authorised = False
    while not is_authorised:
        print("------------------")
        input_email = input("Введите адрес электронной почты: ")
        input_password = input("Введите пароль: ")
        is_authorised = check_credentials(input_email, input_password)
        id = get_user_id(input_email, input_password)
        if is_authorised:
            if check_user_role(input_email, input_password) == "admin":
                print("[Успех] Вход выполнен успешно")
                admin_home()
            else:
                print("[Успех] Вход выполнен успешно")
                user_home()
        if not is_authorised:
            print("[Ошибка] Неправильный адрес электронной почты или пароль.")


def add_user(first_name, middle_name, last_name, email, pwd_hash, role):
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        sql = "INSERT INTO user (first_name, middle_name, last_name, email, password_hash, role) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (first_name, middle_name or None, last_name, email, pwd_hash, role)
        cursor.execute(sql, values)
        connection.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        return False
    finally:
        connection.close()


def register():
    print("------------------")
    input_last_name = input("Введите фамилию: ")
    input_first_name = input("Введите имя: ")
    input_middle_name = input("Введите отчество (при наличии): ")
    input_email = input("Введите адрес электронной почты: ")
    input_password = input(
        "Введите пароль (оставив поле пустым, пароль будет сгенерирован автоматически): "
    )
    if not input_password.strip():
        generated_password = generate_password()

    add_user(
        input_first_name,
        input_middle_name,
        input_last_name,
        input_email,
        compute_sha256_hash(generated_password),
        "user",
    )

    print("[Успех] Регистрация прошла успешно")
    print(f"Ваш пароль: {generated_password}")
    print("Выполните вход в приложение")
    authenticate()


def get_departure_airport():
    cityCount = 0
    connection = mysql.connector.connect(**connection_string)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT city.name, airport.name FROM city INNER JOIN airport ON city.id = airport.city_id"
            cursor.execute(sql)
            result = cursor.fetchall()
            print("Выберите город отправления")
            for row in result:
                cityName = row[0]
                airportName = row[1]
                cityCount += 1
                print(f"\t({cityCount}) {cityName} ({airportName})")
            while True:
                input_str = input("> ")
                if input_str == "1":
                    return "DME"
                elif input_str == "2":
                    return "AER"
                elif input_str == "3":
                    return "LED"
                else:
                    print("Мы не поняли, что вы хотите сделать, попробуйте снова")
                    print("------------------")
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        return "Error"
    finally:
        connection.close()


def get_arrival_airport(airportName):
    cityCount = 0
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT DISTINCT c2.name, a2.name FROM city c1 JOIN airport a1 ON c1.id = a1.city_id JOIN flight f ON f.departure_airport_id = a1.id JOIN airport a2 ON f.arrival_airport_id = a2.id JOIN city c2 ON a2.city_id = c2.id WHERE a1.name = %s",
            (airportName,),
        )
        reader = cursor.fetchall()
        print("Выберите город прибытия")
        for row in reader:
            destinationCity = row[0]
            destinationAirport = row[1]
            cityCount += 1
            print(f"\t({cityCount}) {destinationCity} ({destinationAirport})")
        while True:
            inputStr = input("> ")
            if airportName == "DME":
                if inputStr == "1":
                    return "AER"
                elif inputStr == "2":
                    return "LED"
                else:
                    print("Мы не поняли, что вы хотите сделать, попробуйте снова")
                    print("------------------")
            elif airportName == "AER":
                if inputStr == "1":
                    return "DME"
                elif inputStr == "2":
                    return "LED"
                else:
                    print("Мы не поняли, что вы хотите сделать, попробуйте снова")
                    print("------------------")

            elif airportName == "LED":
                if inputStr == "1":
                    return "DME"
                else:
                    print("Мы не поняли, что вы хотите сделать, попробуйте снова")
                    print("------------------")
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        return "Error"
    finally:
        connection.close()


def get_route(dAirport, aAirport):
    connection = mysql.connector.connect(**connection_string)
    dCityName = ""
    aCityName = ""
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT city.name FROM city WHERE city.id = (SELECT airport.city_id FROM airport WHERE airport.name = %s)",
            (dAirport,),
        )
        result = cursor.fetchone()
        dCityName = result[0]
        cursor.execute(
            "SELECT city.name FROM city WHERE city.id = (SELECT airport.city_id FROM airport WHERE airport.name = %s)",
            (aAirport,),
        )
        result = cursor.fetchone()
        aCityName = result[0]
        print(f"Вы выбрали направление {dCityName} - {aCityName}")
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
    finally:
        connection.close()


def get_flight(departureAirport, arrivalAirport):
    flightCount = 0
    connection = mysql.connector.connect(**connection_string)
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                """SELECT flight.flight_number,
                                      departure_city.name AS departure_city_name,
                                      arrival_city.name AS arrival_city_name,
                                      departure_airport.name AS departure_airport_name,
                                      arrival_airport.name AS arrival_airport_name,
                                      flight.departure_time,
                                      flight.arrival_time,
                                      flight.econom_price,
                                      flight.business_price
                                    FROM flight 
                                      INNER JOIN airport AS departure_airport ON flight.departure_airport_id = departure_airport.id 
                                      INNER JOIN airport AS arrival_airport ON flight.arrival_airport_id = arrival_airport.id 
                                      INNER JOIN city AS departure_city ON departure_airport.city_id = departure_city.id 
                                      INNER JOIN city AS arrival_city ON arrival_airport.city_id = arrival_city.id 
                                    WHERE 
                                      departure_airport.name = %s 
                                      AND arrival_airport.name = %s""",
                (departureAirport, arrivalAirport),
            )
            flights = cursor.fetchall()
            print("Выберите рейс из списка доступных рейсов")
            print(
                "\tНомер рейса\tГород вылета\tГород прилета\tВремя вылета\t\tВремя прилета\t\tЭконом-класс\t\t\tБизнес-класс"
            )
            for flight in flights:
                flightNumber = flight[0]
                departureCityName = flight[1]
                arrivalCityName = flight[2]
                departureAirportName = flight[3]
                arrivalAirportName = flight[4]
                departureTime = flight[5]
                arrivalTime = flight[6]
                economPrice = flight[7]
                businessPrice = flight[8]
                flightCount += 1
                print(
                    f"\t({flightCount}) {flightNumber}\t{departureCityName} ({departureAirportName})\t{arrivalCityName} ({arrivalAirportName})\t{departureTime}\t{arrivalTime}\t{economPrice} ₽\t\t\t{businessPrice} ₽"
                )
            while True:
                inputStr = input("> ")
                if departureAirport == "DME" and arrivalAirport == "AER":
                    if inputStr == "1":
                        return "1"
                    elif inputStr == "2":
                        return "6"
                    else:
                        print("Мы не поняли, что вы хотите сделать, попробуйте снова")
                        print("------------------")
                elif departureAirport == "DME" and arrivalAirport == "LED":
                    if inputStr == "1":
                        return "2"
                    else:
                        print("Мы не поняли, что вы хотите сделать, попробуйте снова")
                        print("------------------")
                elif departureAirport == "AER" and arrivalAirport == "DME":
                    if inputStr == "1":
                        return "3"
                    else:
                        print("Мы не поняли, что вы хотите сделать, попробуйте снова")
                        print("------------------")
                elif departureAirport == "AER" and arrivalAirport == "LED":
                    if inputStr == "1":
                        return "4"
                    elif inputStr == "2":
                        return "7"
                    else:
                        print("Мы не поняли, что вы хотите сделать, попробуйте снова")
                        print("------------------")
                elif departureAirport == "LED" and arrivalAirport == "DME":
                    if inputStr == "1":
                        return "5"
                    else:
                        print("Мы не поняли, что вы хотите сделать, попробуйте снова")
                    print("------------------")
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        return "Error"
    finally:
        connection.close()


def confirm_flight(flight_id):
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        command = "SELECT flight.flight_number, dep_city.name AS departure_city, arr_city.name AS arrival_city, dep_airport.name AS departure_airport, arr_airport.name AS arrival_airport, flight.departure_time, flight.arrival_time FROM flight INNER JOIN airport AS dep_airport ON flight.departure_airport_id = dep_airport.id INNER JOIN city AS dep_city ON dep_airport.city_id = dep_city.id INNER JOIN airport AS arr_airport ON flight.arrival_airport_id = arr_airport.id INNER JOIN city AS arr_city ON arr_airport.city_id = arr_city.id WHERE flight.id = %s"
        cursor.execute(command, (int(flight_id),))
        result = cursor.fetchall()

        print("Вы выбрали рейс")
        print(
            "\tНомер рейса\tГород вылета\tГород прилета\tВремя вылета\t\tВремя прилета"
        )
        for row in result:
            flightNumber = row[0]
            departureCityName = row[1]
            arrivalCityName = row[2]
            departureAirportName = row[3]
            arrivalAirportName = row[4]
            departureTime = row[5]
            arrivalTime = row[6]
            print(
                f"\t{flightNumber}\t\t{departureCityName} ({departureAirportName})\t{arrivalCityName} ({arrivalAirportName})\t{departureTime}\t{arrivalTime}"
            )

        print("Вы уверены в правильности выбора рейса?")
        print("\t(1) Да\n\t(2) Нет")
        while True:
            input_value = input("> ")
            if input_value == "1":
                return True
            elif input_value == "2":
                return False
            else:
                print("Мы не поняли, что вы хотите сделать, попробуйте снова")
                print("------------------")
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        return False
    finally:
        if connection.is_connected():
            connection.close()


def check_ticket_available(flight_id):
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        command = "SELECT ticket_available FROM flight WHERE id = %s"
        cursor.execute(command, (int(flight_id),))
        ticket_available = cursor.fetchone()[0]

        if ticket_available <= 0:
            print("[Предупреждение] Все билеты на этот рейс уже распроданы")
            return False
        else:
            return True
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        return False
    finally:
        connection.close()


def select_airplane_class():
    print("Выберите класс обслуживания в самолете")
    print("\t(1) Эконом-класс\n\t(2) Бизнес-класс")
    while True:
        input_val = input("> ")
        if input_val == "1":
            return "econom"
        elif input_val == "2":
            return "business"
        else:
            print("Мы не поняли, что вы хотите сделать, попробуйте снова")
            print("------------------")


def add_reservation(user_id, flight_id, flight_class, res_status, price):
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        query = "INSERT INTO reservation (user_id, flight_id, class, status, price) VALUES (%s, %s, %s, %s, %s)"
        values = (int(user_id), int(flight_id), flight_class, res_status, int(price))
        cursor.execute(query, values)
        rows_affected = cursor.rowcount
        if rows_affected > 0:
            print("[Успех] Билет успешно зарезервирован")
            query1 = "UPDATE flight SET ticket_available = ticket_available - 1 WHERE id = %s"
            values1 = (int(flight_id),)
            cursor.execute(query1, values1)
            connection.commit()
            return True
        else:
            return False
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        connection.rollback()
        return False
    finally:
        connection.close()


def get_ticket_price(selectedFlight, selectedClass):
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        if selectedClass == "econom":
            query = "SELECT econom_price FROM flight WHERE id = %s"
        else:
            query = "SELECT business_price FROM flight WHERE id = %s"
        cursor.execute(query, (selectedFlight,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return 0
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
        return 0
    finally:
        connection.close()


def pay_ticket(price):
    print("Перейдем к процессу оплаты")
    return True


def get_payment(isReadyToPay, price):
    Facts = [
        "в отличие от взрослых кошек, котята не могут производить мяуканье, пока не достигнут возраста 2-3 недель",
        "гусята могут плавать сразу после рождения",
        "щенки родятся слепыми и глухими, но начинают видеть и слышать в течение нескольких недель",
        "у котят рождается только один зубок, и он не заменяется другим до возраста 3-4 недель",
        "гусята имеют прекрасный зрительный аппарат и могут видеть до 180 градусов, что помогает им обнаруживать возможные опасности",
        "у щенков зубы начинают расти в возрасте около 3-4 недель, и они начинают играть и кусаться, что помогает им тренировать свои челюсти и зубы",
        "котята растут очень быстро: за первую неделю своей жизни они увеличивают свой вес в два раза",
        "гусята считаются одними из самых интеллектуальных птиц и могут узнавать своих хозяев и других гусей по голосу",
        "щенки любят играть и общаться друг с другом, что помогает им развивать социальные навыки и учиться правилам поведения",
        "котята спят примерно 18 часов в день, что помогает им расти и развиваться",
        "у гусят очень чувствительная кожа, что помогает им оставаться теплыми в холодную погоду",
        "щенки растут очень быстро, и уже к 6-месячному возрасту они могут весить в несколько раз больше своего веса при рождении",
        "в некоторых культурах котята считаются символом удачи",
        "гусята могут стать очень привязанными к своим хозяевам и даже следовать за ними, как собаки",
        "щенки могут учиться новым командам и трюкам очень быстро, что делает их отличными домашними питомцами и спутниками",
    ]
    random.seed(time.time())
    time.sleep(3)
    print("Отлично, мы уже нашли данные вашей банковской карты в интернете.")
    print(f"С вашей банковской карты будет списана сумма в размере {price} ₽")
    print("*Производим процесс оплаты*")
    time.sleep(5)
    print(f"А вы знали, что {Facts[random.randint(0, len(Facts) - 1)]}?")
    time.sleep(5)
    print("[Успех] Оплата прошла успешно")


def print_all_reservations(user_id):
    res_count = 0
    connection = mysql.connector.connect(**connection_string)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """SELECT reservation.id, flight.flight_number, departure_city.name AS departure_city,
        departure_airport.name AS departure_airport, arrival_city.name AS arrival_city,
        arrival_airport.name AS arrival_airport, flight.departure_time, flight.arrival_time,
        aircraft.model, reservation.class, reservation.status, reservation.price
        FROM reservation
        INNER JOIN flight ON reservation.flight_id = flight.id
        INNER JOIN aircraft ON flight.aircraft_id = aircraft.id
        INNER JOIN airport AS departure_airport ON flight.departure_airport_id = departure_airport.id
        INNER JOIN city AS departure_city ON departure_airport.city_id = departure_city.id
        INNER JOIN airport AS arrival_airport ON flight.arrival_airport_id = arrival_airport.id
        INNER JOIN city AS arrival_city ON arrival_airport.city_id = arrival_city.id
        WHERE reservation.user_id = %s""",
            (int(user_id),),
        )
        results = cursor.fetchall()
        if len(results) > 0:
            print("Список купленных билетов")
            print("------------------------")
            for row in results:
                reservation_id = row[0]
                flight_number = row[1]
                departure_city = row[2]
                departure_a = row[3]
                arrival_city = row[4]
                arrival_a = row[5]
                dep_time = row[6]
                arr_time = row[7]
                model = row[8]
                aclass = row[9]
                status = row[10]
                price = row[11]
                res_count += 1
                print(
                    f"\t({res_count})\t\t{reservation_id}\t{flight_number}\t\t{departure_city} ({departure_a})\t{arrival_city} ({arrival_a})\t\t{dep_time}\t\t{arr_time}\t\t{model}\t\t{aclass}\t{price}"
                )
        else:
            print("Нет купленных билетов.")
    except mysql.connector.Error as error:
        print(f"[Ошибка базы данных] {error}")
    finally:
        connection.close()


def buy_ticket():
    departureAirport = get_departure_airport()
    arrivalAirport = get_arrival_airport(departureAirport)
    get_route(departureAirport, arrivalAirport)
    selectedFlight = get_flight(departureAirport, arrivalAirport)
    if check_ticket_available(selectedFlight):
        isConfirmed = confirm_flight(selectedFlight)
        selectedClass = ""
        if isConfirmed:
            selectedClass = select_airplane_class()
            get_payment(
                pay_ticket(get_ticket_price(selectedFlight, selectedClass)),
                get_ticket_price(selectedFlight, selectedClass),
            )
            add_reservation(
                id,
                selectedFlight,
                selectedClass,
                "paid",
                get_ticket_price(selectedFlight, selectedClass),
            )
        else:
            while not isConfirmed:
                departureAirport = get_departure_airport()
                arrivalAirport = get_arrival_airport(departureAirport)
                get_route(departureAirport, arrivalAirport)
                selectedFlight = get_flight(departureAirport, arrivalAirport)
                isConfirmed = confirm_flight(selectedFlight)
                selectedClass = select_airplane_class()
                get_payment(
                    pay_ticket(get_ticket_price(selectedFlight, selectedClass)),
                    get_ticket_price(selectedFlight, selectedClass),
                )
                add_reservation(
                    id,
                    selectedFlight,
                    selectedClass,
                    "paid",
                    get_ticket_price(selectedFlight, selectedClass),
                )
    else:
        departureAirport = get_departure_airport()
        arrivalAirport = get_arrival_airport(departureAirport)
        get_route(departureAirport, arrivalAirport)
        selectedFlight = get_flight(departureAirport, arrivalAirport)
        isConfirmed = confirm_flight(selectedFlight)
        if isConfirmed:
            selectedClass = select_airplane_class()
            get_payment(
                pay_ticket(get_ticket_price(selectedFlight, selectedClass)),
                get_ticket_price(selectedFlight, selectedClass),
            )
            add_reservation(
                id,
                selectedFlight,
                selectedClass,
                "paid",
                get_ticket_price(selectedFlight, selectedClass),
            )
        else:
            while not isConfirmed:
                departureAirport = get_departure_airport()
                arrivalAirport = get_arrival_airport(departureAirport)
                get_route(departureAirport, arrivalAirport)
                selectedFlight = get_flight(departureAirport, arrivalAirport)
                isConfirmed = confirm_flight(selectedFlight)
                selectedClass = select_airplane_class()
                get_payment(
                    pay_ticket(get_ticket_price(selectedFlight, selectedClass)),
                    get_ticket_price(selectedFlight, selectedClass),
                )
                add_reservation(
                    id,
                    selectedFlight,
                    selectedClass,
                    "paid",
                    get_ticket_price(selectedFlight, selectedClass),
                )


# ----------
# Приложение
# ----------
def app():
    print("GoslingSkyways - перелеты, которые запомнятся навсегда.")
    print(
        "Нам по плечу любые погодные условия, ведь гуси прекрасно летают и в дождь, и в снегопад!\n"
    )

    while True:  # начальный экран
        print("Выберите действие:")
        print(
            "\t(1) Вход в аккаунт\n\t(2) Регистрация аккаунта\n\t(3) Добавить тестовые данные\n\t(4) Удалить данные\n\t(5) Выход из приложения"
        )
        choice = input("> ")

        if choice == "1":
            authenticate()
            break
        elif choice == "2":
            register()
            break
        elif choice == "3":
            insert_data()
            break
        elif choice == "4":
            delete_data_prompt()
            break
        elif choice == "5":
            print("------------------------------------------")
            print("До свидания. Нажмите любую кнопку, чтобы закрыть окно приложения.")
            input()
            break
        else:
            print("Мы не поняли, что вы хотите сделать, попробуйте снова")
            print("------------------")


def create_db_prompt():
    if not db_connection_check():
        while True:
            print(
                "Желаете создать базу данных?\n\t(1) Да\n\t(2) Нет\n\t(3) Выход из приложения"
            )
            input_str = input("> ")
            if input_str == "1":
                create_db()
                print("[Успех] База данных создана успешно")
                create_tables()
                print("[Успех] Таблицы успешно добавлены в базу данных")
                return
            elif input_str == "2":
                print("Операция отменена пользователем")
                return
            elif input_str == "3":
                print("------------------------------------------")
                print(
                    "До свидания. Нажмите любую кнопку, чтобы закрыть окно приложения."
                )
                input()
                return
            else:
                print("Мы не поняли, что вы хотите сделать, попробуйте снова")
                print("------------------")

    else:
        app()


create_db_prompt()
