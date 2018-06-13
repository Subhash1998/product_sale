from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone as django_tz 
from datetime import datetime
from django.conf import settings

class UserProfile(models.Model):
	user = models.OneToOneField(User,blank=False,on_delete=models.CASCADE)
	address=models.CharField(max_length=200,blank=True)
	mobile=PhoneNumberField()
	image=models.ImageField(upload_to='media/images',blank=True)
	def __unicode__(self):
		return self.user.username

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
	    if created:
	        UserProfile.objects.create(user=instance)

	# @receiver(post_save, sender=User)
	# def save_user_profile(sender, instance, **kwargs):
	#     instance.Userprofile.save()


class Product(models.Model):
	p_name=models.CharField(max_length=300)
	p_description=models.TextField(max_length=10000)
	p_price=models.DecimalField(max_digits=20, decimal_places=2)
	p_image=models.ImageField(upload_to='images',blank=True)

	def __str__(self):
          return self.p_name

class Cart(models.Model):
	model=models.ForeignKey(UserProfile,default=True,on_delete=models.CASCADE)
	cart_pname=models.CharField(max_length=300)
	cart_pprice=models.DecimalField(max_digits=20, decimal_places=2,null=True)
	cart_pimage=models.ImageField(upload_to='images',blank=True)
	cart_pdescription=models.TextField(max_length=10000)

	def __str__(self):
          return self.cart_pname

class Order(models.Model):
	order=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
	order_by=models.CharField(max_length=10000)
	order_product=models.CharField(max_length=300)
	order_price=models.DecimalField(max_digits=20, decimal_places=2,null=True)
	order_payment_status=models.CharField(max_length=50)
	order_cart=models.CharField(max_length=30)
	order_image=models.ImageField(upload_to='images',blank=True)
	order_txn_id=models.CharField(max_length=50,blank=True)
	order_description=models.TextField(max_length=10000,blank=True)
	order_date = models.DateTimeField(default=datetime.today)
	def __str__(self):
          return self.order_product


