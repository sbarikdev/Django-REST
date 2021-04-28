from django.db import models

# Create your models here.
from accounts.models import *


PAYMENT_MODE = (('1','Bank'),('2','UPI'),('3','Card'))
RESPONSE_CODE = (('1','Success'),('2','Failed'))

class Payments(models.Model):
	txn_by 			= models.ForeignKey(User, on_delete=models.CASCADE, related_name='txn_by')
	txn_id 			= models.CharField(unique=True, max_length=30)
	order_id 		= models.CharField(unique=True, max_length=30, blank=True, null=True)
	bank_txn_id 	= models.CharField(blank=True, null=True, max_length=30)
	txn_amount 		= models.IntegerField()
	message 		= models.CharField(max_length=100, blank=True, null=True)
	bank_name 		= models.CharField(max_length=50, blank=True, null=True)
	acc_no 			= models.CharField(max_length=30, blank=True, null=True)
	ifsc_code 		= models.CharField(max_length=20, blank=True, null=True)
	bank_owner_name = models.CharField(max_length=50, blank=True, null=True)
	email 			= models.EmailField(blank=True, null=True)
	phone_no 		= models.CharField(max_length=20, blank=True, null=True)
	currency 		= models.CharField(max_length=30, blank=True, null=True)
	card_no 		= models.CharField(max_length=30, blank=True, null=True)
	card_exp_date 	= models.CharField(max_length=30, blank=True, null=True)
	card_cvv_no 	= models.IntegerField(blank=True, null=True)
	upi_id 			= models.CharField(max_length=30, blank=True, null=True)
	payment_mode 	= models.CharField(max_length=1, choices=PAYMENT_MODE)
	response_code 	= models.CharField(max_length=1, choices=RESPONSE_CODE)
	txn_date 		= models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('txn_id', 'payment_mode')


class Order(models.Model):
	transaction 	= models.ForeignKey(Payments, on_delete=models.PROTECT)
	order_id 		= models.CharField(unique=True, max_length=30, blank=True, null=True)
	order_date 		= models.DateTimeField(auto_now_add=True)



