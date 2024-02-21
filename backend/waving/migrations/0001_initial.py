# Generated by Django 5.0.2 on 2024-02-20 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wave_Send',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('from_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_wave', to='profiles.profile')),
                ('to_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_wave', to='profiles.profile')),
            ],
        ),
    ]
