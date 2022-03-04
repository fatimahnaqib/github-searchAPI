from django.db import models

class Issue(models.Model):
    
    issue_id= models.TextField(unique=True)
    avatar_url =models.TextField(max_length=100,blank=True)
    title= models.TextField(max_length=100,blank=True)
    html_url =models.TextField(max_length=100,blank=True)
    descrip= models.TextField(blank=True,null=True)
    score = models.TextField(blank=True)
    time_stamp=models.DateTimeField(auto_now_add=True, blank=True)
