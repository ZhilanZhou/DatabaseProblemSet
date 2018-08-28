"""
Helper functions for self checking notebook
"""
import json
import hashlib
import pickle
import pprint as p
import os

from bson import json_util

def host():
    """
    returns the host that mongo driver should connect to
    """
    return "mongodb://521:password@ds229835.mlab.com:29835/comp521"

def pprint(obj, count=5):
    """
    pretty prints an object
    """
    printer = p.PrettyPrinter(indent=2)
    printer.pprint(obj[:count])

def fetchall(cursor):
    """
    returns all of the documents from a cursor object
    """
    try:
        results = list(cursor)
    except TypeError:
        results = cursor

    return results

def serialize(obj, indent=None):
    """
    serializes Python object into string
    """
    return json.dumps(
        obj,
        sort_keys=True,
        default=json_util.default,
        ensure_ascii=False,
        indent=indent
    )

def save(letter, number, cursor):
    """
    saves results for a particular question
    """
    with open('exercises.pickle', 'rb') as handle:
        answers = pickle.load(handle)

    if letter not in answers:
        answers[letter] = []
        for i in range(number):
            answers[letter][i] = ''

    answers[letter][number - 1] = sha1(serialize(cursor))

    os.remove('exercises.pickle')

    with open('exercises.pickle', 'wb') as handle:
        pickle.dump(answers, handle, protocol=pickle.HIGHEST_PROTOCOL)

def sha1(data):
    m = hashlib.sha1()
    m.update(data.encode('utf-8'))
    return m.hexdigest()

def sort_results(cursor):
    try:
        results = sorted(list(cursor), key=lambda x: x['_id'])
    except KeyError:
        results = list(cursor)
    except TypeError:
        results = cursor

    return results

def check(letter, number, result, **kwargs):
    """
    checks an answer for equality by comparing hashes
    """

    # if sort set to True, answer should already be in sorted order
    if kwargs.get('sort') is not True:
        result = sort_results(result)

    if kwargs.get('save') is True:
        save(letter, number, result)

    with open('exercises.pickle', 'rb') as handle:
        answers = pickle.load(handle)

    hashed_answer = answers[letter][number - 1]
    serialized_result = serialize(result)

    hashed_result = sha1(serialized_result)

    if hashed_result == hashed_answer:
        print('%s%s is correct.' % (letter, number))
    else:
        print('%s%s is incorrect.' % (letter, number))
