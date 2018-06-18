from django.shortcuts import render, redirect , render_to_response
from django.conf import settings
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import logging, traceback
import pay.constants as constants
import pay.config as config
import hashlib
#import requests
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .forms import UserForm,EditAddress,EditMobile,SearchForm,EditImage
from .models import Product,UserProfile,Cart,Order
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy, resolve
# import urllib # Python URL functions
# import urllib2 # Python URL functions


def homepage(request):
    return render(request,'pay/index.html')

def signup(request):
    context=RequestContext(request)
    registered=False
    if request.method=='POST':         
        form=UserForm(data=request.POST)
        if form.is_valid():
#             recaptcha_response = request.POST.get('g-recaptcha-response')
#             url = 'https://www.google.com/recaptcha/api/siteverify'
#             values = {
#                 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
#                 'response': recaptcha_response
#             }
#             data = urllib.urlencode(values)
#             req = urllib2.Request(url, data)
#             response = urllib2.urlopen(req)
#             result = json.load(response)
            ''' End reCAPTCHA validation '''

            first_name=form.cleaned_data['first_name']
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=form.save()
            user.set_password(user.password)
            user.save()
#             authkey = "210112APJgCTharC5ad321b5" # Your authentication key.

#             mobiles = "919340114842" # Multiple mobiles numbers separated by comma.

#             message = "Test message" # Your message to send.

#             sender = "112233" # Sender ID,While using route4 sender id should be 6 characters long.

#             route = "default" # Define route

#             # Prepare you post parameters
#             values = {
#                       'authkey' : authkey,
#                       'mobiles' : mobiles,
#                       'message' : message,
#                       'sender' : sender,
#                       'route' : route
#                       }


#             url = "http://api.msg91.com/api/sendhttp.php" # API URL

#             postdata = urllib.urlencode(values) # URL encoding the data here.

#             req = urllib2.Request(url, postdata)

#             response = urllib2.urlopen(req)

