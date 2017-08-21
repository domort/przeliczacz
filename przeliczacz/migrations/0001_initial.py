# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ratio', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('already_gave', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MealElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(null=False, max_digits=10, decimal_places=2, default=1, blank=False)),
                ('in_grams', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('protein', models.DecimalField(verbose_name=b'Protein', max_digits=16, decimal_places=2)),
                ('carbo', models.DecimalField(verbose_name=b'Carbo', max_digits=16, decimal_places=2)),
                ('fat', models.DecimalField(verbose_name=b'Fat', max_digits=16, decimal_places=2)),
                ('unit_weight', models.DecimalField(verbose_name=b'Unit weight', max_digits=16, decimal_places=2)),
                ('name', models.CharField(max_length=100, verbose_name=b'Name')),
                ('description', models.TextField(verbose_name=b'Description', blank=True)),
                ('ww', models.DecimalField(null=True, verbose_name=b'WW', max_digits=16, decimal_places=2, blank=True)),
                ('wbt', models.DecimalField(null=True, verbose_name=b'WBT', max_digits=16, decimal_places=2, blank=True)),
                ('cal', models.DecimalField(null=True, verbose_name=b'Calories', max_digits=16, decimal_places=2, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mealelement',
            name='product',
            field=models.OneToOneField(to='przeliczacz.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meal',
            name='user',
            field=models.OneToOneField(related_name='meal', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mealelement',
            name='meal',
            field=models.ManyToManyField(related_name='meal_elements', to='przeliczacz.Meal'),
            preserve_default=True,
        ),
    ]