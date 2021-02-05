"""program URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from project.views import ClientAddView, ClientView, ContractAddView, ContractView, ClientContractAddView, \
    ClientListView, ContractDetails, Main, ClientContractView, ContactPersonAddView, ClientDebtorAddView, \
    ClientDebtorView, ClientDebtorCaseAddView, ClientDebtorCaseView, ClientDebtorCaseCashRegisterView, \
    ClientDebtorCashRegisterAddView, ClientDebtorCashRegisterView, \
    ClientCashRegisterView, ClientCaseView, DebtorListView, CaseListView, \
    CashRegisterListView, ClientLeadingPersonView, \
    LogoutView, AddUserView, LoginView, ClientLeadingPersonAdd

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.as_view()),
    path('add-client/', ClientAddView.as_view(), name='client-add'),
    path('client-list/', ClientListView.as_view()),
    path('debtor-list/', DebtorListView.as_view()),
    path('add-contract/', ContractAddView.as_view(), name='contract-add'),
    path('case-list/', CaseListView.as_view()),
    path('cashregister-list/', CashRegisterListView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('add-user/', AddUserView.as_view()),
    path('accounts/login/', LoginView.as_view()),
    path('login/', LoginView.as_view()),
    path('add-leading-person/', ClientLeadingPersonAdd.as_view()),
    path('leading-person-list', ClientLeadingPersonView.as_view()),
    path('client/<int:client_id>/', ClientView.as_view()),
    path('contract/<int:contract_id>/', ContractView.as_view()),
    path('client/<int:client_id>/add-contract', ClientContractAddView.as_view()),
    path('client/<int:client_id>/<int:contract_id>/', ContractDetails.as_view()),
    path('client/<int:client_id>/contract-list/', ClientContractView.as_view()),
    path('client/<int:client_id>/contact-person-add/', ContactPersonAddView.as_view()),
    path('client/<int:client_id>/add-debtor/', ClientDebtorAddView.as_view()),
    path('client/<int:client_id>/debtor-list', ClientDebtorView.as_view()),
    path('client/<int:client_id>/<int:debtor_id>/add-case', ClientDebtorCaseAddView.as_view()),
    path('client/<int:client_id>/<int:debtor_id>/case-list', ClientDebtorCaseView.as_view()),
    path('client/<int:client_id>/<int:debtor_id>/<int:case_id>/add-cashregister',
         ClientDebtorCashRegisterAddView.as_view()),
    path('client/<int:client_id>/<int:debtor_id>/<int:case_id>/cashregister-list',
         ClientDebtorCaseCashRegisterView.as_view()),
    path('client/<int:client_id>/<int:debtor_id>/cashregister-list', ClientDebtorCashRegisterView.as_view()),
    path('client/<int:client_id>/cashregister-list', ClientCashRegisterView.as_view()),
    path('client/<int:client_id>/case-list', ClientCaseView.as_view()),


]
