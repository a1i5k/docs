from unittest import TestCase, main
from main import AccountGateway
from unittest.mock import MagicMock
from unittest.mock import Mock

LOGIN = "login"
PASSWORD = "password"
PHONE = "89175554498"
MAIL = "mail@mail.ru"
NAME_DIET = "diet"
DESCRIPTION_DIET = "description"
NAME_DISH = "dish"


class AccountGatewayTest(TestCase):
    def test_addAccount(self):
        cursor = MagicMock(return_value=True)
        acc = AccountGateway(cursor)
        self.assertEqual(first=acc.addAccount(LOGIN, PASSWORD, PHONE, MAIL), second=True)

    def test_addAccountFailed(self):
        cursor = MagicMock(return_value=True)
        cursor.execute = Mock(side_effect=KeyError('err'))
        acc = AccountGateway(cursor)
        self.assertEqual(first=acc.addAccount(LOGIN, PASSWORD, PHONE, MAIL), second=False)

    def test_updateAccount(self):
        cursor = MagicMock(return_value=True)
        acc = AccountGateway(cursor)
        self.assertEqual(first=acc.updateAccount(18, 180, 80, 0, LOGIN), second=True)

    def test_updateAccountFailed(self):
        cursor = MagicMock(return_value=True)
        cursor.execute = Mock(side_effect=KeyError('err'))
        acc = AccountGateway(cursor)
        self.assertEqual(first=acc.updateAccount(18, 180, 80, 0, LOGIN), second=False)

    def test_updatePasswordAccount(self):
        cursor = MagicMock(return_value=True)
        acc = AccountGateway(cursor)
        self.assertEqual(first=acc.updatePasswordAccount(LOGIN, PASSWORD), second=True)

    def test_updatePasswordAccountFailed(self):
        cursor = MagicMock(return_value=True)
        cursor.execute = Mock(side_effect=KeyError('err'))
        acc = AccountGateway(cursor)
        self.assertEqual(first=acc.updatePasswordAccount(LOGIN, PASSWORD), second=False)

    def test_getAccount(self):
        res = [{"login": LOGIN, "password": PASSWORD, "phone": PHONE, "mail": MAIL,
                        "type_account": 0, "age": 18, "height": 180, "weight": 80,
                        "special": 0}]
        cursor = MagicMock()
        cursor.fetchall = Mock(return_value=[[LOGIN, PASSWORD, PHONE, MAIL, 0, 18, 180, 80, 0]])
        acc = AccountGateway(cursor)
        self.assertEqual(first=acc.getAccount(LOGIN), second=res)


if __name__ == '__main__':
    main()
