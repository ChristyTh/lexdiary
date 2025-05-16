from django.db import models
from cases.models import Case

class Stage(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='stages')
    stage_name = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case.case_number} - {self.stage_name} ({self.date})"
