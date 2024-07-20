from typing import List

from sqlalchemy.exc import SQLAlchemyError

from .db import sess
from .exceptions import (
    AccountNotCreated,
    AccountNotFound,
    AccountNotUpdated,
    CustomerNotCreated,
    CustomerNotFound,
    InsufficientFunds,
    TransferFailed,
)
from .models import Account, Customer, Transfer


class CustomerRepository:
    def create(self, name: str) -> Customer:
        try:
            customer = Customer(name=name)
            sess.add(customer)
            sess.commit()
        except SQLAlchemyError:
            sess.rollback()
            raise CustomerNotCreated(name)

        return customer

    def get(self, customer_id: int) -> Customer:
        customer = Customer.query.get(customer_id)
        if not customer:
            raise CustomerNotFound(customer_id)

        return customer


class AccountRepository:
    def create(self, customer_id: int, initial_deposit: float) -> Account:
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                raise CustomerNotFound(customer_id)

            account = Account(customer_id=customer_id, balance=initial_deposit)
            sess.add(account)
            sess.commit()
        except SQLAlchemyError:
            sess.rollback()
            raise AccountNotCreated(customer.name)

        return account

    def get(self, account_id: int) -> Account:
        account = Account.query.get(account_id)
        if not account:
            raise AccountNotFound(account_id)

        return account

    def update_balance(self, account_id: int, new_balance: float) -> None:
        try:
            account = self.get(account_id)
            account.balance = new_balance
            sess.commit()
        except SQLAlchemyError:
            sess.rollback()
            raise AccountNotUpdated(account_id)


class TransferRepository:
    def create(self, from_account_id: int, to_account_id: int, amount: float) -> Transfer:
        try:
            from_account = Account.query.get(from_account_id)
            to_account = Account.query.get(to_account_id)

            if not from_account:
                raise AccountNotFound(from_account_id)
            if not to_account:
                raise AccountNotFound(to_account_id)
            if from_account.balance < amount:
                raise InsufficientFunds(from_account_id)

            from_account.balance -= amount
            to_account.balance += amount

            transfer = Transfer(from_account_id=from_account_id, to_account_id=to_account_id, amount=amount)
            sess.add(transfer)
            sess.commit()
        except SQLAlchemyError:
            sess.rollback()
            raise TransferFailed(from_account_id, to_account_id)

        return transfer

    def get_transfers_for_account(self, account_id: int) -> List[Transfer]:
        transfers_sent = Transfer.query.filter_by(from_account_id=account_id).all()
        transfers_received = Transfer.query.filter_by(to_account_id=account_id).all()
        return transfers_sent + transfers_received
