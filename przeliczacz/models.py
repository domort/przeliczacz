from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    protein = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False, verbose_name='Protein')
    carbo = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False, verbose_name='Carbo')
    fat = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False, verbose_name='Fat')

    unit_weight = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False, verbose_name='Unit weight')
    name = models.CharField(blank=False, verbose_name='Name', max_length=100)
    description = models.TextField(blank=True, verbose_name='Description')

    ww = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, verbose_name='WW')
    wbt = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, verbose_name='WBT')
    cal = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, verbose_name='Calories')

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return '{} [{}, {}]'.format(self.name or "<Unnamed Item>", self.ww, self.wbt)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'carbo': self.carbo,
            'protein': self.protein,
            'fat': self.fat,
            'cal': self.cal,
            'unit_weight': self.unit_weight,
            'ww': self.ww,
            'wbt': self.wbt,
            'description': self.description
        }

    def to_json(self):
        dict = self.to_dict()
        return {str(k): unicode(v) for k, v in dict.items()}

    def calculate_units(self):
        self.ww = round(self.unit_weight * (self.carbo / 10) / 100, 2)
        self.wbt = round(self.unit_weight * ((4 * self.protein + 9 * self.fat) / 100) / 100, 2)

    def save(self, *args, **kwargs):
        none_fields = []
        if self.protein is None:
            none_fields.append('protein')
        if self.carbo is None:
            none_fields.append('carbo')
        if self.fat is None:
            none_fields.append('fat')

        if none_fields:
            raise Exception('{} not set!'.format(" and ".join(none_fields)))
        else:
            self.calculate_units()
        super(Product, self).save(*args, **kwargs)


class Meal(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, related_name="meal")
    ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    already_gave = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class MealElement(models.Model):
    meal = models.ManyToManyField(Meal, null=False, blank=False, related_name="meal_elements")
    product = models.OneToOneField(Product, null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=1)
    in_grams = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Product: {}, Amount: {}, In grams: {}'.format(self.product, self.amount, self.in_grams)

