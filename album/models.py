from django.db import models

# Create your models here.
from datetime import datetime
from accounts.models import User

class Music(models.Model):
	title 			= models.CharField(max_length=100, blank=True, null=True)
	dance_ability   = models.IntegerField(blank=True, null=True)
	energy 			= models.FloatField(blank=True, null=True)
	mode 			= models.IntegerField(blank=True, null=True)
	acousticness 	= models.FloatField(blank=True, null=True)
	tempo 			= models.FloatField(blank=True, null=True)
	Duration_ms 	= models.IntegerField(blank=True, null=True)
	Num_sections 	= models.IntegerField(blank=True, null=True)
	Num_segments 	= models.IntegerField(blank=True, null=True)
	created_on      = models.DateTimeField(default=datetime.now())

	def __str__(self):
		return self.title


class Ratings(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='review_user')
    rating = models.DecimalField(max_digits=5,decimal_places=1, default=0.0,blank=False, null=True)
    music = models.ForeignKey(Music, on_delete=models.CASCADE, blank=False, null=False)

    created_on = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return str(self.id)