import datetime

from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core import serializers
import json

from ..models import *


def programme_list(request):
    get_programme = Programme.objects.all()
    get_payment_structure = PaymentStructure.objects.all().values('level__year', 'level__name',
                                                                  'programme__id').distinct()
    context = {
        'programme': get_programme,
        'year': get_payment_structure
    }

    return render(request, 'KCHS/finance/program_list.html', context)


def programme_payment_structure(request, programme_name, level_name):
    get_programme = Programme.objects.get(name=programme_name)
    get_programme_level = get_object_or_404(Level, name=level_name)
    get_payment_structure = PaymentStructure.objects.filter(programme=get_programme, level=get_programme_level)
    get_crdb = BankAccount.objects.filter(bank="CRDB").first()
    get_nmb = BankAccount.objects.filter(bank="NMB").first()
    get_boa = BankAccount.objects.filter(bank="BOA").first()
    get_payment_semester_one = FeeStructure.objects.filter(programme=get_programme, semester__number="1",
                                                           level=get_programme_level)
    get_payment_semester_two = FeeStructure.objects.filter(programme=get_programme, semester__number="2",
                                                           level=get_programme_level)
    context = {
        'programme': get_programme,
        'sem1': get_payment_semester_one,
        'sem2': get_payment_semester_two,
        'nmb': get_nmb,
        'crdb': get_crdb,
        'boa': get_boa,
    }

    return render(request, 'KCHS/finance/payment_structure.html', context)


def financial_year_debt(request):
    today = datetime.datetime.now()
    get_semester = get_object_or_404(AcademicSemester, is_active=True)
    status = Status.objects.get(code="PARTIAL PAID")

    get_payment = Payment.objects.filter(registration__status=status).values(
        'registration').annotate(total=Sum('amount'))
    get_student = Registration.objects.filter(id__in=Payment.objects.filter(registration__status=status).values(
        'registration'), semester=get_semester)

    get_total_amount = PaymentStructure.objects.filter(semester=get_semester.semester).values('programme',
                                                                                              'level').annotate(
        total=Sum('amount'))

    context = {
        'payment': get_payment,
        'registration': get_student,
        'total': get_total_amount,

    }
    return render(request, 'KCHS/finance/financial_year_debt.html', context)


def semester_complete_payment_list(request):
    get_semester = get_object_or_404(AcademicSemester, is_active=True)
    status = Status.objects.get(code="FULL PAID")

    get_payment = Payment.objects.filter(registration__status=status).values(
        'registration').annotate(total=Sum('amount'))
    get_student = Registration.objects.filter(id__in=Payment.objects.filter(registration__status=status).values(
        'registration'), semester=get_semester)

    get_total_amount = PaymentStructure.objects.filter(semester=get_semester.semester).values('programme',
                                                                                              'level').annotate(
        total=Sum('amount'))

    context = {
        'payment': get_payment,
        'registration': get_student,
        'total': get_total_amount,

    }
    return render(request, 'KCHS/finance/semester_income.html', context)


def fee_payment_item(request):
    get_item = FeeItem.objects.all()
    # get_group = GroupAssessment.objects.all().values('group__id', 'group__description', 'group__name').distinct()
    # get_item = GroupAssessment.objects.all().order_by('category')

    context = {
        'item': get_item,

    }

    return render(request, 'KCHS/finance/fee_item.html', context)