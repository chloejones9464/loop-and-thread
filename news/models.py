from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class NewsPost(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [(DRAFT, "Draft"), (PUBLISHED, "Published")]

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(max_length=300, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to="news/", blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT
    )
    publish_at = models.DateTimeField(default=timezone.now)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="news_created"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="news_updated"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publish_at"]

    def __str__(self):
        return self.title

    @property
    def is_live(self):
        return (
            self.status == self.PUBLISHED
            and self.publish_at <= timezone.now()
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            base = (
                slugify(self.title) or "post"
            )
            slug = base
            i = 2
            while (
                NewsPost.objects.filter(slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("news_detail", args=[self.slug])
