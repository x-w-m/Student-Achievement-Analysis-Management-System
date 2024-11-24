import pandas as pd
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView

from xscjgl.forms.student_forms import StudentForm
from xscjgl.mixins.base_views import BaseListView
from xscjgl.models import Student, Class, Exam, Score
from xscjgl.utils.upload_storage_utils import UploadStorage


class StudentDetailView(DetailView):
    model = Student
    template_name = 'xscjgl/student/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        """
        在模板上下文中添加考试记录和成绩的分页数据。
        """
        context = super().get_context_data(**kwargs)

        # 查询学生的成绩记录及关联的考试信息
        scores = Score.objects.filter(student=self.object).select_related('exam').order_by('-exam__exam_time')

        # 获取分页大小参数，默认为10
        paginate_by = int(self.request.GET.get('paginate_by', 10))
        paginator = Paginator(scores, paginate_by)
        page_number = self.request.GET.get('page')

        # 将分页数据传递到上下文
        context['scores'] = paginator.get_page(page_number)
        context['page_obj'] = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['current_paginate_by'] = paginate_by
        return context


class StudentListView(BaseListView):
    model = Student
    template_name = 'xscjgl/student/lookstu.html'
    paginate_by = 20
    allowed_paginate_sizes = [10, 20, 50]

    def get_queryset(self):
        """
        重写查询集方法，根据学号或姓名搜索学生。
        """
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            # 精确匹配学号或模糊匹配姓名
            queryset = queryset.filter(
                Q(student_code=search_query) | Q(name__icontains=search_query)
            )
        return queryset.order_by("-student_code")


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'xscjgl/student/student_form.html'
    success_url = reverse_lazy('student_list')


class StudentUpdateView(UpdateView):
    model = Student
    # fields = ['name', 'gender', 'age', 'grade', 'class_id']
    form_class = StudentForm
    template_name = 'xscjgl/student/student_form.html'
    success_url = reverse_lazy('student_list')

    # 重写方法，传递学生所处年级班级列表
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()  # 获取当前学生实例
        context['classes'] = Class.objects.filter(year=student.grade)  # 将所有班级查询并添加到上下文
        return context


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'xscjgl/student/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')  # 重定向到的 URL


class StudentBulkUploadView(View):
    template_name = 'xscjgl/student/bulk_upload.html'

    def get(self, request, *args, **kwargs):
        # 由于当前版本Pycharm（2024.3）不能提示self.template_name引用的模板，此处保留一个使用硬编码形式编写的模板路径，方便跳转模板页面。
        return render(request, 'xscjgl/student/student_bulk_upload.html')

    def post(self, request):
        excel_file = request.FILES.get('student_upload')

        if not excel_file:
            return render(request, self.template_name, {'error': '请上传文件。'})

        # 保存文件
        fs = UploadStorage(sub_path="student")  # 保存到“student”子目录
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)  # 文件路径

        # 用于记录错误信息
        errors = []
        students_to_create = []
        class_cache = {}

        try:
            with transaction.atomic():
                # 读取 Excel 文件
                df = pd.read_excel(file_path, dtype=str)
                df.dropna(axis=1, how='all', inplace=True)

                # 校验列是否完整
                required_columns = ['编号', '姓名', '班级']
                for col in required_columns:
                    if col not in df.columns:
                        raise ValueError(f"缺少必要的列: {col}")

                # 遍历每一行并构建 Student 对象
                for index, row in df.iterrows():
                    try:
                        # 获取班级对象，使用缓存减少查询
                        class_name = row['班级']
                        if class_name not in class_cache:
                            class_cache[class_name] = Class.objects.get(name=class_name)

                        class_enrolled = class_cache[class_name]

                        # 创建 Student 实例（暂不保存到数据库）
                        student = Student(
                            student_code=row['编号'],
                            name=row['姓名'],
                            gender=row.get('性别', ''),
                            age=row.get('年龄', None),
                            grade=row.get('年级', ''),
                            class_enrolled=class_enrolled,
                            subject_group=row.get('科目组', '全科')
                        )
                        students_to_create.append(student)

                    except Exception as e:
                        # 捕获当前行的错误并记录
                        errors.append(f"行 {int(index) + 2} 错误: {e}")  # index + 2 表示 Excel 中的真实行号

                # 如果存在错误，抛出异常以触发事务回滚
                if errors:
                    raise ValueError("上传数据存在错误，请检查以下错误详情。")

                # 批量创建学生记录
                Student.objects.bulk_create(students_to_create)

        except Exception as e:
            # 捕获事务中的错误并追加到错误信息
            errors.append(f"批量上传失败: {e}")

        # 根据结果返回模板
        if errors:
            return render(request, self.template_name, {'errors': errors})

        messages.success(request, f"成功上传 {len(students_to_create)} 条学生记录。")
        return redirect('student_list')


class StudentBulkUpdateView(View):
    template_name = 'xscjgl/student/bulk_update.html'

    def get(self, request, *args, **kwargs):
        # 渲染模板页面
        return render(request, 'xscjgl/student/student_bulk_update.html')

    def post(self, request):
        excel_file = request.FILES.get('student_update')

        if not excel_file:
            return render(request, self.template_name, {'error': '请上传文件。'})

        # 保存文件
        fs = UploadStorage(sub_path="student")  # 保存到“student”子目录
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)  # 文件路径

        errors = []
        class_cache = {}

        try:
            with transaction.atomic():
                # 读取 Excel 文件
                df = pd.read_excel(file_path, dtype=str)
                df.dropna(axis=1, how='all', inplace=True)

                # 校验列是否完整
                required_columns = ['编号', '姓名', '班级']
                for col in required_columns:
                    if col not in df.columns:
                        raise ValueError(f"缺少必要的列: {col}")

                # 遍历每一行并更新 Student 对象
                for index, row in df.iterrows():
                    try:
                        # 获取学生对象
                        student_code = row['编号']
                        student = Student.objects.get(student_code=student_code)

                        # 获取班级对象，使用缓存减少查询
                        class_name = row['班级']
                        if class_name not in class_cache:
                            class_cache[class_name] = Class.objects.get(name=class_name)

                        class_enrolled = class_cache[class_name]

                        # 更新 Student 对象字段
                        student.name = row['姓名']
                        student.gender = row.get('性别', student.gender)
                        student.age = row.get('年龄', student.age)
                        student.grade = row.get('年级', student.grade)
                        student.class_enrolled = class_enrolled
                        student.subject_group = row.get('科目组', student.subject_group)
                        student.save()

                    except Student.DoesNotExist:
                        errors.append(f"行 {index + 2} 错误: 学生编号 {student_code} 不存在。")
                    except Class.DoesNotExist:
                        errors.append(f"行 {index + 2} 错误: 班级 {class_name} 不存在。")
                    except Exception as e:
                        errors.append(f"行 {index + 2} 错误: {e}")

                # 如果存在错误，抛出异常以触发事务回滚
                if errors:
                    raise ValueError("更新数据存在错误，请检查以下错误详情。")

        except Exception as e:
            # 捕获事务中的错误并追加到错误信息
            errors.append(f"批量更新失败: {e}")

        # 根据结果返回模板
        if errors:
            return render(request, self.template_name, {'errors': errors})

        messages.success(request, f"成功更新 {len(df)} 条学生记录。")
        return redirect('student_list')
