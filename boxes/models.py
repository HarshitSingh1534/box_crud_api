from django.db import models

# Create your models here.
import uuid

from django.contrib.auth.models import User

# Create your models here.
class Boxes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)

    height = models.IntegerField(default=1)
    length = models.IntegerField(default=1)
    breadth = models.IntegerField(default=1)

    volume = models.IntegerField(default=1)
    area = models.IntegerField(default=1)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Box"
        verbose_name_plural = "Boxes"

    def __str__(self):
        return f"{self.creator.username} | {self.height} | {self.length} | {self.breadth} | {self.area} | {self.volume}"

    def save(self, *args, **kwargs):
        self.area = 2 * (
            self.height * self.length
            + self.height * self.breadth
            + self.length * self.breadth
        )
        self.volume = self.height * self.length * self.breadth

        super().save(*args, **kwargs)
