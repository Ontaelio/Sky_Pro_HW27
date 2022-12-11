# Generated by Django 4.1.3 on 2022-12-11 16:53

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(default="1979-10-10", validators=[authentication.models.check_birth_date]),
            preserve_default=False,
        ),
    ]
