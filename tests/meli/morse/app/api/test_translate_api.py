import json


class TestTranslate2Text:

    endpoint = '/translate/v1/2text'

    # Happy path
    
    def test_morse_source(self, test_client, morse2text):
        content = morse2text[0]
        translated_content = morse2text[1]
        req = {
            'msg': {
                'src': 'morse',
                'content': content,
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 200   # SUCCESS(200)
        assert res.content_type == 'application/json'
        assert 'msg' in res.get_json()
        assert all(key in res.get_json()['msg'] for key in ['src', 'content'])
        assert res.get_json()['msg']['src'] == 'text'
        assert res.get_json()['msg']['content'] == translated_content

    def test_bits_source(self, test_client, bits2text):
        content = bits2text[0]
        translated_content = bits2text[1]
        req = {
            'msg': {
                'src': 'bits',
                'content': content,
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 200   # SUCCESS(200)
        assert res.content_type == 'application/json'
        assert 'msg' in res.get_json()
        assert all(key in res.get_json()['msg'] for key in ['src', 'content'])
        assert res.get_json()['msg']['src'] == 'text'
        assert res.get_json()['msg']['content'] == translated_content

    # Invalid data

    def test_invalid_morse(self, test_client, invalid_morse):
        req = {
            'msg': {
                'src': 'morse',
                'content': invalid_morse,
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Invalid morse code' in res.get_json()['message']

    def test_invalid_bits(self, test_client, invalid_bits):
        req = {
            'msg': {
                'src': 'bits',
                'content': invalid_bits,
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Invalid bit' in res.get_json()['message']

    # Invalid request
    
    def test_invalid_msg_src(self, test_client):
        req = {
            'msg': {
                'src': 'text',
                'content': '.-.-.-',
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message source not valid'

    def test_missing_msg_src(self, test_client):
        req = {
            'msg': {
                'content': '.-.-.-',
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message not valid'

    def test_missing_msg_content(self, test_client):
        req = {
            'msg': {
                'src': 'morse',
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message not valid'

    def test_missing_msg(self, test_client):
        req = { }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Missing msg attribute'


    def test_invalid_content_type(self, test_client):
        req = {
            'msg': {
                'src': 'morse',
                'content': '.-.-.-',
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req))

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Invalid content type' in res.get_json()['message']


    def test_big_content(self, test_client):
        req = {
            'msg': {
                'src': 'morse',
                'content': '.-' * 1000,
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Character limit exceeded' in res.get_json()['message']


class TestTranslate2Morse:

    endpoint = '/translate/v1/2morse'

    # Happy path
    
    def test_text_source(self, test_client, text2morse):
        content = text2morse[0]
        translated_content =text2morse[1]
        req = {
            'msg': {
                'src': 'text',
                'content': content,
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 200   # SUCCESS(200)
        assert res.content_type == 'application/json'
        assert 'msg' in res.get_json()
        assert all(key in res.get_json()['msg']
                   for key in ['src', 'content', 'format'])
        assert res.get_json()['msg']['src'] == 'morse'
        assert res.get_json()['msg']['content'] == translated_content

    def test_bits_source(self, test_client, bits2morse):
        content = bits2morse[0]
        translated_content = bits2morse[1]
        req = {
            'msg': {
                'src': 'bits',
                'content': content,
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 200   # SUCCESS(200)
        assert res.content_type == 'application/json'
        assert 'msg' in res.get_json()
        assert all(key in res.get_json()['msg']
                   for key in ['src', 'content', 'format'])
        assert res.get_json()['msg']['src'] == 'morse'
        assert res.get_json()['msg']['content'] == translated_content

    # Invalid data

    def test_invalid_text(self, test_client, invalid_text):
        req = {
            'msg': {
                'src': 'text',
                'content': invalid_text,
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Invalid character' in res.get_json()['message']

    def test_invalid_bits(self, test_client, invalid_bits):
        req = {
            'msg': {
                'src': 'bits',
                'content': invalid_bits,
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Invalid bit' in res.get_json()['message']

    # Invalid request
    
    def test_invalid_msg_src(self, test_client):
        req = {
            'msg': {
                'src': 'morse',
                'content': '.-.-.-',
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message source not valid'

    def test_missing_msg_src(self, test_client):
        req = {
            'msg': {
                'content': '.-.-.-',
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message not valid'

    def test_missing_msg_content(self, test_client):
        req = {
            'msg': {
                'src': 'text',
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message not valid'

    def test_missing_msg(self, test_client):
        req = { }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Missing msg attribute'


    def test_invalid_content_type(self, test_client):
        req = {
            'msg': {
                'src': 'text',
                'content': '.-.-.-',
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req))

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Invalid content type' in res.get_json()['message']


    def test_big_content(self, test_client):
        req = {
            'msg': {
                'src': 'text',
                'content': 'A' * 1001,
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Character limit exceeded' in res.get_json()['message']


class TestTranslate2Bits:

    endpoint = '/translate/v1/2bits'

    # Happy path
    
    def test_text_source(self, test_client, text2bits):
        content = text2bits[0]
        translated_content =text2bits[1]
        req = {
            'msg': {
                'src': 'text',
                'content': content,
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 200   # SUCCESS(200)
        assert res.content_type == 'application/json'
        assert 'msg' in res.get_json()
        assert all(key in res.get_json()['msg'] for key in ['src', 'content'])
        assert res.get_json()['msg']['src'] == 'bits'
        assert res.get_json()['msg']['content'] == translated_content

    def test_morse_source(self, test_client, morse2bits):
        content = morse2bits[0]
        translated_content = morse2bits[1]
        req = {
            'msg': {
                'src': 'morse',
                'content': content,
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 200   # SUCCESS(200)
        assert res.content_type == 'application/json'
        assert 'msg' in res.get_json()
        assert all(key in res.get_json()['msg'] for key in ['src', 'content'])
        assert res.get_json()['msg']['src'] == 'bits'
        assert res.get_json()['msg']['content'] == translated_content

    # Invalid data

    def test_invalid_text(self, test_client, invalid_text):
        req = {
            'msg': {
                'src': 'text',
                'content': invalid_text,
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Invalid character' in res.get_json()['message']

    def test_invalid_morse(self, test_client, invalid_morse):
        req = {
            'msg': {
                'src': 'morse',
                'content': invalid_morse,
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Invalid morse' in res.get_json()['message']

    # Invalid request
    
    def test_invalid_msg_src(self, test_client):
        req = {
            'msg': {
                'src': 'bits',
                'content': '101010',
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message source not valid'

    def test_missing_msg_src(self, test_client):
        req = {
            'msg': {
                'content': '.-.-.-',
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message not valid'

    def test_missing_msg_content(self, test_client):
        req = {
            'msg': {
                'src': 'text',
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message not valid'

    def test_missing_msg(self, test_client):
        req = { }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Missing msg attribute'


    def test_invalid_content_type(self, test_client):
        req = {
            'msg': {
                'src': 'text',
                'content': '.-.-.-',
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req))

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Invalid content type' in res.get_json()['message']


    def test_big_content(self, test_client):
        req = {
            'msg': {
                'src': 'text',
                'content': 'A' * 1001,
            }
        }
        res = test_client.post(self.endpoint,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Character limit exceeded' in res.get_json()['message']
