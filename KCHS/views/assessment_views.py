import decimal

from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from ..models import *
from ..forms import *
from ..models import *

User = settings.AUTH_USER_MODEL

from django.contrib.auth.decorators import login_required


@login_required(login_url='/user-authentication/')


def tutor_course(request):
    get_workload = Workload.objects.filter(tutor=request.user)

    context = {
        'workload': get_workload,

    }
    return render(request, 'KCHS/academic/tutor_subject.html', context)


def tutor_course_assessment(request, assessment):
    get_course = get_object_or_404(Course, code=assessment)
    get_course_workload = Workload.objects.get(course__course=get_course)
    get_semester = AcademicSemester.objects.get(is_active=True)

    get_course_group = get_course_workload.course.group
    get_group_assessment_ca = GroupAssessment.objects.filter(group=get_course_group, category="CA")
    get_group_assessment_es = GroupAssessment.objects.filter(group=get_course_group, category="ES")

    upload_status = GroupAssessment.objects.filter(group=get_course_group, category="CA").exclude(
        id__in=SemesterAssessment.objects.filter(programme_course=get_course_workload.course,
                                                 academic_semester=get_semester).values('assessment_group__id'))

    get_course_status = SemesterResult.objects.filter(programme_course=get_course_workload.course,
                                                      academic_semester=get_semester)

    get_result = SemesterResult.objects.filter(
        programme_course__course=get_course,
        academic_semester=get_semester, )

    context = {
        'course': get_course_workload.course,
        'assessment': get_group_assessment_ca,
        'final': get_group_assessment_es,
        'semester': get_semester,
        'result': get_result,
        'upload_status': upload_status,
        'status': get_course_status,

    }
    return render(request, 'KCHS/academic/tutor_course_assessment.html', context)


def course_assessment_result(request, assessment, course):
    # get_user = User.objects.get(title="teacher", id=request.user.id)
    get_group_assessment = GroupAssessment.objects.get(id=assessment)
    get_semester = AcademicSemester.objects.get(is_active=True)

    get_course = ProgrammeCourseStructure.objects.get(course__code=course)
    get_results = SemesterAssessment.objects.filter(programme_course=get_course, assessment_group=get_group_assessment,
                                                    academic_semester=get_semester)
    get_course_status = SemesterResult.objects.filter(programme_course=get_course,
                                                      academic_semester=get_semester).count()

    context = {
        'result': get_results,
        'subject': get_course,
        'rank': get_group_assessment,

        'event': get_semester,
        'get_course_status': get_course_status,

    }
    return render(request, 'KCHS/academic/course_assessment_result.html', context)


def pie_chart(request):
    labels = []
    data = []

    queryset = SemesterAssessment.objects.order_by('-id')[:5]
    for city in queryset:
        labels.append(city.assessment_group.item)
        data.append(city.weight)

    return render(request, 'KCHS/finance/financial_year_income.html', {
        'labels': labels,
        'data': data,
    })
