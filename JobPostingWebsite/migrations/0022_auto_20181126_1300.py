# Generated by Django 2.1.2 on 2018-11-26 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobPostingWebsite', '0021_auto_20181126_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='profile_image'),
        ),
    ]