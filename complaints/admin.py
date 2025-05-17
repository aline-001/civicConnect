from django.contrib import admin
from .models import Complaint, Agency, Response

admin.site.register(Complaint)
admin.site.register(Agency)
admin.site.register(Response)
