import django.forms as forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from .models import Client, DOCUMENT, RODZAJ
from .validators import has_valid_checksum, length_of_post_code, validate_login, length_of_phone_number, \
    validate_client, validate_debtor, validate_case, validate_contract, validate_client_nip, validate_debtor_nip, \
    validate_account_number


class ClientAddForm(forms.Form):

    """ Formularz nowego klienta """

    name = forms.CharField(label="Nazwa Klienta", validators=[validate_client])
    address = forms.CharField(label="Ulica i numer budynku")
    post_code = forms.CharField(label="Kod pocztowy (Wpisz kod w formacie XXXXX, bez dodatkowych znaków)",
                                validators=[length_of_post_code])
    city = forms.CharField(label="Miasto")
    nip = forms.CharField(label="NIP", validators=[has_valid_checksum, validate_client_nip])


class ContractAddForm(forms.Form):

    """
    Formularz nowej umowy
    """

    number = forms.CharField(label="Oznaczenie umowy", validators=[validate_contract])
    date_from = forms.DateField(widget=forms.SelectDateWidget, label="Data początku umowy")
    date_to = forms.DateField(widget=forms.SelectDateWidget, label="Data końca umowy")
    corespondent_cost = forms.BooleanField(widget=forms.CheckboxInput, required=False,
                                           label="Klient pokrywa koszty korespondencji?")
    law_cost = forms.BooleanField(widget=forms.CheckboxInput, required=False, label="Klient pokrywa koszty prawne?")
    zaliczka = forms.BooleanField(widget=forms.CheckboxInput, required=False, label="Klient zaliczkowy")
    client = forms.ModelChoiceField(queryset=Client.objects.all(), label="Klient")

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        if date_from > date_to:
            raise forms.ValidationError('Data początku umowy musi być wcześniejsza niż data jej zakończenia')


class ClientContractAddForm(forms.Form):

    number = forms.CharField(label="Oznaczenie umowy", validators=[validate_contract])
    date_from = forms.DateField(widget=forms.SelectDateWidget, label="Data początku umowy")
    date_to = forms.DateField(widget=forms.SelectDateWidget, label="Data końca umowy")
    corespondent_cost = forms.BooleanField(widget=forms.CheckboxInput, required=False,
                                           label="Klient pokrywa koszty korespondencji?")
    law_cost = forms.BooleanField(widget=forms.CheckboxInput, required=False, label="Klient pokrywa koszty prawne?")
    zaliczka = forms.BooleanField(widget=forms.CheckboxInput, required=False, label="Klient zaliczkowy")

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        if date_from > date_to:
            raise forms.ValidationError('Data początku umowy musi być wcześniejsza niż data jej zakończenia')


class ContactPersonAddForm(forms.Form):

    """ Formularz nowej osoby kontaktowej"""

    surname = forms.CharField(label="Imię i nazwisko")
    email = forms.CharField(widget=forms.EmailInput, label="email", validators=[EmailValidator()])
    phone_number = forms.CharField(label="numer telefonu (od 9 do 12 cyfr)", validators=[length_of_phone_number])


class DebtorAddForm(forms.Form):

    """ Formularz nowego dłuznika """

    name = forms.CharField(label="nazwa", validators=[validate_debtor])
    nip = forms.CharField(label="NIP", validators=[has_valid_checksum, validate_debtor_nip])


class CaseAddForm(forms.Form):

    """Formularz nowej sprawy """

    case_number = forms.CharField(label="Numer sprawy", validators=[validate_case])
    case_description = forms.CharField(label="Opis sprawy")


class ClientDebtorCaseCashRegisterAddForm(forms.Form):

    """Formularz nowego rozliczenia dla klienta jego dłużnika i jego danej sprawy"""

    addressee = forms.CharField(label="adresat")
    account_number = forms.CharField(label="numer konta", validators=[validate_account_number])
    transfer_title = forms.CharField(label="tytuł przelewu")
    value = forms.FloatField(label="wartość")
    document = forms.ChoiceField(label="Rodzaj dokumentu", choices=DOCUMENT)
    rodzaj_rozliczenia = forms.ChoiceField(label="rodzaj rozliczenia", choices=RODZAJ)


class LeadingPersonAddForm(forms.Form):

    """Formualrz nowych opiekunów Klienta"""

    name = forms.CharField(label="Imię i nazwisko")
    client = forms.ModelMultipleChoiceField(queryset=Client.objects.all(),
                                            label="Klient", widget=forms.CheckboxSelectMultiple)


class LoginForm(forms.Form):

    """Formularz logowania"""

    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddUserForm(forms.Form):

    """Formularz dodawania nowego uzytkownika"""

    login = forms.CharField(label='Nazwa użytkownika', validators=[validate_login])
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    passwordTwo = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    email = forms.CharField(label='Email', validators=[EmailValidator()])

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['passwordTwo']:
            raise ValidationError('Wpisane hasła nie są takie same.')
        return cleaned_data
