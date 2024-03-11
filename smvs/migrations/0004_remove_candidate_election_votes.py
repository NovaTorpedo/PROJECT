# Generated by Django 4.2.1 on 2024-02-22 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smvs', '0003_candidate_profile_picture_election_candidates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='election',
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smvs.candidate')),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smvs.election')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
