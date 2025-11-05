from django.db import models
from django.utils.text import slugify

class Dashboard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class System(models.Model):
    dashboard = models.ForeignKey(Dashboard, related_name='systems', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)

    class Meta:
        unique_together = ('dashboard', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.dashboard.name} - {self.name}'

class Deployment(models.Model):
    system = models.ForeignKey(System, related_name='deployments', on_delete=models.CASCADE)
    git_hash = models.CharField(max_length=40)
    git_link = models.URLField(blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.system} - {self.git_hash[:7]} at {self.timestamp}'
