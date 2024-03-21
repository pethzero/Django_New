# Generated by Django 5.0.1 on 2024-03-19 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_author_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='TbStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('score', models.IntegerField()),
                ('grade', models.CharField(max_length=1)),
                ('filename', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'students',
                'managed': False,
            },
        ),
    ]