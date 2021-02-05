import pytest
from project.models import Client, LeadingPerson, Contract, Debtor, ContactPerson, Case, CashRegister


# dodawanie klienta
@pytest.mark.django_db
def test_client_add(client):
    response = client.post('/add-client/', {'name': 'KlientTestowy12345', 'address': 'Malinowa 13',
                                            'post_code': '62052', 'city': 'Poznań', 'nip': '2918089285'})
    assert Client.objects.filter(name='KlientTestowy12345')


# dodawanie umowy
@pytest.mark.django_db
def test_contract_add(client):
    test_client = Client.objects.create(name='KlientTestowy', address='Malinowa 13', post_code='60222',
                                        city='Kraków', nip='2918089285')
    response = client.post(f'/client/{test_client.id}/add-contract', {'number': 'XX/20/2020', 'date_from': '2020-03-10',
                                                                      'date_to': '2021-02-10',
                                                                      'corespondent_cost': 'True', 'law_cost': 'True',
                                                                      'zaliczka': 'False', 'client': [test_client.id]})
    assert Contract.objects.filter(number='XX/20/2020')


@pytest.mark.django_db
def test_debtor_add(client, test_client):
    response = client.post(f'/client/{test_client.id}/add-debtor/', {'name': 'TestowyDłużnik', 'nip': '3813758713',
                                                                     'client': [test_client.id]})
    assert Debtor.objects.filter(name='TestowyDłużnik')


@pytest.mark.django_db
def test_contactperson_add(client, test_client):
    response = client.post(f'/client/{test_client.id}/contact-person-add/',
                           {'surname': 'TestoweNazwisko', 'email': 'testowy@wp.pl', 'phone_number': '504015615',
                            'client': [test_client.id]})
    assert ContactPerson.objects.filter(surname='TestoweNazwisko')


@pytest.mark.django_db
def test_case_add(client, test_client):
    debtor = Debtor.objects.create(name="Testowydłużnik", nip='3813758713', client=test_client)
    response = client.post(f'/client/{test_client.id}/{debtor.id}/add-case', {'case_number': '22/2020/25689WW',
                                                                              'case_description': 'SprawaTestowa',
                                                                              'client': [test_client.id],
                                                                              'debtor': [debtor.id]})
    assert Case.objects.filter(case_number='22/2020/25689WW')


@pytest.mark.django_db
def test_cashregister_add(client, test_client):
    debtor = Debtor.objects.create(name="Testowydłużnik", nip='3813758713', client=test_client)
    case = Case.objects.create(case_number='22/2020/25689WX', case_description='SprawaTestowa1', client=test_client,
                               debtor=debtor)
    response = client.post(f'/client/{test_client.id}/{debtor.id}/{case.id}/add-cashregister',
                           {'addressee': 'Testowyadresat1', 'account_number': '123567893258',
                            'transfer_title': 'przykładowyTytuł', 'value': '100.00',
                            'document': '1', 'rodzaj_rozliczenia': '2', 'client': [test_client.id],
                            'id_debtor': [debtor.id], 'id_case': [case.id]})
    assert CashRegister.objects.filter(addressee='Testowyadresat1')


@pytest.mark.django_db
def test_case_add(client, test_client, test_debtor):
    response = client.post(f'/client/{test_client.id}/{test_debtor.id}/add-case', {'case_number': '22/2020/25689WW',
                                                                                  'case_description': 'SprawaTestowa',
                                                                                  'client': [test_client.id],
                                                                                  'debtor': [test_debtor.id]})
    assert Case.objects.filter(case_number='22/2020/25689WW')


@pytest.mark.django_db
def test_add_leadingperson(client, authorized_user, test_client):
    client.force_login(authorized_user)
    response = client.post('/add-leading-person/', {'name': 'Agnieszka', 'client': [test_client.id]})
    assert LeadingPerson.objects.filter(name='Agnieszka')


@pytest.mark.django_db
def test_add_leadingperson_missing_permission(client, unauthorized_user, test_client):
    client.force_login(unauthorized_user)
    response = client.post('/add-leading-person/', {'name': 'Agnieszka', 'client': [test_client.id]})
    assert response.status_code == 403
