class CustomerNotFound(Exception):
    def __init__(self, customer_id: int) -> None:
        super().__init__("Customer with id %d not found." % customer_id)


class CustomerNotCreated(Exception):
    def __init__(self, name: str) -> None:
        super().__init__("Customer with name %s not created." % name)


class AccountNotFound(Exception):
    def __init__(self, account_id: int) -> None:
        super().__init__("Account with id %d not found." % account_id)


class AccountNotCreated(Exception):
    def __init__(self, customer_name: str) -> None:
        super().__init__("Account for %s not created." % customer_name)


class AccountNotUpdated(Exception):
    def __init__(self, account_id: int) -> None:
        super().__init__("Account with id %d not updated." % account_id)


class InsufficientFunds(Exception):
    def __init__(self, account_id: int) -> None:
        super().__init__("Account with id %d has insufficient funds." % account_id)


class TransferFailed(Exception):
    def __init__(self, from_account_id: int, to_account_id: int) -> None:
        super().__init__(
            "Transfer from account with id %d to account with id %d failed." % (from_account_id, to_account_id)
        )
