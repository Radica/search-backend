from django.db import models
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class GithubCache(models.Model):
    github_url = models.URLField(max_length=255, unique=True)
    fetched = models.DateTimeField('time fetched', default=timezone.now)
    json = models.TextField()

    # Override save method to allow `github_url` to be unique and NULL (not present)
    # ref https://docs.djangoproject.com/en/1.8/topics/db/models/#overriding-model-methods
    def save(self, *args, **kwargs):
        self.github_url = self.github_url or None
        super(GithubCache, self).save(*args, **kwargs)

    def __str__(self):
        return self.github_url

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    homepage = models.URLField(max_length=255)
    github_url = models.URLField(max_length=255, unique=True, null=True)
    categories = models.ManyToManyField(Category)

    # Override save method to allow `github_url` to be unique and NULL (not present)
    # ref https://docs.djangoproject.com/en/1.8/topics/db/models/#overriding-model-methods
    def save(self, *args, **kwargs):
        self.github_url = self.github_url or None
        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    homepage = models.URLField(max_length=255)
    github_url = models.URLField(max_length=255, unique=True, null=True)
    github_data = models.ForeignKey(GithubCache, null=True)
    organization = models.ForeignKey(Organization, null=True)
    tags = models.ManyToManyField(Tag)

    # Override save method to allow `github_url` to be unique and NULL (not present)
    # ref https://docs.djangoproject.com/en/1.8/topics/db/models/#overriding-model-methods
    def save(self, *args, **kwargs):
        self.github_url = self.github_url or None
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
