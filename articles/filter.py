import django_filters
from articles.models.article import Article


class DateRangeFilter(django_filters.rest_framework.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Article
        fields = ('start_date', 'end_date')
