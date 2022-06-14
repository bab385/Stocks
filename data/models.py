from django.db import models
from django.test import tag


class Sub(models.Model):
    AFS_CHOICES = (
        ('1-LAF', 'Large Accelerated'),
        ('2-ACC', 'Accelerated'),
        ('3-SRA', 'Smaller Reporting Accelerated'),
        ('4-NON', 'Non-Accelerated'),
        ('5-SML', 'Smaller Reporting Filer'),
    )

    FP_CHOICES = (
        ('FY', 'FY'),
        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4'),
        ('H1', 'H1'),
        ('H2', 'H2'),
        ('M9', 'M9'),
        ('T1', 'T1'),
        ('T2', 'T2'),
        ('T3', 'T3'),
        ('M8', 'M8'),
        ('CY', 'CY'),
    )

    adsh = models.CharField(max_length=20)
    cik = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=150)
    sic = models.PositiveSmallIntegerField(null=True, blank=True)
    countryba = models.CharField(max_length=2)
    stprba = models.CharField(max_length=2, null=True, blank=True)
    cityba = models.CharField(max_length=30)
    zipba = models.CharField(max_length=10, null=True, blank=True)
    bas1 = models.CharField(max_length=40, null=True, blank=True)
    bas2 = models.CharField(max_length=40, null=True, blank=True)
    baph = models.CharField(max_length=12, null=True, blank=True)
    countryma = models.CharField(max_length=2, null=True, blank=True)
    stprma = models.CharField(max_length=2, null=True, blank=True)
    cityma = models.CharField(max_length=30, null=True, blank=True)
    zipma = models.CharField(max_length=10, null=True, blank=True)
    mas1 = models.CharField(max_length=40, null=True, blank=True)
    mas2 = models.CharField(max_length=40, null=True, blank=True)
    countryinc = models.CharField(max_length=3)
    stprinc = models.CharField(max_length=2, null=True, blank=True)
    ein = models.PositiveSmallIntegerField(null=True, blank=True)
    former = models.CharField(max_length=150, null=True, blank=True)
    changed = models.CharField(max_length=8, null=True, blank=True)
    afs = models.CharField(max_length=5, null=True,
                           blank=True, choices=AFS_CHOICES)
    wksi = models.BooleanField(default=False)
    fye = models.CharField(max_length=4)
    form = models.CharField(max_length=10)
    period = models.CharField(max_length=8)
    fy = models.CharField(max_length=4)
    fp = models.CharField(max_length=2, choices=FP_CHOICES)
    filed = models.CharField(max_length=8)
    accepted = models.DateTimeField()
    prevrpt = models.BooleanField(default=False)
    detail = models.BooleanField(default=False)
    instance = models.CharField(max_length=32)
    nciks = models.PositiveSmallIntegerField()
    aciks = models.CharField(max_length=120, null=True, blank=True)


class Tag(model.Models):
    IORD_CHOICES = (
        ('I', 'Point in Time'),
        ('D', 'Duration'),
    )

    CRDR_CHOICES = (
        ('C', 'Credit'),
        ('D', 'Debit'),
    )

    tag = models.CharField(max_length=256, unique=True)
    version = models.CharField(max_length=20)
    custom = models.BooleanField(default=False)
    abstract = models.BooleanField(default=True)
    datatype = models.CharField(max_length=20, null=True, blank=True)
    iord = models.CharField(max_length=1, null=True,
                            blank=True, choices=IORD_CHOICES)
    crdr = models.CharField(max_length=1, null=True,
                            blank=True, choices=CRDR_CHOICES)
    tlabel = models.CharField(max_length=512, null=True, blank=True)
    doc = models.CharField(max_length=2048, null=True, blank=True)


class Num(model.Models):
    adsh = models.CharField(max_length=20)
    tag = models.CharField(max_length=256)
    version = models.CharField(max_length=20)
    coreg = models.PositiveIntegerField(null=True, blank=True)
    ddate = models.CharField(max_length=8)
    qtrs = models.PositiveSmallIntegerField()
    uom = models.CharField(max_length=20)
    value = models.FloatField()
    footnote = models.CharField(max_length=512, null=True, blank=True)


class Pre(model.Models):
    STMT_CHOICES = (
        ('BS', 'Balance Sheet'),
        ('IS', 'Income Statement'),
        ('CF', 'Cash Flow'),
        ('EQ', 'Equity'),
        ('CI', 'Comprehensive Income'),
        ('UN', 'Unclassified Statement'),
        ('CP', 'Cover Page'),
    )

    adsh = models.CharField(max_length=20)
    report = models.PositiveSmallIntegerField()
    line = models.PositiveSmallIntegerField()
    stmt = models.CharField(max_length=2, choices=STMT_CHOICES)
    inpth = models.BooleanField(default=False)
    rfile = models.CharField(max_length=1)
    tag = models.CharField(max_length=256)
    version = models.CharField(max_length=20)
    plabel = models.CharField(max_length=512)
