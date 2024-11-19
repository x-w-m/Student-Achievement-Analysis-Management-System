"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from xscjgl.views import main_views, StudentBulkUploadView, StudentCreateView, StudentBulkUpdateView, StudentDetailView
from xscjgl.views import StudentListView, StudentDeleteView, StudentUpdateView
from django.contrib.auth import views as auth_views

from xscjgl.views.class_views import ClassListView, ClassCreateView, ClassUpdateView, ClassDeleteView, ClassDetailView, \
    ClassBulkUploadView, UpdateClassesBasedOnGradeView
from xscjgl.views.exam_views import ExamListView, ExamCreateView, ExamUpdateView, ExamDeleteView, ExamDetailView, \
    ImportStudentExamNumbersView, ImportExamScoresView, ExamScoresView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('hello/', main_views.hello),

    # 学生相关路由
    path('stu/list', StudentListView.as_view(), name='student_list'),
    path('stu/<int:pk>', StudentDetailView.as_view(), name='student_detail'),
    path('stu/create', StudentCreateView.as_view(), name='student_create'),
    path('stu/edit/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('stu/del/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),
    path('stu/bulk-upload/', StudentBulkUploadView.as_view(), name='student_bulk_upload'),
    path('stu/bulk-update/', StudentBulkUpdateView.as_view(), name='student_bulk_update'),

    # 班级相关路由
    path('class/list', ClassListView.as_view(), name='class_list'),  # 班级列表
    path('class/<int:pk>/', ClassDetailView.as_view(), name='class_detail'),  # 班级详情
    path('class/create/', ClassCreateView.as_view(), name='class_create'),  # 创建班级
    path('class/update/<int:pk>/', ClassUpdateView.as_view(), name='class_update'),  # 更新班级
    path('class/delete/<int:pk>/', ClassDeleteView.as_view(), name='class_delete'),  # 删除班级
    path('class/bulk-upload/', ClassBulkUploadView.as_view(), name='class_bulk_upload'),  # 批量导入班级
    path('class/get-by-grade/', UpdateClassesBasedOnGradeView.as_view(), name='get_classes_based_on_grade'),  # 指定年级班级

    # 考试相关路由
    path('exam/<int:pk>', ExamDetailView.as_view(), name='exam_detail'),
    path('exam/list', ExamListView.as_view(), name='exam_list'),  # 考试列表
    path('exam/create/', ExamCreateView.as_view(), name='exam_create'),  # 创建考试
    path('exam/update/<int:pk>/', ExamUpdateView.as_view(), name='exam_update'),  # 更新考试
    path('exam/delete/<int:pk>/', ExamDeleteView.as_view(), name='exam_delete'),  # 删除考试

    path('exam/import_stu_num/<int:pk>', ImportStudentExamNumbersView.as_view(), name='import_student_numbers'),
    path('exam/import_exam_scores/<int:pk>/', ImportExamScoresView.as_view(), name='import_exam_scores'),
    path('exam/scores/<int:pk>/', ExamScoresView.as_view(), name='exam_scores'),

]
