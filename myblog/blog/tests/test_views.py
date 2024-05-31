import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestUserAuthViews:
    @pytest.fixture()
    def user(self, db):
        return User.objects.create_user(username="testuser", password="1234")

    def test_login_page(self, client):
        url = reverse('user_login')
        response = client.get(url)
        assert response.status_code == 200

    def test_register_page(self, client):
        url = reverse('user_reg')
        response = client.get(url)
        assert response.status_code == 200

    def test_logout_page(self, client, user):
        client.login(username='testuser', password='testpassword')
        url = reverse('logout')
        response = client.get(url)
        assert response.status_code == 302
