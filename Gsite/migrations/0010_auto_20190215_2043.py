# Generated by Django 2.1.2 on 2019-02-15 16:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Gsite', '0009_infoaboutrock_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumb',
            field=models.ImageField(blank=True, null=True, upload_to='post_image'),
        ),
    ]
