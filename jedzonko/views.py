import random
from datetime import datetime
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import Recipe, Plan, DAY_NAME, DayName, RecipePlan, Page
from jedzonko.models import Recipe, Plan, DAY_NAME, DayName, RecipePlan
from django.http import Http404


class IndexView(View):

    def get(self, request):
        recipes = Recipe.objects.all()
        plans = Plan.objects.all().order_by('-created')
        if recipes and plans:
            random_recipes = random.choices(recipes, k=3)
            plan = plans[0]
            ctx = {"actual_date": datetime.now(), 'recipes': random_recipes, 'plan': plan}
            return render(request, "index.html", ctx)
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


class RecipeListLinkView(View):
    def get(self, request):
        recipes_list = Recipe.objects.all().order_by('-votes').order_by('-created')
        paginator = Paginator(recipes_list, 5)  # 5 przepisows na stronie( a nie 50)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {'recipes': recipes})


class DashboardView(View):

    def get(self, request):
        recipe_counter = Recipe.objects.count()
        plan_counter = Plan.objects.count()

        plans = Plan.objects.all().order_by('-created')
        plan = plans[0]

        recipe_plans = RecipePlan.objects.filter(plan=plan).order_by('day_name')
        days_in_plan = sorted(list(set(day.day_name.day for day in recipe_plans)))
        return render(request, 'dashboard.html', {'plan_counter': plan_counter,
                                                  'recipe_counter': recipe_counter,
                                                  'plan': plan,
                                                  'recipe_plans': recipe_plans,
                                                  'day_name': DAY_NAME,
                                                  'days_in_plan': days_in_plan})


class PlanListView(View):
    def get(self, request):
        plans_list = Plan.objects.all().order_by('name')
        paginator = Paginator(plans_list, 5)  # 5 przepisows na stronie( a nie 50)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, 'app-schedules.html', {'plans': plans})


class AddPlanView(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        plan_name = request.POST['plan_name']
        plan_description = request.POST['plan_description']
        if plan_name and plan_description:
            plan = Plan.objects.create(name=plan_name, description=plan_description)
            return redirect("/plan/list/")
        return render(request, 'app-add-schedules.html', {'message': 'Wypełnij poprawnie wszystkie pola'})


class AddRecipeToPlanView(View):
    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        return render(request, 'app-schedules-meal-recipe.html', {'plans': plans, 'recipes': recipes, 'days': DAY_NAME})

    def post(self, request):
        plan = request.POST.get('plan')
        nazwa_posilku = request.POST.get('nazwa_posilku')
        numer_posilku = request.POST.get('numer_posilku')
        recipe = request.POST.get('recipe')
        day = request.POST.get('day')

        recipe_object = Recipe.objects.get(name=recipe)
        plan_object = Plan.objects.get(name=plan)
        new_day_name = DayName.objects.create(day=day)
        new_recipe_plan = RecipePlan.objects.create(recipe=recipe_object, plan=plan_object, day_name=new_day_name,
                                                    meal_name=nazwa_posilku, order=numer_posilku)
        return redirect(f"/plan/{plan_object.id}/")


class RecipeDetailsView(View):
    def get(self, request, id):
        return render(request, 'app-recipe-details.html',
                      {'recipe': Recipe.objects.get(pk=id)})

    def post(self, request, id):
        dk = request.POST.get('id')
        kb = request.POST.get('id_dislike')
        if dk:
            recipe = Recipe.objects.get(pk=dk)
            recipe.votes += 1
            recipe.save()
            return redirect(f"/recipe/{dk}/")
        if kb:
            recipe = Recipe.objects.get(pk=kb)
            recipe.votes -= 1
            recipe.save()
            return redirect(f"/recipe/{kb}/")


class ModifyRecipeView(View):
    def get(self, request, id):
        przepis = get_object_or_404(Recipe, pk=id)
        return render(request, 'app-edit-recipe.html', {'recipe': przepis})

    def post(self, request, id):
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        preparing_method = request.POST.get('preparing_method')
        if name and ingredients and description and preparation_time and preparing_method:
            rec = Recipe.objects.get(pk=id)
            rec.name = name
            rec.ingredients = ingredients
            rec.description = description
            rec.preparation_time = preparation_time
            rec.preparing_method = preparing_method
            rec.save()
            return redirect('/recipe/list/')
        return render(request, 'app-edit-recipe.html', {'message': 'Wypełnij poprawnie wszystkie pola'})


class PlanDetailsView(View):
    def get(self, request, id):
        plan = Plan.objects.get(pk=id)
        try:
            recipe_plans = RecipePlan.objects.filter(plan=plan).order_by('day_name')
            days_in_plan = sorted(list(set(day.day_name.day for day in recipe_plans)))
            return render(request, 'app-details-schedules.html',
                          {'plan': plan, 'recipe_plans': recipe_plans, 'day_name': DAY_NAME,
                           'days_in_plan': days_in_plan})
        except RecipePlan.DoesNotExist:
            return render(request, 'app-details-schedules.html', {'plan': plan})


class AddRecipeView(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')

    def post(self, request):
        name = request.POST['name']
        ingredients = request.POST['ingredients']
        description = request.POST['description']
        preparation_time = request.POST['preparation_time']
        preparing_method = request.POST['preparing_method']
        if name and ingredients and description and preparation_time and preparing_method:
            recipe = Recipe.objects.create(name=name, ingredients=ingredients, description=description,
                                           preparation_time=preparation_time, preparing_method=preparing_method)
            return redirect("/recipe/list/")
        return render(request, 'app-add-recipe.html', {'message': 'Wypełnij poprawnie wszystkie pola'})


class AboutApplicationView(View):
    def get(self, request):
        article = Page.objects.get(slug='najlepsze-papu-w-galaktyce')
        return render(request, 'about_app.html', {'article': article})


class ContactView(View):
    def get(self, request):
        contact = Page.objects.get(slug='nasze-dane-kontaktowe')
        return render(request, 'kontakt.html', {'contact': contact})
