from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from project.models import Client, Debtor, Case, Contract


def has_valid_checksum(value):
    multiple_table = (6, 5, 7, 2, 3, 4, 5, 6, 7)
    result = 0
    for i in range(len(multiple_table)):
        result += int(value[i]) * multiple_table[i]
    result %= 11
    if result != int(value[-1]):
        raise ValidationError('Podaj poprawny numer NIP!')


def length_of_post_code(value):
    """

    Weryfikacja kodu pocztowego
    """

    if len(value) > 5:
        raise ValidationError('Kod pocztowy jest za długi, wpisz go w formacie "XXXXX"')


def validate_login(login):

    """
    Sprawdzenie czy dany użytkownik już istnieje w bazie danych
    """
    if User.objects.filter(username=login):
        raise ValidationError('Taki login jest zajęty')


def length_of_phone_number(value):
    """
    Sprawdzenie długości numeru telefonu
    """
    if len(value) > 12:
        raise ValidationError('Numer telefonu jest za długi, długość powinna wynosić od 9 do 12 cyfr')
    elif len(value) < 9:
        raise ValidationError('Numer telefonu jest za krótki, długość powinna wynosić od 9 do 12 cyfr')


def validate_client(value):
    if Client.objects.filter(name=value):
        raise ValidationError('Podany klient już istnieje!')


def validate_debtor(value):
    if Debtor.objects.filter(name=value):
        raise ValidationError('Podany dłużnik już istnieje!')


def validate_case(value):
    if Case.objects.filter(case_number=value):
        raise ValidationError('Podana sprawa już istnieje!')


def validate_contract(value):
    if Contract.objects.filter(number=value):
        raise ValidationError('Podana umowa już istnieje!')


def validate_client_nip(value):
    if Client.objects.filter(nip=value):
        raise ValidationError('Klient o takim numerze NIP już istnieje!')
    if Debtor.objects.filter(nip=value):
        raise ValidationError('Podany NIP jest przypisany do dłużnika!')


def validate_debtor_nip(value):
    if Client.objects.filter(nip=value):
        raise ValidationError('Ten NIP jest już przypisany do innego podmiotu!')
    if Debtor.objects.filter(nip=value):
        raise ValidationError('Dłużnik o takim numerze NIP już istnieje!')


def validate_account_number(value):
    if len(value) < 24:
        raise ValidationError('Numer konta nie może być krótszy niż 24 cyfry')
