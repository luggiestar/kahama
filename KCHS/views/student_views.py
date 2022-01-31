import decimal

from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from ..models import *
from ..forms import *
from ..models import *

from django.contrib.auth.decorators import login_required


@login_required(login_url='/user-authentication/')
def student_semester_course(request):
    if not request.user.is_staff:

        get_semester = AcademicSemester.objects.filter(is_active=True).first()
        get_student = Registration.objects.filter(student__user=request.user, semester=get_semester).first()
        get_structure = ProgrammeCourseStructure.objects.filter(programme=get_student.student.programme,
                                                                semester=get_semester.semester, level=get_student.level)
        total_credit = ProgrammeCourseStructure.objects.filter(programme=get_student.student.programme,
                                                               semester=get_semester.semester,
                                                               level=get_student.level).aggregate(
            total=Sum('credit'))

        context = {

            'semester': get_semester,
            'registration': get_student,
            'structure': get_structure,
            'credit': total_credit,
        }

        return render(request, 'KCHS/student/student_course_semester.html', context)
    else:
        return redirect('KCHS:logout')


def student_semester_payment(request):
    if not request.user.is_staff:

        get_semester = AcademicSemester.objects.filter(is_active=True).first()
        get_student = Registration.objects.filter(student__user=request.user, semester=get_semester).first()
        get_payment = Payment.objects.filter(registration=get_student).order_by('account', '-id')
        get_direct_due = Payment.objects.filter(registration=get_student, account__bank="CRDB").order_by('-id').first()
        get_other_due = Payment.objects.filter(registration=get_student, account__bank="NMB").order_by('-id').first()
        try:

            get_debt = get_direct_due.due + get_other_due.due
        except:

            get_debt = ""

        context = {
            'semester': get_semester,
            'registration': get_student,
            'structure': get_payment,
            'due': get_debt,
        }

        return render(request, 'KCHS/student/student_semester_payment.html', context)
    else:
        return redirect('KCHS:logout')


def student_semester_result(request):
    if not request.user.is_staff:

        get_semester = AcademicSemester.objects.filter(is_active=True).first()
        get_student = Registration.objects.filter(student__user=request.user, semester=get_semester).first()
        get_result = SemesterResult.objects.filter(registration=get_student, academic_semester=get_semester).order_by(
            'academic_semester__semester', )
        # get_direct_due = Payment.objects.filter(registration=get_student,account__bank="CRDB").order_by('-id').first()
        # get_other_due = Payment.objects.filter(registration=get_student,account__bank="NMB").order_by('-id').first()
        # get_debt =get_direct_due.due + get_other_due.due
        # total_credit = ProgrammeCourseStructure.objects.filter(programme=get_student.student.programme,
        #                                                        semester=get_semester.semester,level=get_student.level).aggregate(
        #     total=Sum('credit'))

        context = {
            'registration': get_student,
            'result': get_result,
            # 'due': get_debt,
        }

        return render(request, 'KCHS/student/student_semester_exam_result.html', context)
    else:
        return redirect('KCHS:logout')


def student_programme_payment_structure(request):
    get_semester = AcademicSemester.objects.get(is_active=True)
    get_student = get_object_or_404(Registration, student__user=request.user)

    get_payment_structure = PaymentStructure.objects.filter(programme=get_student.student.programme,
                                                            level=get_student.level, semester=get_semester.semester)
    get_crdb = BankAccount.objects.filter(bank="CRDB").first()
    get_nmb = BankAccount.objects.filter(bank="NMB").first()
    get_boa = BankAccount.objects.filter(bank="BOA").first()
    get_payment_semester_one = FeeStructure.objects.filter(programme=get_student.student.programme,
                                                           semester__number="1",
                                                           level=get_student.level)
    get_payment_semester_two = FeeStructure.objects.filter(programme=get_student.student.programme,
                                                           semester__number="2",
                                                           level=get_student.level)
    context = {
        'semester': get_semester,
        'registration': get_student,
        'programme': get_student.student.programme,
        'structure': get_payment_structure,
        'sem1': get_payment_semester_one,
        'sem2': get_payment_semester_two,
        'nmb': get_nmb,
        'crdb': get_crdb,
        'boa': get_boa,
    }

    return render(request, 'KCHS/student/student_payment_structure.html', context)


def user_profile(request):
    try:
        get_student = get_object_or_404(Registration, student__user=request.user)
    except:
        get_student = request.user

    context = {
        'student': get_student,
    }

    return render(request, 'KCHS/student/user_profile.html', context)


#
# def programme_course_structure(request, programme_name, level_name):
#     get_programme = Programme.objects.get(name=programme_name)
#     get_programme_level = get_object_or_404(Level, name=level_name)
#
#     get_courses_semester_one = ProgrammeCourseStructure.objects.filter(programme=get_programme, semester__number="1",
#                                                                        level=get_programme_level)
#     get_courses_semester_two = ProgrammeCourseStructure.objects.filter(programme=get_programme, semester__number="2",
#                                                                        level=get_programme_level)
#     context = {
#         'programme': get_programme,
#         'level': get_programme_level,
#         'sem1': get_courses_semester_one,
#         'sem2': get_courses_semester_two,
#
#     }
#
#     return render(request, 'KCHS/academic/programme_course_structure.html', context)
#
#
# def course_assessment_group(request):
#     get_group = GroupAssessment.objects.all().values('group', 'group__description', 'group__name').distinct()
#     get_item = GroupAssessment.objects.all()
#     print(get_group)
#
#     context = {
#         'group': get_group,
#         'item': get_item
#     }
#
#     return render(request, 'KCHS/academic/group_list.html', context)
#
#
# def course_list(request):
#     get_course = ProgrammeCourseStructure.objects.all()
#     get_group = GroupAssessment.objects.all().values('group__id', 'group__description', 'group__name').distinct()
#     get_item = GroupAssessment.objects.all().order_by('category')
#
#     context = {
#         'course': get_course,
#         'group': get_group,
#         'item': get_item
#     }
#
#     return render(request, 'KCHS/academic/course_assessment_structure.html', context)
#
#
# def department_tutor_list(request):
#     get_tutors = User.objects.all()
#     # get_group = GroupAssessment.objects.all().values('group__id', 'group__description', 'group__name').distinct()
#     # get_item = GroupAssessment.objects.all().order_by('category')
#
#     context = {
#         'tutor': get_tutors,
#
#     }
#
#     return render(request, 'KCHS/academic/tutors_list.html', context)


def department_semester_student_list(request):
    get_student = Registration.objects.all()
    # get_group = GroupAssessment.objects.all().values('group__id', 'group__description', 'group__name').distinct()
    # get_item = GroupAssessment.objects.all().order_by('category')

    context = {
        'student': get_student,

    }

    return render(request, 'KCHS/academic/student_list.html', context)
