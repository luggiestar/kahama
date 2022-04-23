import decimal

from django.conf import settings
from django.contrib import messages
from django.db.models import Sum, Count, Case, When, IntegerField
from django.shortcuts import render, redirect, get_object_or_404

from ..models import *
from ..forms import *
from ..models import *

# User = settings.AUTH_USER_MODEL

from django.contrib.auth.decorators import login_required


@login_required(login_url='/user-authentication/')
def student_entry_list(request):
    get_registration = Registration.objects.all()
    # get_group = GroupAssessment.objects.all().values('group__id', 'group__description', 'group__name').distinct()
    # get_item = GroupAssessment.objects.all().order_by('category')

    context = {
        'registration': get_registration,

    }

    return render(request, 'KCHS/registration/student_entry.html', context)


def staff_entry_list(request):
    get_registration = User.objects.all().exclude(id__in=User.objects.filter(title="student").values('id'))
    # students=('staff','Accountant')
    # get_registration = User.objects.filter(title__in=students)
    # get_group = GroupAssessment.objects.all().values('group__id', 'group__description', 'group__name').distinct()
    # get_item = GroupAssessment.objects.all().order_by('category')

    context = {
        'registration': get_registration,

    }

    return render(request, 'KCHS/registration/staff_entry.html', context)