#             output = response.read() # Get Response



            registered=True
            return redirect('/pay/')   
        else:
            print(form.errors)
    else:
        form=UserForm()

    return render_to_response('pay/index.html',{'form':form,'registered':registered},context)


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                response=False
                login(request,user)
                return HttpResponseRedirect('/pay/profile/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            response=True
            return render(request,'pay/index.html',{'response':response})
           
    else:
        return render_to_response('pay/index.html', {}, context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/pay/login/')

@login_required
def search_view(request):
    cart=Cart.objects.all()
    data = Product.objects.all()
    form = SearchForm()
    if request.method=='POST':
        q = request.POST.get('q')
        data = data.filter(p_name__icontains=q)
                # return render(request,'pay/search.html',{'countries':countries})
    return render(request, "pay/search.html",
            {"form": form,'data':data,'cart':cart})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@login_required
def profile(request):
    cart=Cart.objects.all()
    data=Product.objects.all()
    paginator = Paginator(data, 4) # Show 25 contacts per page

    page = request.GET.get('page')

    try:

        contacts = paginator.page(page)

    except PageNotAnInteger:

        # If page is not an integer, deliver first page.

        contacts = paginator.page(1)

    except EmptyPage:

        # If page is out of range (e.g. 9999), deliver last page of results.

        contacts = paginator.page(paginator.num_pages)
    args={'user':request.user}
    return render(request,'pay/profile_product.html',{'data':data,'cart':cart,'contacts':contacts},args)

@login_required
def profile_info(request):
    cart=Cart.objects.all()
    args={'user':request.user}
    return render(request,'pay/profile_info.html',{'cart':cart},args)

@login_required
def edit_address(request):
   cart=Cart.objects.all()
   if request.method=='POST':
      form = EditAddress(request.POST)
      if form.is_valid():
         a=UserProfile.objects.get(user_id=request.user.id)
         a.address=request.POST.get('address')
         a.save()
         return redirect('/pay/profile/profile_info')
   else:
      form= EditAddress()
   return render(request,'pay/profile_info.html',{'form':form,'cart':cart})

@login_required
def edit_mobile(request):
   u=User.objects.get(id=request.user.id)
   print(u)
   form = EditMobile(instance=request.user)
   if request.method=='POST':
      form = EditMobile(request.POST)
      if form.is_valid():
         print("xxxxxxxxxxxx")
         u.email=form.cleaned_data['email']
         u.first_name=form.cleaned_data['first_name']
         u.save()
         a=UserProfile.objects.get(user_id=request.user.id)
         a.mobile=request.POST.get('mobile')
         a.address=form.cleaned_data['address']
         a.save()
         return redirect('/pay/profile/profile_info')
   else:
      form= EditMobile()
   return render(request,'pay/profile_info.html',{'form':form})


def edit_image(request):
    if request.method=='POST':
        image_form = EditImage(request.FILES)
        if image_form.is_valid():
            a=UserProfile.objects.get(user_id=request.user.id)
            if 'image' in request.FILES:
                a.image = request.FILES['image']
                a.save()
        return redirect('/pay/profile/profile_info')
    else:
            image_form= EditImage()
    return render(request,'pay/profile_info.html',{'image_form':image_form})     



@login_required
def cart(request,p_id):
    product=get_object_or_404(Product,pk=p_id)
    carts=Cart()
    carts.cart_pname=product.p_name
    carts.cart_pprice=product.p_price
    carts.cart_pimage=product.p_image
    carts.cart_pdescription=product.p_description
    ob=UserProfile.objects.get(user_id=request.user.id)
    carts.model=ob
    carts.save()
    return redirect('/pay/profile/')

@login_required
def mycart(request):
    ob=UserProfile.objects.get(user_id=request.user.id)
    cart=Cart.objects.all()
    return render(request,'pay/cart.html',{'cart':cart,'ob':ob})

@login_required
def myorder(request):
    cart=Cart.objects.all()
    ob=UserProfile.objects.get(user_id=request.user.id)
    order=Order.objects.all()
    return render(request,'pay/order.html',{'order':order,'ob':ob,'cart':cart})


class delete_cart(DeleteView):
    model=Cart
    success_url=reverse_lazy('pay:mycart')


class delete_order(DeleteView):
    model=Order
    success_url=reverse_lazy('pay:myorder')

@login_required
def payment(request,p_id):   
    product=get_object_or_404(Cart,pk=p_id)
    ob=UserProfile.objects.get(user_id=request.user.id)
    ob2=Order()
    ob2.order_product=product.cart_pname
    ob2.order_price=product.cart_pprice
    ob2.order_payment_status="Not done"
    ob2.order_cart="Not added"
    ob2.order_image=product.cart_pimage
    ob2.order_description=product.cart_pdescription
    PAID_FEE_AMOUNT = str(product.cart_pprice)
    PAID_FEE_PRODUCT_INFO = str(product.cart_pdescription)
    data = {}
    txnid = get_transaction_id()
    ob2.order_txn_id=txnid
    ob2.order=ob
    ob2.save()
    # hash_ = generate_hash(request, txnid)
    #hash_string = get_hash_string(request, txnid)
    # use constants file to store constant values.
    # use test URL for testing
    data["action"] = constants.PAYMENT_URL_LIVE 
    data["amount"] = PAID_FEE_AMOUNT
    data["productinfo"]  = PAID_FEE_PRODUCT_INFO
    data["key"] = config.KEY
    data["txnid"] = txnid

    first_name=request.user.first_name
    user_email=request.user.email
    print(user_email)
    data["name"] = str(first_name)
    data["email"] = str(user_email)
    data["phone"] = ob.mobile
    data["service_provider"] = constants.SERVICE_PROVIDER
    hash_string = config.KEY+"|"+txnid+"|"+PAID_FEE_AMOUNT+"|"+PAID_FEE_PRODUCT_INFO+"|"
    hash_string += data["name"]+"|"+data["email"]+"|"
    hash_string += "||||||||||"+config.SALT
    data["hash_string"] = hash_string
    hash_ = generate_hash(request, txnid,hash_string)
    data["hash"] = hash_
    print(hash_string)
    data["furl"] = request.build_absolute_uri(reverse("pay:payment_failure"))
    data["surl"] = request.build_absolute_uri(reverse("pay:payment_success"))
    return render(request, "pay/payment_form.html",data) 

@login_required
def make_payment(request,p_id):
    ob2=UserProfile.objects.get(user_id=request.user.id)
    ob=Order.objects.get(id=p_id)   
    PAID_FEE_AMOUNT = str(ob.order_price)
    PAID_FEE_PRODUCT_INFO = str(ob.order_description)
    data = {}
    # hash_ = generate_hash(request, txnid)
    #hash_string = get_hash_string(request, txnid)
    # use constants file to store constant values.
    # use test URL for testing
    data["action"] = constants.PAYMENT_URL_LIVE 
    data["amount"] = PAID_FEE_AMOUNT
    data["productinfo"]  = PAID_FEE_PRODUCT_INFO
    data["key"] = config.KEY
    data["txnid"] = ob.order_txn_id

    first_name=request.user.first_name
    user_email=request.user.email
    print(user_email)
    data["name"] = str(first_name)
    data["email"] = str(user_email)
    data["phone"] = ob2.mobile
    data["service_provider"] = constants.SERVICE_PROVIDER
    hash_string = config.KEY+"|"+ob.order_txn_id+"|"+PAID_FEE_AMOUNT+"|"+PAID_FEE_PRODUCT_INFO+"|"
    hash_string += data["name"]+"|"+data["email"]+"|"
    hash_string += "||||||||||"+config.SALT
    data["hash_string"] = hash_string
    hash_ = generate_hash(request, ob.order_txn_id,hash_string)
    data["hash"] = hash_
    print(hash_string)
    data["furl"] = request.build_absolute_uri(reverse("pay:payment_failure"))
    data["surl"] = request.build_absolute_uri(reverse("pay:payment_success"))
    return render(request, "pay/payment_form.html", data) 

@login_required
def direct_payment(request,p_id):
    product=get_object_or_404(Product,pk=p_id)
    ob2=UserProfile.objects.get(user_id=request.user.id)
    ob=Order()
    ob.order_product=product.p_name
    ob.order_price=product.p_price
    ob.order_payment_status="Not done"
    ob.order_cart="Not added"
    ob.order_image=product.p_image
    ob.order_description=product.p_description
    ob.order_by=str(request.user.username)
    PAID_FEE_AMOUNT = str(product.p_price)
    PAID_FEE_PRODUCT_INFO = str(product.p_description)
    data = {}
    txnid = get_transaction_id()
    ob.order_txn_id=txnid
    ob.order=ob2
    ob.save()
    print(ob.order_id)
    # hash_ = generate_hash(request, txnid)
    #hash_string = get_hash_string(request, txnid)
    # use constants file to store constant values.
    # use test URL for testing
    data["action"] = constants.PAYMENT_URL_LIVE 
    data["amount"] = PAID_FEE_AMOUNT
    data["productinfo"]  = PAID_FEE_PRODUCT_INFO
    data["key"] = config.KEY
    data["txnid"] = txnid
    
    first_name=request.user.first_name
    user_email=request.user.email
    data["name"] = str(first_name)
    data["email"] = str(user_email)
    data["phone"] = ob2.mobile
    data["service_provider"] = constants.SERVICE_PROVIDER
    hash_string = config.KEY+"|"+txnid+"|"+PAID_FEE_AMOUNT+"|"+PAID_FEE_PRODUCT_INFO+"|"
    hash_string += data["name"]+"|"+data["email"]+"|"
    hash_string += "||||||||||"+config.SALT
    data["hash_string"] = hash_string
    hash_ = generate_hash(request, txnid,hash_string)
    data["hash"] = hash_
    data["furl"] = request.build_absolute_uri(reverse("pay:payment_failure"))
    data["surl"] = request.build_absolute_uri(reverse("pay:payment_success"))
    return render(request, "pay/payment_form.html", data) 
    
# generate the hash
def generate_hash(request, txnid,hash_string):
    try:
        # get keys and SALT from dashboard once account is created.
        hashSequence = "key|txnid|amount|productinfo|name|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        #hash_string = get_hash_string(request,txnid)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower() 
        return generated_hash
    except Exception as e:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
 
# create hash string using all the fields
# def get_hash_string(request, txnid):
#     hash_string = config.KEY+"|"+txnid+"|"+str(float(constants.PAID_FEE_AMOUNT))+"|"+constants.PAID_FEE_PRODUCT_INFO+"|"
#     hash_string += "Aman"+"|"+"omkshatri98@gmail.com"+"|"
#     hash_string += "||||||||||"+config.SALT
 
#     return hash_string
 
# generate a random transaction Id.
def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0,9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid
 
# no csrf token require to go to Success page. 
# This page displays the success/confirmation message to user indicating the completion of transaction.
# from reportlab.pdfgen import canvas
# from django.http import HttpResponse
# def some_view(request):
#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

#     # Create the PDF object, using the response object as its "file."
#     p = canvas.Canvas(response)

#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.
#     p.drawString(100, 100, "Hello world.")

#     # Close the PDF object cleanly, and we're done.
#     p.showPage()
#     p.save()
#     return response


import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
import datetime
from xhtml2pdf import pisa 
from django.core.mail import EmailMessage

@csrf_exempt
def payment_success(request):
    data = {}
    ob = Order.objects.filter(order_by=request.user.username)
    ob.update(order_payment_status="Done")
    ob2=ob.latest('order_date')
    data = {'ob2':ob2,'user':request.user}
    template = get_template('pay/success.html')
    html  = template.render(Context(data))
    file = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,encoding='utf-8')
    file.seek(0)
    pdf = file.read()
    file.close()
    msg = EmailMessage("title", "content", to=[request.user.email])
    msg.attach('my_pdf.pdf', pdf, 'application/pdf')
    msg.content_subtype = "html"
    msg.send()
    # return (request, "pay/success.html",{'ob2':ob2})
    return HttpResponse(pdf,'application/pdf')

# no csrf token require to go to Failure page. This page displays the message and reason of failure.
@csrf_exempt
def payment_failure(request):
    data = {}
    return render(request, "pay/failure.html", data)


from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings

class NewSessionMiddleware(SessionMiddleware):

    def process_response(self, request, response):
        response = super(NewSessionMiddleware, self).process_response(request, response)
        #You have access to request.user in this method
        if not request.user.is_authenticated():
            del response.cookies[settings.SESSION_COOKIE_NAME]
        return response
