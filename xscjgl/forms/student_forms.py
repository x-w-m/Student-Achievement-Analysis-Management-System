from django import forms

from xscjgl.models import Student, Class


class StudentForm(forms.ModelForm):
    # 如果要根据班级名来直接进行修改操作，需重新映射班级名称字段
    # class_enrolled = forms.ModelChoiceField(
    #     queryset=Class.objects.all(),
    #     empty_label="选择班级",
    #     to_field_name='name'  # 这里假设用户输入班级名称
    # )

    class Meta:
        model = Student
        fields = ['student_code', 'name', 'gender', 'age', 'grade', 'subject_group', 'class_enrolled']
        labels = {
            'student_code': '编号',
            'name': '姓名',
            'gender': '性别',
            'age': '年龄',
            'grade': '年级',
            'subject_group': '科目组',
            'class_enrolled': '班级ID',
        }
