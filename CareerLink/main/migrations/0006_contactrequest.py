# Generated by Django 5.0.4 on 2024-05-03 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_candidate_specialization'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
