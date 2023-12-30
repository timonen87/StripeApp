# Generated by Django 3.2.10 on 2023-12-26 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_pay', '0002_auto_20231225_1040'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'default_related_name': 'order', 'verbose_name': 'Ордер', 'verbose_name_plural': 'Ордер'},
        ),
        migrations.AlterField(
            model_name='discount',
            name='amount',
            field=models.IntegerField(blank=True, verbose_name='Значение скидки'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='type',
            field=models.CharField(choices=[('percentage', 'В процентах'), ('fixed', 'Фикс')], default='percentage', max_length=32, verbose_name='Тип скидки'),
        ),
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('rub', 'Рубль'), ('usd', 'Доллар')], default='usd', max_length=5, verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.CharField(choices=[('rub', 'Рубль'), ('usd', 'Доллар')], default='usd', max_length=10, verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='stripe_pay.discount', verbose_name='Скидка'),
        ),
        migrations.AlterField(
            model_name='order',
            name='tax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='stripe_pay.tax', verbose_name='Налог'),
        ),
        migrations.AlterField(
            model_name='tax',
            name='percent',
            field=models.IntegerField(default=20),
        ),
    ]