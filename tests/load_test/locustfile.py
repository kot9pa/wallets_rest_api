import logging
import gevent.pool
import httpx
from locust import FastHttpUser, between, task, events
from locust.env import Environment

from src.config import settings
from src.api_v1 import Wallet


rest_api_host = f"http://{settings.SERVER_DOMAIN}:{settings.SERVER_PORT}"
wallets_endpoint = f"{settings.api_v1_prefix}/wallets/"
wallets: list[Wallet] = list()


@events.test_start.add_listener
def on_test_start(environment: Environment, **kwargs):
    logging.info(f"{environment.__dict__=}")
    try:
        wallets.clear()
        response = httpx.get(f"{rest_api_host}{wallets_endpoint}")
        response_json = response.json()
        if "detail" in response_json:
            raise TypeError(f"Detail from response: {response_json['detail']}")
        wallets.extend([Wallet(**w) for w in response_json])
    except httpx.RequestError as exc:
        logging.error(f"An error occurred while requesting {exc.request.url!r}.")
    except Exception as exc:
        logging.error(exc)


class WalletAPITest(FastHttpUser):
    wait_time = between(0.5, 1.5)
    host = rest_api_host

    @task
    def test_get_wallet(self):
        logging.info(f"Run test_get_wallet..")

        def concurrent_request(url):
            self.client.get(url)

        pool = gevent.pool.Pool()
        urls = [f"{wallets_endpoint}{w.wallet_uuid}" for w in wallets]
        for url in urls:
            pool.spawn(concurrent_request, url)
        pool.join()

    @task
    def test_get_wallets(self):
        logging.info(f"Run test_get_wallets..")
        with self.rest("GET", wallets_endpoint) as resp:
            if resp.status_code != 200:
                resp.failure(f"Status code incorrect {resp.status_code}")
            elif "detail" in resp.js:
                resp.failure(f"Detail from response: {resp.js['detail']}")

            # Parse and compare data without balance
            compare_data = [
                {"response": {
                    "wallet_uuid": response["wallet_uuid"],
                    "id": response["id"],
                }, "wallet": {
                    "wallet_uuid": wallet.wallet_uuid,
                    "id": wallet.id,
                }} for wallet, response in zip(wallets, resp.js)]
            if any(data['response'] != data['wallet'] for data in compare_data):
                resp.failure(f"Response incorrect: {compare_data=}")

    @task
    def test_deposit_operation(self):
        logging.info(f"Run test_deposit_operation..")
        for wallet in wallets:
            deposit_amount = 100
            with self.rest(
                "POST",
                f"{settings.api_v1_prefix}/wallets/{wallet.wallet_uuid}/operation",
                json={
                    "operation_type": "DEPOSIT",
                    "amount": deposit_amount
                },
            ) as resp:
                if resp.status_code != 202:
                    resp.failure(f"Status code incorrect {resp.status_code}")
                elif "detail" in resp.js:
                    resp.failure(f"Detail from response: {resp.js['detail']}")
                elif "wallet" not in resp.js:
                    resp.failure(f"'wallet' missing in response {resp.text}")

                wallet_data = {
                    "wallet_uuid": wallet.wallet_uuid,
                    "id": wallet.id,
                }
                op_data = {
                    "operation_type": "DEPOSIT",
                    "amount": deposit_amount,
                    "wallet_id": wallet.id,
                }
                if resp.js['operation']['operation_type'] != op_data['operation_type']:
                    resp.failure(f"'operation_type' incorrect in response: {resp.js=} {wallet_data=}")
                elif resp.js['operation']['amount'] != op_data['amount']:
                    resp.failure(f"'amount' incorrect in response: {resp.js=} {wallet_data=}")
                elif resp.js['operation']['wallet_id'] != op_data['wallet_id']:
                    resp.failure(f"'wallet_id' incorrect in response: {resp.js=} {wallet_data=}")
                elif resp.js['wallet']['wallet_uuid'] != wallet_data['wallet_uuid']:
                    resp.failure(f"'wallet_uuid' incorrect in response: {resp.js=} {wallet_data=}")
                elif resp.js['wallet']['id'] != wallet_data['id']:
                    resp.failure(f"'id' incorrect in response: {resp.js=} {wallet_data=}")

                # If users > 1 error will be raised because of concurrent update
                # wallet_data = {
                #     "balance": wallet.balance + deposit_amount,
                #     "wallet_uuid": wallet.wallet_uuid,
                #     "id": wallet.id,
                # }
                # wallet.balance += deposit_amount
                # if resp.js["wallet"] != wallet_data:
                #     resp.failure(f"{resp.js['wallet']=} != {wallet_data=}")

    @task
    def test_withdraw_operation(self):
        logging.info(f"Run test_withdraw_operation..")
        for wallet in wallets:
            withdraw_amount = 100
            with self.rest(
                "POST",
                f"{settings.api_v1_prefix}/wallets/{wallet.wallet_uuid}/operation",
                json={
                    "operation_type": "WITHDRAW",
                    "amount": withdraw_amount
                },
            ) as resp:
                if resp.status_code != 202:
                    resp.failure(f"Status code incorrect {resp.status_code}")
                elif "detail" in resp.js:
                    resp.failure(f"Detail from response: {resp.js['detail']}")
                elif "wallet" not in resp.js:
                    resp.failure(f"'wallet' missing in response {resp.text}")

                wallet_data = {
                    "wallet_uuid": wallet.wallet_uuid,
                    "id": wallet.id,
                }
                op_data = {
                    "operation_type": "WITHDRAW",
                    "amount": withdraw_amount,
                    "wallet_id": wallet.id,
                }
                if resp.js['operation']['operation_type'] != op_data['operation_type']:
                    resp.failure(f"'operation_type' incorrect in response: {resp.js=} {wallet_data=}")
                elif resp.js['operation']['amount'] != op_data['amount']:
                    resp.failure(f"'amount' incorrect in response: {resp.js=} {wallet_data=}")
                elif resp.js['operation']['wallet_id'] != op_data['wallet_id']:
                    resp.failure(f"'wallet_id' incorrect in response: {resp.js=} {wallet_data=}")
                elif resp.js['wallet']['wallet_uuid'] != wallet_data['wallet_uuid']:
                    resp.failure(f"'wallet_uuid' incorrect in response: {resp.js=} {wallet_data=}")
                elif resp.js['wallet']['id'] != wallet_data['id']:
                    resp.failure(f"'id' incorrect in response: {resp.js=} {wallet_data=}")

                # If users > 1 error will be raised because of concurrent update
                # wallet_data = {
                #     "balance": wallet.balance - withdraw_amount,
                #     "wallet_uuid": wallet.wallet_uuid,
                #     "id": wallet.id,
                # }
                # wallet.balance -= withdraw_amount
                # if resp.js["wallet"] != wallet_data:
                #     resp.failure(f"{resp.js['wallet']=} != {wallet_data=}")
