from django.views.generic.list import ListView


class BaseListView(ListView):
    """
    通用视图基类，处理上下文数据（分页、搜索等）。
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['total_count'] = queryset.count()
        context['current_paginate_by'] = self.get_paginate_by(queryset)
        context['search_query'] = self.request.GET.get('search', '')
        return context
