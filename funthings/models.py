from django.db import models
from django.conf import settings
from datetime import date 

class Thing(models.Model):
    funster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    thing = models.CharField(
        max_length=160, 
        help_text="Max 160 Chars."
        )
    thing_date = models.DateField(
        default=date.today, 
        verbose_name="Thing Date"
        )
    photo = models.ImageField(
        upload_to ='uploads/%Y/%m/%d/', 
        blank=True,editable=True,
        verbose_name="Thing Photo"
        )

    class Meta:
        ordering = ["-thing_date"]

    def __str__(self):
        return self.thing + " on " + self.thing_date.strftime("%Y-%m-%d")
