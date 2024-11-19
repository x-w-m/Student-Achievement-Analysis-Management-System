import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
django.setup()


def import_students_from_excel(excel_path):
    # 读取 Excel 文件
    df = pd.read_excel(excel_path, engine='openpyxl')
    print(df.head())
    # 遍历 DataFrame 中的每一行
    for index, row in df.iterrows():
        # 创建 Student 实例
        student = Student(
            student_id=row['student_id'],
            name=row['name'],
            grade=row['grade'] if 'grade' in df.columns else '',
            class_id=row['class_id'] if 'class_id' in df.columns else ''
        )
        # 保存到数据库
        student.save(update_fields=['name', 'grade', 'class_id'])

    # for index, row in df.iterrows():
    #     Student.objects.filter(student_id=row['student_id']).update(
    #         name=row['name'],
    #         grade=row.get('grade', ''),
    #         class_id=row.get('class_id', ''),
    #     )


if __name__ == '__main__':
    from xscjgl.models import Student
    import pandas as pd
    from django.contrib.auth.models import User

    # 创建普通用户
    # user = User.objects.create_user('username', 'email@example.com', 'password')

    # 调用函数
    import_students_from_excel('2023级学生名单.xlsx')
