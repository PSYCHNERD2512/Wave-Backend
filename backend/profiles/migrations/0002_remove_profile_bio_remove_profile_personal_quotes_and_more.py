# Generated by Django 5.0.2 on 2024-03-14 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='personal_quotes',
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(default='gender', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='password',
            field=models.CharField(default='pass', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(default='user', max_length=150, unique=True),
            preserve_default=False,
        ),
    ]
