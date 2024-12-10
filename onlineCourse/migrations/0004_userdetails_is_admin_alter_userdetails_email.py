# Generated by Django 5.1.4 on 2024-12-07 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineCourse', '0003_enrollmentlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
