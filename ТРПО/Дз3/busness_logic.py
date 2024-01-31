
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