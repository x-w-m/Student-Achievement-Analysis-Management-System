from django.db import models


class StudentScore(models.Model):
    # 基本信息
    school = models.CharField(max_length=100, blank=True, null=True, verbose_name="学校")
    grade = models.CharField(max_length=50, blank=True, null=True, verbose_name="年级")
    class_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="班级")
    name = models.CharField(max_length=100, verbose_name="姓名")  # 唯一的非空字段
    student_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="学号")
    exam_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="考号")

    # 总分信息
    original_total_score = models.FloatField(null=True, verbose_name="原始总分")
    adjusted_total_score = models.FloatField(null=True, verbose_name="赋分总分")
    class_rank_total = models.IntegerField(null=True, verbose_name="总分班名")
    school_rank_total = models.IntegerField(null=True, verbose_name="总分校名")
    joint_rank_total = models.IntegerField(null=True, verbose_name="总分联名")

    # 各科成绩及排名
    # 语文
    chinese_score = models.FloatField(null=True, verbose_name="语文原始分数")
    chinese_class_rank = models.IntegerField(null=True, verbose_name="语文班名")
    chinese_school_rank = models.IntegerField(null=True, verbose_name="语文校名")
    chinese_joint_rank = models.IntegerField(null=True, verbose_name="语文联名")

    # 数学
    math_score = models.FloatField(null=True, verbose_name="数学原始分数")
    math_class_rank = models.IntegerField(null=True, verbose_name="数学班名")
    math_school_rank = models.IntegerField(null=True, verbose_name="数学校名")
    math_joint_rank = models.IntegerField(null=True, verbose_name="数学联名")

    # 英语
    english_score = models.FloatField(null=True, verbose_name="英语原始分数")
    english_class_rank = models.IntegerField(null=True, verbose_name="英语班名")
    english_school_rank = models.IntegerField(null=True, verbose_name="英语校名")
    english_joint_rank = models.IntegerField(null=True, verbose_name="英语联名")

    # 物理
    physics_score = models.FloatField(null=True, verbose_name="物理原始分数")
    physics_class_rank = models.IntegerField(null=True, verbose_name="物理班名")
    physics_school_rank = models.IntegerField(null=True, verbose_name="物理校名")
    physics_joint_rank = models.IntegerField(null=True, verbose_name="物理联名")

    # 化学
    chemistry_score = models.FloatField(null=True, verbose_name="化学原始分数")
    chemistry_adjusted_score = models.FloatField(null=True, verbose_name="化学赋分分数")
    chemistry_class_rank = models.IntegerField(null=True, verbose_name="化学班名")
    chemistry_school_rank = models.IntegerField(null=True, verbose_name="化学校名")
    chemistry_joint_rank = models.IntegerField(null=True, verbose_name="化学联名")

    # 生物
    biology_score = models.FloatField(null=True, verbose_name="生物原始分数")
    biology_adjusted_score = models.FloatField(null=True, verbose_name="生物赋分分数")
    biology_class_rank = models.IntegerField(null=True, verbose_name="生物班名")
    biology_school_rank = models.IntegerField(null=True, verbose_name="生物校名")
    biology_joint_rank = models.IntegerField(null=True, verbose_name="生物联名")

    # 时间戳字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "学生分数"
        verbose_name_plural = "学生分数"

    def __str__(self):
        return self.name
