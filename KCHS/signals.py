import decimal
import json
import requests

from django.db import transaction
from django.db.models import Sum

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.http import request

from .models import *

User = settings.AUTH_USER_MODEL


#
@receiver(post_save, sender=SemesterAssessment, dispatch_uid='save_student_coursework')
def calculate_student_semester_ca(sender, instance, created, raw=False, **kwargs):
    if created and instance.assessment_group.category == "CA":

        get_group_assessment_ca = GroupAssessment.objects.filter(group=instance.assessment_group.group,
                                                                 category="CA").count()
        count_assessment = SemesterAssessment.objects.filter(registration=instance.registration,
                                                             programme_course=instance.programme_course,
                                                             academic_semester=instance.academic_semester,
                                                             assessment_group__category="CA").count()
        # print(count_assessment)
        # print(get_group_assessment_ca)
        if get_group_assessment_ca == count_assessment:
            with transaction.atomic():
                cards = SemesterAssessment.objects.select_for_update().filter(
                    registration=instance.registration,
                    programme_course=instance.programme_course,
                    academic_semester=instance.academic_semester,
                    assessment_group__category="CA"
                ).order_by('-weight')
                if cards:

                    total_weight = 0

                    for mark in cards:
                        total_weight = total_weight + mark.weight

                    get_year_result = SemesterResult(
                        registration=instance.registration,
                        programme_course=instance.programme_course,
                        academic_semester=instance.academic_semester,
                        ca=decimal.Decimal(total_weight),
                        grade="-",
                        remark="-"
                    )
                    get_year_result.save()


@receiver(post_save, sender=SemesterAssessment, dispatch_uid='save_student_end_of_semester')
def calculate_student_semester_es(sender, instance, created, raw=False, **kwargs):
    # if created:

    get_group_assessment_ca = GroupAssessment.objects.filter(group=instance.assessment_group.group,
                                                             category="ES").count()
    count_assessment = SemesterAssessment.objects.filter(registration=instance.registration,
                                                         programme_course=instance.programme_course,
                                                         academic_semester=instance.academic_semester,
                                                         assessment_group__category="ES").count()
    print(count_assessment)
    print(get_group_assessment_ca)
    if get_group_assessment_ca == count_assessment:
        with transaction.atomic():
            cards = SemesterAssessment.objects.select_for_update().filter(
                registration=instance.registration,
                programme_course=instance.programme_course,
                academic_semester=instance.academic_semester,
                assessment_group__category="ES"
            ).order_by('-weight')
            if cards:

                total_weight = 0

                for mark in cards:
                    total_weight = total_weight + mark.weight
                    print(total_weight)

                get_year_result = SemesterResult.objects.filter(
                    registration=instance.registration,
                    programme_course=instance.programme_course,
                    academic_semester=instance.academic_semester

                ).first()
                get_year_result.es = decimal.Decimal(total_weight)
                get_year_result.save()
                print(get_year_result)


@receiver(post_save, sender=Student, dispatch_uid='create_registration_of_new_user')
def create_registration(sender, instance, created, **kwargs):
    if created:
        get_status = Status.objects.get(code="NOT PAID")
        get_semester = AcademicSemester.objects.filter(is_active=True).first()
        save_registration = Registration(student=instance, level=instance.entry_level, status=get_status,
                                         semester=get_semester)
        save_registration.save()

        URL = 'https://apisms.beem.africa/v1/send'
        api_key = '2799f1a807695012'
        secret_key = 'YTU2NTkxZjQxZDc4NTY2NGZiZTVkYzI5ZWU1MzFmYzM4NzA4MTBkYjk5NWE4MzZmZmU0MjQ2OTU3YjJjN2IxZg===='
        content_type = 'application/json'
        source_addr = 'KAHAMA COLL'
        apikey_and_apisecret = api_key + ':' + secret_key

        '''Get name and concatenate them'''
        first_name = instance.user.first_name
        last_name = instance.user.last_name
        full_name = f"{first_name} {last_name}"

        '''Get amount invested and daily amount earning'''
        program = instance.programme
        username = instance.user.username
        password = last_name

        '''Get phone detail and convert and user id as recipient_id on api'''
        # number= "255755422199"
        phone = str(instance.user.phone)
        # phone = str(number)
        phone = phone[1:10]
        # phone = phone
        phone = '255' + phone

        user_id = instance.id

        message_body = f"Congratulation,Dear {full_name}, \nyou have been selected to join KAHAMA COLLEGE OF HEALTH " \
                       f"SCIENCE to pursue {program}\n please login to our system through \n " \
                       f"https://kachs.herokuapp.com/login to proceed with  " \
                       f"registration\n username:{username},\n password:{password} "

        print(message_body)
        first_request = requests.post(url=URL, data=json.dumps({
            'source_addr': source_addr,
            'schedule_time': '',
            'encoding': '0',
            'message': message_body,
            'recipients': [
                {
                    'recipient_id': user_id,
                    'dest_addr': phone,
                },
            ],
        }),

                                      headers={
                                          'Content-Type': content_type,
                                          'Authorization': 'Basic ' + api_key + ':' + secret_key,
                                      },

                                      auth=(api_key, secret_key), verify=False)

        print(first_request.status_code)
        if first_request.status_code == 200:
            full_name = ''
            phone = ''
        print(first_request.json())

        # return (first_request.json())


