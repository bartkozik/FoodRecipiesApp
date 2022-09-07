from django.db import models

# Create your models here.
from django.utils.text import slugify


class Recipe(models.Model):
    name = models.CharField(max_length=225)
    ingredients = models.TextField()
    description = models.TextField()
    preparing_method = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through="RecipePlan")


DAY_NAME = (
    (1, 'Poniedziałek'),
    (2, 'Wtorek'),
    (3, 'Środa'),
    (4, 'Czwartek'),
    (5, 'Piątek'),
    (6, 'Sobota'),
    (7, 'Niedziela')
)


class DayName(models.Model):
    day = models.IntegerField(choices=DAY_NAME)
    # order = models.IntegerField(unique=True)


class RecipePlan(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)
