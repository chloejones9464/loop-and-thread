from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from patterns.models import Pattern
from accounts.models import Profile
from checkout.models import OrderLineItem


class Review(models.Model):
    pattern = models.ForeignKey(
        Pattern,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(5)]
    )
    title = models.CharField(max_length=120, blank=True)
    body = models.TextField(max_length=2000)
    verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("pattern", "user_profile")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.pattern.title} - {self.user_profile} ({self.rating}/5)"

    def mark_verified(self):
        """Set verified_purchase=True if user
        has an order containing this pattern."""
        purchased = OrderLineItem.objects.filter(
            pattern=self.pattern, order__user_profile=self.user_profile
        ).exists()
        self.verified_purchase = purchased
