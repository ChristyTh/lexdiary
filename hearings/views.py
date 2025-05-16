from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Hearing
from .forms import HearingForm
from cases.models import Case

from django.utils.timezone import now
from django.db.models import Prefetch

from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Hearing
from cases.models import Case

@login_required
def dashboard_home(request):
    selected_date = request.GET.get('date')
    today = now().date()
    user_cases = Case.objects.filter(user=request.user).order_by('-created_at')

    try:
        date = selected_date or today
    except:
        date = today

    # Hearings for selected date
    hearings_for_date = Hearing.objects.filter(
        case__user=request.user,
        hearing_date=date
    ).select_related('case')

    # Upcoming hearings for next 30 days
    upcoming_hearings = Hearing.objects.filter(
        case__user=request.user,
        hearing_date__gt=today
    ).select_related('case').order_by('hearing_date')[:10]

    # Stats
    total_cases = Case.objects.filter(user=request.user).count()
    total_hearings = Hearing.objects.filter(case__user=request.user).count()

    return render(request, 'hearings/home_dashboard.html', {
        'selected_date': date,
        'hearings_for_date': hearings_for_date,
        'upcoming_hearings': upcoming_hearings,
        'today': today,
        'total_cases': total_cases,
        'total_hearings': total_hearings,
         'user_cases': user_cases,
    })



@login_required
def dashboard_view(request):
    selected_date = request.GET.get('date')
    
    if selected_date:
        try:
            date = selected_date
        except:
            date = now().date()
    else:
        date = now().date()

    hearings = Hearing.objects.filter(
        case__user=request.user,
        hearing_date=date
    ).select_related('case').order_by('hearing_date')

    return render(request, 'hearings/dashboard.html', {
        'hearings': hearings,
        'selected_date': date
    })




@login_required
def add_hearing(request, case_id):
    case = get_object_or_404(Case, id=case_id, user=request.user)
    if request.method == 'POST':
        form = HearingForm(request.POST)
        if form.is_valid():
            hearing = form.save(commit=False)
            hearing.case = case
            hearing.save()
            return redirect('hearings:view_hearings', case_id=case.id)
    else:
        form = HearingForm()
    return render(request, 'hearings/add_hearing.html', {'form': form, 'case': case})

@login_required
def view_hearings(request, case_id):
    case = get_object_or_404(Case, id=case_id, user=request.user)
    hearings = case.hearings.order_by('-hearing_date')
    return render(request, 'hearings/view_hearings.html', {'case': case, 'hearings': hearings})
