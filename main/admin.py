from django.contrib import admin
from .models import Company, ReportType, AccnNumber, StatementFields

admin.site.register(Company)
admin.site.register(ReportType)
admin.site.register(AccnNumber)
admin.site.register(StatementFields)
