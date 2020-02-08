import json


class TestTranslateAPI:

    url_2text = '/translate/v1/2text'
    url_2morse = '/translate/v1/2morse'
    url_2bits = '/translate/v1/2bits'

    def test_2text_from_morse(self, test_client, morse2text):
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
        res = test_client.post(self.url_2text,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 200   # SUCCESS(200)
        assert res.get_json()['msg']['content'] == translated_content

    def test_2text_invalid_morse(self, test_client, invalid_morse):
        req = {
            'msg': {
                'src': 'morse',
                'content': invalid_morse,
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.url_2text,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Invalid morse code' in res.get_json()['message']

    def test_2text_from_bits(self, test_client, bits2text):
        content = bits2text[0]
        translated_content = bits2text[1]
        req = {
            'msg': {
                'src': 'bits',
                'content': content,
            }
        }
        res = test_client.post(self.url_2text,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 200   # SUCCESS(200)
        assert res.get_json()['msg']['content'] == translated_content

    def test_2text_invalid_bits(self, test_client, invalid_bits):
        req = {
            'msg': {
                'src': 'bits',
                'content': invalid_bits,
            }
        }
        res = test_client.post(self.url_2text,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Invalid bit' in res.get_json()['message']

    def test_2text_invalid_msg_src(self, test_client):
        req = {
            'msg': {
                'src': 'INVALID SOURCE',
                'content': '.-.-.-',
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.url_2text,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message source not valid'

    def test_2text_missing_msg_src(self, test_client):
        req = {
            'msg': {
                'content': '.-.-.-',
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.url_2text,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message not valid'

    def test_2text_missing_content_src(self, test_client):
        req = {
            'msg': {
                'src': 'morse',
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.url_2text,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert res.get_json()['message'] == 'Message not valid'

    def test_2text_big_content(self, test_client):
        req = {
            'msg': {
                'src': 'morse',
                'content': '.-' * 1000,
                'format': {
                    'inter_word': ' / '
                }
            }
        }
        res = test_client.post(self.url_2text,
                               data=json.dumps(req),
                               content_type='application/json')

        assert res.status_code == 400   # BAD REQUEST(400)
        assert res.get_json()['error'] == 'bad request'
        assert 'Character limit exceeded' in res.get_json()['message'] 
