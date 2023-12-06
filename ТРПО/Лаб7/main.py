# import sqlite3


# def connect_db():
#     return sqlite3.connect('server.db')


# connection = connect_db()
# cursor = connection.cursor()

# cursor.execute("""CREATE TABLE IF NOT EXISTS Account(
#     `id` INTEGER PRIMARY KEY AUTOINCREMENT,
#     `login` varchar(255),
#     `password` varchar(255),
#     `phone` varchar(255),
#     `mail` varchar(255),
#     `type_account` INTEGER DEFAULT 0,
#     `age` INTEGER,
#     `height` float,
#     `weight` float,
#     `special` INTEGER
#   )""")
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS Diet(
#     `id` INTEGER PRIMARY KEY AUTOINCREMENT,
#     `name` varchar(255),
#     `description` varchar(255),
#     `age` int,
#     `height` float,
#     `weight` float,
#     `special` INTEGER
#   )""")
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS Dishes(
#     `id` INTEGER PRIMARY KEY AUTOINCREMENT,
#     `name` varchar(255),
#     `diet` INTEGER
#   )""")
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS HistoryDiet(
#     `id` INTEGER PRIMARY KEY AUTOINCREMENT,
#     `account` INTEGER,
#     `diet` INTEGER
#   )""")


class AccountGateway:
    def __init__(self, cursor):
        self.cursor = cursor

    def addAccount(self, login, password, phone, mail):
        try:
            self.cursor.execute("INSERT INTO Account (login, password, phone, mail) VALUES (?, ?, ?, ?)",
                           (login, password, phone, mail))
        except:
            return False
        return True

    def updateAccount(self, age, height, weight, special, login):
        try:
            self.cursor.execute("UPDATE Account SET age = ?, height = ?, weight = ?, special = ? WHERE login = ?",
                           (age, height, weight, special, login))
        except:
            return False
        return True

    def updatePasswordAccount(self, password, login):
        try:
            self.cursor.execute("UPDATE Account SET password = ? WHERE login = ?", (password, login))
        except:
            return False
        return True

    def getAccount(self, login):
        self.cursor.execute(
            "SELECT login, password, phone, mail, type_account, age, height, weight, special FROM Account WHERE login = ?",
            (login,))
        query = self.cursor.fetchall()

        res = []
        for str_db in query:
            res.append({"login": str_db[0], "password": str_db[1], "phone": str_db[2], "mail": str_db[3],
                        "type_account": str_db[4], "age": str_db[5], "height": str_db[6], "weight": str_db[7],
                        "special": str_db[8]})
        return res


class DietGateway:
    def __init__(self, cursor):
        self.cursor = cursor

    def addDiet(self, name, description, age, height, weight, special):
        try:
            self.cursor.execute(
                "INSERT INTO Diet (name, description, age, height, weight, special) VALUES (?, ?, ?, ?, ?, ?)",
                (name, description, age, height, weight, special))
        except:
            return False
        return True

    def updateDiet(self, name, description, age, height, weight, special, id_diet):
        try:
            self.cursor.execute(
                "UPDATE Diet SET name = ?, description = ?, age = ?, height = ?, weight = ?, special = ? WHERE id = ?",
                (name, description, age, height, weight, special, id_diet))
        except:
            return False
        return True

    def getDiet(self, name):
        self.cursor.execute("SELECT name, description, age, height, weight, special FROM Diet WHERE name = ?", (name,))
        query = self.cursor.fetchall()

        res = []
        for str_db in query:
            res.append({"name": str_db[0], "description": str_db[1], "age": str_db[2], "height": str_db[3],
                        "weight": str_db[4], "special": str_db[5]})
        return res

    def getDiets(self):
        self.cursor.execute("SELECT id, name, description, age, height, weight, special FROM Diet")
        query = self.cursor.fetchall()

        res = []
        for str_db in query:
            res.append({"id": str_db[0], "name": str_db[1], "description": str_db[2], "age": str_db[3],
                        "height": str_db[4], "weight": str_db[5], "special": str_db[6]})
        return res

    def deleteDiet(self, name, description, age, height, weight, special):
        try:
            self.cursor.execute(
                "DELETE FROM Diet WHERE name = ?, description = ?, age = ?, height = ?, weight = ?, special = ?",
                (name, description, age, height, weight, special))
        except:
            return False
        return True


class DishesGateway:
    def __init__(self, cursor):
        self.cursor = cursor

    def addDish(self, name, diet):
        try:
            self.cursor.execute("INSERT INTO Dishes (name, diet) VALUES (?, ?)", (name, diet))
        except:
            return False
        return True

    def updateDish(self, name, id_dish):
        try:
            self.cursor.execute("UPDATE Dishes SET name = ? WHERE id = ?", (name, id_dish))
        except:
            return False
        return True

    def getDish(self, id_dish):
        self.cursor.execute("SELECT name FROM Dishes WHERE id = ?", (id_dish,))
        query = self.cursor.fetchall()

        res = []
        for str_db in query:
            res.append({"name": str_db[0]})
        return res

    def getDishes(self, diet):
        self.cursor.execute("SELECT name FROM Dishes WHERE diet = ?", (diet,))
        query = self.cursor.fetchall()

        res = []
        for str_db in query:
            res.append({"name": str_db[0]})
        return res

    def deleteDish(self, name):
        try:
            self.cursor.execute("DELETE FROM Dish WHERE name = ?", (name,))
        except:
            return False
        return True


class HistoryDietGateway:
    def __init__(self, cursor):
        self.cursor = cursor

    def addDiet(self, account, diet):
        try:
            self.cursor.execute("INSERT INTO HistoryDiet (account, diet) VALUES (?, ?)", (account, diet))
        except:
            return False
        return True

    def getHistoryDiet(self, login):
        self.cursor.execute(
            "SELECT Diet.name FROM HistoryDiet JOIN Diet on HistoryDiet.diet = Diet.id JOIN Account on Account.id = HistoryDiet.account WHERE Account.login = ?",
            (login,))
        query = self.cursor.fetchall()

        res = []
        for str_db in query:
            res.append({"name": str_db[0]})
        return res


class InterfaceRun:
    def run(self):
        pass


class Registration(InterfaceRun):
    def __init__(self, login, password, mail, phone, cursor):
        super().__init__()
        self.login = login
        self.password = password
        self.mail = mail
        self.phone = phone
        self.cursor = cursor

    def run(self):
        return AccountGateway(self.cursor).addAccount(self.login, self.password, self.phone, self.mail)


class Authorization(InterfaceRun):
    def __init__(self, login, password, cursor):
        super().__init__()
        self.login = login
        self.password = password
        self.cursor = cursor

    def run(self):
        acc = AccountGateway(self.cursor).getAccount(self.login)
        if acc[0]["password"] == self.password:
            return True
        else:
            return False


class AddDiet(InterfaceRun):
    def __init__(self, name, description, age, height, weight, special, cursor):
        super().__init__()
        self.name = name
        self.description = description
        self.age = age
        self.height = height
        self.weight = weight
        self.special = special
        self.cursor = cursor

    def run(self):
        return DietGateway(self.cursor).addDiet(self.name, self.description, self.age, self.height, self.weight, self.special)


class FillAboutMe(InterfaceRun):
    def __init__(self, age, height, weight, special, login, cursor):
        super().__init__()
        self.age = age
        self.height = height
        self.weight = weight
        self.special = special
        self.login = login
        self.cursor = cursor

    def run(self):
        return AccountGateway(self.cursor).updateAccount(self.age, self.height, self.weight, self.special, self.login)


class FindDiet(InterfaceRun):
    def __init__(self, login, cursor):
        super().__init__()
        self.login = login
        self.cursor = cursor

    def run(self):
        account = AccountGateway(self.cursor).getAccount(self.login)
        diets = DietGateway(self.cursor).getDiets()

        # Подбор диеты
        diet_id = diets[0]["id"]
        diet_name = diets[0]["name"]

        # Вернуть блюда + название диеты
        return diet_name, DishesGateway(self.cursor).getDishes(diet_id)


class GetHistoryDiet(InterfaceRun):
    def __init__(self, login, cursor):
        super().__init__()
        self.login = login
        self.cursor = cursor

    def run(self):
        return HistoryDietGateway(self.cursor).getHistoryDiet(self.login)


class RestorePassword(InterfaceRun):
    def __init__(self, login, phone, password, cursor):
        super().__init__()
        self.login = login
        self.phone = phone
        self.password = password
        self.cursor = cursor

    def run(self):
        acc = AccountGateway(self.cursor)
        res = acc.getAccount(self.login)
        return acc.updatePasswordAccount(self.login, res[0]['password'])


class GetDiets(InterfaceRun):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor

    def run(self):
        return DietGateway(self.cursor).getDiets()


class AddDish(InterfaceRun):
    def __init__(self, name, diet, cursor):
        super().__init__()
        self.name = name
        self.diet = diet
        self.cursor = cursor

    def run(self):
        return DishesGateway(self.cursor).addDish(self.name, self.diet)
