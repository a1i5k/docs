from unittest import TestCase, main
from unittest.mock import MagicMock
from unittest.mock import Mock

from main import Registration, Authorization, AddDiet, FillAboutMe, RestorePassword, GetHistoryDiet, GetDiets, AddDish, \
    FindDiet

# cursor = MagicMock(return_value=True)

# mock = Mock(side_effect=KeyError('foo'))

LOGIN = "login"
PASSWORD = "password"
PHONE = "89175554498"
MAIL = "mail@mail.ru"
NAME_DIET = "diet"
DESCRIPTION_DIET = "description"
NAME_DISH = "dish"


class RunTest(TestCase):
    def test_registration_run(self):
        cursor = MagicMock(return_value=True)
        reg = Registration(LOGIN, PASSWORD, PHONE, MAIL, cursor)
        self.assertEqual(first=reg.run(), second=True)

    def test_registration_run_failed(self):
        cursor = MagicMock(return_value=True)
        cursor.execute = Mock(side_effect=KeyError('err'))
        reg = Registration(LOGIN, PASSWORD, PHONE, MAIL, cursor)
        self.assertEqual(first=reg.run(), second=False)

    def test_authorization_run(self):
        cursor = MagicMock(return_value=True)
        cursor.fetchall = Mock(return_value=[[LOGIN, PASSWORD, PHONE, MAIL, 0, 18, 180, 80, 0]])
        auth = Authorization(LOGIN, PASSWORD, cursor)
        self.assertEqual(first=auth.run(), second=True)

    def test_authorization_run_failed(self):
        cursor = MagicMock(return_value=True)
        cursor.fetchall = Mock(return_value=[[LOGIN, PASSWORD, PHONE, MAIL, 0, 18, 180, 80, 0]])
        auth = Authorization(LOGIN, "wrong_password", cursor)
        self.assertEqual(first=auth.run(), second=False)

    def test_addDiet_run(self):
        cursor = MagicMock(return_value=True)
        diet = AddDiet(NAME_DIET, DESCRIPTION_DIET, 18, 180, 80, 0, cursor)
        self.assertEqual(first=diet.run(), second=True)

    def test_fillAboutMe_run(self):
        cursor = MagicMock(return_value=True)
        aboutme = FillAboutMe(18, 180, 80, 0, LOGIN, cursor)
        self.assertEqual(first=aboutme.run(), second=True)

    def test_findDiet_run(self):
        cursor = MagicMock(return_value=True)
        cursor.fetchall = Mock(side_effect=[
            [[LOGIN, PASSWORD, PHONE, MAIL, 0, 18, 180, 80, 0]],
            [[1, NAME_DIET, DESCRIPTION_DIET, 18, 180, 80, 0]],
            [[NAME_DISH]]
        ])
        diet = FindDiet(LOGIN, cursor)
        result1, result2 = diet.run()
        self.assertEqual(first=result1, second=NAME_DIET)
        self.assertEqual(first=result2, second=[{'name': NAME_DISH}])

    def test_getHistoryDiet_run(self):
        res = [{"name": NAME_DIET}]
        cursor = MagicMock()
        cursor.fetchall = Mock(return_value=[[NAME_DIET]])
        history = GetHistoryDiet(LOGIN, cursor)
        self.assertEqual(first=history.run(), second=res)

    def test_restorePassword_run(self):
        cursor = MagicMock(return_value=True)
        cursor.fetchall = Mock(side_effect=[[[LOGIN, PASSWORD, PHONE, MAIL, 0, 18, 180, 80, 0]], True])
        restore = RestorePassword(LOGIN, PHONE, PASSWORD, cursor)
        self.assertEqual(first=restore.run(), second=True)

    def test_getDiets_run(self):
        res = [{"id": 1, "name": NAME_DIET, "description": DESCRIPTION_DIET, "age": 18, "height": 180, "weight": 80,
                "special": 0}]
        cursor = MagicMock(return_value=True)
        cursor.fetchall = Mock(return_value=[[1, NAME_DIET, DESCRIPTION_DIET, 18, 180, 80, 0]])
        dish = GetDiets(cursor)
        self.assertEqual(first=dish.run(), second=res)

    def test_addDish_run(self):
        cursor = MagicMock(return_value=True)
        dish = AddDish(NAME_DISH, 1, cursor)
        self.assertEqual(first=dish.run(), second=True)


if __name__ == '__main__':
    main()
