# Generated by Django 2.0.1 on 2018-07-22 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userinfor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=11)),
                ('password', models.CharField(max_length=11)),
                ('email', models.CharField(max_length=22)),
                ('phone_number', models.PositiveIntegerField()),
            ],
        ),
    ]
