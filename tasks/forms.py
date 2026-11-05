from django import forms
from .models import Task, Project
from django.db.models import Q

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'project',
            'assignee',
            'status',
            'priority',
            'due_date'
        )

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'project': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'assignee': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'status': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'priority': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'due_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['project'].queryset = Project.objects.filter(
                Q(owner=user) | Q(members=user)
            ).distinct()