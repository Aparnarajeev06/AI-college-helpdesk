from django.db import models


class ChatFeedback(models.Model):
    question = models.CharField(max_length=1000)
    is_helpful = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "chat feedback"
        verbose_name_plural = "chat feedback"

    def __str__(self):
        rating = "helpful" if self.is_helpful else "not helpful"
        return f"{rating}: {self.question[:80]}"
