import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from xscjgl.forms.class_forms import ClassForm
from xscjgl.mixins.base_views import BaseListView
from xscjgl.models import Class


class ClassListView(BaseListView):
    model = Class
    template_name = 'xscjgl/class/class_list.html'
    paginate_by = 20  # 默认分页大小
    allowed_paginate_sizes = [10, 20, 50]  # 允许的分页大小

    def get_queryset(self):
        """
        返回过滤和排序后的班级数据，支持通过名称或其他字段搜索。
        """
        queryset = super().get_queryset().order_by("name")  # 默认按名称排序
        search_query = self.request.GET.get('search', '').strip()  # 获取搜索框输入内容
        if search_query:
            # 模糊匹配班级名称或年级
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(year__icontains=search_query)
            )
        return queryset


class ClassDetailView(DetailView):
    model = Class
    template_name = 'xscjgl/class/class_detail.html'


class ClassCreateView(CreateView):
    model = Class
    fields = ['name', 'year', 'subject_group']
    template_name = 'xscjgl/class/class_form.html'
    success_url = reverse_lazy('class_list')


class ClassUpdateView(UpdateView):
    model = Class
    form_class = ClassForm  # 使用自定义表单内容及说明，不能再同时设置表单属性
    # fields = ['name', 'year', 'subject_group']
    template_name = 'xscjgl/class/class_form.html'
    success_url = reverse_lazy('class_list')


class ClassDeleteView(DeleteView):
    model = Class
    template_name = 'xscjgl/class/class_confirm_delete.html'
    success_url = reverse_lazy('class_list')


class ClassBulkUploadView(View):
    def get(self, request):
        return render(request, 'xscjgl/class/class_bulk_upload.html')

    def post(self, request):
        excel_file = request.FILES.get('excel_file')

        if excel_file:
            # Save file temporarily
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            file_path = fs.path(filename)

            # Read the Excel file
            df = pd.read_excel(file_path, dtype=str)

            # Iterate through the rows and create Class instances
            for index, row in df.iterrows():
                Class.objects.create(
                    year=row['年级'],
                    name=row['班级'],
                    subject_group=row.get('科目组', '全科')
                )

            # Delete the file after processing
            fs.delete(filename)

            # Redirect to class list
            return redirect('class_list')

        return render(request, 'xscjgl/class/class_bulk_upload.html', {'error': 'Please upload a file.'})


class UpdateClassesBasedOnGradeView(View):
    def get(self, request, *args, **kwargs):
        grade = request.GET.get('grade')
        if grade is not None:
            classes = Class.objects.filter(year=grade)
            classes_list = [{'pk': cls.pk, 'name': cls.name} for cls in classes]
            return JsonResponse({'classes': classes_list})
        return JsonResponse({'classes': []})
