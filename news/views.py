from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import NewsPost


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class NewsListView(ListView):
    model = NewsPost
    template_name = "news/news_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        qs = NewsPost.objects.filter(
            status=NewsPost.PUBLISHED,
            publish_at__lte=timezone.now()
        )
        q = self.request.GET.get("q")
        if q:
            qs = (
                qs.filter(title__icontains=q)
                | qs.filter(summary__icontains=q)
                | qs.filter(body__icontains=q)
            )
        return qs


class NewsDetailView(DetailView):
    model = NewsPost
    template_name = "news/news_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(
            status=NewsPost.PUBLISHED,
            publish_at__lte=timezone.now()
        )


class NewsCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = NewsPost
    fields = ["title", "summary", "body", "image", "status", "publish_at"]
    template_name = "news/news_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "News post created.")
        return super().form_valid(form)


class NewsUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = NewsPost
    fields = ["title", "summary", "body", "image", "status", "publish_at"]
    template_name = "news/news_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, "News post updated.")
        return super().form_valid(form)


class NewsDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = NewsPost
    template_name = "news/news_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("news_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "News post deleted.")
        return super().delete(request, *args, **kwargs)
