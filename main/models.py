from django.db import models


class Company(models.Model):
    cik = models.CharField('CIK', max_length=50)
    ticker = models.CharField('Ticker Symbol', unique=True, max_length=50)
    name = models.CharField('Name', max_length=300)

    def __str__(self):
        return self.ticker


class ReportType(models.Model):
    report_type = models.CharField('Report Type', max_length=10)

    def __str__(self):
        return self.report_type


class AccnNumber(models.Model):
    accn = models.CharField('Accn Number', max_length=50)
    filed_date = models.DateField('Filed Date')
    cik = models.ForeignKey(Company, on_delete=models.CASCADE)
    report_type = models.ForeignKey(ReportType, on_delete=models.PROTECT)
    interactive_data = models.BooleanField(default=False)

    class Meta:
        unique_together = ('accn', 'cik')

    def __str__(self):
        return self.accn


class StatementFields(models.Model):
    STATEMENT_CHOICES = (
        ('BS', 'Balance Sheet'),
        ('I', 'Income'),
        ('CF', 'Cash Flow'),
    )
    HEADER_CHOICES = (
        ('CA', 'Current assets'),
        ('NCA', 'Non-current assets'),
        ('CL', 'Current liabilities'),
        ('NCL', 'Non-current liabilities'),
        ('SE', 'Stockholders\' equity'),

    )

    line_number = models.FloatField()
    statement_field = models.CharField(
        'Statement Field', unique=True, max_length=1000)
    readable_field = models.CharField('Readable Field', max_length=1000)
    header = models.CharField(
        'Header', max_length=1000, choices=HEADER_CHOICES, null=True, blank=True)
    statement = models.CharField(max_length=2, choices=STATEMENT_CHOICES)
    reverse = models.BooleanField(default=False)

    def __str__(self):
        return self.readable_field
