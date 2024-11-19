from django import forms

from xscjgl.models import Exam


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_id', 'exam_name', 'exam_time', 'exam_platform', 'grade']

    exam_time = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
