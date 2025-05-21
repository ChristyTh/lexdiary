from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Case
from .forms import CaseForm
from django.contrib import messages

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

@login_required
def edit_case(request, pk):
    case = get_object_or_404(Case, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, "Case updated successfully.")
            return redirect('cases:list_cases')
    else:
        form = CaseForm(instance=case)
    return render(request, 'cases/edit_case.html', {'form': form, 'case': case})


@login_required
def delete_case(request, pk):
    case = get_object_or_404(Case, pk=pk, user=request.user)
    if request.method == 'POST':
        case.delete()
        messages.success(request, "Case deleted successfully.")
        return redirect('cases:list_cases')
    return render(request, 'cases/confirm_delete.html', {'case': case})
