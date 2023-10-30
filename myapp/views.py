from django.shortcuts import render,redirect
from . models import Products,OrderDetail
from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView

from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy,reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import stripe


# Create your views here.

# def home(request):
#     product=Products.objects.all()
#     produt=request.GET.get('product')
#     paginator=paginator
 
#     context={
#         'products':product
#     }
#     return render(request,'myapp/home.html',context)


class ProductsListView(ListView):
    model=Products
    template_name='myapp/home.html'
    context_object_name='products'
    paginate_by=8
# def product_detail(request,id):
#     product=Products.objects.get(id=id)
#     context={
#         'product':product
#     } 
#     return render(request,'myapp/detail.html',context)

class ProductsDetailView(DetailView):
    model=Products
    template_name='myapp/detail.html'
    context_object_name='product'
    pk_url_kwarg='pk'
    
    def get_context_data(self,**kwargs):
        context = super(ProductsDetailView,self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY 
        return context



@login_required
def addproduct(request):
    if request.method=='POST':
        if all(list(request.POST.values())):
            name=request.POST.get('name')
            price=request.POST.get('price')
            desc=request.POST.get('desc')
            image=request.FILES['upload']
            seller=request.user
            product=Products(name=name,price=price,desc=desc,image=image,seller=seller)
            product.save()


    return render(request,'myapp/addproduct.html')
# class ProductCreateView(CreateView):
#     model=Products
#     fields=['name','price','desc','image','seller']
    



def Update(request,id):
    
    product=Products.objects.get(id=id)
    if request.method=='POST':
        product.name=request.POST.get('name')
        product.price=request.POST.get('price')
        product.desc=request.POST.get('desc')
        product.image=request.FILES['upload']
        product.save()
        return  redirect('/myapp/home')

    context={
        'product':product
    } 

    return render(request,'myapp/updateproduct.html',context)


def Delete(request,id):
    product=Products.objects.get(id=id)
    context={
        'product':product
    } 
    if request.method=='POST':
        product.delete()
        return redirect('/myapp/home')
    
    return render(request,'myapp/delete.html',context)


def listings(request):
    product=Products.objects.filter(seller=request.user)
    context={
        'products':product
    }
    return render(request,'myapp/mylistings.html',context)

@csrf_exempt
def create_checkout_session(request,id):
    import pdb;pdb.set_trace();
    product=get_object_or_404(Products,pk=id)
    stripe.api_key=settings.STRIPE_SECRET_KEY
    checkout_session=stripe.checkout.Session.create(
        # customer_email=request.user.email,
        customer_email="abc@db.com",
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'usd',
                    'product_data':{
                        'name':product.name,
                    },
                    # 'unit_amount':int(product.price*100),
                    'unit_amount':int(200),
                },
                'quantity':1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('myapp:success'))+"?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('myapp:failed')),

    )

    order=OrderDetail()
    order.cutomer_username=request.user.username
    order.product=product
    # order.stripe_payment_intent=checkout_session['payment_intent']
    order.stripe_payment_intent=200
    order.amount=int(product.price*100)
    order.save()
    return JsonResponse({'sessionId':checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name='myapp/payment_success.html'
    def get(self,request,*args,**kwargs):
        session_id=request.GET.get('seesion_id')
        if session_id is None:
            return HttpResponseNotFound()
        session=stripe.checkout.Session.retrieve(session_id)
        stripe.settings.STRIPE_SECRET_KEY
        order=get_object_or_404(OrderDetail,stripe_payment_intent=session.payment_intent)
        order.has_paid=True
        order.save()
        return render(request,self.template_name)
    
class PaymentFailedView(TemplateView):
    template_name='myapp/payment_failed.html'    


def about(request):
    return render(request,'myapp/about.html')


