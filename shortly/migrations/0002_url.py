# Generated by Django 4.2.7 on 2024-09-07 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortly', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.URLField(max_length=600)),
                ('short', models.CharField(max_length=100)),
            ],
        ),
    ]
