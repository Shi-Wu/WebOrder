from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from management import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LM.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', views.home, name='home'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^history/order_list/$', views.order_list,name='order_list'),
    url(r'^history/', views.history, name='history'),
    url(r'^about/', views.about, name='about'),
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup,name='signup'),
    url(r'^order/$', views.order,name='order'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^setpassword/$', views.setpassword, name='set_password'),
    url(r'^add/$', views.add, name='add_instrument'),
    url(r'^add_to_cart/$', views.add_to_cart, name='add_to_cart'),
    url(r'^delete_from_cart/$', views.delete_from_cart, name='delete_from_cart'),
    url(r'^view/$', views.view, name='view_instrument'),
    url(r'^view/detail/$', views.detail, name='view_detail'),
    url(r'^image/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_PATH}),
)
