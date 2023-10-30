from django.contrib import admin
from django.urls import path
from . import views

app_name='myapp'

urlpatterns = [
    path('home/',views.ProductsListView.as_view(),name='home'),
    path('product/<int:pk>/',views.ProductsDetailView.as_view(),name='product_detail'),
    path('product/add/',views.addproduct,name='addproduct'),
    path('product/update/<int:id>',views.Update,name='update'),
    path('product/delete/<int:id>',views.Delete,name='delete'),
    path('product/mylistings',views.listings,name='mylistings'),
    path('success/',views.PaymentSuccessView.as_view(),name='success'),
    path('failed/',views.PaymentFailedView.as_view(),name='failed'),
    path('api/checkout-session/<id>',views.create_checkout_session,name='apicheckoutsession'),
    path('about',views.about,name='about'),

    


]
