from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.core.validators import RegexValidator
from datetime import datetime

class Meta:

    app_label = 'ComplaintMS'
class Profile(models.Model):
    typeuser =(('user','user'),('grievance', 'grievance'))
    COL=(('Samudrala','Samudrala'),('Village2','Village2')) #change village names
    user =models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    villagename=models.CharField(max_length=29,choices=COL,blank=False)
    phone_regex =RegexValidator(regex=r'^\d{10,10}$', message="Phone number must be entered in the format:Up to 10 digits allowed.")
    contactnumber = models.CharField(validators=[phone_regex], max_length=10, blank=True) 
    type_user=models.CharField(max_length=20,default='student',choices=typeuser)
    CB=(('ward1',"ward1"),('ward2',"ward2"),('ward3',"ward3"),('ward4',"ward4"),('ward5',"ward5"))
    Ward=models.CharField(choices=CB,max_length=29,default='Ward1')
    def __str__(self):
        return self.villagename
    def __str__(self):
        return self.user.username
    
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

'''@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()'''


class Complaint(models.Model):
    STATUS =((1,'Solved'),(2, 'InProgress'),(3,'Pending'))
    TYPE=(('water',"water"),('road',"road"),('electricity',"electricity"),('streetlight',"streetlight"),('Other',"Other"))
    
    Subject=models.CharField(max_length=200,blank=False,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    
    Type_of_complaint=models.CharField(choices=TYPE,null=True,max_length=200)
    Description=models.TextField(max_length=4000,blank=False,null=True)
    Time = models.DateField(auto_now=True)
    status=models.IntegerField(choices=STATUS,default=3)
    
   
    def __init__(self, *args, **kwargs):
        super(Complaint, self).__init__(*args, **kwargs)
        self.__status = self.status

    def save(self, *args, **kwargs):
        if self.status and not self.__status:
            self.active_from = datetime.now()
        super(Complaint, self).save(*args, **kwargs)
    
    def __str__(self):
     	return self.get_Type_of_complaint_display()
    def __str__(self):
 	    return str(self.user)

class Grievance(models.Model):
    guser=models.OneToOneField(User,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.guser