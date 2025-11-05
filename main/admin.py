from django.contrib import admin
from .models import Dashboard, System, Deployment

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'dashboard', 'slug')
    list_filter = ('dashboard',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = ('system', 'git_hash', 'timestamp')
    list_filter = ('system__dashboard', 'system')
