from django.db import models
from django.contrib.auth.models import User
import datetime
import pytz
# Create your models here.

import string
import random
def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

class URLShortener(models.Model):
	created_by = models.ForeignKey(User)
	longurl = models.CharField(max_length=300)
	create_date = models.DateTimeField('date_started')
	end_date = models.DateTimeField('date_ended')
	uuid = models.CharField(max_length=10, unique=True, primary_key=True)
	visits = models.IntegerField(default=0)
	users_visible_to = models.ManyToManyField(User, blank=True, related_name='visible_to')
	def save(self, *args, **kwargs):
		if(self.uuid==None or self.uuid==''):
			newid = id_generator()
			self.uuid = newid
			while not URLShortener.objects.filter(pk=newid).count() == 0:
				newid = id_generator()
				self.uuid = newid
			self.create_date=datetime.datetime.now()
		super(URLShortener, self).save(*args, **kwargs)
	def present_or_past(self):
		present = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
		if self.end_date < present:
			return "Expired" 
		else:
			delta = self.end_date - present
			str_del = str(delta.days)+" days, "+str(delta.seconds//3600%24)+" hours, "+str((delta.seconds//60)%60)+" minutes"
			return str_del





