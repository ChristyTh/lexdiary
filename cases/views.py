from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Case
from .forms import CaseForm

@login_required
def add_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user
            case.save()
            return redirect('cases:list_cases')
    else:
        form = CaseForm()
    return render(request, 'cases/add_case.html', {'form': form})

@login_required
def list_cases(request):
    cases = Case.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cases/list_cases.html', {'cases': cases})
