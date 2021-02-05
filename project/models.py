from django.db import models

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    post_code = models.IntegerField()
    city = models.CharField(max_length=64)
    nip = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Contract(models.Model):
    number = models.CharField(max_length=255, unique=True)
    date_from = models.DateField()
    date_to = models.DateField()
    corespondent_cost = models.BooleanField()
    law_cost = models.BooleanField()
    zaliczka = models.BooleanField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class ContactPerson(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=12, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Debtor(models.Model):
    name = models.CharField(max_length=64, unique=True)
    nip = models.CharField(max_length=10, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Case(models.Model):
    case_number = models.CharField(max_length=64, unique=True)
    case_description = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE)

    def __str__(self):
        return self.case_number



DOCUMENT = (
    (1, "fatura"),
    (2, "nota księgowa")
)

RODZAJ = (
    (1, "WYDATEK"),
    (2, "WPŁYW")
)


class CashRegister(models.Model):
    id_case = models.ForeignKey(Case, on_delete=models.CASCADE)
    id_debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    addressee = models.CharField(max_length=64)
    account_number = models.CharField(max_length=26)
    transfer_title = models.CharField(max_length=64)
    value = models.FloatField()
    document = models.IntegerField(choices=DOCUMENT)
    rodzaj_rozliczenia = models.IntegerField(choices=RODZAJ, null=True)


class LeadingPerson(models.Model):
    name = models.CharField(max_length=64)
    client = models.ManyToManyField(Client, through="LeadingPersonClient")

    def __str__(self):
        return self.name


class LeadingPersonClient(models.Model):
    name = models.ForeignKey(LeadingPerson, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name













