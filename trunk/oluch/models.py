# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.db.models.signals import post_save


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    secondname = models.CharField('Отчество', max_length=100, blank=True)
    #work = models.CharField(max_length=1000, blank=True)
    position = models.CharField(max_length=1000, blank=True)
    hours = models.CharField(max_length=1000, blank=True)
    circles = models.CharField(max_length=1000, blank=True)
    university = models.CharField(max_length=1000, blank=True)
    workplace = models.CharField(max_length=1000, blank=True)
    tel = models.CharField(max_length=1000, blank=True)
    address = models.CharField(max_length=1000, blank=True)  

    def __unicode__(self):
        return self.user.username
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Problem(models.Model):
    number = models.CharField(max_length=10)
    title = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField()
                        

    def __unicode__(self):
        return (self.number + '. ' + self.title) if self.title else self.number

class Submit(models.Model):
    #submit description
    author = models.ForeignKey(User, related_name='submit')
    problem = models.ForeignKey(Problem)
    datetime = models.DateTimeField(auto_now_add=True)

    #marks info
    first_mark = models.IntegerField(default=-2) #-2: not evaluated yet, -1: is evaluatting just now
    first_judge = models.ForeignKey(User, related_name='first_mark_submit', blank=True, null=True)
    first_comment = models.CharField(max_length=1000, blank=True)
    second_mark = models.IntegerField(default=-2)
    second_judge = models.ForeignKey(User, related_name='second_mark_submit', blank=True, null=True)
    second_comment = models.CharField(max_length=1000, blank=True)
    final_mark = models.IntegerField(default=-2)

    #file info
    def filepath(instance, filename):
        return str(instance.author.id) + '_' + instance.problem.number + '_' + filename
    
    file = models.FileField(upload_to=filepath)

    def __unicode__(self):
        if hasattr(self.author, 'lastname'):
            result = self.author.lastname
        else:
            result = self.author.username
        
        if self.problem.title:
            result = result + ', #' + self.problem.number + '. ' + self.problem.title # + ': ' + self.file.url
        else:
            result = result + ', #' + self.problem.number # + ': '  + self.file.url

        return result

admin.site.register(UserProfile)
admin.site.register(Problem)
admin.site.register(Submit)    