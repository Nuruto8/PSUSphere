from django.contrib import admin
from django.urls import path

from studentorg.views import HomePageView, OrganizationList, OrganizationCreateView, OrganizationUpdateView, OraganizationDeleteView
from studentorg import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('organization_list', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<pk>', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<pk>/delete', OraganizationDeleteView.as_view(), name='organization-delete'),
]
