from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from .fetch import fetch
from .models import Region,City
from .tables import CityTable
from django_tables2.export.export import TableExport
# Create your views here.
class Signup(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name =  'account/signup.html'

class Profile(LoginRequiredMixin,generic.TemplateView):
    login_url = '/login/'
    template_name = "account/index.html"

class UserUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = get_user_model()
    success_url=reverse_lazy('profile')
    fields=['username','email']
    template_name = "account/user_update_form.html"

def druglist(request):
    client = fetch('68251993000010000','Modern@123','http://tandtwstest.sfda.gov.sa:8080/ws/DrugListService/DrugListService?wsdl')
    drugs = client.service.getDrugList('1')
    return render(request,'account/druglist.html',{'drugs':drugs})
def accept(request):
    client = fetch('68251993000010000','Modern@123','http://tandtwstest.sfda.gov.sa:8080/ws/DrugListService/DrugListService?wsdl')
    drugs = client.service.getDrugList('1')
    client =fetch('68251993000010000','Modern@123', 'http://tandtwstest.sfda.gov.sa:8080/ws/AcceptService/AcceptService?wsdl')
    for drug in drugs:
        accept = client.service.notifyAccept(drug)
        return render(request, 'account/acceptRequest.html',{'accept':accept})
def cities(request):
    client = fetch('68251993000010000','Modern@123','http://tandtwstest.sfda.gov.sa:8080/ws/CityListService/CityListService?wsdl')
    citylist=client.service.getCityList();
    for region in citylist:
        regions = Region.objects.get_or_create(region=region.REGIONNAME,regionId=region.REGIONID)
        for city in region.CITYLIST.CITY:
            cities = City.objects.get_or_create(regions,city=city.CITYNAME,cityId=city.CITYID)
    table = CityTable(City.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('cities.{}'.format(export_format))
    return render(request,'account/cities.html',{'table':table})


