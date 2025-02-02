# Generated by Django 5.1.4 on 2024-12-23 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('full-time', 'Full-Time'), ('part-time', 'Part-Time')], max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
                ('salary', models.CharField(max_length=50)),
                ('companyname', models.CharField(max_length=50)),
                ('companydescription', models.TextField(max_length=1000)),
                ('company_contactemail', models.EmailField(max_length=254)),
                ('company_contactphone', models.CharField(max_length=20)),
            ],
        ),
    ]
