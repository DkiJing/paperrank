# Generated by Django 2.1.1 on 2018-12-26 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_auto_20181225_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='rankCache',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('paperid', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'author',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='citation',
            name='title',
        ),
    ]
