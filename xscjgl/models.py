from django.db import models
from django.db.models import UniqueConstraint


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)  # 班级ID，自动生成
    name = models.CharField(max_length=20, unique=True, null=False)  # 班级名称
    year = models.CharField(max_length=10, null=False)  # 年级或学年
    # 科目组
    subject_group = models.CharField(max_length=20, null=False, default='全科')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=False)

    class Meta:
        db_table = 't_class'  # 数据库表名

    def __str__(self):
        return f"{self.name} ({self.year})"


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_code = models.CharField(max_length=20, null=False, unique=True)
    name = models.CharField(max_length=10, null=False)
    gender = models.CharField(max_length=10, blank=True)
    age = models.IntegerField(null=True, blank=True)
    grade = models.CharField(max_length=10, blank=True)
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE)  # 关联班级
    # 科目组
    subject_group = models.CharField(max_length=10, null=False, default='全科')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=False)

    class Meta:
        db_table = 't_student'


class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length=50, null=False)
    exam_time = models.DateField(null=False, blank=False)
    # 考试平台
    exam_platform = models.CharField(max_length=50, blank=True)
    grade = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=False)

    class Meta:
        db_table = 't_exam'


# 学生考号信息。多对多关联表
class StudentExamNumber(models.Model):
    exam_number_id = models.AutoField(primary_key=True)
    exam_candidate_number = models.IntegerField(null=False)
    exam_room_number = models.CharField(max_length=10, null=False)
    seat_number = models.CharField(max_length=10, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=False)

    class Meta:
        db_table = 't_student_exam_number'
        constraints = [
            UniqueConstraint(fields=['student_id', 'exam'], name='unique_student_exam'),  # 确保同一学生在同一考试中的唯一性
            # 确保每个考试中的考生号唯一
            UniqueConstraint(fields=['exam', 'exam_candidate_number'], name='unique_exam_candidate_number')
        ]


class Score(models.Model):
    score_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    exam_number = models.ForeignKey(StudentExamNumber, on_delete=models.CASCADE)
    total_score_original = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_score_assigned = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    class_rank = models.IntegerField(null=True, blank=True)
    school_rank = models.IntegerField(null=True, blank=True)
    chinese_score_original = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    math_score_original = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    foreign_language_score_original = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    physics_score_original = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    history_score_original = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    chemistry_score_original = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    chemistry_score_assigned = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    biology_score_original = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    biology_score_assigned = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    politics_score_original = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    politics_score_assigned = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    geography_score_original = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    geography_score_assigned = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=False)

    class Meta:
        db_table = 't_score'
