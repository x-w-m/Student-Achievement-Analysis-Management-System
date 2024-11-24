from django.views.generic.list import ListView


class BaseListView(ListView):
    """
    通用视图基类，处理上下文数据（分页、搜索等）。
    """
    paginate_by = 20  # 默认分页大小
    allowed_paginate_sizes = [10, 20, 50]  # 允许的分页大小

    def get_paginate_by(self, queryset):
        """
        动态获取每页显示的记录数，通过 URL 参数 `paginate_by`。
        """
        try:
            paginate_by = int(self.request.GET.get('paginate_by', self.paginate_by))
            if paginate_by in self.allowed_paginate_sizes:
                return paginate_by
        except (ValueError, TypeError):
            pass
        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['total_count'] = queryset.count()
        context['current_paginate_by'] = self.get_paginate_by(queryset)
        context['search_query'] = self.request.GET.get('search', '')
        return context
