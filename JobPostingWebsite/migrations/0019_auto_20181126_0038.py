# Generated by Django 2.1.2 on 2018-11-25 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobPostingWebsite', '0018_auto_20181126_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='img',
            field=models.ImageField(blank=True, default='static/img/logo.jpg', null=True, upload_to='profile_image'),
        ),
    ]
