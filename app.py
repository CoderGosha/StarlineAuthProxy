import json
import logging
from types import SimpleNamespace
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

import requests
from flask import Flask, request, abort

from loggerinitializer import initialize_logger
from models import SyncLogs

app = Flask(__name__)
initialize_logger("log")
logging.info("Start proxy api")

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("34567890erdfghjkljhgfdxcvbnjkliuytrdf"),
    "starline": generate_password_hash("erdfghjkljhgfdxcvbnjkliuytrdf")
}


def __get_slnet_token(slid_token) -> (str, int):
    """
    Авторизация пользователя по токену StarLineID. Токен авторизации предварительно необходимо получить на сервере StarLineID.
    :param slid_token: Токен StarLineID
    :return: Токен пользователя на StarLineAPI
    """
    url = 'https://developer.starline.ru/json/v2/auth.slid'
    logging.info('execute request: {}'.format(url))
    data = {
        'slid_token': slid_token
    }
    r = requests.post(url, json=data)
    if r.status_code == 200:
        response = r.json()
        logging.info('response info: {}'.format(r))
        logging.info('response data: {}'.format(response))
        slnet_token = ""
        user_id = ""
        if "slnet" in r.cookies:
            slnet_token = r.cookies["slnet"]
        logging.info('slnet token: {}'.format(slnet_token))
        message = ""
        if "codestring" in response:
            message = response["codestring"]

        if "user_id" in response:
            user_id = response["user_id"]
        return slnet_token, r.status_code, message, user_id
    else:
        return None, r.status_code, r.text, ""


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/auth.slid')
def get_slnet_token():  # put application's code here
    slid_token = request.args.get('slid_token', default=None, type=str)
    if slid_token is None:
        return "", 400

    slnet_token, status_code, message, user_id = __get_slnet_token(slid_token)
    result = {
        "slnet_token": slnet_token,
        "user_id": user_id,
        "message": message
    }
    return result, status_code


@app.route('/sync.logs', methods=['POST'])
@auth.login_required
def sync_logs():
    if request.json:
        logs = SyncLogs(**request.json)
        app.logger.info(logs)
        return "ok"
    abort(400)


if __name__ == '__main__':
    app.run()
