from django import forms

from xscjgl.models import Class


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'year', 'subject_group']
        labels = {
            'name': '班级名称',
            'year': '入学年份',
            'subject_group': '科目组合',
        }
        error_messages = {
            'name': {
                'unique': "班级名称已存在，请输入其他名称。",
                'blank': "班级名称不能为空。"
            },
            'year': {
                'invalid': "请输入有效的年份。",
                'blank': "入学年份不能为空。"
            },
            'subject_group': {
                'blank': "科目组合不能为空。"
            },

        }

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year and (year < 1900 or year > 2100):  # 例如，对年进行一个范围校验
            raise forms.ValidationError("年级或学年必须在1900到2100之间。")
        return year

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isdigit():  # 例如，对年进行一个范围校验
            raise forms.ValidationError("班级名称只能包含数字。")
        return name
