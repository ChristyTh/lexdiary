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

from django.db.models import Count
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from stages.models import Stage
from cases.models import Case
from dateutil.parser import parse as parse_date

@login_required
def dashboard_view(request):
    selected_date = request.GET.get('date')
    today = now().date()
    date = selected_date or today

    # Stages on selected date
    stages_for_date = Stage.objects.filter(case__user=request.user, date=date).select_related('case')

    # Upcoming stages
    upcoming_stages = Stage.objects.filter(case__user=request.user, date__gte=today).select_related('case').order_by('date')[:10]

    # User cases
    total_cases = Case.objects.filter(user=request.user).count()
    total_stages = Stage.objects.filter(case__user=request.user).count()
    user_cases = Case.objects.filter(user=request.user).order_by('-created_at')

    # Count stage types
    stage_summary = (
        Stage.objects.filter(case__user=request.user)
        .values('stage_name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    return render(request, 'dashboard.html', {
        'selected_date': date,
        'stages_for_date': stages_for_date,
        'upcoming_stages': upcoming_stages,
        'total_cases': total_cases,
        'total_stages': total_stages,
        'user_cases': user_cases,
        'stage_summary': stage_summary,
        'today': today,
    })





@login_required
def upcoming_stages_json(request):
    start_date_str = request.GET.get('start')
    end_date_str = request.GET.get('end')

    stages = Stage.objects.filter(case__user=request.user)

    try:
        if start_date_str:
            start_date = parse_date(start_date_str).date()
            stages = stages.filter(date__gte=start_date)

        if end_date_str:
            end_date = parse_date(end_date_str).date()
            stages = stages.filter(date__lte=end_date)

    except Exception as e:
        return JsonResponse({'error': f'Invalid date: {e}'}, status=400)

    data = [
        {
            'title': f"{stage.case.case_number} - {stage.stage_name}",
            'start': stage.date.isoformat(),
            'url': f"/stages/filter/?date={stage.date.isoformat()}"
        }
        for stage in stages
    ]

    return JsonResponse(data, safe=False)
