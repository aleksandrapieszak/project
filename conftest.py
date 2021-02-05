import pytest
from django.contrib.auth.models import User, Permission

from project.models import Client, Debtor, Case


@pytest.fixture
def unauthorized_user():
    unauthorized_user = User.objects.create_user("Ola")
    return unauthorized_user


@pytest.fixture
def authorized_user():
    authorized_user = User.objects.create_user("Ola")
    perm = Permission.objects.get(codename="add_leadingperson")
    authorized_user.user_permissions.add(perm)
    return authorized_user


@pytest.fixture
def test_client():
    client = Client.objects.create(name='KlientTestowy', address='Malinowa 13', post_code='60222', city='Kraków',
                                        nip='2918089285')
    return client


@pytest.fixture
def test_debtor():
    client = Client.objects.create(name='KlientTestowy1', address='Malinowa 13', post_code='60222', city='Kraków',
                                   nip='2918089286')
    debtor = Debtor.objects.create(name="Testowydłużnik", nip='3813758713', client=client)
    return debtor


@pytest.fixture
def test_case():
    client = Client.objects.create(name='KlientTestowy12', address='Malinowa 13', post_code='60222', city='Kraków',
                                   nip='2918089289')
    debtor = Debtor.objects.create(name="Testowydłużnik1", nip='3813758714', client=client)
    case = Case.objects.create(case_number='22/2020/25689WX', case_description='SprawaTestowa1', client=client,
                               debtor=debtor)
    return case
