# Generated by Django 5.0.4 on 2024-04-30 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_candidate'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='biography',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='candidate_images/'),
        ),
    ]
