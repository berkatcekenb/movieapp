from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    username_changed = models.BooleanField(default=False)  # Yeni alan

    class Meta:
        db_table = 'users'  # Özel tablo adı belirtiyoruz
        
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.pk:  # Eğer kullanıcı zaten varsa (yani güncelleme işlemiyse)
            old_user = CustomUser.objects.get(pk=self.pk)
            if old_user.username != self.username:  # Kullanıcı adı değiştirilmeye çalışılıyorsa
                if old_user.username_changed:  # Daha önce değiştirilmişse
                    self.username = old_user.username  # Eski kullanıcı adını koru
                else:
                    self.username_changed = True  # İlk değişiklikse işaretle
        super().save(*args, **kwargs)
