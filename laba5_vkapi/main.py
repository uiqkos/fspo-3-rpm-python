from collections import Counter

import plotly

from get import *
from datetime import datetime

import plotly.graph_objs as go
from plotly import plot


def get_scope(user_id, scope, fields='', **kwargs):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    response = get_fields(user_id, scope, fields, **kwargs)
    print(response)
    return response['response']['items']


def age_predict(user_id):
    """
    >>> age_predict(???)
    ???
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    ages = \
        list(
            map(lambda str_date: datetime.date.today().year - int(str_date[2]),
                filter(lambda str_date: len(str_date) == 3,
                       map(lambda str_date: str_date.split('.'),
                           map(lambda user: user['bdate'],
                               filter(lambda user: 'bdate' in user.keys(),
                                      get_scope(user_id, 'friends', 'bdate')
                                      )
                               )
                           )
                       )
                )
        )

    return int(sum(ages) / len(ages))


def messages_get_history(user_id, offset=0, count=20):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "offset must be positive integer"
    assert count >= 0, "count must be positive integer"

    return get_scope(user_id, 'messages', offset=offset, count=count, method='getHistory')


def count_dates_from_messages(messages):
    counter = Counter(map(
        lambda message:
        datetime.fromtimestamp(message['date']),
        messages
    ))

    return list(counter.keys()), list(counter.values())



import plotly.offline.offline as of

x, y = count_dates_from_messages(messages_get_history(default_user_id, count=200))

print('\n'.join([str(pair) for pair in zip(x, y)]))

fig = go.Figure()
fig.add_scatter(go.Scatter({'x': x, 'y': y}))
of.plot({'x': x, 'y': y})

