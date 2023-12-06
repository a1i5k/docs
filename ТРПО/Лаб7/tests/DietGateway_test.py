from unittest import TestCase, main
from main import DietGateway
from unittest.mock import MagicMock
from unittest.mock import Mock

# cursor = MagicMock(return_value=True)

# mock = Mock(side_effect=KeyError('foo'))

LOGIN = "login"
PASSWORD = "password"
PHONE = "89175554498"
MAIL = "mail@mail.ru"
NAME_DIET = "diet"
DESCRIPTION_DIET = "description"
NAME_DISH = "dish"


class DietGatewayTest(TestCase):
    def test_addDiet(self):
        cursor = MagicMock(return_value=True)
        diet = DietGateway(cursor)
        self.assertEqual(first=diet.addDiet(NAME_DIET, DESCRIPTION_DIET, 18, 180, 80, 0), second=True)

    def test_addDietFailed(self):
        cursor = MagicMock(return_value=True)
        cursor.execute = Mock(side_effect=KeyError('err'))
        diet = DietGateway(cursor)
        self.assertEqual(first=diet.addDiet(NAME_DIET, DESCRIPTION_DIET, 18, 180, 80, 0), second=False)

    def test_updateDiet(self):
        cursor = MagicMock(return_value=True)
        diet = DietGateway(cursor)
        self.assertEqual(first=diet.updateDiet(NAME_DIET, DESCRIPTION_DIET, 18, 180, 80, 0, 1), second=True)

    def test_updateDietFailed(self):
        cursor = MagicMock(return_value=True)
        cursor.execute = Mock(side_effect=KeyError('err'))
        diet = DietGateway(cursor)
        self.assertEqual(first=diet.updateDiet(NAME_DIET, DESCRIPTION_DIET, 18, 180, 80, 0, 1), second=False)

    def test_deleteDiet(self):
        cursor = MagicMock(return_value=True)
        diet = DietGateway(cursor)
        self.assertEqual(first=diet.deleteDiet(NAME_DIET, DESCRIPTION_DIET, 18, 180, 80, 0), second=True)

    def test_deleteDietFailed(self):
        cursor = MagicMock(return_value=True)
        cursor.execute = Mock(side_effect=KeyError('err'))
        diet = DietGateway(cursor)
        self.assertEqual(first=diet.deleteDiet(NAME_DIET, DESCRIPTION_DIET, 18, 180, 80, 0), second=False)

    def test_getDiet(self):
        res = [{"name": NAME_DIET, "description": DESCRIPTION_DIET, "age": 18, "height": 180, "weight": 80,
                "special": 0}]
        cursor = MagicMock()
        cursor.fetchall = Mock(return_value=[[NAME_DIET, DESCRIPTION_DIET, 18, 180, 80, 0]])
        diet = DietGateway(cursor)
        self.assertEqual(first=diet.getDiet(NAME_DIET), second=res)

    def test_getDiets(self):
        res = [{"id": 1, "name": NAME_DIET, "description": DESCRIPTION_DIET, "age": 18, "height": 180, "weight": 80,
                "special": 0}]
        cursor = MagicMock()
        cursor.fetchall = Mock(return_value=[[1, NAME_DIET, DESCRIPTION_DIET, 18, 180, 80, 0]])
        diet = DietGateway(cursor)
        self.assertEqual(first=diet.getDiets(), second=res)


if __name__ == '__main__':
    main()
