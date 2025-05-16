from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Stage
from .forms import StageForm
from cases.models import Case

@login_required
def add_stage(request, case_id):
    case = get_object_or_404(Case, id=case_id, user=request.user)

    if request.method == 'POST':
        form = StageForm(request.POST)
        if form.is_valid():
            stage = form.save(commit=False)
            stage.case = case
            stage.save()
            return redirect('stages:view_stages', case_id=case.id)
    else:
        form = StageForm()

    return render(request, 'stages/add_stage.html', {'form': form, 'case': case})

@login_required
def view_stages(request, case_id):
    case = get_object_or_404(Case, id=case_id, user=request.user)
    stages = case.stages.order_by('-date')
    return render(request, 'stages/view_stages.html', {'case': case, 'stages': stages})
