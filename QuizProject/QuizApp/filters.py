import django_filters
from .models import Quiz

class QuizFilter(django_filters.FilterSet):
    topic=django_filters.CharFilter(lookup_expr='icontains')
    difficulty_level=django_filters.ChoiceFilter(choices=Quiz.DIFFICULTY_CHOICES)
    created_date=django_filters.DateTimeFilter(field_name='date_created',lookup_expr='date')

    class Meta:
        model=Quiz
        fields=['topic','difficulty_level','created_date']
