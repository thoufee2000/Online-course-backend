# Generated by Django 5.1.4 on 2024-12-09 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineCourse', '0011_alter_enrollmentlist_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='dateOfBirth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
