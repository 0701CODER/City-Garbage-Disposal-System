from unicodedata import name
from django.contrib import admin
from django.urls import path
from garbage import views
from django.contrib.auth.views import LoginView,LogoutView

admin.site.site_header = "Zero Trash Admin"
admin.site.site_title = "Zero Trash Admin Portal"
admin.site.index_title = "Welcome to Zero Trash Researcher Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    path('ngoclick', views.ngoclick_view,name='ngoclick'),
    path('disposalclick', views.disposalclick_view,name='disposalclick'),

    path('ngosignup', views.ngo_signup_view,name='ngosignup'),
    path('disposalsignup', views.disposal_signup_view,name='disposalsignup'),
    path('ngologin', LoginView.as_view(template_name='ngologin.html')),
    path('disposallogin', LoginView.as_view(template_name='disposallogin.html')),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='index.html'),name='logout'),

    path('ngo-dashboard', views.ngo_dashboard_view,name='ngo-dashboard'),
    path('ngo-collection', views.ngo_collection_view,name='ngo-collection'),
    path('ngo-notice', views.ngo_notice_view,name='ngo-notice'),
    path('claim-collection/<int:pk1>/<int:pk2>/<str:pk3>', views.claim_collection_view, name='claim-collection'),
    
    path('disposal-dashboard', views.disposal_dashboard_view,name='disposal-dashboard'),
    path('disposal-collection', views.disposal_collection_view,name='disposal-collection'),
    path('claimed-collection', views.claimed_collection_view,name='claimed-collection'),
    path('disposal-collection-history', views.disposal_collection_history_view,name='disposal-collection-history'),

    path('aboutus', views.aboutus_view,name='aboutus'),
    path('contactus', views.contactus_view,name='contactus'),

]

