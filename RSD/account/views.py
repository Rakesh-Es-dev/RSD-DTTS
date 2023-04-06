from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from .fetch import fetch
from .models import Region,City,Drugs,Supplier
from .tables import CityTable,DrugTable
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

def accept(request):
    client = fetch('68251993000010000','Modern@123','http://tandtwstest.sfda.gov.sa:8080/ws/DrugListService/DrugListService?wsdl')
    drugs = client.service.getDrugList('1')
    client =fetch('68251993000010000','Modern@123', 'http://tandtwstest.sfda.gov.sa:8080/ws/AcceptService/AcceptService?wsdl')
    for drug in drugs:
        accept = client.service.notifyAccept(drug)
        return render(request, 'account/acceptRequest.html',{'accept':accept})
def cities(request):
    client = fetch('68251993000010000','Modern@123','http://tandtwstest.sfda.gov.sa:8080/ws/CityListService/CityListService?wsdl')
    citylist=client.service.getCityList()
    for region in citylist:
        for city in region.CITYLIST.CITY:
            regions = Region.objects.update_or_create(region=region.REGIONNAME,regionId=region.REGIONID)
            getRegion=Region.objects.get(region=region.REGIONNAME)
            cities = City.objects.update_or_create(region=getRegion,city=city.CITYNAME,cityId=city.CITYID)
    table = CityTable(City.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('cities.{}'.format(export_format))
    return render(request,'account/cities.html',{'table':table})

def druglist(request):
    client = fetch('68251993000010000','Modern@123','http://tandtwstest.sfda.gov.sa:8080/ws/DrugListService/DrugListService?wsdl')
    drugs = client.service.getDrugList('1') 
    for drug in drugs:
        print(drug)
        Drug = Drugs.objects.update_or_create(gtin=drug.GTIN,name = drug.DRUGNAME,domain = drug.DOMAINID,legal = True if drug.LEGALSTATUS==1 else False,marketing = True if drug.MARKETINGSTATUS == 1 else False,importable = True if drug.ISIMPORTABLE == 1 else False,exportable = True if drug.ISEXPORTABLE == 1 else False,drugStatus = True if drug.DRUGSTATUS == 1 else False,genericName=drug.GENERICNAME,registrationNumber=drug.REGISTRATIONNUMBER,price = drug.PRICE,dosage = drug.DOSAGEFORM,packageSize = drug.PACKAGESIZE,packageType = drug.PACKAGETYPE,strength = drug.STRENGTHVALUE,unitStrength = drug.STRENGTHVALUEUNIT,volume = drug.VOLUME,volumeUnit = drug.UNITOFVOLUME)
        newDrug = Drugs.objects.get(gtin=drug.GTIN,name = drug.DRUGNAME,domain = drug.DOMAINID,legal = True if drug.LEGALSTATUS==1 else False,marketing = True if drug.MARKETINGSTATUS == 1 else False,importable = True if drug.ISIMPORTABLE == 1 else False,exportable = True if drug.ISEXPORTABLE == 1 else False,drugStatus = True if drug.DRUGSTATUS == 1 else False,genericName=drug.GENERICNAME,registrationNumber=drug.REGISTRATIONNUMBER,price = drug.PRICE,dosage = drug.DOSAGEFORM,packageSize = drug.PACKAGESIZE,packageType = drug.PACKAGETYPE,strength = drug.STRENGTHVALUE,unitStrength = drug.STRENGTHVALUEUNIT,volume = drug.VOLUME,volumeUnit = drug.UNITOFVOLUME)
        if(any(x is not None for x in drug.SUPPLIERLIST.SUPPLIER)):
            for supplier in drug.SUPPLIERLIST.SUPPLIER:
                newSupplier = Supplier.objects.update_or_create(gln=supplier.GLN,name=supplier.SUPPLIERNAME)
                supp = Supplier.objects.get(gln=supplier.GLN,name=supplier.SUPPLIERNAME);
                newDrug.suppliers.add(supp.id)
                newDrug.save()
    table = DrugTable(Drugs.objects.all())
    table.paginate(page = request.GET.get("page",1),per_page=10)
    export_format = request.GET.get('_export',None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format,table)
        return exporter.response('drugs.{}'.format(export_format))
    return render(request,'account/druglist.html',{'table':table})

