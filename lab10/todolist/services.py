# File for additional functions, classes, etc that are useful in any kind of this project
import random
import string

def create_auth_header(session):
    token = session.get('token', None)
    return {'Authorization': 'Token {}'.format(token if token else '')}

def generate_confirmation_token(length=50):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))

def convert_from_json_to_obj(st):
    '''
    >> convert_from_json_to_obj("abc, bde, fds, etc")
    return ['abc', 'bde', 'fds', 'etc']
    '''
    return [str.strip(x) for x in st.split(',')]