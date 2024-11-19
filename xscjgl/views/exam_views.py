import pandas as pd
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from ..forms.exam_forms import ExamForm
from ..mixins.base_views import BaseListView
from ..models import Exam, Student, StudentExamNumber, Score
from ..utils.upload_storage_utils import UploadStorage


class ExamDetailView(DetailView):
    model = Exam
    template_name = 'xscjgl/exam/exam_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = self.get_object()

        # 计算参考人数
        candidate_count = StudentExamNumber.objects.filter(exam=exam).count()
        context['candidate_count'] = candidate_count

        # 计算成绩记录数
        score_count = Score.objects.filter(exam=exam).count()
        context['score_count'] = score_count

        return context


class ExamListView(BaseListView):
    model = Exam
    template_name = 'xscjgl/exam/exam_list.html'


    def get_queryset(self):
        """
        返回排序和过滤后的考试数据，默认按考试时间排序。
        """
        # 获取基本查询集
        queryset = super().get_queryset().order_by("-exam_time")

        # 处理搜索功能
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(exam_name__icontains=search_query)

        return queryset




class ExamCreateView(CreateView):
    model = Exam
    # fields = ['exam_name', 'exam_time', 'exam_place', 'grade']
    form_class = ExamForm
    template_name = 'xscjgl/exam/exam_form.html'
    success_url = reverse_lazy('exam_list')

    def form_valid(self, form):
        print('Form is valid')
        return super().form_valid(form)

    def form_invalid(self, form):
        print('Form is invalid')
        print(form.errors)
        return super().form_invalid(form)


class ExamUpdateView(UpdateView):
    model = Exam
    # fields = ['exam_name', 'exam_time', 'exam_platform', 'grade']
    form_class = ExamForm
    template_name = 'xscjgl/exam/exam_form.html'
    success_url = reverse_lazy('exam_list')


class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'xscjgl/exam/exam_confirm_delete.html'
    success_url = reverse_lazy('exam_list')


class ImportStudentExamNumbersView(View):
    template_name = 'xscjgl/exam/import_student_numbers.html'

    def get(self, request, pk):
        # form = ImportStudentExamNumbersForm()
        exam = get_object_or_404(Exam, pk=pk)
        context = {'exam': exam}
        return render(request, 'xscjgl/exam/import_student_numbers.html', context)

    def post(self, request, pk):
        """
        处理上传的 Excel 文件并批量导入学生考号。
        """
        # 获取指定考试
        exam = get_object_or_404(Exam, pk=pk)

        # 获取上传的文件
        excel_file = request.FILES.get('exam_numbers_upload')
        if not excel_file:
            return render(request, self.template_name, {'exam': exam, 'errors': ['请上传 Excel 文件。']})

        # 保存上传的文件
        fs = UploadStorage(sub_path="exam_numbers")
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        errors = []  # 错误信息收集
        records_created = 0  # 成功导入记录计数

        try:
            with transaction.atomic():  # 启用事务，保证操作原子性
                # 读取 Excel 文件
                df = pd.read_excel(file_path, dtype=str)
                df.dropna(axis=1, how='all', inplace=True)

                # 校验列是否完整
                required_columns = ['学号', '考号', '考室号', '座位号']
                for col in required_columns:
                    if col not in df.columns:
                        raise ValueError(f"缺少必要的列: {col}")

                # 遍历每一行并处理数据
                for index, row in df.iterrows():
                    try:
                        student_code = row['学号']
                        student = Student.objects.get(student_code=student_code)

                        # 创建或更新 StudentExamNumber
                        StudentExamNumber.objects.update_or_create(
                            student=student,
                            exam=exam,
                            defaults={
                                'exam_candidate_number': row['考号'],
                                'exam_room_number': row['考室号'],
                                'seat_number': row['座位号'],
                            }
                        )
                        records_created += 1
                    except Student.DoesNotExist:
                        errors.append(f"第 {int(index) + 2} 行: 学号 {student_code} 不存在。")
                    except Exception as e:
                        errors.append(f"第 {index + 2} 行: {e}")

                # 如果有错误信息，抛出异常回滚事务
                if errors:
                    raise ValueError("部分数据存在错误，请查看错误详细信息。")

        except Exception as e:
            errors.append(f"批量导入失败: {e}")

        # 根据结果返回模板
        if errors:
            return render(request, self.template_name, {'exam': exam, 'errors': errors})

        messages.success(request, f"成功导入 {records_created} 条学生考号记录。")
        return redirect('exam_detail', pk=pk)


class ImportExamScoresView(View):
    template_name = "xscjgl/exam/import_exam_scores.html"

    def get(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        return render(request, "xscjgl/exam/import_exam_scores.html", {"exam": exam})

    def post(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        excel_file = request.FILES.get('score_file')

        # 初始化错误列表
        errors = []

        # 检查是否上传了文件
        if not excel_file:
            errors.append("请上传 Excel 文件。")
            return render(request, self.template_name, {"exam": exam, "errors": errors})

        # 保存上传的文件
        fs = UploadStorage(sub_path="exam_scores")
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        scores_to_create = []

        try:
            with transaction.atomic():
                # 读取 Excel 文件
                df = pd.read_excel(file_path, dtype=str)
                df.dropna(axis=1, how='all', inplace=True)  # 移除全空列

                # 检查必要的列是否存在
                required_columns = ['学生编号', '总成绩']
                for col in required_columns:
                    if col not in df.columns:
                        errors.append(f"缺少必要的列: {col}")
                        raise ValueError("文件格式错误。")

                # 遍历 Excel 文件中的数据
                for index, row in df.iterrows():
                    try:
                        student_code = row['学生编号']
                        total_score = row['总成绩']

                        # 获取学生和考生号信息
                        student = Student.objects.get(student_code=student_code)
                        student_exam_number = StudentExamNumber.objects.get(student=student, exam=exam)

                        # 创建成绩对象
                        score = Score(
                            student=student,
                            exam=exam,
                            exam_number=student_exam_number,
                            total_score_original=float(total_score),
                        )
                        scores_to_create.append(score)
                    except Exception as e:
                        errors.append(f"行 {index + 2} 错误: {e}")

                # 如果存在错误，终止导入
                if errors:
                    raise ValueError("上传数据存在错误，请检查以下错误详情。")

                # 批量创建成绩记录
                Score.objects.bulk_create(scores_to_create)

        except Exception as e:
            if not errors:  # 捕获其他非数据相关的异常
                errors.append(f"导入失败: {e}")

        # 返回模板并显示错误或成功消息
        if errors:
            return render(request, self.template_name, {"exam": exam, "errors": errors})

        messages.success(request, f"成功导入 {len(scores_to_create)} 条成绩记录。")
        return redirect("exam_detail", pk=exam.pk)


class ExamScoresView(BaseListView):
    model = Score
    template_name = "xscjgl/exam/exam_scores.html"

    def get_queryset(self):
        exam_id = self.kwargs.get('pk')
        return Score.objects.filter(exam_id=exam_id).select_related('student', 'exam_number').order_by(
            '-total_score_original')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam'] = get_object_or_404(Exam, pk=self.kwargs.get('pk'))
        return context
