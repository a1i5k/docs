
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