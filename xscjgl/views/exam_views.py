from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from ..forms.exam_forms import ExamForm
from ..mixins.base_views import BaseListView
from ..models import Exam


class ExamListView(BaseListView):
    model = Exam
    template_name = 'xscjgl/exam/exam_list.html'
    paginate_by = 20  # 默认分页大小
    allowed_paginate_sizes = [10, 20, 50]  # 允许的分页大小

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

    def get_paginate_by(self, queryset):
        """
        动态获取每页显示的记录数，通过 URL 参数 `paginate_by`。
        """
        try:
            paginate_by = int(self.request.GET.get('paginate_by', self.paginate_by))
            if paginate_by in self.allowed_paginate_sizes:
                return paginate_by
        except (ValueError, TypeError):
            pass
        return self.paginate_by


class ExamDetailView(DetailView):
    model = Exam
    template_name = 'xscjgl/exam/exam_detail.html'


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
