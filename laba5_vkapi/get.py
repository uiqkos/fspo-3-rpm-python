from time import sleep

import requests

default_domain = "https://api.vk.com/method"
default_access_token = 'TOKEN'
default_user_id = 450835010


def get_fields(
        user_id, scope,
        fields='',
        domain=default_domain,
        access_token=default_access_token,
        method='get',
        **kwargs
):
    response_params = {
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields,
        'v': '5.80',
        **kwargs
    }

    param_list = '&' \
        .join([
        str(key) + '=' + str(value)
        for key, value in response_params.items()
        if value != ''
    ])

    response = requests.get(
        f"{domain}/{scope}.{method}"
        f"?{param_list}")

    return response.json()


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    backoff = 1

    for i in range(max_retries):
        if len(params.items()) != 0:
            print(requests.get(
                url + '?' +
                '&'.join([
                    '{}={}'.format(*item)
                    for item in params.items()
                ]), timeout=timeout
            ))
        else:
            print(requests.get(url, timeout=timeout))

        sleep(backoff)
        backoff *= backoff_factor
