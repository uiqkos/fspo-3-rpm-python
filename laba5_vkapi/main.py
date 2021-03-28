from collections import Counter
from functools import reduce
import network
from get import *
from datetime import datetime


def get_scope(user_id, scope, fields='i', **kwargs):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    response = get_fields(user_id, scope, fields, **kwargs)
    print(response)
    return response['response']['items'] if 'response' in response.keys() else []


def age_predict(user_id):
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


# import plotly.offline.offline as of
#
# x, y = count_dates_from_messages(messages_get_history(default_user_id, count=200))
#
# print('\n'.join([str(pair) for pair in zip(x, y)]))
#
# fig = go.Figure()
# fig.add_scatter(go.Scatter({'x': x, 'y': y}))
# of.plot({'x': x, 'y': y})


def user_friends_and_their_friends(user_id, max_depth=3, depth=1, friends_limit=50):
    if depth >= max_depth:
        return []
    users = get_scope(user_id, 'friends')[:friends_limit]
    friend_ids = list(map(lambda user: user['id'], users))
    return [*[(user_id, friend_id) for friend_id in friend_ids], *reduce(
        list.__add__,
        map(lambda friend_id: user_friends_and_their_friends(
            friend_id, max_depth=max_depth, depth=depth + 1
        ), friend_ids),
        list()
    )]


d = dict()
c = 0


def map_id(id_):
    if id_ in d.keys():
        return d[id_]
    global c
    d[id_] = c
    c += 1
    return d[id_]


edges = [(map_id(id1), map_id(id2)) for id1, id2 in user_friends_and_their_friends(default_user_id, max_depth=3)][:500]
network.plot_graph(list(set(edges)))
