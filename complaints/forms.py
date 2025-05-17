from django import forms
from .models import Complaint, Response

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'email', 'category', 'description', 'location', 'image']

class TrackForm(forms.Form):
    email = forms.EmailField()
    category = forms.ChoiceField(choices=[
        ('water', 'Water'),
        ('sanitation', 'Sanitation'),
        ('roads', 'Roads'),
        ('electricity', 'Electricity'),
        
    ])
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        category = cleaned_data.get("category")
        if not Complaint.objects.filter(email=email, category=category).exists():
            raise forms.ValidationError("No complaint found with this email and category.")
        return cleaned_data
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['comment', 'updated_status']
