from django.views import generic
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.exceptions import SuspiciousOperation
from django.core import serializers
from django.shortcuts import redirect
import models
import json
from forms import ProductForm


class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        try:
            meal = models.Meal.objects.get(user=self.request.user)
        except models.Meal.DoesNotExist:
            meal = None
        context.update({"title": "Home", 'meal': meal})
        return context


class ProductListView(generic.ListView):
    model = models.Product
    template_name = 'product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context.update({"title": "Product List"})
        context.update({'object_list': models.Product.objects.all().extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')})
        return context


def get_products(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = models.Product.objects.filter(name__icontains=q)[:20]
        results = []
        for product in products:
            product_json = {}
            product_json['id'] = product.pk
            product_json['label'] = product.name
            product_json['name'] = product.name
            product_json['unit_weight'] = float(product.unit_weight or 0)
            product_json['ww'] = float(product.ww)
            product_json['wbt'] = float(product.wbt)
            results.append(product_json)
        data = json.dumps(results)
    else:
        raise SuspiciousOperation("get_products does not like NON-ajax requests!")
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


class ProductUpdateView(generic.UpdateView):
    model = models.Product
    template_name = 'product_form.html'
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context.update({"action": "Update"})
        return context

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise SuspiciousOperation("ProductUpdateView does not like non-ajax POST requests!")
        form = ProductForm(request.POST)
        if form.is_valid():
            product = self.get_object()
            product.name = form.cleaned_data['name']
            # product.description = form.cleaned_data['description']
            product.protein = form.cleaned_data['protein']
            product.carbo = form.cleaned_data['carbo']
            product.fat = form.cleaned_data['fat']
            product.unit_weight = form.cleaned_data['unit_weight']
            product.cal = form.cleaned_data['cal']
            product.save()
            return JsonResponse(product.to_json())
        else:
            response = render_to_response('product_form.html', {'form': form}, context_instance=RequestContext(request))
            response.status_code = 400
            return response


class ProductCreateView(generic.CreateView):
    model = models.Product
    template_name = 'product_form.html'
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context.update({"action": "Create"})
        return context

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise SuspiciousOperation("ProductUpdateView does not like non-ajax POST requests!")
        form = ProductForm(request.POST)
        if form.is_valid():
            product = models.Product()
            product.name = form.cleaned_data['name']
            # product.description = form.cleaned_data['description']
            product.protein = form.cleaned_data['protein']
            product.carbo = form.cleaned_data['carbo']
            product.fat = form.cleaned_data['fat']
            product.unit_weight = form.cleaned_data['unit_weight']
            product.cal = form.cleaned_data['cal']
            product.save()
            success_message = "Product '{}' has been created".format(product.name)
            messages.success(self.request, success_message)
            return JsonResponse({'refresh': True})
        else:
            response = render_to_response('product_form.html', {'form': form}, context_instance=RequestContext(request))
            response.status_code = 400
            return response


class ProductDeleteView(generic.UpdateView):
    model = models.Product

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise SuspiciousOperation("ProductDeleteView does not like non-ajax POST requests!")
        href = request.POST.get('href')
        name = self.get_object().name
        self.get_object().delete()
        messages.success(request, "Product '{}' has been deleted".format(name))
        return redirect(href)


class MealUpdateView(generic.UpdateView):
    model = models.Meal

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise SuspiciousOperation("MealUpdateView does not like non-ajax POST requests!")
        user = request.user
        try:
            meal = user.meal
        except models.Meal.DoesNotExist:
            meal = models.Meal(user=user)
            meal.save()

        for existing_meal_element in meal.meal_elements.all():
            existing_meal_element.delete()

        post_meal_elements = json.loads(request.POST.get('meal_elements'))
        print "post els: ", post_meal_elements, type(post_meal_elements)
        meal.meal_elements.clear()
        for element in post_meal_elements:
            product_id = element.get('id')
            try:
                product = models.Product.objects.get(id=product_id)
            except models.Product.DoesNotExist:
                return JsonResponse({'error': 'Product with id="{}" does not exist in the datastore.'.format(product_id)}, status=400)
            meal_element = models.MealElement(product=product)
            meal_element.amount = element.get('amount') or 1
            meal_element.in_grams = element.get('in_grams')
            meal_element.save()
            meal.meal_elements.add(meal_element)
        meal.ratio = request.POST.get('ratio', 1)
        try:
            meal.ratio = float(meal.ratio)
        except ValueError:
            meal.ratio = 1
        meal.save()
        return JsonResponse({})
