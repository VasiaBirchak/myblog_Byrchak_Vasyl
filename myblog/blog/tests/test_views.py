import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestUserAuthViews:
    @pytest.fixture()
    def user(self, db):
        return User.objects.create_user(username="testuser", password="1234")

    def test_login_page(self, client, user):
        url = reverse('user_login')
        response = client.get(url)
        assert response.status_code == 200
        response = client.post(url, {'username': 'testuser', 'password': '1234'}, follow=True)
        assert response.status_code == 200
        assert '_auth_user_id' in client.session
        user_id_in_session = client.session['_auth_user_id']
        logged_in_user = User.objects.get(pk=user_id_in_session)
        assert logged_in_user.username == 'testuser'

    def test_register_page(self, client):
        url = reverse('user_reg')
        response = client.get(url)
        assert response.status_code == 200
        response = client.post(url, {
            'username': 'newuser',
            'password1': 'complexpassword',
            'password2': 'complexpassword',
            'email': 'newuser@example.com'
        }, follow=True)
        assert response.status_code == 200
        assert '_auth_user_id' in client.session

    def test_logout_page(self, client, user):
        client.login(username='testuser', password='testpassword')
        url = reverse('logout')
        response = client.get(url, follow=True)
        assert response.status_code == 200
        assert '_auth_user_id' not in client.session
