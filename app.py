import logging

import requests
from flask import Flask, request

app = Flask(__name__)


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
        slnet_token = r.cookies["slnet"]
        logging.info('slnet token: {}'.format(slnet_token))
        return slnet_token, r.status_code
    else:
        return None, r.status_code


@app.route('/auth.slid')
def get_slnet_token():  # put application's code here
    slid_token = request.args.get('slid_token', default=None, type=str)
    if slid_token is None:
        return "", 400

    slnet_token, status_code = __get_slnet_token(slid_token)
    result = {
        "slnet_token": slnet_token
    }
    return result, status_code


if __name__ == '__main__':
    app.run()
