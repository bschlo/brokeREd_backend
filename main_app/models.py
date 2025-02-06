from django.db import models
from django.utils import timezone

DEALTYPES = (
    ('Acquisition', 'Acquisition'),
    ('Condo Inventory', 'Condo Inventory'),
    ('Construction', 'Construction'),
    ('Covered Land', 'Covered Land'),
    ('Office to Condo Conversion', 'Office to Condo Conversion'),
    ('Office to Multifamily Conversion', 'Office to Multifamily Conversion'),
    ('Refinance', 'Refinance'),
    ('TCO', 'TCO'),
)

ASSETCLASSES = (
    ("Condo", "Condo"),
    ("Hospitality", "Hospitality"),
    ("Industrial", "Industrial"),
    ("Land", "Land"),
    ("Mixed-Use", "Mixed-Use"),
    ("Multifamily", "Multifamily"),
    ("Office", "Office"),
    ("Retail", "Retail"),
)

RATETYPES = (
    ('Fixed', 'Fixed'),
    ('Floating Rate (1-YR Treasury)', 'Floating Rate (1-YR Treasury)'),
    ('Floating Rate (10-YR Treasury)', 'Floating Rate (10-YR Treasury)'),
    ('Floating Rate (5-YR Treasury)', 'Floating Rate (5-YR Treasury)'),
    ('Floating Rate (LIBOR)', 'Floating Rate (LIBOR)'),
    ('Floating Rate (SOFR)', 'Floating Rate (SOFR)'),
    ('Other', 'Other'),
)

class Developer(models.Model):
    name = models.CharField(max_length=50)
    def _str__(self):
        return self.name


class Deal(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, default='Your default address')
    stories = models.PositiveIntegerField(default=1)
    square_feet = models.PositiveIntegerField(default=1)
    rate_type = models.CharField(
        max_length=100,
        choices=RATETYPES,
        default=RATETYPES[0][0]
    )
    minimum_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    maximum_rate= models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    developer = models.ManyToManyField(Developer)
    loan_amount = models.PositiveIntegerField()
    deal_type = models.CharField(
        max_length=100,
        choices=DEALTYPES,
        default=DEALTYPES[0][0]
        )
    asset_class = models.CharField(
        max_length=100,
        choices=ASSETCLASSES,
        default=ASSETCLASSES[0][0]
    )
    image_url = models.URLField(default='default url')
    description = models.TextField(default='default description')
    date = models.DateField()
    time = models.TimeField()
    
    def __str__(self):
        return self.name
    