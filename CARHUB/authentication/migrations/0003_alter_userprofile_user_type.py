# Generated by Django 5.0.6 on 2024-06-16 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_userprofile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('dealer', 'Dealer'), ('customer', 'Customer')], max_length=10),
        ),
    ]
