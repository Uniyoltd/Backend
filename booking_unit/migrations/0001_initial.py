# Generated by Django 4.1.7 on 2023-04-09 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_at', models.DateTimeField(auto_now=True)),
                ('delivery_at', models.DateTimeField(null=True)),
                ('duration_in_hours', models.FloatField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('transport_per_km', models.DecimalField(decimal_places=2, max_digits=8)),
                ('address', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('S', 'Paid'), ('C', 'Completed')], default='P', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(null=True, upload_to='business/images')),
                ('status', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.TextField()),
                ('image', models.ImageField(null=True, upload_to='request/images')),
                ('video', models.FileField(null=True, upload_to='request/videos')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('delivery_at', models.DateTimeField(null=True)),
                ('duration_in_hours', models.FloatField(null=True)),
                ('status', models.CharField(choices=[('O', 'Open'), ('C', 'Closed')], default='O', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('transport_per_km', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('availability', models.CharField(max_length=255)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='booking_unit.business')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='services/videos')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='booking_unit.service')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='services/images')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='booking_unit.service')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='booking_unit.service')),
            ],
        ),
    ]
