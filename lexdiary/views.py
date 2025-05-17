from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import now
from cases.models import Case
from stages.models import Stage


from django.conf import settings
from django.http import JsonResponse
import os

def list_static_files(request):
    static_dir = settings.STATIC_ROOT
    file_list = []

    for root, dirs, files in os.walk(static_dir):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), static_dir)
            file_list.append(file_path)

    return JsonResponse({'static_files': file_list})



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