def start_registration(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "GET":
            try:
                username = request.GET.get('registration_number', False)
                get_account = Student.objects.filter(user__username=username).first()

                return redirect('KCHS:register_phase_one', username=get_account.user)
            except:
                pass

        return render(request, 'KCHS/registration/registration_home.html')
    else:
        return redirect('KCHS:logout')


def register_phase_one(request, username):
    get_account = get_object_or_404(Student, user__username=username)
    get_semester = get_object_or_404(AcademicSemester, is_active=True)
    get_crdb = BankAccount.objects.filter(bank="CRDB").first()
    get_nmb = BankAccount.objects.filter(bank="NMB").first()
    get_boa = BankAccount.objects.filter(bank="BOA").first()
    # try:
    # get_amount = Payment.objects.filter(registration=get_account).aggregate(total=Sum('amount'))
    get_direct_payment_amount = PaymentStructure.objects.get(programme=get_account.programme,
                                                             level=get_account.entry_level, account=get_crdb,
                                                             semester=get_semester.semester)
    get_development_payment_amount = PaymentStructure.objects.get(programme=get_account.programme,
                                                                  level=get_account.entry_level, account=get_nmb,
                                                                  semester=get_semester.semester)

    get_direct_due = Payment.objects.filter(registration__student=get_account, account=get_crdb).order_by(
        '-id').first()
    get_development_due = Payment.objects.filter(registration__student=get_account, account=get_nmb).order_by(
        '-id').first()
    # except:
    #     get_development_due = None
    #     get_direct_payment_amount = None
    #     get_development_payment_amount = None
    #     get_direct_due = None

    context = {
        'get_account': get_account,
        'direct': get_direct_payment_amount,
        'development': get_development_payment_amount,
        'get_direct_due': get_direct_due,
        'get_development_due': get_development_due,
    }
    return render(request, 'KCHS/registration/semester_registration_phase_one.html', context)


def save_student_payments(request):
    if request.method == "POST":
        # try:
        get_id = request.POST['id']
        direct = request.POST['direct']
        development = request.POST['development']
        get_status = Status.objects.get(code="NOT PAID")
        get_account = Student.objects.get(user__username=get_id)
        get_semester = get_object_or_404(AcademicSemester, is_active=True)
        get_crdb = BankAccount.objects.filter(bank="CRDB").first()
        get_nmb = BankAccount.objects.filter(bank="NMB").first()
        if direct and development:

            try:
                register_student = Registration(
                    student=get_account,
                    level=get_account.entry_level,
                    semester=get_semester,
                    registerer=request.user,
                    status=get_status,
                    is_active=True,

                )
                register_student.save()
                get_registration = Registration.objects.filter(student=get_account).order_by('-id').first()
                if decimal.Decimal(direct) >= 1:
                    save_direct = Payment.objects.create(registration=get_registration, account=get_crdb,
                                                         amount=decimal.Decimal(direct), created_by=request.user)
                if decimal.Decimal(development) >= 1:
                    save_development = Payment.objects.create(registration=get_registration, account=get_nmb,
                                                              amount=decimal.Decimal(development),
                                                              created_by=request.user)
            except:

                get_registration = Registration.objects.filter(student=get_account).order_by('-id').first()
                if decimal.Decimal(direct) >= 1:
                    save_direct = Payment.objects.create(registration=get_registration, account=get_crdb,
                                                         amount=decimal.Decimal(direct), created_by=request.user)
                if decimal.Decimal(development) >= 1:
                    save_development = Payment.objects.create(registration=get_registration, account=get_nmb,
                                                              amount=decimal.Decimal(development),
                                                              created_by=request.user)
        elif direct:
            get_registration = Registration.objects.filter(student=get_account).order_by('-id').first()
            if decimal.Decimal(direct) >= 1:
                save_direct = Payment.objects.create(registration=get_registration, account=get_crdb,
                                                     amount=decimal.Decimal(direct), created_by=request.user)
        elif development:

            get_registration = Registration.objects.filter(student=get_account).order_by('-id').first()
            if decimal.Decimal(development) >= 1:
                save_development = Payment.objects.create(registration=get_registration, account=get_nmb,
                                                          amount=decimal.Decimal(development), created_by=request.user)

        messages.success(request, f"Payment Added Successfully")
        return redirect('KCHS:register_phase_one', username=get_account.user)

        # except:
        #     return redirect('SRS:registration_home')
    #     messages.error(request, f"Failed, Invalid Entry")


def registration_phase_two(request):
    if request.method == "GET":
        try:
            username = request.GET.get('admission', False)
            # get_student = Registration.objects.filter(student__user__username=username).first()
            get_registration = Registration.objects.filter(student__user__username=username).order_by('-id').first()
            get_crdb = BankAccount.objects.filter(bank="CRDB").first()
            get_nmb = BankAccount.objects.filter(bank="NMB").first()
            get_total = Payment.objects.filter(registration=get_registration).aggregate(total=Sum('amount'))

            get_payment_exam = Payment.objects.filter(registration=get_registration, account=get_crdb).aggregate(
                total=Sum('amount'))
            get_due_exam = Payment.objects.filter(registration=get_registration, account=get_crdb).order_by(
                '-id').first()
            get_payment_other = Payment.objects.filter(registration=get_registration, account=get_nmb).aggregate(
                total=Sum('amount'))
            get_due_other = Payment.objects.filter(registration=get_registration, account=get_nmb).order_by(
                '-id').first()

            form = RegistrationForm(request.POST)

            context = {
                'form': form,
                'payment_exam': get_payment_exam,
                'due_exam': get_due_exam,
                'payment_other': get_payment_other,
                'due_other': get_due_other,
                'student': get_registration.student,
                'get_total': get_total,
                'get_registration': get_registration,
            }

            return render(request, 'KCHS/registration/semester_registration_complete.html', context)

        except:
            return render(request, 'KCHS/registration/semester_registration_complete.html')


def complete_student_registration(request, student):
    get_student = Student.objects.get(user__username=student)

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save(commit=False)

            save_registration = Student.objects.get(user__username=student)
            save_registration.parent_phone = form.cleaned_data['parent_phone']
            # save_registration.school = form.cleaned_data['school']
            save_registration.dob = form.cleaned_data['dob']
            save_registration.residency = form.cleaned_data['residency']
            save_registration.save()
            if save_registration:
                update_registration = Registration.objects.filter(student=get_student).order_by('-id').first()
                update_registration.is_registered = True
                # update_registration.created_by = request.user
                update_registration.save()
                messages.success(request, f"Student is registered Successfully")
                return redirect('KCHS:registration_phase_two')

        else:
            messages.error(request, f"Failed, Something went wrong")

            return redirect('KCHS:registration_phase_two')


def registration_report(request):
    get_semester = get_object_or_404(AcademicSemester, is_active=True)
    get_student_paid_full = Registration.objects.filter(semester=get_semester,status__code="FULL PAID").values('level__name','student__programme__name', 'status').annotate(
        total=Count('status')).order_by('student__programme__name','level__name')
    get_student_paid_partial = Registration.objects.filter(semester=get_semester, status__code="PARTIAL PAID").values('level__name','student__programme__name', 'status').annotate(
        total=Count('status')).order_by('student__programme__name','level__name')
    get_student_not_paid = Registration.objects.filter(semester=get_semester,status__code="NOT PAID").values('level__name','student__programme__name', 'status').annotate(
        total=Count('status')).order_by('student__programme__name','level__name')
    get_programme = Registration.objects.filter(semester=get_semester).values('level__name', 'student__programme__name').distinct()
    get_total_full_paid = Registration.objects.filter(semester=get_semester,status__code="FULL PAID").aggregate(
        Count('status'))['status__count'] or 0.00
    get_total_partial_paid = Registration.objects.filter(semester=get_semester,status__code="PARTIAL PAID").aggregate(
        Count('status'))['status__count'] or 0.00
    get_total_unpaid = Registration.objects.filter(semester=get_semester, status__code="NOT PAID").aggregate(
        Count('status'))['status__count'] or 0.00


    # get_item = GroupAssessment.objects.all().order_by('category')

    context = {
        'semester': get_semester,
        'full': get_student_paid_full,
        'partial': get_student_paid_partial,
        'unpaid': get_student_not_paid,
        'programme': get_programme,
        'total': get_total_full_paid,
        'due': get_total_partial_paid,
        'total_unpaid': get_total_unpaid,

    }

    return render(request, 'KCHS/registration/registration_report.html', context)
