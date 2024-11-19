# cjfx/main_views.py
import time
import uuid

import numpy as np
from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse, Http404
import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts

from .models import StudentScore


def upload_file(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        print("读取文件")
        start_time = time.perf_counter()
        # 读取Excel文件，不处理标题行
        df = pd.read_excel(excel_file)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"文件读取时间：{execution_time} 秒")
        # print(df)

        start_time = time.perf_counter()
        # 空值处理
        # df = df.fillna(0)
        # 从文件中读取的''空字符串值为NaN，操作df生成的空字符串还是空字符串。
        # 前者能被fillna匹配，后者不会被匹配到。
        df = df.fillna(np.nan).replace([np.nan], [None])
        print("空值处理完成")
        # print(df)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"空值处理时间：{execution_time} 秒")

        start_time = time.perf_counter()
        # 准备批量插入的数据列表
        instances = []

        for index, row in df.iterrows():
            instance = StudentScore(
                school=row['学校'],
                grade=row['年级'],
                class_number=row['班级'],
                name=row['姓名'],
                student_id=row['学号'],
                exam_id=row['考号'],
                original_total_score=row['原始总分'],
                adjusted_total_score=row['赋分总分'],
                class_rank_total=row['总分班名'],
                school_rank_total=row['总分校名'],
                joint_rank_total=row['总分联名'],
                chinese_score=row['语文原始分数'],
                chinese_class_rank=row['语文班名'],
                chinese_school_rank=row['语文校名'],
                chinese_joint_rank=row['语文联名'],
                math_score=row['数学原始分数'],
                math_class_rank=row['数学班名'],
                math_school_rank=row['数学校名'],
                math_joint_rank=row['数学联名'],
                english_score=row['英语原始分数'],
                english_class_rank=row['英语班名'],
                english_school_rank=row['英语校名'],
                english_joint_rank=row['英语联名'],
                physics_score=row['物理原始分数'],
                physics_class_rank=row['物理班名'],
                physics_school_rank=row['物理校名'],
                physics_joint_rank=row['物理联名'],
                chemistry_score=row['化学原始分数'],
                chemistry_adjusted_score=row['化学赋分分数'],
                chemistry_class_rank=row['化学班名'],
                chemistry_school_rank=row['化学校名'],
                chemistry_joint_rank=row['化学联名'],
                biology_score=row['生物原始分数'],
                biology_adjusted_score=row['生物赋分分数'],
                biology_class_rank=row['生物班名'],
                biology_school_rank=row['生物校名'],
                biology_joint_rank=row['生物联名'],
            )
            instances.append(instance)

        # 使用事务确保数据完整性
        with transaction.atomic():
            StudentScore.objects.bulk_create(instances)

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"数据写入时间：{execution_time} 秒")
        return HttpResponse("文件上传成功，数据已插入数据库。")
    return render(request, 'upload.html')


def export_page(request):
    return render(request, 'filedown.html')


def export_to_excel(request):
    start_time = time.perf_counter()
    # 从数据库中读取数据，懒加载模式，只有被使用时才会真正执行查询操作。
    data = StudentScore.objects.all().values()
    # 正式执行查询操作
    df = pd.DataFrame(list(data))
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"数据读取时间：{execution_time} 秒")
    start_time = time.perf_counter()
    print("格式转换")
    # 打印开头几行，验证数据
    print(df.head())
    # 假设date_column1和date_column2是你想要去除的日期时间列
    df = df.drop(['created_at', 'updated_at'], axis=1)
    # 将数据写入Excel文件
    excel_file = pd.ExcelWriter('StudentScores.xlsx', engine='openpyxl')
    df.to_excel(excel_file, index=False)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    excel_file.close()
    print(f"写入文件时间：{execution_time} 秒")

    # 将Excel文件发送给用户
    with open('StudentScores.xlsx', 'rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="StudentScores.xlsx"'
        return response


def top_students(request):
    # 获取总分联名前1000名的学生
    top_stus = StudentScore.objects.filter(joint_rank_total__lte=1000).order_by('joint_rank_total')
    # 按学校统计人数
    df = pd.DataFrame(top_stus.values())
    school_counts = df.groupby('school').size().sort_values(ascending=False)

    # 创建柱形图
    bar = Bar()
    bar.add_xaxis(school_counts.index.tolist())
    bar.add_yaxis("学生人数", school_counts.values.tolist())

    # 设置图表的标题和 x 轴标签
    bar.set_global_opts(title_opts=opts.TitleOpts(title="各学校总分联名前1000名学生人数"),
                        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)))

    # # 渲染图表到 HTML 文件
    # # 生成唯一的文件名
    # chart_id = uuid.uuid4()
    # filename = f"chart_{chart_id}.html"
    # file_path = f"templates/charts/{filename}"
    # bar.render(file_path)
    #
    # # 将数据传递给模板
    # return render(request, 'charts.html', {'chart_id': chart_id})
    stuhtml = bar.render_embed()
    # 将图表HTML代码作为上下文传递给模板
    context = {'chart_html': stuhtml}
    return render(request, 'charts.html', context)


def chart_view(request, chart_id):
    try:
        with open(f'templates/charts/chart_{chart_id}.html', 'r', encoding='utf-8') as file:
            return HttpResponse(file.read())
    except FileNotFoundError:
        raise Http404("Chart not found")
