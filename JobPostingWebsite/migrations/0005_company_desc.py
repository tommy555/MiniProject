# Generated by Django 2.1.2 on 2018-11-22 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobPostingWebsite', '0004_auto_20181122_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='desc',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
