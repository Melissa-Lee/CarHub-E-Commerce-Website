# Generated by Django 5.0.6 on 2024-06-16 00:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_userprofile_user_type'),
        ('cars', '0002_category_car_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='images',
        ),
        migrations.AddField(
            model_name='car',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='car_images/'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='cars.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='authentication.userprofile')),
            ],
        ),
    ]