@receiver(post_save, sender=FeeStructure, dispatch_uid='calculate_the_total_cost')
def find_total_payment_per_each_course_year(sender, instance, **kwargs):
    try:
        get_total_fee = FeeStructure.objects.filter(semester=instance.semester, level=instance.level,
                                                    programme=instance.programme, account=instance.account).aggregate(
            Sum('amount'))[
            'amount__sum']
        total_update = decimal.Decimal(get_total_fee)
        get_structure = PaymentStructure.objects.filter(semester=instance.semester, level=instance.level,
                                                        programme=instance.programme, account=instance.account).first()

        get_structure.amount = total_update
        get_structure.minimum = total_update * decimal.Decimal(0.5)
        get_structure.save()
    except:
        minimum = instance.amount * decimal.Decimal(0.5)
        save_payment = PaymentStructure(
            semester=instance.semester,
            level=instance.level,
            programme=instance.programme,
            account=instance.account,
            amount=instance.amount,
            minimum=minimum,
        )
        save_payment.save()


@receiver(post_save, sender=Payment, dispatch_uid='calculate_the_remaining_cost')
def remaining_cost(sender, instance, **kwargs):
    try:
        get_latest_balance = Payment.objects.filter(
            registration=instance.registration, account=instance.account, ).order_by(
            '-id')
        get_previous_balance = get_latest_balance[1]

        if get_previous_balance.due > 0:
            get_remaining = get_previous_balance.due - instance.amount
            Payment.objects.filter(id=instance.id).update(due=get_remaining)
            get_status = Status.objects.get(code="PARTIAL PAID")
            save_registration = Registration.objects.get(id=instance.registration.id)
            save_registration.status = get_status
            save_registration.save()
        else:
            complete_registration = Payment.objects.filter(
                registration=instance.registration, due__lte=0.00).order_by(
                '-id').count()
            if complete_registration == 0:
                get_status = Status.objects.get(code="FULL PAID")
                save_registration = Registration.objects.get(id=instance.registration.id)
                save_registration.status = get_status
                save_registration.save()

    except:
        get_payment_structure = PaymentStructure.objects.get(programme=instance.registration.student.programme,
                                                             level=instance.registration.student.entry_level,
                                                             account=instance.account,
                                                             semester=instance.registration.semester.semester)
        get_remaining = get_payment_structure.amount - instance.amount
        Payment.objects.filter(id=instance.id).update(due=get_remaining)
        get_status = Status.objects.get(code="PARTIAL PAID")
        save_registration = Registration.objects.get(id=instance.registration.id)
        save_registration.status = get_status
        save_registration.save()


@receiver(post_save, sender=Payment, dispatch_uid='check_status_change')
def check_full_payment(sender, instance, **kwargs):
    get_payment_structure = PaymentStructure.objects.filter(programme=instance.registration.student.programme,
                                                            level=instance.registration.student.entry_level,

                                                            semester=instance.registration.semester.semester).aggregate(
        Sum('amount'))['amount__sum'] or 0.00
    get_payment_structure2 = Payment.objects.filter(registration=instance.registration).aggregate(Sum('amount'))[
                                 'amount__sum'] or 0.00
    balance = get_payment_structure - get_payment_structure2
    try:

        get_latest_balance = PaymentSummary.objects.get(registration=instance.registration)
        get_latest_balance.amount = get_payment_structure2
        get_latest_balance.due = balance
        get_latest_balance.save()
    except:
        PaymentSummary.objects.create(registration=instance.registration, amount=get_payment_structure2, due=balance)

    if balance <= 0:
        get_status = Status.objects.get(code="FULL PAID")
        save_registration = Registration.objects.get(id=instance.registration.id)
        save_registration.status = get_status
        save_registration.save()

#
# @receiver(post_save, sender=Type, dispatch_uid='create_payment_structure')
# def create_payment_structure_total(sender, instance, created, **kwargs):
#     if created:
#         get_ordinary_level = Level.objects.get(name="O-Level")
#         get_advanced_level = Level.objects.get(name="A-Level")
#
#         PaymentStructure.objects.create(type=instance, level=get_ordinary_level)
#         PaymentStructure.objects.create(type=instance, level=get_advanced_level)

# @receiver(post_save, sender=Payment, dispatch_uid='update_balance')
# def update_remaining_fee_amount(sender, instance, created, **kwargs):
#     if created:
#         get_latest_balance = InvestmentTracking.objects.filter(
#             investment__account__code=instance.investment.account.invite).order_by(
#             '-id').first()
#         get_user = Investment.objects.filter(account__code=instance.investment.account.invite).order_by('-id').first()
#
#         # print(get_latest_balance.balance)
#
#         save_balance = InvestmentTracking(
#             investment=get_user,
#             total_referral=get_latest_balance.total_referral + decimal.Decimal(float(instance.amount)),
#             total_earning=get_latest_balance.total_earning,
#             total_withdraw=get_latest_balance.total_withdraw,
#
#             balance=get_latest_balance.balance + instance.amount
#         )
#         save_balance.save()
