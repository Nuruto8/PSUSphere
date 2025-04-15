from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import College, Organization, Student, Program, OrgMember
from studentorg.forms import (
    CollegeForm, OrganizationForm, StudentForm, ProgramForm, OrgMemberForm
)
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from fire.models import FireStation


@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"


# ✅ College Views
class CollegeList(ListView):
    model = College
    context_object_name = 'colleges'
    template_name = 'college_list.html'
    paginate_by = 5


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
class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'organization_list.html'
    paginate_by = 5

    def get_queryset(self, *args,  **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args,  **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))

        return qs


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
class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'student_list.html'
    paginate_by = 5


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
class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'prog_list.html'
    paginate_by = 5


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
class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'OrgMember_list.html'
    paginate_by = 5


class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'OrgMember_add.html'
    success_url = reverse_lazy('OrgMember-list')


class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'OrgMember_edit.html'
    success_url = reverse_lazy('OrgMember-list')


class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'OrgMember_del.html'
    success_url = reverse_lazy('OrgMember-list')

# Fire Station Views
@method_decorator(login_required, name='dispatch')
class FireStationList(ListView):
    model = FireStation
    context_object_name = 'firestations'
    template_name = 'firestation_list.html'
    paginate_by = 5

class FireStationCreateView(CreateView):
    model = FireStation
    fields = '__all__'  # Or create a FireStationForm if needed
    template_name = 'firestation_add.html'
    success_url = reverse_lazy('firestation-list')

class FireStationUpdateView(UpdateView):
    model = FireStation
    fields = '__all__'  # Or use FireStationForm
    template_name = 'firestation_edit.html'
    success_url = reverse_lazy('firestation-list')

class FireStationDeleteView(DeleteView):
    model = FireStation
    template_name = 'firestation_del.html'
    success_url = reverse_lazy('firestation-list')

# Map View
@method_decorator(login_required, name='dispatch')
def map_station(request):
    fireStations = FireStation.objects.values('name', 'latitude', 'longitude')
    
    # Convert string coordinates to float
    fireStations_list = []
    for fs in fireStations:
        fs_data = {
            'name': fs['name'],
            'latitude': float(fs['latitude']),
            'longitude': float(fs['longitude'])
        }
        fireStations_list.append(fs_data)
    
    context = {
        'fireStations': fireStations_list,
    }
    
    return render(request, 'map_station.html', context)