from django.shortcuts import render, get_object_or_404, redirect
from .forms import ComplaintForm, TrackForm, ResponseForm
from .models import Complaint, Response, Agency
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            category = complaint.category

            
            try:
                complaint.assigned_agency = Agency.objects.filter(name__icontains=category).first()
            except:
                complaint.assigned_agency = None

            complaint.save()

            
            if complaint.email:
                send_mail(
                    'CivicConnect – Complaint Received',
                    f'Dear{complaint.name},\n\nThank you for submitting your complaint to CivicConnect. '
                    'It has been received and assigned to the appropriate agency. '
                    'We will notify you of any updates.\n\nBest regards,\nCivicConnect Team', 
                    settings.DEFAULT_FROM_EMAIL, 
                    [complaint.email],         
                    fail_silently=False,         
                )

            messages.success(request, 'Complaint submitted successfully!')
            return redirect('submit_complaint')

        else:
            print(form.errors) 
    else:
        form = ComplaintForm()
    
    return render(request, 'complaints/submit.html', {'form': form})

def track_complaint(request):
    complaint = None

    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            category = form.cleaned_data['category']

            try:
                complaint = Complaint.objects.get(email=email, category=category)
            except Complaint.DoesNotExist:
                complaint = None
    else:
        form = TrackForm()

    return render(request, 'complaints/track.html', {'form': form, 'complaint': complaint})

def admin_dashboard(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'complaints/dashboard.html', {'complaints': complaints})

def respond_to_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.complaint = complaint
            complaint.status = response.updated_status
            complaint.save()
            response.save()
            messages.success(request, 'Response submitted.')
            return redirect('admin_dashboard')
    else:
        form = ResponseForm()
    return render(request, 'complaints/respond.html', {'form': form, 'complaint': complaint})

def home(request):
    return render(request, 'complaints/home.html')
def edit_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'complaints/edit_complaint.html', {'form': form})

def delete_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        complaint.delete()
        return redirect('admin_dashboard')
    return render(request, 'complaints/delete_confirm.html', {'complaint': complaint})
