# import sqlite3
#
#
# def connect_db():
#     return sqlite3.connect('server.db')
#
#
# connection = connect_db()
# cursor = connection.cursor()
#
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
#     `name` varchar(255) UNIQUE,
#     `description` varchar(255),
#     `age` int,
#     `height` float,
#     `weight` float,
#     `special` varchar(255)
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

    def addAccount(self, login, password, phone, mail, type_account):
        try:
            self.cursor.execute("INSERT INTO Account (login, password, phone, mail, type_account) VALUES (?, ?, ?, ?, ?)",
                           (login, password, phone, mail, type_account))
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
            "SELECT login, password, phone, mail, type_account, age, height, weight, special, id FROM Account WHERE login = ?",
            (login,))
        query = self.cursor.fetchall()

        res = []
        for str_db in query:
            res.append({"login": str_db[0], "password": str_db[1], "phone": str_db[2], "mail": str_db[3],
                        "type_account": str_db[4], "age": str_db[5], "height": str_db[6], "weight": str_db[7],
                        "special": str_db[8], "id": str_db[9]})
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

    def updateDiet(self, old_name, name, description, age, height, weight, special):
        try:
            self.cursor.execute(
                "UPDATE Diet SET name = ?, description = ?, age = ?, height = ?, weight = ?, special = ? WHERE name = ?",
                (name, description, age, height, weight, special, old_name))
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

    def getIdDiet(self, name):
        self.cursor.execute("SELECT id FROM Diet WHERE name = ?", (name,))
        query = self.cursor.fetchall()

        res = []
        for str_db in query:
            res.append({"id": str_db[0]})
        return res

    def getDiets(self):
        self.cursor.execute("SELECT id, name, description, age, height, weight, special FROM Diet")
        query = self.cursor.fetchall()

        res = []
        for str_db in query:
            res.append({"id": str_db[0], "name": str_db[1], "description": str_db[2], "age": str_db[3],
                        "height": str_db[4], "weight": str_db[5], "special": str_db[6]})
        return res

    def selectDiet(self, age, height, weight, special):
        self.cursor.execute("SELECT id, name, description, age, height, weight, special FROM Diet WHERE "
                            "age > ? - 5 AND age < ? + 5 AND height < ? + 5 AND height > ? - 5"
                            " AND weight < ? + 5 AND weight > ? - 5 AND special = ?", (age, age, height, height, weight, weight, special,))
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

    def updateDish(self, old_name, name):
        try:
            self.cursor.execute("UPDATE Dishes SET name = ? WHERE name = ?", (name, old_name))
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
    def __init__(self, login, password, mail, phone, type_account, cursor):
        super().__init__()
        self.login = login
        self.password = password
        self.mail = mail
        self.phone = phone
        self.type_account = type_account
        self.cursor = cursor

    def run(self):
        return AccountGateway(self.cursor).addAccount(self.login, self.password, self.phone, self.mail, self.type_account)


class Authorization(InterfaceRun):
    def __init__(self, login, password, cursor):
        super().__init__()
        self.login = login
        self.password = password
        self.cursor = cursor

    def run(self):
        acc = AccountGateway(self.cursor).getAccount(self.login)
        if acc == []:
            return False
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
        if account == []:
            return False, False
        diet = DietGateway(self.cursor).selectDiet(account[0]['age'], account[0]['height'],
                                                   account[0]['weight'], account[0]['special'])
        if diet == []:
            return False, False

        diet_id = diet[0]["id"]
        diet_name = diet[0]["name"]

        HistoryDietGateway(self.cursor).addDiet(account=account[0]['id'], diet=diet[0]["id"])

        return diet_name, DishesGateway(self.cursor).getDishes(diet_id)


class GetHistoryDiet(InterfaceRun):
    def __init__(self, login, cursor):
        super().__init__()
        self.login = login
        self.cursor = cursor

    def run(self):
        diets = HistoryDietGateway(self.cursor).getHistoryDiet(self.login)
        dishes = {}
        for diet in diets:
            diet_name = diet['name']
            dish_in_query = []
            for name in DishesGateway(self.cursor).getDishes(DietGateway(self.cursor).getIdDiet(name=diet_name)[0]['id']):
                dish_in_query.append(name)
            dishes[diet_name] = dish_in_query
        return diets, dishes


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
        if res == []:
            return False
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
        return DishesGateway(self.cursor).addDish(self.name, DietGateway(self.cursor).getIdDiet(name=self.diet)[0]['id'])


class UpdateDiet(InterfaceRun):
    def __init__(self, old_name, name, description, age, height, weight, special, cursor):
        super().__init__()
        self.old_name = old_name
        self.name = name
        self.description = description
        self.age = age
        self.height = height
        self.weight = weight
        self.special = special
        self.cursor = cursor

    def run(self):
        return DietGateway(self.cursor).updateDiet(self.old_name, self.name, self.description, self.age, self.height, self.weight, self.special)


class UpdateDish(InterfaceRun):
    def __init__(self, old_name, name, cursor):
        super().__init__()
        self.old_name = old_name
        self.name = name
        self.cursor = cursor

    def run(self):
        return DishesGateway(self.cursor).updateDish(self.old_name, self.name)


class GetTypeAccount(InterfaceRun):
    def __init__(self, login, cursor):
        super().__init__()
        self.login = login
        self.cursor = cursor

    def run(self):
        return AccountGateway(self.cursor).getAccount(self.login)[0]['type_account']

