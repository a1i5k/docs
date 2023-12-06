from unittest import TestCase, main
from main import DishesGateway
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


class DishGatewayTest(TestCase):
    def test_addDish(self):
        cursor = MagicMock(return_value=True)
        dish = DishesGateway(cursor)
        self.assertEqual(first=dish.addDish(NAME_DISH, 1), second=True)

    def test_addDishFailed(self):
        cursor = MagicMock(return_value=True)
        cursor.execute = Mock(side_effect=KeyError('err'))
        dish = DishesGateway(cursor)
        self.assertEqual(first=dish.addDish(NAME_DISH, 1), second=False)

    def test_updateDish(self):
        cursor = MagicMock(return_value=True)
        dish = DishesGateway(cursor)
        self.assertEqual(first=dish.updateDish(NAME_DISH, 1), second=True)

    def test_updateDishFailed(self):
        cursor = MagicMock(return_value=True)
        cursor.execute = Mock(side_effect=KeyError('err'))
        dish = DishesGateway(cursor)
        self.assertEqual(first=dish.updateDish(NAME_DISH, 1), second=False)

    def test_deleteDish(self):
        cursor = MagicMock(return_value=True)
        dish = DishesGateway(cursor)
        self.assertEqual(first=dish.deleteDish(NAME_DISH), second=True)

    def test_deleteDishFailed(self):
        cursor = MagicMock(return_value=True)
        cursor.execute = Mock(side_effect=KeyError('err'))
        dish = DishesGateway(cursor)
        self.assertEqual(first=dish.deleteDish(NAME_DISH), second=False)

    def test_getDish(self):
        res = [{"name": NAME_DIET}]
        cursor = MagicMock()
        cursor.fetchall = Mock(return_value=[[NAME_DIET]])
        dish = DishesGateway(cursor)
        self.assertEqual(first=dish.getDish(1), second=res)

    def test_getDishes(self):
        res = [{"name": NAME_DIET}]
        cursor = MagicMock()
        cursor.fetchall = Mock(return_value=[[NAME_DIET]])
        dish = DishesGateway(cursor)
        self.assertEqual(first=dish.getDishes(1), second=res)


if __name__ == '__main__':
    main()
