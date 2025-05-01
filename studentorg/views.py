from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import College, Organization, Student, Program, OrgMember
from studentorg.forms import (
    CollegeForm, OrganizationForm, StudentForm, ProgramForm, OrgMemberForm
)
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q, Count
from django.http import JsonResponse
from django.db import connection
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class BaseListView(ListView):
    paginate_by = 5
    search_fields = []
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": query})
            qs = qs.filter(q_objects)
        return qs


# Home Page View
@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"


# Chart View Template
class ChartView(TemplateView):
    template_name = 'chart.html'


# Chart Data Views
class BaseChartData:
    @staticmethod
    def get_json_response(query, params=None):
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
            rows = cursor.fetchall()
        result = {name: count for name, count in rows}
        return JsonResponse(result)


class OrgMemDoughnutChart(BaseChartData):
    @staticmethod
    def get(request):
        query = """
            SELECT o.name, COUNT(m.id) AS student_count
            FROM studentorg_orgmember m
            INNER JOIN studentorg_organization o ON m.organization_id = o.id
            GROUP BY o.name
        """
        return BaseChartData.get_json_response(query)


class StudentCountEveryCollege(BaseChartData):
    @staticmethod
    def get(request):
        college_student_counts = Student.objects.values(
            'program__college__college_name'
        ).annotate(student_count=Count('id'))
        result = {
            college['program__college__college_name']: college['student_count'] 
            for college in college_student_counts
        }
        return JsonResponse(result)


class RadarStudentCountEveryCollege(StudentCountEveryCollege):
    pass  # Same functionality as StudentCountEveryCollege


class ProgramPolarChart(BaseChartData):
    @staticmethod
    def get(request):
        query = """
            SELECT p.prog_name, COUNT(s.id) AS student_count
            FROM studentorg_program p
            INNER JOIN studentorg_student s ON p.id = s.program_id
            GROUP BY p.prog_name
        """
        return BaseChartData.get_json_response(query)


class HTMLLegendsChart:
    @staticmethod
    def get(request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT o.name, COUNT(m.id) AS student_count, 
                       STRFTIME('%m', m.date_joined) AS joined_month
                FROM studentorg_orgmember m
                INNER JOIN studentorg_organization o ON m.organization_id = o.id
                GROUP BY o.name, joined_month
            """)
            rows = cursor.fetchall()

        result = {}
        for org_name, count, joined_month in rows:
            if org_name not in result:
                result[org_name] = {'student_count': {}, 'total_students': 0}
            result[org_name]['student_count'][joined_month] = count
            result[org_name]['total_students'] += count

        return JsonResponse(result)


# College Views
class CollegeList(BaseListView):
    model = College
    context_object_name = 'colleges'
    template_name = 'college_list.html'
    search_fields = ['college_name', 'college_dean']


class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')


class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')


class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')


# Organization Views
class OrganizationList(BaseListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    search_fields = ['name', 'description', 'college__college_name']


class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')


class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')


class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')


# Student Views
class StudentList(BaseListView):
    model = Student
    context_object_name = 'student'
    template_name = 'student_list.html'
    search_fields = [
        'student_id', 'lastname', 'firstname', 
        'middlename', 'program__prog_name'
    ]


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student-list')


# Program Views
class ProgramList(BaseListView):
    model = Program
    context_object_name = 'program'
    template_name = 'prog_list.html'
    search_fields = ['prog_name', 'college__college_name']


class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'prog_add.html'
    success_url = reverse_lazy('prog-list')


class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'prog_edit.html'
    success_url = reverse_lazy('prog-list')


class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'prog_del.html'
    success_url = reverse_lazy('prog-list')


# OrgMember Views
class OrgMemberList(BaseListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'OrgMember_list.html'
    search_fields = [
        'student__firstname', 'student__lastname', 
        'organization__name', 'date_joined'
    ]


class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'OrgMember_add.html'
    success_url = reverse_lazy('orgmember-list')


class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'OrgMember_edit.html'
    success_url = reverse_lazy('orgmember-list')


class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'OrgMember_del.html'
    success_url = reverse_lazy('orgmember-list')


# URL-compatible view functions
def orgMemDoughnutChart(request):
    return OrgMemDoughnutChart.get(request)

def studentCountEveryCollege(request):
    return StudentCountEveryCollege.get(request)

def radarStudenCountEveryCollege(request):
    return RadarStudentCountEveryCollege.get(request)

def programPolarchart(request):
    return ProgramPolarChart.get(request)

def htmlLegendsChart(request):
    return HTMLLegendsChart.get(request)