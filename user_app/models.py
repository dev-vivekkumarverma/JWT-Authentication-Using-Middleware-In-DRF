from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, User
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Department(models.Model):
    id=models.CharField(primary_key=True,blank=False,max_length=100)
    name=models.CharField(unique=True,blank=False,null=False,max_length=100)

    def __str__(self):
        return f"{self.name}"


class Role(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True,blank=False)
    tag=models.CharField(unique= True, blank=True,max_length=100)

    def __str__(self):
        return f"{self.tag}"

class CustomUser(models.Model):
    is_active=True
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    username=models.CharField(unique=True, blank= False, null=False,db_index=True,max_length=100)
    password=models.CharField(blank= False, null=False,max_length=100)
    email=models.EmailField(null=False,blank=False, unique=True,max_length=100)
    role=models.ForeignKey(Role,on_delete=models.SET_NULL,null=True)
    dept=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    first_name=models.CharField(null=False, blank=False,max_length=100)
    middle_name=models.CharField(null=True, blank=True,max_length=100)
    last_name=models.CharField(null=True, blank=True,max_length=100)


    def is_active_user(self):
        return self.is_active
    
    def set_password(self,password):
        self.password=make_password(password=password)


    def deactivate_user(self):
        self.is_active=False
        return not self.is_active
        
    def create_user(self, username:str,email:str,password:str,first_name:str,role_id:int=None, dept_id:int=None, last_name:str=None,middle_name:str=None):
        
        try:
            self.username=username.strip()
            self.password=password
            self.email=email.strip()
            self.role=role_id
            self.dept=dept_id
            self.first_name=first_name.strip()
            self.last_name=last_name.strip()
            self.middle_name=middle_name.strip()
            self.save()
            return (True,"successed")
            
        except Exception as e:
            return (False, str(e))
        
    def save(self, *args, **kwargs):
        print("before hash:",self.password)
        self.set_password(password=self.password)
        print("after hash:",self.password)
        super(CustomUser, self).save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.username}"
        
    


    def validate_password(self,password:str):
        return check_password(password=password, encoded=self.password)

