from unittest import TestCase, main
from main import HistoryDietGateway
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


class HistoryDietGatewayTest(TestCase):
    def test_addDiet(self):
        cursor = MagicMock(return_value=True)
        history = HistoryDietGateway(cursor)
        self.assertEqual(first=history.addDiet(1, 1), second=True)

    def test_addDietFailed(self):
        cursor = MagicMock(return_value=True)
        cursor.execute = Mock(side_effect=KeyError('err'))
        history = HistoryDietGateway(cursor)
        self.assertEqual(first=history.addDiet(1, 1), second=False)

    def test_getDiet(self):
        res = [{"name": NAME_DIET}]
        cursor = MagicMock()
        cursor.fetchall = Mock(return_value=[[NAME_DIET]])
        history = HistoryDietGateway(cursor)
        self.assertEqual(first=history.getHistoryDiet(LOGIN), second=res)


if __name__ == '__main__':
    main()
