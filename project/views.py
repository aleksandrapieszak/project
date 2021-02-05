from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import CreateView

from project.forms import ClientAddForm, ContractAddForm, ClientContractAddForm, ContactPersonAddForm, DebtorAddForm, \
    CaseAddForm, ClientDebtorCaseCashRegisterAddForm, \
    LoginForm, AddUserForm
from project.models import Client, Contract, ContactPerson, Debtor, Case, CashRegister, LeadingPerson, \
    LeadingPersonClient


class Main(View):
    """
    The view returns the home page of the application
    """

    def get(self, request):
        return render(request, 'main.html')


class ClientAddView(View):
    """

The view after entering with the method of get shows the form for adding a new client,
after entering with the method of post, it saves the client in the database and redirects to the list of clients

    """

    def get(self, request):
        form = ClientAddForm()
        return render(request, 'client_add.html', {'form': form})

    def post(self, request):
        form = ClientAddForm(request.POST)
        if form.is_valid():
            client = Client.objects.create(
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                post_code=form.cleaned_data['post_code'],
                city=form.cleaned_data['city'],
                nip=form.cleaned_data['nip'],
            )
            return redirect(f'../client/{client.id}')
        else:
            return render(request, 'client_add.html', {'form': form})


class ClientView(View):
    """ The view after entering with the get method returns the data of the given client
    and contact persons for a given client. """

    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        contracts = Contract.objects.filter(client=client)
        contact_person = ContactPerson.objects.filter(client=client)
        return render(request, 'client.html',
                      {'client': client, 'contracts': contracts, 'contact_person': contact_person})


class ClientContractView(View):
    """
    The view after entering the get method shows the data of a given customer and all his contracts
    """

    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        contracts = Contract.objects.filter(client=client)
        return render(request, 'contract_list.html', {'client': client, 'contracts': contracts})


class ContractAddView(View):
    """
    After entering the get method, the view returns a form for creating a new contract,
    based on the already created client.
    After entering the post method, he saves a new contract to the database assigning it to the selected customer
    """

    def get(self, request):
        form = ContractAddForm()
        return render(request, 'contract_add.html', {'form': form})

    def post(self, request):
        form = ContractAddForm(request.POST)
        if form.is_valid():
            contract = Contract.objects.create(
                number=form.cleaned_data['number'],
                date_from=form.cleaned_data['date_from'],
                date_to=form.cleaned_data['date_to'],
                corespondent_cost=form.cleaned_data['corespondent_cost'],
                law_cost=form.cleaned_data['law_cost'],
                zaliczka=form.cleaned_data['zaliczka'],
                client=form.cleaned_data['client'],

            )
            return redirect(f'../contract/{contract.id}')
        else:
            return render(request, 'contract_add.html', {'form': form})


class ContractView(View):
    """
    The view returns the selected contract based on the contract's "id" passed in the get method"""

    def get(self, request, contract_id):
        contract = Contract.objects.get(id=contract_id)
        return render(request, 'contract.html', {'contract': contract})


class ClientContractAddView(View):
    """
    After entering the get method, the view returns a form for creating a new contract,
     based on the "id_clienta" argument,
     after entering the post method, he adds the contract to
     the database and redirects to the list of all contracts concluded with this client"""

    def get(self, request, client_id):
        client_id = Client.objects.get(id=client_id)
        form = ClientContractAddForm()
        return render(request, 'client_contract_add.html', {'form': form})

    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        form = ClientContractAddForm(request.POST)
        if form.is_valid():
            contract = Contract.objects.create(
                number=form.cleaned_data['number'],
                date_from=form.cleaned_data['date_from'],
                date_to=form.cleaned_data['date_to'],
                corespondent_cost=form.cleaned_data['corespondent_cost'],
                law_cost=form.cleaned_data['law_cost'],
                zaliczka=form.cleaned_data['zaliczka'],
                client=client

            )
            return redirect(f'../{client_id}/contract-list')
        else:
            return render(request, 'client_contract_add.html', {'form': form})


class ClientListView(View):
    """
    The view after entering with the get method retrieves a list of all saved clients
     in the database and returns them sorted by "name"
     """

    def get(self, request):
        clients = Client.objects.all().order_by("name")
        return render(request, 'client_list.html', {'clients': clients})


