# Generated by Django 2.1.2 on 2019-04-08 08:59

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gsite', '0026_auto_20190408_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
