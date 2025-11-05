import json
from django.db.models import OuterRef, Subquery
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Dashboard, System, Deployment

@csrf_exempt
@require_POST
def add_deployment(request, dashboard_slug, system_slug):
    try:
        dashboard = get_object_or_404(Dashboard, slug=dashboard_slug)
        system = get_object_or_404(System, dashboard=dashboard, slug=system_slug)

        data = json.loads(request.body)
        git_hash = data.get('git_hash')
        git_link = data.get('git_link')

        if not git_hash:
            return HttpResponseBadRequest("git_hash is required")

        deployment = Deployment.objects.create(
            system=system,
            git_hash=git_hash,
            git_link=git_link
        )

        return JsonResponse({
            'status': 'success',
            'deployment_id': deployment.id
        }, status=201)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def dashboard_list(request):
    dashboards = Dashboard.objects.all()
    return render(request, 'main/dashboard_list.html', {'dashboards': dashboards})

def dashboard_detail(request, dashboard_slug):
    dashboard = get_object_or_404(Dashboard, slug=dashboard_slug)

    latest_deployment = Deployment.objects.filter(
        system=OuterRef('pk')
    ).order_by('-timestamp')

    systems = dashboard.systems.annotate(
        latest_deployment_git_hash=Subquery(latest_deployment.values('git_hash')[:1]),
        latest_deployment_git_link=Subquery(latest_deployment.values('git_link')[:1]),
        latest_deployment_timestamp=Subquery(latest_deployment.values('timestamp')[:1]),
    ).all()

    return render(request, 'main/dashboard_detail.html', {'dashboard': dashboard, 'systems': systems})
