# Generated by Django 4.0 on 2022-07-23 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0002_task_accomplished_notification_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('User', 'User'), ('SuperUser', 'SuperUser')], max_length=50),
        ),
    ]
