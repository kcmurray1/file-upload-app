from django.db import models

class File(models.Model):
    name = models.CharField(max_length=100)
    size = models.BigIntegerField(null=True, blank=True)
    time_uploaded = models.DateTimeField(auto_now_add=True)

    # files can be a parent of one or more other files
    parent = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.CASCADE,
        related_name="children"
    )

    def __str__(self):
        if self.parent:
            return f"{self.id} {self.name} with parent {self.parent}"
        return f"{self.id} {self.name}"

