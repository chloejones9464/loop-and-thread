from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ["name"]

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Pattern(models.Model):
    DIFFICULTY = [
        ("easy", "Easy"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="patterns"
    )
    summary = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY,
        default="easy"
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0  # 0 for free
    )
    cover_image = models.ImageField(
        upload_to="patterns/covers/",
        blank=True,
        null=True
    )
    file = models.FileField(
        upload_to="patterns/files/"  # pdf or zip of assets
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
