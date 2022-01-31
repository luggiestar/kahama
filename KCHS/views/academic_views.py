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
def workload_setting(request):
    if request.user.is_staff or request.user.is_superuser:
        get_workload = Workload.objects.all()
        total = Workload.objects.all().count()

        context = {
            'workload': get_workload,
            'total': total,
        }

        return render(request, 'KCHS/academic/teaching_workload.html', context)
    else:
        return redirect('KCHS:logout')


def programme_available(request):
    get_programme = Programme.objects.all()
    get_programme_structure = ProgrammeCourseStructure.objects.all().values('level', 'level__name', 'level__year',
                                                                            'programme__id').order_by(
        'level__name').distinct()
    context = {
        'programme': get_programme,
        'year': get_programme_structure
    }

    return render(request, 'KCHS/academic/program_available.html', context)


def programme_course_structure(request, programme_name, level_name):
    get_programme = Programme.objects.get(name=programme_name)
    get_programme_level = get_object_or_404(Level, name=level_name)

    get_courses_semester_one = ProgrammeCourseStructure.objects.filter(programme=get_programme, semester__number="1",
                                                                       level=get_programme_level)
    get_courses_semester_two = ProgrammeCourseStructure.objects.filter(programme=get_programme, semester__number="2",
                                                                       level=get_programme_level)
    context = {
        'programme': get_programme,
        'level': get_programme_level,
        'sem1': get_courses_semester_one,
        'sem2': get_courses_semester_two,

    }

    return render(request, 'KCHS/academic/programme_course_structure.html', context)


def course_assessment_group(request):
    get_group = GroupAssessment.objects.all().values('group', 'group__description', 'group__name').distinct()
    get_item = GroupAssessment.objects.all()
    print(get_group)

    context = {
        'group': get_group,
        'item': get_item
    }

    return render(request, 'KCHS/academic/group_list.html', context)


def course_list(request):
    get_course = ProgrammeCourseStructure.objects.all()
    get_group = GroupAssessment.objects.all().values('group__id', 'group__description', 'group__name').distinct()
    get_item = GroupAssessment.objects.all().order_by('category')

    context = {
        'course': get_course,
        'group': get_group,
        'item': get_item
    }

    return render(request, 'KCHS/academic/course_assessment_structure.html', context)


def department_tutor_list(request):
    get_tutors = User.objects.all()
    # get_group = GroupAssessment.objects.all().values('group__id', 'group__description', 'group__name').distinct()
    # get_item = GroupAssessment.objects.all().order_by('category')

    context = {
        'tutor': get_tutors,

    }

    return render(request, 'KCHS/academic/tutors_list.html', context)


def department_semester_student_list(request):
    get_student = Registration.objects.all()
    # get_group = GroupAssessment.objects.all().values('group__id', 'group__description', 'group__name').distinct()
    # get_item = GroupAssessment.objects.all().order_by('category')

    context = {
        'student': get_student,

    }

    return render(request, 'KCHS/academic/student_list.html', context)


