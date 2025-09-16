from django.db import models
import uuid

class MagicLinkToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} — {self.token}"
