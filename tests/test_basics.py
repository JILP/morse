from flask import current_app


class TestBasics:

    def test_app_exists(self, test_client):
        assert current_app is not None

    def test_app_is_testing(self, test_client):
        assert current_app.config['TESTING']
