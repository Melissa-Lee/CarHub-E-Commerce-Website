# Generated by Django 5.0.6 on 2024-06-16 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_remove_car_images_car_image_review_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Hatchback', 'Hatchback'), ('Coupe', 'Coupe'), ('Convertible', 'Convertible')], default='Sedan', max_length=100),
        ),
    ]
