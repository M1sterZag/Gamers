from django.db import models

class AuthUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    # avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    @property
    def is_authentificated(self):
        return True
