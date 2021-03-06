# Generated by Django 2.1.2 on 2019-02-15 16:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Gsite', '0007_infoaboutrock_formula'),
    ]

    operations = [
        migrations.AddField(
            model_name='infoaboutrock',
            name='Cleavage',
            field=models.CharField(max_length=50, null=True, verbose_name='Спайность'),
        ),
        migrations.AddField(
            model_name='infoaboutrock',
            name='CristalSystem',
            field=models.CharField(max_length=50, null=True, verbose_name='Кристаллография'),
        ),
        migrations.AddField(
            model_name='infoaboutrock',
            name='Fracture',
            field=models.CharField(max_length=50, null=True, verbose_name='Трещиноватость'),
        ),
        migrations.AddField(
            model_name='infoaboutrock',
            name='Lustre',
            field=models.CharField(max_length=50, null=True, verbose_name='Блеск'),
        ),
        migrations.AddField(
            model_name='infoaboutrock',
            name='SpecificGravity',
            field=models.IntegerRangeField(null=True, verbose_name='Удельный вес'),
        ),
        migrations.AlterField(
            model_name='infoaboutrock',
            name='color',
            field=models.CharField(max_length=50, null=True, verbose_name='Цвет'),
        ),
    ]
