from datetime import datetime

from rest_framework import filters
from rest_framework.exceptions import ValidationError


class DateFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        date_format = '%Y-%m-%d'
        date_start = request.query_params.get('from', None)
        date_end =  request.query_params.get('to', None)

        if date_start:
            try:
                date = datetime.strptime(date_start, date_format).date()
                queryset = queryset.filter(date__gte=date)
            except ValueError:
                raise ValidationError({
                    'message': ('Incorrect format for "from" parameter - use "%s"' % date_format),
                })

        if date_end:
            try:
                date = datetime.strptime(date_end, date_format).date()
                queryset = queryset.filter(date__lte=date)
            except ValueError:
                raise ValidationError({
                    'message': ('Incorrect format for "to" parameter - use "%s"' % date_format),
                })

        return queryset
