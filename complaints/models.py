from django.db import models

CATEGORY_CHOICES = [
    ('water', 'Water'),
    ('sanitation', 'Sanitation'),
    ('roads', 'Roads'),
    ('electricity', 'Electricity'),
]

STATUS_CHOICES = [
    ('submitted', 'Submitted'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
]

class Agency(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()

    def __str__(self):
        return self.name

class Complaint(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='complaints/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    assigned_agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        agency_map = {
            'water': 'Water Board Department',
            'sanitation': 'Sanitation Agency',
            'roads': 'Roads & Transport Authority',
            'electricity': 'Electric Utility Company',
        }
        agency_name = agency_map.get(self.category)
        if agency_name:
            try:
                self.assigned_agency = Agency.objects.get(name=agency_name)
            except Agency.DoesNotExist:
                self.assigned_agency = None  # Or you can create a fallback
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} complaint from {self.name}"

class Response(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    comment = models.TextField()
    updated_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Response to {self.complaint} on {self.updated_at}"
