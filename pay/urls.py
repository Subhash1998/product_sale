from django.conf.urls import url
from pay import views
from django.conf import settings
from django.contrib.auth.views import logout,password_reset,password_reset_done,password_reset_confirm,password_reset_complete
from django.contrib.auth import views as auth_views	 
 
app_name = "pay"
urlpatterns = [
	url(r'^$', views.homepage, name="home"),
	url(r'^register/$', views.signup, name="signup"),
	url(r'^login/$', views.user_login, name="login"),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^search/$', views.search_view, name='search'),
	url(r'^profile/$',views.profile, name="profile"),
	url(r'^profile/cart/$', views.mycart, name="mycart"),
	url(r'^profile/order/$', views.myorder, name="myorder"),
	url(r'^profile/profile_info/$', views.profile_info, name="profile_info"),
	url(r'^profile/edit_address/$',views.edit_address,name='edit_address'),
	url(r'^profile/edit_mobile/$',views.edit_mobile,name='edit_mobile'),
	url(r'^profile/edit_image/$',views.edit_image,name='edit_image'),
	url(r'^profile/add_cart/(?P<p_id>[0-9]+)/$',views.cart,name='cart'),
	url(r'^profile/(?P<pk>[0-9]+)/delete_cart/$',views.delete_cart.as_view(),name='delete_cart'),
	url(r'^profile/(?P<pk>[0-9]+)/delete_order/$',views.delete_order.as_view(),name='delete_order'),
    url(r'^payment/(?P<p_id>[0-9]+)/$', views.payment, name="payment"),
    url(r'^direct_payment/(?P<p_id>[0-9]+)/$', views.direct_payment, name="direct_payment"),
    url(r'^make_payment/(?P<p_id>[0-9]+)/$', views.make_payment, name="make_payment"),
    url(r'^payment/success$', views.payment_success, name="payment_success"),
    url(r'^payment/failure$', views.payment_failure, name="payment_failure"),



    url(r'^password_reset/$',password_reset,{'template_name': 'pay/password_reset_form.html'},name='password_reset'),
    url(r'^password_reset/done/$',password_reset_done,{'template_name': 'pay/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',password_reset_confirm,{'template_name': 'pay/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$',password_reset_complete,{'template_name': 'pay/password_reset_complete.html'},name='password_reset_complete'),
]