class DebtorListView(View):
    """
    The view after entering the get method takes a list of all debtors and returns them sorted by. "client"
    """

    def get(self, request):
        debtors = Debtor.objects.all().order_by("client")
        return render(request, 'all_debtor_list.html', {'debtors': debtors})


class CaseListView(View):
    """
    The view after entering with the get method retrieves a list of all case in the database sorted by "client_id"
    """

    def get(self, request):
        cases = Case.objects.all().order_by("client_id")
        return render(request, 'all_case_list.html', {'cases': cases})


class CashRegisterListView(View):
    """
   The view after entering with the get method retrieves all cashregister from the database sorted by "client"
    """

    def get(self, request):
        cashregisters = CashRegister.objects.all().order_by("client")
        return render(request, 'all_cashregister_list.html', {'cashregisters': cashregisters})


class ContractDetails(View):
    def get(self, request, contract_id, client_id):
        client = Client.objects.get(id=client_id)
        contract = Contract.objects.get(id=contract_id)
        return render(request, 'contract_details.html', {'contract': contract,
                                                         'client': client})


class ContactPersonAddView(View):
    """
    After entry, the get method returns a form for adding a contact person to a given customer
     based on its id given in the argument. After entering the post method, he saves the Contact Person assigned
     to this client to the database.
    """

    def get(self, request, client_id):
        client_id = Client.objects.get(id=client_id)
        form = ContactPersonAddForm()
        return render(request, 'contact_person_add.html', {'form': form})

    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        form = ContactPersonAddForm(request.POST)
        if form.is_valid():
            contact_person = ContactPerson.objects.create(
                surname=form.cleaned_data['surname'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                client=client

            )
            return redirect(f'../')
        else:
            return render(request, 'contact_person_add.html', {'form': form})


class ClientDebtorAddView(View):
    """

After entering the get method, the view displays a form for adding a new debtor to the selected customer whose id
    is passed to the argument of this method, upon entry with the method of post assigned debtor
     to the client is written to the data base.
    """

    def get(self, request, client_id):
        client_id = Client.objects.get(id=client_id)
        form = DebtorAddForm()
        return render(request, 'client_debtor_add.html', {'form': form})

    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        form = DebtorAddForm(request.POST)
        if form.is_valid():
            debtor = Debtor.objects.create(
                name=form.cleaned_data['name'],
                nip=form.cleaned_data['nip'],
                client=client

            )
            return redirect(f'../debtor-list')
        else:
            return render(request, 'client_debtor_add.html', {'form': form})


class ClientDebtorView(View):
    """ After entering the get method, the view retrieves all debtors of a given client, based on the given client's id
     in the method argument"""

    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        debtors = Debtor.objects.filter(client=client)
        return render(request, 'debtor_list.html', {'client': client, 'debtors': debtors})


class ClientDebtorCaseAddView(View):
    """ After entering the get method, the view displays a form for adding a case to a given debtor
    a given client. Information about the client id and the id of his debtor to whom it is assigned
    is a new case provided by the arguments of the get method. After entering the post method, the new case is saved
     to the database"""

    def get(self, request, client_id, debtor_id):
        client_id = Client.objects.get(id=client_id)
        debtor_id = Debtor.objects.get(id=debtor_id)
        form = CaseAddForm()
        return render(request, 'client_debtor_case_add.html', {'form': form, 'client': client_id, 'debtor': debtor_id})

    def post(self, request, client_id, debtor_id):
        client = Client.objects.get(id=client_id)
        debtor = Debtor.objects.get(id=debtor_id)
        form = CaseAddForm(request.POST)
        if form.is_valid():
            case = Case.objects.create(
                case_number=form.cleaned_data['case_number'],
                case_description=form.cleaned_data['case_description'],
                client=client,
                debtor=debtor
            )
            return redirect(f'../../{client_id}/{debtor_id}/case-list')
        else:
            return render(request, 'client_debtor_case_add.html', {'form': form})


class ClientDebtorCaseView(View):
    """
    The view after entering with the get method gets all the cases where the client id and debtor id match
    those passed in the arguments of the get method. So for a given client and his debtor, he collects all his cases.
    """

    def get(self, request, client_id, debtor_id):
        client = Client.objects.get(id=client_id)
        debtor = Debtor.objects.get(id=debtor_id)
        cases = Case.objects.filter(debtor=debtor)
        return render(request, 'case_list.html', {'client': client, 'debtor': debtor, 'cases': cases})


class ClientDebtorCashRegisterAddView(View):
    """The view after entering the get method displays a form for adding a cashregister to a given case,
    a given debtor, a given client, the identification of the client, debtor and the case is based on arguments
     passed in the get method. After entering the post method, a new cashregister is added to the database"""

    def get(self, request, client_id, debtor_id, case_id):
        client_id = Client.objects.get(id=client_id)
        debtor_id = Debtor.objects.get(id=debtor_id)
        case_id = Case.objects.get(id=case_id)
        form = ClientDebtorCaseCashRegisterAddForm()
        return render(request, 'client_debtor_case_cashregister_add.html', {'form': form, 'client': client_id,
                                                                            'debtor': debtor_id, 'case': case_id})

    def post(self, request, client_id, debtor_id, case_id):
        client = Client.objects.get(id=client_id)
        debtor = Debtor.objects.get(id=debtor_id)
        case = Case.objects.get(id=case_id)
        form = ClientDebtorCaseCashRegisterAddForm(request.POST)
        if form.is_valid():
            cashregister = CashRegister.objects.create(
                addressee=form.cleaned_data['addressee'],
                account_number=form.cleaned_data['account_number'],
                transfer_title=form.cleaned_data['transfer_title'],
                value=form.cleaned_data['value'],
                document=form.cleaned_data['document'],
                rodzaj_rozliczenia=form.cleaned_data['rodzaj_rozliczenia'],
                id_case=case,
                id_debtor=debtor,
                client=client,
            )
            return redirect(f'../../../{client_id}/{debtor_id}/{case_id}/cashregister-list')
        else:
            return render(request, 'client_debtor_case_cashregister_add.html', {'form': form})


class ClientDebtorCaseCashRegisterView(View):
    """ The view after entering the get method retrieves all cashregisters for a given case.
    The data is collected on the basis of the client's id, debtor's id and case id,
     which are passed in arguments to the get method. The method also calculates the current balance of a given case,
     first, it sums up all cashregisters marked as WYDATEK,
     then sums all calculations marked as WPLATA and then subtracts the value of expenses from the value of payments"""

    def get(self, request, client_id, debtor_id, case_id):
        client = Client.objects.get(id=client_id)
        debtor = Debtor.objects.get(id=debtor_id)
        case = Case.objects.get(id=case_id)
        cashregisters = CashRegister.objects.filter(id_case=case)
        wydatki = CashRegister.objects.filter(id_case=case, rodzaj_rozliczenia=1).aggregate(Sum('value'))
        wplaty = CashRegister.objects.filter(id_case=case, rodzaj_rozliczenia=2).aggregate(Sum('value'))
        kwota_wplaty = wplaty['value__sum']
        kwota_wydatki = wydatki['value__sum']
        if kwota_wplaty == None and kwota_wydatki == None:
            suma = 0
        elif kwota_wplaty == None:
            suma = - kwota_wydatki
        elif kwota_wydatki == None:
            suma = kwota_wplaty
        else:
            result = - kwota_wydatki + kwota_wplaty
            suma = round(result, 2)
        return render(request, 'cashregister_list.html',
                      {'client': client, 'debtor': debtor, 'case': case, 'cashregisters': cashregisters, 'suma': suma})


class ClientDebtorCashRegisterView(View):
    """ The view after entering the get method retrieves all cashregisters of all cases of a given debtor.
    The data is collected on the basis of the client's id, debtor's id,
     which are passed in arguments to the get method. The method also calculates the current balance of a given debtor,
     first, he sums up all cashregister of all cases of this debtor marked as WYDATEK,
     then sums up all settlements of all cases marked as WPLATA,
      then subtracts the value of expenses from the value of contributions"""

    def get(self, request, client_id, debtor_id):
        client = Client.objects.get(id=client_id)
        debtor = Debtor.objects.get(id=debtor_id)
        cashregisters = CashRegister.objects.filter(id_debtor=debtor)
        wydatki = CashRegister.objects.filter(id_debtor=debtor, rodzaj_rozliczenia=1).aggregate(Sum('value'))
        wplaty = CashRegister.objects.filter(id_debtor=debtor, rodzaj_rozliczenia=2).aggregate(Sum('value'))
        kwota_wplaty = wplaty['value__sum']
        kwota_wydatki = wydatki['value__sum']
        if kwota_wplaty == None and kwota_wydatki == None:
            suma = 0
        elif kwota_wplaty == None:
            suma = - kwota_wydatki
        elif kwota_wydatki == None:
            suma = kwota_wplaty
        else:
            result = - kwota_wydatki + kwota_wplaty
            suma = round(result, 2)
        return render(request, 'debtor_cashregister_list.html',
                      {'client': client, 'debtor': debtor, 'cashregisters': cashregisters, 'suma': suma})


class ClientCashRegisterView(View):
    """ The view after entering the get method retrieves all cashregisters of all cases,
    all debtors of the selected client.
    Data is collected based on the customer's id,
     which are passed in arguments to the get method. The method also calculates the current balance of a given,
     first it sums up all cashregisters of all cases, all debtors of this client marked as EXPENDITURE,
     then it sums up all cashregisters of all cases, all debtors of this client
      marked as WPLATA and then subtracts the value of expenses from the value of payments"""

    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        cashregisters = CashRegister.objects.filter(client=client)
        wydatki = CashRegister.objects.filter(client=client, rodzaj_rozliczenia=1).aggregate(Sum('value'))
        wplaty = CashRegister.objects.filter(client=client, rodzaj_rozliczenia=2).aggregate(Sum('value'))
        kwota_wydatki = wydatki['value__sum']
        kwota_wplaty = wplaty['value__sum']
        if kwota_wplaty == None and kwota_wydatki == None:
            suma = 0
        elif kwota_wplaty == None:
            suma = - kwota_wydatki
        elif kwota_wydatki == None:
            suma = kwota_wplaty
        else:
            result = - kwota_wydatki + kwota_wplaty
            suma = round(result, 2)
        return render(request, 'client_debtor_cashregister_list.html',
                      {'client': client, 'cashregisters': cashregisters, 'suma': suma})


class ClientCaseView(View):
    """
    The view after entering with the get method retrieves all cases of a given client based on his id,
    passed in the argument of the get method."""

    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        debtors = Debtor.objects.filter(client=client)
        cases = Case.objects.filter(client=client)
        return render(request, 'client_case_list.html', {'client': client, 'debtors': debtors, 'cases': cases})


class ClientLeadingPersonAdd(PermissionRequiredMixin, CreateView):
    """
    The view after entering the get method displays a form for adding a new person "leadingperson" of the client.
    Upon entry, the post method saves that person to the database.
    """

    permission_required = 'project.add_leadingperson'
    model = LeadingPerson
    fields = '__all__'
    success_url = '/leading-person-list'


class ClientLeadingPersonView(View):
    """
The view is taken by all people "leadingperson" all clients """

    def get(self, request):
        leading_person = LeadingPersonClient.objects.all()
        return render(request, 'leading_person_all.html', {'leading_person': leading_person})


class LoginView(View):
    """
    After using the get method, the view displays the login form,
    after using the method, it logs the user in"""

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})


class LogoutView(View):
    """ The view logs the user out"""

    def get(self, request):
        logout(request)
        return redirect('/')


class AddUserView(View):
    """
    The view after entering the get method displays a form for adding a new user.
    After entering the post method, it saves the user to the database."""

    def get(self, request):
        form = AddUserForm()
        return render(request, 'user_profile.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data['login'],
                                     password=form.cleaned_data['password'],
                                     email=form.cleaned_data['email'],
                                     first_name=form.cleaned_data['first_name'],
                                     last_name=form.cleaned_data['last_name'])
            return redirect('../login/')
        else:
            return render(request, 'user_profile.html', {'form': form})
