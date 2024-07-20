from typing import Any, Dict, List, Tuple

from flask import Flask, request

from .db import Session
from .exceptions import AccountNotCreated, AccountNotFound, AccountNotUpdated, CustomerNotCreated, TransferFailed
from .logger import setup_logger
from .services import BankService

app = Flask(__name__)
app.config.from_object("api.settings.DevelopmentConfig")


@app.teardown_appcontext
def teardown_db(resp_or_exc):
    Session.remove()


service = BankService()
logger = setup_logger()


@app.route("/customers", methods=["POST"])
def create_customer() -> Tuple[Dict[str, Any], int]:
    data = request.json
    try:
        customer = service.create_customer(data["name"])
    except KeyError:
        logger.error("Malformed request.")
        return {"error": "Malformed request."}, 400
    except CustomerNotCreated:
        logger.error("Customer not created.")
        return {"error": "Customer not created."}, 503
    logger.info("Customer created successfully.")
    return {"id": customer.id, "name": customer.name}, 201


@app.route("/accounts", methods=["POST"])
def create_account() -> Tuple[Dict[str, Any], int]:
    data = request.json
    try:
        account = service.create_account(data["customer_id"], data["initial_deposit"])
    except KeyError:
        logger.error("Malformed request.")
        return {"error": "Malformed request."}, 400
    except AccountNotCreated:
        logger.error("Account not created.")
        return {"error": "Account not created."}, 503
    logger.info("Account created successfully.")
    return {"id": account.id, "customer_id": account.customer_id, "balance": account.balance}, 201


@app.route("/accounts/<int:account_id>/balance", methods=["GET"])
def get_balance(account_id: int) -> Tuple[Dict[str, Any], int]:
    try:
        balance = service.get_balance(account_id)
    except AccountNotFound:
        logger.error("Account not found.")
        return {"error": "Account not found."}, 404
    logger.info("Balance fetched successfully.")
    return {"balance": balance}, 200


@app.route("/transfers", methods=["POST"])
def transfer_amount() -> Tuple[Dict[str, Any], int]:
    data = request.json
    try:
        transfer = service.transfer_amount(data["from_account_id"], data["to_account_id"], data["amount"])
    except KeyError:
        logger.error("Malformed request.")
        return {"error": "Malformed request."}, 400
    except AccountNotFound:
        logger.error("Account not found.")
        return {"error": "Account not found."}, 404
    except ValueError:
        logger.error("Insufficient funds.")
        return {"error": "Insufficient funds."}, 403
    except AccountNotUpdated:
        logger.error("Account not updated.")
        return {"error": "Account not updated."}, 503
    except TransferFailed:
        logger.error("Transfer failed.")
        return {"error": "Transfer failed."}, 503
    logger.info("Amount transferred successfully.")
    return {
        "id": transfer.id,
        "from_account_id": transfer.from_account_id,
        "to_account_id": transfer.to_account_id,
        "amount": transfer.amount,
        "timestamp": transfer.created_at,
    }, 200


@app.route("/accounts/<int:account_id>/transfers", methods=["GET"])
def get_transfer_history(account_id: int) -> Tuple[List[Dict[str, Any]], int]:
    transfers = service.get_transfer_history(account_id)
    logger.info("Transfer history fetched successfully.")
    return [
        {
            "id": transfer.id,
            "from_account_id": transfer.from_account_id,
            "to_account_id": transfer.to_account_id,
            "amount": transfer.amount,
            "timestamp": transfer.created_at,
        }
        for transfer in transfers
    ], 200
