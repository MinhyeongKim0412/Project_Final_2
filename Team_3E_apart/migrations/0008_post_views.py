# Generated by Django 5.1 on 2024-10-09 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Team_3E_apart', '0007_customuser_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
