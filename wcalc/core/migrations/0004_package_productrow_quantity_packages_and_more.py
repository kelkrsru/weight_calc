# Generated by Django 5.1.1 on 2024-10-05 05:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_productrow_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('ACTIVE', models.BooleanField(default=True, verbose_name='Активность')),
                ('NAME', models.CharField(max_length=255, unique=True, verbose_name='Наименование')),
                ('WEIGHT', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Вес')),
                ('QUANTITY_JARS', models.PositiveIntegerField(verbose_name='Количество банок')),
                ('QUANTITY_ON_PALLET', models.PositiveIntegerField(verbose_name='Количество на паллете')),
                ('WEIGHT_BRUTTO', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Вес брутто паллета')),
            ],
            options={
                'verbose_name': 'Упаковка',
                'verbose_name_plural': 'Упаковки',
            },
        ),
        migrations.AddField(
            model_name='productrow',
            name='QUANTITY_PACKAGES',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество упаковок'),
        ),
        migrations.AddField(
            model_name='productrow',
            name='QUANTITY_PALLETS',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Количество паллет'),
        ),
        migrations.AddField(
            model_name='productrow',
            name='TONNAGE',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Тоннаж заказа'),
        ),
        migrations.AlterField(
            model_name='productrow',
            name='RESERVE_QUANTITY',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Количество в резерве'),
        ),
        migrations.AddField(
            model_name='productrow',
            name='PACKAGE',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='package_productrows', to='core.package', verbose_name='Упаковка'),
        ),
    ]
