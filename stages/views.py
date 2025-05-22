from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Stage
from .forms import StageForm
from cases.models import Case

# views.py in stages app
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Stage
from datetime import datetime
from django.core.exceptions import ValidationError

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




@login_required
def filter_by_stage(request):
    user = request.user
    selected_date = request.GET.get('date')
    selected_stage = request.GET.get('stage_name')  # ✅ Get from GET params

    stage_choices = (
        Stage.objects.filter(case__user=user)
        .values_list('stage_name', flat=True)
        .distinct()
    )

    stages = Stage.objects.filter(case__user=user)

    if selected_stage:
        stages = stages.filter(stage_name=selected_stage)

    if selected_date:
        try:
            parsed_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            stages = stages.filter(date=parsed_date)
        except ValueError:
            pass  # ignore invalid dates

    return render(request, 'stages/stage_filter.html', {
        'stages': stages,
        'stage_choices': stage_choices,
        'selected_stage': selected_stage,  # ✅ used in the template
        'selected_date': selected_date,
    })