# Generated by Django 5.0 on 2024-11-09 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xscjgl', '0004_alter_class_year_alter_exam_grade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_time',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentexamnumber',
            name='exam_room_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='studentexamnumber',
            name='seat_number',
            field=models.CharField(max_length=10),
        ),
    ]
