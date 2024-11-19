# Generated by Django 5.0 on 2024-10-20 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('class_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('subject_group', models.CharField(default='全科', max_length=20)),
            ],
            options={
                'db_table': 't_class',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('exam_id', models.IntegerField(primary_key=True, serialize=False)),
                ('exam_name', models.CharField(blank=True, max_length=50)),
                ('exam_time', models.DateTimeField(blank=True, null=True)),
                ('exam_place', models.CharField(blank=True, max_length=50)),
                ('grade', models.CharField(blank=True, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 't_exam',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.IntegerField(primary_key=True, serialize=False)),
                ('student_code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('gender', models.CharField(blank=True, max_length=10)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('grade', models.CharField(blank=True, max_length=20)),
                ('subject_group', models.CharField(default='全科', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('class_enrolled', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xscjgl.class')),
            ],
            options={
                'db_table': 't_student',
            },
        ),
        migrations.CreateModel(
            name='StudentExamNumber',
            fields=[
                ('exam_number_id', models.AutoField(primary_key=True, serialize=False)),
                ('exam_candidate_number', models.IntegerField()),
                ('exam_room_number', models.IntegerField()),
                ('seat_number', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xscjgl.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xscjgl.student')),
            ],
            options={
                'db_table': 't_student_exam_number',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('score_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_score_original', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('total_score_assigned', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('class_rank', models.IntegerField(blank=True, null=True)),
                ('school_rank', models.IntegerField(blank=True, null=True)),
                ('chinese_score_original', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('math_score_original', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('foreign_language_score_original', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('physics_score_original', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('history_score_original', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('chemistry_score_original', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('chemistry_score_assigned', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('biology_score_original', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('biology_score_assigned', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('politics_score_original', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('politics_score_assigned', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('geography_score_original', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('geography_score_assigned', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xscjgl.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xscjgl.student')),
                ('exam_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xscjgl.studentexamnumber')),
            ],
            options={
                'db_table': 't_score',
            },
        ),
        migrations.AddConstraint(
            model_name='studentexamnumber',
            constraint=models.UniqueConstraint(fields=('student_id', 'exam'), name='unique_student_exam'),
        ),
        migrations.AddConstraint(
            model_name='studentexamnumber',
            constraint=models.UniqueConstraint(fields=('exam', 'exam_candidate_number'), name='unique_exam_candidate_number'),
        ),
    ]
