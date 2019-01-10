''' project utils '''

import time
import functools
import json
import os

__all__ = ['clock', 'assure_path', 'write_to_json', 'read_from_json']

def clock(name=None):
    ''' timming decorator, name="job name" '''
    if not name:
        raise ValueError('decorator clock missing argument: name')
    def wrap(func):
        @functools.wraps(func)
        def wrapped_f(*args, **kwargs):
            start = time.time()
            print(f'{name} started...')
            res = func(*args, **kwargs)
            print(f'{name} finished with elapsed time: {time.time() - start:.3f}')
            return res
        return wrapped_f
    return wrap

def assure_path(*dargs):
    ''' assert all paths exist, args=[path] '''
    for path in dargs:
        if not os.path.exists(path):
            raise ValueError(f'path: {path} not exist')
    return lambda func: func

def write_to_json(path, data):
    ''' write json to current dir, path="out path", data="json serializable data" '''
    dir = os.path.dirname(path)
    if not (os.path.exists(dir) and os.path.isdir(dir)):
        os.makedirs(dir)
    with open(path, 'w+') as outfile:
        json.dump(data, outfile)

def read_from_json(path):
    ''' return data from json, path="read path" '''
    with open(path, 'rb') as infile:
        return json.load(infile)

if __name__ == '__main__':
    pass