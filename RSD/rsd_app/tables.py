import django_tables2 as tables
from .models import City,Drugs

class CityTable(tables.Table):
    class Meta:
        model = City
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('city','cityId','region')


class DrugTable(tables.Table):
    class Meta:
        model = Drugs
        template_name = "django_tables2/bootstrap5.html"
        fields = ('gtin','name',"registrationNumber",'genericName',"price","suppliers")

