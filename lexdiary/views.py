from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import now
from cases.models import Case
from stages.models import Stage


from django.conf import settings
from django.http import JsonResponse
import os

import subprocess
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required




from datetime import datetime
from django.utils.timezone import now

@login_required
def dashboard_view(request):
    selected_date_str = request.GET.get('date')
    today = now().date()

    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = today  # fallback if date is malformed
    else:
        selected_date = today

    stages_for_date = Stage.objects.filter(case__user=request.user, date=selected_date).select_related('case')
    upcoming_stages = Stage.objects.filter(case__user=request.user, date__gt=today).select_related('case').order_by('date')[:10]

    total_cases = Case.objects.filter(user=request.user).count()
    total_stages = Stage.objects.filter(case__user=request.user).count()
    user_cases = Case.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'dashboard.html', {
        'selected_date': selected_date,
        'stages_for_date': stages_for_date,
        'upcoming_stages': upcoming_stages,
        'total_cases': total_cases,
        'total_stages': total_stages,
        'user_cases': user_cases,
        'today': today
    })
