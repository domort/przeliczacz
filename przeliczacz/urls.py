from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from views import *
from django.conf import settings

urlpatterns = patterns('',
   url(r'^$', login_required(HomeView.as_view()), name="home"),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^logout/$', 'django.contrib.auth.views.logout',
       {'next_page': '/'}, name='logout'),
   url(r'^' + settings.LOGIN_URL + '$', 'django.contrib.auth.views.login',
       {'template_name': 'login.html', "extra_context": {"title": "Login"}}, name='login'),

   url(r'^product/add/$', login_required(ProductCreateView.as_view()), name='product_add'),
   url(r'^product/delete/(?P<pk>.+)/$', login_required(ProductDeleteView.as_view()), name='product_delete'),
   url(r'^product/list/$', login_required(ProductListView.as_view()), name='product_list'),
   url(r'^product/get_products/', get_products, name='get_products'),
   url(r'^product/update/(?P<pk>.+)/$', login_required(ProductUpdateView.as_view()), name='product_update'),
   url(r'^meal/update/$', login_required(MealUpdateView.as_view()), name='meal_update'),
   )