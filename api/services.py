from typing import List

from .models import Account, Customer, Transfer
from .repositories import AccountRepository, CustomerRepository, TransferRepository


class BankService:
    def __init__(self):
        self.customer_repo = CustomerRepository()
        self.account_repo = AccountRepository()
        self.transfer_repo = TransferRepository()

    def create_customer(self, name: str) -> Customer:
        return self.customer_repo.create(name)

    def create_account(self, customer_id: int, initial_deposit: float) -> Account:
        return self.account_repo.create(customer_id, initial_deposit)

    def transfer_amount(self, from_account_id: int, to_account_id: int, amount: float) -> Transfer:
        from_account = self.account_repo.get(from_account_id)
        to_account = self.account_repo.get(to_account_id)

        if from_account.balance < amount:
            raise ValueError("Insufficient funds.")

        from_account.balance -= amount
        to_account.balance += amount

        self.account_repo.update_balance(from_account_id, from_account.balance)
        self.account_repo.update_balance(to_account_id, to_account.balance)

        return self.transfer_repo.create(from_account_id, to_account_id, amount)

    def get_balance(self, account_id: int) -> float:
        account = self.account_repo.get(account_id)
        return account.balance

    def get_transfer_history(self, account_id: int) -> List[Transfer]:
        return self.transfer_repo.get_transfers_for_account(account_id)
