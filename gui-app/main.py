import hashlib
import random
import string
import sys

import mysql.connector
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

id = ""
connection_string = {
    "user": "root",
    "password": "", # возможно нужно изменить на root
    "host": "localhost",
    "database": "goslingskyways"
}

connection_string_for_db_create = {
    "user": "root",
    "password": "", # возможно нужно изменить на root
    "host": "localhost"
}


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(450, 300)
        self.setWindowTitle("GoslingSkyways")

        logo_label = QLabel(self)
        pixmap = QPixmap("gui-app/airplane.png")
        pixmap2 = pixmap.scaledToWidth(128)
        pixmap3 = pixmap.scaledToHeight(128)
        logo_label.setPixmap(pixmap3)
        logo_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(
            "Добро пожаловать в приложение авиакомпании GoslingSkyways.\nВойдите в аккаунт или создайте новый.")
        text_label.setAlignment(Qt.AlignCenter)

        login_button = QPushButton("Вход")
        login_button.clicked.connect(self.open_login_window)
        reg_button = QPushButton("Регистрация")
        reg_button.clicked.connect(self.open_register_window)

        db_man_button = QPushButton("Операции с базой данных")
        db_man_button.clicked.connect(self.open_db_man_window)

        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(text_label)
        layout.addWidget(login_button)
        layout.addWidget(reg_button)
        layout.addWidget(db_man_button)
        self.setLayout(layout)

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.hide()

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.hide()

    def open_db_man_window(self):
        self.db_man_window = DatabaseActionsWindow()
        self.db_man_window.show()
        self.hide()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoslingSkyways - вход")
        self.setFixedSize(400, 200)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.authenticate)
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Адрес электронной почты:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password)
        layout.addWidget(login_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def check_user_role(self, email, password):
        pwd_hash = self.compute_sha256_hash(password)
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
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def compute_sha256_hash(self, input_str):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_str.encode("utf-8"))
        return sha256_hash.hexdigest()

    def generate_password(self):
        valid_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        buffer = [random.choice(valid_chars) for i in range(17)]
        return ''.join(buffer)

    def check_credentials(self, email, password):
        pwd_hash = self.compute_sha256_hash(password)
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "SELECT email, password_hash FROM user WHERE email=%s AND password_hash=%s"
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
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return False
        finally:
            connection.close()

    def get_user_id(self, email, password):
        pwd_hash = self.compute_sha256_hash(password)
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
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()

    def authenticate(self):
        global id
        is_authorised = False
        input_email = self.username.text()
        input_password = self.password.text()
        is_authorised = self.check_credentials(input_email, input_password)
        id = self.get_user_id(input_email, input_password)
        if is_authorised:
            if self.check_user_role(input_email, input_password) == "admin":
                msg = QMessageBox()

                msg.setText("Успех")
                msg.setInformativeText("Вход выполнен успешно")
                msg.setWindowTitle("Внимание")
                msg.exec_()
                self.go_admin_window()
            elif self.check_user_role(input_email, input_password) == "user":
                msg = QMessageBox()

                msg.setText("Успех")
                msg.setInformativeText("Вход выполнен успешно")
                msg.setWindowTitle("Внимание")
                msg.exec_()
                self.go_user_window()
            elif self.check_user_role(input_email, input_password) == "manager":
                msg = QMessageBox()

                msg.setText("Успех")
                msg.setInformativeText("Вход выполнен успешно")
                msg.setWindowTitle("Внимание")
                msg.exec_()
                self.go_manager_window()
            elif self.check_user_role(input_email, input_password) == "finance":
                msg = QMessageBox()

                msg.setText("Успех")
                msg.setInformativeText("Вход выполнен успешно")
                msg.setWindowTitle("Внимание")
                msg.exec_()
                self.go_finance_window()
        if not is_authorised:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText("Неправильный адрес электронной почты или пароль")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def go_back(self):
        self.start_window = StartWindow()
        self.start_window.show()
        self.hide()

    def go_admin_window(self):
        self.admin_window = AdminWindow()
        self.admin_window.show()
        self.hide()

    def go_user_window(self):
        self.user_window = UserWindow()
        self.user_window.show()
        self.hide()

    def go_manager_window(self):
        self.manager_window = ManagerWindow()
        self.manager_window.show()
        self.hide()

    def go_finance_window(self):
        self.finance_window = FinanceWindow()
        self.finance_window.show()
        self.hide()


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoslingSkyways - регистрация")
        self.setFixedSize(500, 400)

        self.lastname = QLineEdit()
        self.firstname = QLineEdit()
        self.middlename = QLineEdit()
        self.email = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        reg_button = QPushButton("Зарегистрироваться")
        reg_button.clicked.connect(self.register)
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Фамилия:"))
        layout.addWidget(self.lastname)
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.firstname)
        layout.addWidget(QLabel("Отчество (при наличии):"))
        layout.addWidget(self.middlename)
        layout.addWidget(QLabel("Адрес электронной почты:"))
        layout.addWidget(self.email)
        layout.addWidget(QLabel("Пароль (оставив поле пустым, пароль будет сгенерирован автоматически):"))
        layout.addWidget(self.password)
        layout.addWidget(reg_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def go_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.hide()

    def go_back(self):
        self.start_window = StartWindow()
        self.start_window.show()
        self.hide()

    def compute_sha256_hash(self, input_str):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_str.encode("utf-8"))
        return sha256_hash.hexdigest()

    def generate_password(self):
        valid_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        buffer = [random.choice(valid_chars) for i in range(17)]
        return ''.join(buffer)

    def add_user(self, first_name, middle_name, last_name, email, pwd_hash, role):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO user (first_name, middle_name, last_name, email, password_hash, role) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (first_name, middle_name or None, last_name, email, pwd_hash, role)
            cursor.execute(sql, values)
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return False
        finally:
            connection.close()

    def register(self):
        input_firstname = self.firstname.text()
        input_middlename = self.middlename.text()
        input_lastname = self.lastname.text()
        input_email = self.email.text()
        input_password = self.password.text()
        if not input_password.strip():
            generated_password = self.generate_password()
            self.add_user(input_firstname, input_middlename, input_lastname, input_email,
                          self.compute_sha256_hash(generated_password), "user")

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"Пользователь успешно создан\nВаш пароль: {generated_password}")
            msg.setWindowTitle("Успех")
            msg.exec_()
            print("[Успех] Регистрация прошла успешно")
            print(f"Ваш пароль: {generated_password}")
        else:
            self.add_user(input_firstname, input_middlename, input_lastname, input_email,
                          self.compute_sha256_hash(input_password), "user")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"Пользователь успешно создан")
            msg.setWindowTitle("Успех")
            msg.exec_()
            print("[Успех] Регистрация прошла успешно")
        self.go_login_window()
        # print("Выполните вход в приложение")
        # authenticate()


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoslingSkyways")
        self.setFixedSize(500, 400)
        global id

        greeting_label = QLabel(f"Здравствуйте, {self.get_name(id)}\nЧто вы хотите сделать?")
        greeting_label.setAlignment(Qt.AlignCenter)

        buy_ticket_button = QPushButton("Купить билет")
        buy_ticket_button.clicked.connect(self.buy_ticket)
        ticket_list_button = QPushButton("Посмотреть купленные билеты")
        ticket_list_button.clicked.connect(self.go_reservations)
        add_admin_button = QPushButton("Добавить администратора")
        add_admin_button.clicked.connect(self.go_admin_reg)
        delete_account_button = QPushButton("Удалить аккаунт")
        delete_account_button.clicked.connect(self.delete_account)
        exit_button = QPushButton("Выйти")
        exit_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(greeting_label)

        layout.addWidget(buy_ticket_button)
        layout.addWidget(ticket_list_button)
        layout.addWidget(add_admin_button)
        layout.addWidget(delete_account_button)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def get_name(self, id):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "SELECT first_name FROM user WHERE id=%s"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if row is not None:
                user_id = row[0]
                return user_id
            return "Error"
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()

    def buy_ticket(self):
        self.buy_ticket_window = BuyTicketWindow()
        self.buy_ticket_window.show()
        self.hide()

    def go_reservations(self):
        self.go_reservations = GetReservations()
        self.go_reservations.show()
        self.hide()

    def go_admin_reg(self):
        self.go_admin_reg = AdminRegisterWindow()
        self.go_admin_reg.show()
        self.hide()

    def go_start(self):
        self.go_start = StartWindow()
        self.go_start.show()
        self.hide()

    def delete_account(self):
        global id
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM reservation WHERE user_id = %s", (id,))
            count = cursor.fetchone()[0]
            if count > 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка удаления пользователя")
                msg.setInformativeText("Нельзя удалить пользователя, у которого есть бронирования на рейсы")
                msg.setWindowTitle("Ошибка")
                msg.exec_()
                return
            cursor.execute("DELETE FROM user WHERE id = %s", (id,))
            connection.commit()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Пользователь успешно удален")
            msg.setWindowTitle("Успех")
            msg.exec_()
            self.go_start()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()


class UserWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoslingSkyways")
        self.setFixedSize(500, 400)
        global id

        greeting_label = QLabel(f"Здравствуйте, {self.get_name(id)}\nЧто вы хотите сделать?")
        greeting_label.setAlignment(Qt.AlignCenter)

        buy_ticket_button = QPushButton("Купить билет")
        buy_ticket_button.clicked.connect(self.buy_ticket)
        ticket_list_button = QPushButton("Посмотреть купленные билеты")
        ticket_list_button.clicked.connect(self.go_reservations)
        delete_account_button = QPushButton("Удалить аккаунт")
        delete_account_button.clicked.connect(self.delete_account)
        exit_button = QPushButton("Выйти")
        exit_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(greeting_label)

        layout.addWidget(buy_ticket_button)
        layout.addWidget(ticket_list_button)
        layout.addWidget(delete_account_button)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def get_name(self, id):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "SELECT first_name FROM user WHERE id=%s"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if row is not None:
                user_id = row[0]
                return user_id
            return "Error"
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()

    def buy_ticket(self):
        self.buy_ticket_window = BuyTicketWindow()
        self.buy_ticket_window.show()
        self.hide()

    def go_reservations(self):
        self.go_reservations = GetReservations()
        self.go_reservations.show()
        self.hide()

    def go_start(self):
        self.go_start = StartWindow()
        self.go_start.show()
        self.hide()

    def delete_account(self):
        global id
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM reservation WHERE user_id = %s", (id,))
            count = cursor.fetchone()[0]
            if count > 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка удаления пользователя")
                msg.setInformativeText("Нельзя удалить пользователя, у которого есть бронирования на рейсы")
                msg.setWindowTitle("Ошибка")
                msg.exec_()
                return
            cursor.execute("DELETE FROM user WHERE id = %s", (id,))
            connection.commit()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Пользователь успешно удален")
            msg.setWindowTitle("Успех")
            msg.exec_()
            self.go_start()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()


class FinanceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoslingSkyways")
        self.setFixedSize(500, 400)
        global id

        greeting_label = QLabel(f"Здравствуйте, {self.get_name(id)}\nЧто вы хотите сделать?")
        greeting_label.setAlignment(Qt.AlignCenter)

        buy_ticket_button = QPushButton("Купить билет")
        buy_ticket_button.clicked.connect(self.buy_ticket)
        ticket_list_button = QPushButton("Посмотреть купленные билеты")
        ticket_list_button.clicked.connect(self.go_reservations)
        report_button = QPushButton("Посмотреть отчет")
        report_button.clicked.connect(self.get_report)
        delete_account_button = QPushButton("Удалить аккаунт")
        delete_account_button.clicked.connect(self.delete_account)
        exit_button = QPushButton("Выйти")
        exit_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(greeting_label)

        layout.addWidget(buy_ticket_button)
        layout.addWidget(ticket_list_button)
        layout.addWidget(report_button)
        layout.addWidget(delete_account_button)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def get_name(self, id):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "SELECT first_name FROM user WHERE id=%s"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if row is not None:
                user_id = row[0]
                return user_id
            return "Error"
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()

    def buy_ticket(self):
        self.buy_ticket_window = BuyTicketWindow()
        self.buy_ticket_window.show()
        self.hide()

    def go_reservations(self):
        self.go_reservations = GetReservations()
        self.go_reservations.show()
        self.hide()

    def go_start(self):
        self.go_start = StartWindow()
        self.go_start.show()
        self.hide()

    def get_report(self):
        self.get_report = ReportWindow()
        self.get_report.show()
        self.hide()

    def delete_account(self):
        global id
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM reservation WHERE user_id = %s", (id,))
            count = cursor.fetchone()[0]
            if count > 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка удаления пользователя")
                msg.setInformativeText("Нельзя удалить пользователя, у которого есть бронирования на рейсы")
                msg.setWindowTitle("Ошибка")
                msg.exec_()
                return
            cursor.execute("DELETE FROM user WHERE id = %s", (id,))
            connection.commit()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Пользователь успешно удален")
            msg.setWindowTitle("Успех")
            msg.exec_()
            self.go_start()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()


class ReportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoslingSkyways")
        self.setFixedSize(500, 400)
        global id

        heading_label = QLabel("Финансовый отчет")
        heading_label.setAlignment(Qt.AlignCenter)
        r1_label = QLabel(f"Самый популярный рейс: {self.get_most_popular_flight()}")
        r1_label.setAlignment(Qt.AlignLeft)
        r2_label = QLabel(f"Доход от самого популярного рейса: {self.get_most_popular_flight_revenue()}")
        r2_label.setAlignment(Qt.AlignLeft)
        r3_label = QLabel(f"Общий доход за все время: {self.get_total_revenue()}")
        r3_label.setAlignment(Qt.AlignLeft)

        go_back_button = QPushButton("Назад")
        go_back_button.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(heading_label)
        layout.addWidget(r1_label)
        layout.addWidget(r2_label)
        layout.addWidget(r3_label)
        layout.addWidget(go_back_button)

        self.setLayout(layout)

    def get_most_popular_flight(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            most_popular_direction_query = """
            SELECT flight.flight_number, COUNT(*) AS reservation_count
            FROM reservation
            INNER JOIN flight ON reservation.flight_id = flight.id
            GROUP BY flight.id
            ORDER BY reservation_count DESC
            LIMIT 1
            """
            cursor.execute(most_popular_direction_query)
            most_popular_direction = cursor.fetchone()
            return most_popular_direction
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()

    def get_flight_id(self, flight_number):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "SELECT id FROM flight WHERE flight_number = %s"
            values = (flight_number,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result[0]
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            connection.rollback()
            return False
        finally:
            connection.close()

    def get_most_popular_flight_revenue(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()

            most_popular_direction_query = """
                        SELECT flight.flight_number, COUNT(*) AS reservation_count
                        FROM reservation
                        INNER JOIN flight ON reservation.flight_id = flight.id
                        GROUP BY flight.id
                        ORDER BY reservation_count DESC
                        LIMIT 1
                        """
            cursor.execute(most_popular_direction_query)
            most_popular_direction = cursor.fetchone()

            most_popular_direction_revenue_query = f"""
            SELECT SUM(price) AS revenue
            FROM reservation
            WHERE flight_id = {self.get_flight_id(most_popular_direction[0])}
            """
            cursor.execute(most_popular_direction_revenue_query)
            most_popular_direction_revenue = cursor.fetchone()
            return most_popular_direction_revenue
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()

    def get_total_revenue(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            total_revenue_query = """
            SELECT SUM(price) AS revenue
            FROM reservation
            """
            cursor.execute(total_revenue_query)
            total_revenue = cursor.fetchone()
            return total_revenue
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()

    def go_back(self):
        self.finance_window = FinanceWindow()
        self.finance_window.show()
        self.hide()


class ManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoslingSkyways")
        self.setFixedSize(500, 400)
        global id

        greeting_label = QLabel(f"Здравствуйте, {self.get_name(id)}\nЧто вы хотите сделать?")
        greeting_label.setAlignment(Qt.AlignCenter)

        buy_ticket_button = QPushButton("Купить билет")
        buy_ticket_button.clicked.connect(self.buy_ticket)
        ticket_list_button = QPushButton("Посмотреть купленные билеты")
        ticket_list_button.clicked.connect(self.go_reservations)
        all_ticket_list_button = QPushButton("Посмотреть все рейсы")
        all_ticket_list_button.clicked.connect(self.go_routes)
        delete_account_button = QPushButton("Удалить аккаунт")
        delete_account_button.clicked.connect(self.delete_account)
        exit_button = QPushButton("Выйти")
        exit_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(greeting_label)

        layout.addWidget(buy_ticket_button)
        layout.addWidget(ticket_list_button)
        layout.addWidget(all_ticket_list_button)
        layout.addWidget(delete_account_button)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def get_name(self, id):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "SELECT first_name FROM user WHERE id=%s"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if row is not None:
                user_id = row[0]
                return user_id
            return "Error"
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()

    def buy_ticket(self):
        self.buy_ticket_window = BuyTicketWindow()
        self.buy_ticket_window.show()
        self.hide()

    def go_reservations(self):
        self.go_reservations = GetReservations()
        self.go_reservations.show()
        self.hide()

    def go_start(self):
        self.go_start = StartWindow()
        self.go_start.show()
        self.hide()

    def go_routes(self):
        self.go_routes = RoutesWindow()
        self.go_routes.show()
        self.hide()

    def delete_account(self):
        global id
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM reservation WHERE user_id = %s", (id,))
            count = cursor.fetchone()[0]
            if count > 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка удаления пользователя")
                msg.setInformativeText("Нельзя удалить пользователя, у которого есть бронирования на рейсы")
                msg.setWindowTitle("Ошибка")
                msg.exec_()
                return
            cursor.execute("DELETE FROM user WHERE id = %s", (id,))
            connection.commit()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Пользователь успешно удален")
            msg.setWindowTitle("Успех")
            msg.exec_()
            self.go_start()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()


class RoutesWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.setFixedSize(450, 300)
        self.setWindowTitle("GoslingSkyways - просмотр всех рейсов")

        self.rou_table = QTableWidget()

        self.rou_update_button = QPushButton("Обновить список рейсов")
        self.rou_update_button.clicked.connect(self.print_all_routes)
        self.go_back_button = QPushButton("Назад")
        self.go_back_button.clicked.connect(self.go_home)

        layout = QVBoxLayout()
        layout.addWidget(self.rou_table)
        layout.addWidget(self.rou_update_button)
        layout.addWidget(self.go_back_button)
        self.setLayout(layout)

    def print_all_routes(self):
        global id
        res_count = 0
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM flight")
            results = cursor.fetchall()
            if len(results) > 0:
                self.rou_table.setRowCount(len(results))
                self.rou_table.setColumnCount(len(results[0]))
                self.rou_table.setHorizontalHeaderLabels(
                    ['Ид', 'Номер рейса', 'Аэропорт отправления', 'Аэропорт прибытия', 'Модель самолета',
                     'Время отправления', 'Время прибытия', 'Остаток билетов', 'Цена эконом-класс',
                     'Цена бизнес-класс'])
                for i, row in enumerate(results):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.rou_table.setItem(i, j, item)

                self.rou_table.setSelectionBehavior(QTableWidget.SelectRows)
                self.rou_table.setEditTriggers(QTableWidget.NoEditTriggers)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Внимание")
                msg.setInformativeText("Нет рейсов")
                msg.setWindowTitle("Ошибка")
                msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def check_role(self):
        global id
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "SELECT u.role FROM user u WHERE u.id = %s"
            values = (id,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            connection.rollback()
            return False
        finally:
            connection.close()

    def go_home(self):
        if self.check_role()[0] == "admin":
            self.admin_window = AdminWindow()
            self.admin_window.show()
            self.hide()
        elif self.check_role()[0] == "user":
            self.user_window = UserWindow()
            self.user_window.show()
            self.hide()
        elif self.check_role()[0] == "manager":
            self.manager_window = ManagerWindow()
            self.manager_window.show()
            self.hide()
        elif self.check_role()[0] == "finance":
            self.finance_window = FinanceWindow()
            self.finance_window.show()
            self.hide()


class BuyTicketWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.setFixedSize(450, 300)
        self.setWindowTitle("GoslingSkyways - покупка билета")

        dep_label = QLabel("Выберите город отправления")
        dep_label.setAlignment(Qt.AlignCenter)

        self.selectList1 = QComboBox()
        dep_cities = self.get_departure_airport()
        self.selectList1.addItems(dep_cities)

        self.check_direction_button = QPushButton("Обновить список направлений")
        self.check_direction_button.clicked.connect(self.check_arr)

        self.selectList2 = QComboBox()

        self.check_flights_button = QPushButton("Обновить список рейсов")
        self.check_flights_button.clicked.connect(self.check_flight)

        self.flight_table = QTableWidget()

        self.btngroup = QButtonGroup()
        self.btngroup.setExclusive(True)
        self.ebutton = QRadioButton("Эконом-класс")
        self.ebutton.setChecked(True)
        self.btngroup.addButton(self.ebutton)
        self.bbutton = QRadioButton("Бизнес-класс")
        self.bbutton.setChecked(False)
        self.btngroup.addButton(self.bbutton)

        self.buy_ticket_button = QPushButton("Купить билет")
        self.buy_ticket_button.clicked.connect(self.add_reservation)

        self.go_back_button = QPushButton("Назад")
        self.go_back_button.clicked.connect(self.go_home)

        layout = QVBoxLayout()
        layout.addWidget(self.selectList1)
        layout.addWidget(self.check_direction_button)
        layout.addWidget(self.selectList2)
        layout.addWidget(self.check_flights_button)
        layout.addWidget(self.flight_table)
        layout.addWidget(self.ebutton)
        layout.addWidget(self.bbutton)
        layout.addWidget(self.buy_ticket_button)
        layout.addWidget(self.go_back_button)
        self.setLayout(layout)

    def get_departure_airport(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT city.name, airport.name FROM city INNER JOIN airport ON city.id = airport.city_id"
                cursor.execute(sql)
                results = cursor.fetchall()
                return [result[0] for result in results]
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()

    def get_arrival_airport(self, airportName):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT DISTINCT c2.name
        FROM flight f
        JOIN airport a1 ON f.departure_airport_id = a1.id
        JOIN airport a2 ON f.arrival_airport_id = a2.id
        JOIN city c1 ON a1.city_id = c1.id
        JOIN city c2 ON a2.city_id = c2.id
        WHERE c1.name = %s""",
                (airportName,))
            reader = cursor.fetchall()
            return [result[0] for result in reader]

        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()

    def check_arr(self):
        self.selectList2.clear()
        arr_cities = self.get_arrival_airport(str(self.selectList1.currentText()))
        self.selectList2.addItems(arr_cities)

    def get_flight(self, departureAirport, arrivalAirport):
        connection = mysql.connector.connect(**connection_string)
        try:
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("""SELECT f.id, f.flight_number, c1.name AS departure_city, a1.name AS departure_airport, c2.name AS arrival_city, a2.name AS arrival_airport,
           f.departure_time, f.arrival_time, f.econom_price, f.business_price
    FROM flight f
    JOIN airport a1 ON f.departure_airport_id = a1.id
    JOIN airport a2 ON f.arrival_airport_id = a2.id
    JOIN city c1 ON a1.city_id = c1.id
    JOIN city c2 ON a2.city_id = c2.id
    WHERE c1.name = %s AND c2.name = %s""",
                               (departureAirport, arrivalAirport))
                flights = cursor.fetchall()
                return flights
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return "Error"
        finally:
            connection.close()

    def check_flight(self):
        flights = self.get_flight(self.selectList1.currentText(), self.selectList2.currentText())
        self.flight_table.setColumnCount(len(flights[0]))
        self.flight_table.setHorizontalHeaderLabels(
            ['Выбор', 'Номер рейса', 'Город отправления', 'Аэропорт отправления', 'Город прибытия', 'Аэропорт прибытия',
             'Время отправления', 'Время прибытия', 'Эконом-цена', 'Бизнес-цена'])
        self.flight_table.setRowCount(len(flights))
        for i, flight in enumerate(flights):
            radiobutton = QRadioButton()
            radiobutton.setProperty("flight_id", flight[0])
            self.flight_table.setCellWidget(i, 0, radiobutton)
            for j, cell in enumerate(flight):
                item = QTableWidgetItem(str(cell))
                self.flight_table.setItem(i, j, item)

        self.flight_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.flight_table.setEditTriggers(QTableWidget.NoEditTriggers)

    def get_flight_id(self, flight_number):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "SELECT id FROM flight WHERE flight_number = %s"
            values = (flight_number,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result[0]
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            connection.rollback()
            return False
        finally:
            connection.close()

    def db_res(self, id, flight_id, eprice, bprice):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "INSERT INTO reservation (user_id, flight_id, class, status, price) VALUES (%s, %s, %s, %s, %s)"
            if self.ebutton.isChecked():
                values = (int(id), int(flight_id), "econom", "paid", eprice)
            else:
                values = (int(id), int(flight_id), "business", "paid", bprice)
            cursor.execute(query, values)
            rows_affected = cursor.rowcount
            if rows_affected > 0:
                msg = QMessageBox()
                msg.setText("Успех")
                msg.setInformativeText("Билет успешно зарезервирован")
                msg.setWindowTitle("Успех")
                msg.exec_()
                query1 = "UPDATE flight SET ticket_available = ticket_available - 1 WHERE id = %s"
                values1 = (int(flight_id),)
                cursor.execute(query1, values1)
                connection.commit()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка")
                msg.setInformativeText("Нет доступных билетов на этот рейс")
                msg.setWindowTitle("Ошибка")
                msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            connection.rollback()
            return False
        finally:
            connection.close()

    def add_reservation(self):
        global id
        selected_item = self.flight_table.selectedItems()
        row = self.flight_table.currentRow()
        if row != -1:
            fid = self.flight_table.item(row, 1).text()
            dc = self.flight_table.item(row, 2).text()
            da = self.flight_table.item(row, 3).text()
            ac = self.flight_table.item(row, 4).text()
            aa = self.flight_table.item(row, 5).text()
            dt = self.flight_table.item(row, 6).text()
            at = self.flight_table.item(row, 7).text()
            ep = self.flight_table.item(row, 8).text()
            bp = self.flight_table.item(row, 9).text()
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            if self.ebutton.isChecked():
                msgBox.setText(
                    f"Вы выбрали рейс {fid} {dc} ({da}) - {ac} ({aa})\nВремя отправления: {dt}\nВремя прибытия: {at}\nСтоимость билета эконом-класса: {ep}₽")
            else:
                msgBox.setText(
                    f"Вы выбрали рейс {fid} {dc} ({da}) - {ac} ({aa})\nВремя отправления: {dt}\nВремя прибытия: {at}\n Стоимость билета бизнес-класса: {bp}₽")

            msgBox.setWindowTitle("Подтверждение выбора")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            ret = msgBox.exec_()
            if ret == QMessageBox.Ok:
                if self.db_res(id, self.get_flight_id(fid), ep, bp):
                    self.go_home()
            else:
                print("cancelled")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText("Пожалуйста, выберите рейс")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return

    def check_role(self):
        global id
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "SELECT u.role FROM user u WHERE u.id = %s"
            values = (id,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            connection.rollback()
            return False
        finally:
            connection.close()

    def go_home(self):
        if self.check_role()[0] == "admin":
            self.admin_window = AdminWindow()
            self.admin_window.show()
            self.hide()
        elif self.check_role()[0] == "user":
            self.user_window = UserWindow()
            self.user_window.show()
            self.hide()
        elif self.check_role()[0] == "manager":
            self.manager_window = ManagerWindow()
            self.manager_window.show()
            self.hide()
        elif self.check_role()[0] == "finance":
            self.finance_window = FinanceWindow()
            self.finance_window.show()
            self.hide()


class GetReservations(QWidget):
    def __init__(self):
        super().__init__()
        # self.setFixedSize(450, 300)
        self.setWindowTitle("GoslingSkyways - список бронирований")

        self.res_table = QTableWidget()

        self.res_update_button = QPushButton("Обновить список бронирований")
        self.res_update_button.clicked.connect(self.print_all_reservations)
        self.res_delete_button = QPushButton("Удалить бронирование")
        self.res_delete_button.clicked.connect(self.delete_res)
        self.go_back_button = QPushButton("Назад")
        self.go_back_button.clicked.connect(self.go_home)

        layout = QVBoxLayout()
        layout.addWidget(self.res_table)
        layout.addWidget(self.res_update_button)
        layout.addWidget(self.res_delete_button)
        layout.addWidget(self.go_back_button)
        self.setLayout(layout)

    def print_all_reservations(self):
        global id
        res_count = 0
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT reservation.id, flight.flight_number, departure_city.name AS departure_city,
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
            WHERE reservation.user_id = %s""", (id,))
            results = cursor.fetchall()
            if len(results) > 0:
                self.res_table.setRowCount(len(results))
                self.res_table.setColumnCount(len(results[0]))
                self.res_table.setHorizontalHeaderLabels(
                    ['', 'Номер рейса', 'Город отправления', 'Аэропорт отправления', 'Город прибытия',
                     'Аэропорт прибытия',
                     'Время отправления', 'Время прибытия', 'Модель самолета', 'Класс обслуживания', 'Статус', 'Цена'])
                for i, row in enumerate(results):
                    radiobutton = QRadioButton()
                    radiobutton.setProperty('', row[0])
                    self.res_table.setCellWidget(i, 0, radiobutton)
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.res_table.setItem(i, j, item)

                self.res_table.setSelectionBehavior(QTableWidget.SelectRows)
                self.res_table.setEditTriggers(QTableWidget.NoEditTriggers)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Внимание")
                msg.setInformativeText("У вас нет купленных билетов")
                msg.setWindowTitle("Ошибка")
                msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def check_role(self):
        global id
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "SELECT u.role FROM user u WHERE u.id = %s"
            values = (id,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            connection.rollback()
            return False
        finally:
            connection.close()

    def go_home(self):
        if self.check_role()[0] == "admin":
            self.admin_window = AdminWindow()
            self.admin_window.show()
            self.hide()
        elif self.check_role()[0] == "user":
            self.user_window = UserWindow()
            self.user_window.show()
            self.hide()
        elif self.check_role()[0] == "manager":
            self.manager_window = ManagerWindow()
            self.manager_window.show()
            self.hide()
        elif self.check_role()[0] == "finance":
            self.finance_window = FinanceWindow()
            self.finance_window.show()
            self.hide()

    def get_flight_id(self, flight_number):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            query = "SELECT id FROM flight WHERE flight_number = %s"
            values = (flight_number,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result[0]
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            connection.rollback()
            return False
        finally:
            connection.close()

    def del_res(self, r_id):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM reservation WHERE id = {int(r_id)}")
            connection.commit()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            connection.rollback()
        finally:
            connection.close()

    def delete_res(self):
        selected_item = self.res_table.selectedItems()
        row = self.res_table.currentRow()
        if row != -1:
            fid = self.res_table.item(row, 0).text()
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("Вы действительно хотите удалить бронивароние?")
            msgBox.setWindowTitle("Подтверждение выбора")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            ret = msgBox.exec_()
            if ret == QMessageBox.Ok:
                self.del_res(fid)
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Question)
                msgBox.setText("Бронирование успешно удалено")
                msgBox.setWindowTitle("Успех")
                msgBox.exec_()
            else:
                print("cancelled")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText("Пожалуйста, выберите бронирование")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return


class AdminRegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoslingSkyways - регистрация администратора")
        self.setFixedSize(500, 400)

        self.lastname = QLineEdit()
        self.firstname = QLineEdit()
        self.middlename = QLineEdit()
        self.email = QLineEdit()

        reg_button = QPushButton("Добавить администратора")
        reg_button.clicked.connect(self.register)
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Фамилия:"))
        layout.addWidget(self.lastname)
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.firstname)
        layout.addWidget(QLabel("Отчество (при наличии):"))
        layout.addWidget(self.middlename)
        layout.addWidget(QLabel("Адрес электронной почты:"))
        layout.addWidget(self.email)
        layout.addWidget(reg_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def go_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.hide()

    def go_back(self):
        self.start_window = StartWindow()
        self.start_window.show()
        self.hide()

    def compute_sha256_hash(self, input_str):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_str.encode("utf-8"))
        return sha256_hash.hexdigest()

    def generate_password(self):
        valid_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        buffer = [random.choice(valid_chars) for i in range(17)]
        return ''.join(buffer)

    def add_user(self, first_name, middle_name, last_name, email, pwd_hash, role):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO user (first_name, middle_name, last_name, email, password_hash, role) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (first_name, middle_name or None, last_name, email, pwd_hash, role)
            cursor.execute(sql, values)
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return False
        finally:
            connection.close()

    def register(self):
        input_firstname = self.firstname.text()
        input_middlename = self.middlename.text()
        input_lastname = self.lastname.text()
        input_email = self.email.text()
        generated_password = self.generate_password()

        self.add_user(input_firstname, input_middlename, input_lastname, input_email,
                      self.compute_sha256_hash(generated_password), "admin")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Администратор успешно создан\nПароль нового администратора: {generated_password}")
        msg.setWindowTitle("Успех")
        msg.exec_()

        print("[Успех] Регистрация прошла успешно")
        print(f"Пароль нового администратора: {generated_password}")
        self.go_login_window()


class DatabaseActionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(450, 300)
        self.setWindowTitle("GoslingSkyways - операции с базой данных")

        text_label = QLabel("Выберите действие:")
        text_label.setAlignment(Qt.AlignCenter)

        create_db_button = QPushButton("Создать базу данных")
        create_db_button.clicked.connect(self.create_db)
        create_tables_button = QPushButton("Добавить таблицы в базу данных")
        create_tables_button.clicked.connect(self.create_tables)
        add_data_button = QPushButton("Добавить тестовые данные")
        add_data_button.clicked.connect(self.insert_data)
        delete_data_button = QPushButton("Удалить данные из базы данных")
        delete_data_button.clicked.connect(self.delete_data)
        delete_db_button = QPushButton("Удалить базу данных")
        delete_db_button.clicked.connect(self.delete_db)
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(text_label)
        layout.addWidget(create_db_button)
        layout.addWidget(create_tables_button)
        layout.addWidget(add_data_button)
        layout.addWidget(delete_data_button)
        layout.addWidget(delete_db_button)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def create_db(self):
        connection = mysql.connector.connect(**connection_string_for_db_create)
        try:
            cursor = connection.cursor()
            cursor.execute(
                "DROP DATABASE IF EXISTS goslingskyways; CREATE DATABASE goslingskyways; USE goslingskyways;")
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("База данных goslingskyways создана")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def create_aircraft_table(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute(
                """CREATE TABLE aircraft (
                    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    model varchar(50) NOT NULL,
                    capacity int(11) NOT NULL);""")
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Создана таблица aircraft")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def create_city_table(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute(
                """CREATE TABLE city (
                id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name varchar(50) NOT NULL);""")
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Создана таблица city")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def create_user_table(self):
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
                    role enum('user','admin','manager','finance') NOT NULL);""")
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Создана таблица user")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def create_airport_table(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute(
                """CREATE TABLE airport (
                    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    city_id int(11) NOT NULL,
                    name varchar(8) NOT NULL,
                    KEY airport_FK (city_id),
                    FOREIGN KEY (city_id) REFERENCES city (id));""")
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Создана таблица airport")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def create_flight_table(self):
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
                    FOREIGN KEY (aircraft_id) REFERENCES aircraft (id));""")
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Создана таблица flight")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def create_reservation_table(self):
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
                    FOREIGN KEY (flight_id) REFERENCES flight (id));""")
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Создана таблица reservation")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def create_tables(self):
        self.create_aircraft_table()
        self.create_city_table()
        self.create_user_table()
        self.create_airport_table()
        self.create_flight_table()
        self.create_reservation_table()
        msg = QMessageBox()

        msg.setText("Успех")
        msg.setInformativeText("Все таблицы были добавлены в базу данных")
        msg.setWindowTitle("Успех")
        msg.exec_()

    def insert_aircraft_data(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO aircraft (id, model, capacity) VALUES (1, 'Boeing 737-800', 189), (2, 'Airbus A320', 180);")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Добавлены модели самолетов")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def insert_airport_data(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO airport (id, city_id, name) VALUES(1, 1, 'DME'), (2, 2, 'AER'), (3, 3, 'LED');")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Добавлены аэропорты")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def insert_city_data(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO city (id, name) VALUES (1, 'Москва'), (2, 'Сочи'), (3, 'Санкт-Петербург');")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Добавлены города")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def insert_flight_data(self):
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
    (7, 'G-4375', 2, 3, 1, '2023-05-19 20:20:00.000', '2023-05-20 00:40:00.000', 189, 38504, 57756);""")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Добавлены рейсы")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def insert_user_data(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO user (id, first_name, middle_name, last_name, email, password_hash, `role`)
    VALUES(1, 'admin', NULL, 'admin', 'admin@gosling.com', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin'),
    (2, 'user', NULL, 'user', 'user@gosling.com', '04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb', 'user'),
    (3, 'manager', NULL, 'manager', 'manager@gosling.com', '6ee4a469cd4e91053847f5d3fcb61dbcc91e8f0ef10be7748da4c4a1ba382d17', 'manager'),
    (4, 'finance', NULL, 'finance', 'finance@gosling.com', 'eab762a03fd979a04cc4706e6536d382bc89d2d1356afcd054a16b2235ecd471', 'finance');""")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Добавлены базовые пользователи")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def insert_data(self):
        self.insert_aircraft_data()
        self.insert_city_data()
        self.insert_airport_data()
        self.insert_flight_data()
        self.insert_user_data()
        msg = QMessageBox()

        msg.setText("Успех")
        msg.setInformativeText("Все тестовые данные добавлены")
        msg.setWindowTitle("Успех")
        msg.exec_()

    def delete_aircraft_data(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM aircraft")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Удалены данные о самолетах")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def delete_city_data(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM city")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Удалены данные о городах")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def delete_airport_data(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM airport")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Удалены данные об аэропортах")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def delete_flight_data(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM flight")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Удалены данные о рейсах")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def delete_user_data(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM user")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Удалены данные о пользователях")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def delete_reservation_data(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM reservation")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("Удалены данные о бронированиях")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def delete_data(self):
        self.delete_reservation_data()
        self.delete_user_data()
        self.delete_flight_data()
        self.delete_airport_data()
        self.delete_city_data()
        self.delete_aircraft_data()
        msg = QMessageBox()

        msg.setText("Успех")
        msg.setInformativeText("Все тестовые данные удалены")
        msg.setWindowTitle("Успех")
        msg.exec_()

    def delete_db(self):
        connection = mysql.connector.connect(**connection_string)
        try:
            cursor = connection.cursor()
            cursor.execute("DROP DATABASE goslingskyways")
            connection.commit()
            msg = QMessageBox()

            msg.setText("Успех")
            msg.setInformativeText("База данных удалена полностью")
            msg.setWindowTitle("Успех")
            msg.exec_()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(f"[Ошибка базы данных] {error}")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        finally:
            connection.close()

    def go_back(self):
        self.start_window = StartWindow()
        self.start_window.show()
        self.hide()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello")
        label = QLabel(self)
        label.setText("Hello")


def db_connection_check():
    try:
        connection = mysql.connector.connect(**connection_string)
        connection.close()
        return True
    except mysql.connector.Error as error:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Ошибка")
        msg.setInformativeText(f"[Ошибка базы данных] {error}")
        msg.setWindowTitle("Ошибка")
        msg.exec_()
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("gui-app/logo_mini.svg"))
    main = StartWindow()
    main.show()
    db_connection_check()
    app.exec_()
