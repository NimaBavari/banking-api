import dataclasses
import unittest
from unittest.mock import MagicMock, patch

from .exceptions import AccountNotCreated, AccountNotFound, CustomerNotCreated
from .main import app, service


@dataclasses.dataclass
class MockCustomerCreateResponse:
    id: int
    name: str


class BankApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch("api.main.logger.error")
    @patch("api.main.logger.info")
    @patch.object(service, "create_customer")
    def test_create_customer_success(self, mock_create_customer, mock_logger_info, mock_logger_error):
        mock_create_customer.return_value = MockCustomerCreateResponse(id=1, name="John Doe")

        response = self.app.post("/customers", json={"name": "John Doe"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"id": 1, "name": "John Doe"})
        mock_logger_info.assert_called_with("Customer created successfully.")

    @patch("api.main.logger.error")
    @patch("api.main.logger.info")
    @patch.object(service, "create_customer", side_effect=CustomerNotCreated("John Doe"))
    def test_create_customer_failure(self, mock_create_customer, mock_logger_info, mock_logger_error):
        response = self.app.post("/customers", json={"name": "John Doe"})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json, {"error": "Customer not created."})
        mock_logger_error.assert_called_with("Customer not created.")

    @patch("api.main.logger.error")
    @patch("api.main.logger.info")
    @patch.object(service, "create_account")
    def test_create_account_success(self, mock_create_account, mock_logger_info, mock_logger_error):
        mock_create_account.return_value = MagicMock(id=1, customer_id=1, balance=100.0)

        response = self.app.post("/accounts", json={"customer_id": 1, "initial_deposit": 100.0})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"id": 1, "customer_id": 1, "balance": 100.0})
        mock_logger_info.assert_called_with("Account created successfully.")

    @patch("api.main.logger.error")
    @patch("api.main.logger.info")
    @patch.object(service, "create_account", side_effect=AccountNotCreated("John Doe"))
    def test_create_account_failure(self, mock_create_account, mock_logger_info, mock_logger_error):
        response = self.app.post("/accounts", json={"customer_id": 1, "initial_deposit": 100.0})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json, {"error": "Account not created."})
        mock_logger_error.assert_called_with("Account not created.")

    @patch("api.main.logger.error")
    @patch("api.main.logger.info")
    @patch.object(service, "get_balance")
    def test_get_balance_success(self, mock_get_balance, mock_logger_info, mock_logger_error):
        mock_get_balance.return_value = 100.0

        response = self.app.get("/accounts/1/balance")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"balance": 100.0})
        mock_logger_info.assert_called_with("Balance fetched successfully.")

    @patch("api.main.logger.error")
    @patch("api.main.logger.info")
    @patch.object(service, "get_balance", side_effect=AccountNotFound(1))
    def test_get_balance_failure(self, mock_get_balance, mock_logger_info, mock_logger_error):
        response = self.app.get("/accounts/1/balance")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Account not found."})
        mock_logger_error.assert_called_with("Account not found.")

    @patch("api.main.logger.error")
    @patch("api.main.logger.info")
    @patch.object(service, "transfer_amount")
    def test_transfer_amount_success(self, mock_transfer_amount, mock_logger_info, mock_logger_error):
        mock_transfer_amount.return_value = MagicMock(
            id=1, from_account_id=1, to_account_id=2, amount=50.0, created_at="2024-07-19T12:00:00"
        )

        response = self.app.post("/transfers", json={"from_account_id": 1, "to_account_id": 2, "amount": 50.0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {"id": 1, "from_account_id": 1, "to_account_id": 2, "amount": 50.0, "timestamp": "2024-07-19T12:00:00"},
        )
        mock_logger_info.assert_called_with("Amount transferred successfully.")

    @patch("api.main.logger.error")
    @patch("api.main.logger.info")
    @patch.object(service, "transfer_amount", side_effect=AccountNotFound(1))
    def test_transfer_amount_failure_account_not_found(self, mock_transfer_amount, mock_logger_info, mock_logger_error):
        response = self.app.post("/transfers", json={"from_account_id": 1, "to_account_id": 2, "amount": 50.0})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Account not found."})
        mock_logger_error.assert_called_with("Account not found.")

    @patch("api.main.logger.error")
    @patch("api.main.logger.info")
    @patch.object(service, "transfer_amount", side_effect=ValueError("Insufficient funds."))
    def test_transfer_amount_failure_insufficient_funds(
        self, mock_transfer_amount, mock_logger_info, mock_logger_error
    ):
        response = self.app.post("/transfers", json={"from_account_id": 1, "to_account_id": 2, "amount": 50.0})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {"error": "Insufficient funds."})
        mock_logger_error.assert_called_with("Insufficient funds.")

    @patch("api.main.logger.error")
    @patch("api.main.logger.info")
    @patch.object(service, "get_transfer_history")
    def test_get_transfer_history_success(self, mock_get_transfer_history, mock_logger_info, mock_logger_error):
        mock_get_transfer_history.return_value = [
            MagicMock(id=1, from_account_id=1, to_account_id=2, amount=50.0, created_at="2024-07-19T12:00:00"),
            MagicMock(id=2, from_account_id=2, to_account_id=1, amount=30.0, created_at="2024-07-20T12:00:00"),
        ]

        response = self.app.get("/accounts/1/transfers")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [
                {"id": 1, "from_account_id": 1, "to_account_id": 2, "amount": 50.0, "timestamp": "2024-07-19T12:00:00"},
                {"id": 2, "from_account_id": 2, "to_account_id": 1, "amount": 30.0, "timestamp": "2024-07-20T12:00:00"},
            ],
        )
        mock_logger_info.assert_called_with("Transfer history fetched successfully.")


if __name__ == "__main__":
    unittest.main()
