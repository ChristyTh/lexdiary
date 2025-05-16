from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import now
from cases.models import Case
from stages.models import Stage

@login_required
def dashboard_view(request):
    selected_date = request.GET.get('date')
    today = now().date()
    date = selected_date or today

    stages_for_date = Stage.objects.filter(case__user=request.user, date=date).select_related('case')
    upcoming_stages = Stage.objects.filter(case__user=request.user, date__gt=today).select_related('case').order_by('date')[:10]

    total_cases = Case.objects.filter(user=request.user).count()
    total_stages = Stage.objects.filter(case__user=request.user).count()
    user_cases = Case.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'dashboard.html', {
        'selected_date': date,
        'stages_for_date': stages_for_date,
        'upcoming_stages': upcoming_stages,
        'total_cases': total_cases,
        'total_stages': total_stages,
        'user_cases': user_cases,
        'today': today
    })
