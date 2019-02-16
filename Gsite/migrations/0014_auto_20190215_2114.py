# Generated by Django 2.1.2 on 2019-02-15 17:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Gsite', '0013_auto_20190215_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infoaboutrock',
            name='Streak',
            field=models.CharField(choices=[('Белый', 'Белый'), ('Черный', 'Черный')], max_length=30, null=True,
                                   verbose_name='полоса, жилка'),
        ),
        migrations.AlterField(
            model_name='infoaboutrock',
            name='hardness',
            field=models.IntegerRangeField(null=True, verbose_name='Твердость'),
        ),
    ]
