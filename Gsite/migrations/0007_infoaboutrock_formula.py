# Generated by Django 2.1.2 on 2019-02-15 15:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Gsite', '0006_infoaboutrock_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='infoaboutrock',
            name='formula',
            field=models.TextField(null=True, verbose_name='Формула'),
        ),
    ]
