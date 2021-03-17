from __main__ import bcrypt
import datetime
from flask import url_for, redirect
from flask_admin.form.upload import ImageUploadField
from flask_admin.contrib.sqla import ModelView
from flask_login.utils import current_user
from path import FILE_UPLOAD_DIR 
from wtforms.fields import TextField, DateTimeField, SelectField, PasswordField
from utils.fields import MultipleImageUploadField
from utils.models import PageTypes 
 
def prefix_name(obj, file_data):
    return file_data.filename
    
class LoginView(ModelView):  
    def is_accessible(self):  
        return current_user.is_authenticated 
            
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login')) 

class AdminView(LoginView):          
    def on_model_change(self, form, model, is_created):
        model.password = bcrypt.generate_password_hash(model.password).decode('utf8')
        # as another example 
        if is_created:
            model.confirmed_at = datetime.datetime.now()    

    form_extra_fields = {
        'password': PasswordField() 
    }

class SlideView(LoginView):     
    column_exclude_list = ['imgs',] 
    form_extra_fields = {
        'imgs': MultipleImageUploadField(
            'Images',
            base_path = FILE_UPLOAD_DIR,  
            thumbnail_size=(100, 100, True),
            namegen=prefix_name, 
        )
    } 
                              
class HighlightView(LoginView):    
    column_exclude_list = ['imgs',] 
    form_extra_fields = {
        'postdate': DateTimeField(),
        'author': TextField(),
        'imgs': MultipleImageUploadField(
            'Images',
            base_path = FILE_UPLOAD_DIR,  
            thumbnail_size=(100, 100, True),
            namegen=prefix_name, 
        )
    }   
        
class PageView(LoginView):
    column_exclude_list = ['imgs',] 
    form_extra_fields = {
        'type': SelectField('Type of Page', choices=PageTypes),
        'postdate': DateTimeField(),
        'author': TextField(), 
        'imgs': MultipleImageUploadField(
            'Images',
            base_path = FILE_UPLOAD_DIR,  
            thumbnail_size=(100, 100, True), 
            namegen=prefix_name, 
        )
    }    

class MemberView(LoginView):
    column_exclude_list = ['selfie',] 
    form_extra_fields = { 
        'selfie': MultipleImageUploadField(
            'Selfie Image',  
            base_path = FILE_UPLOAD_DIR,  
            thumbnail_size=(100, 100, True),
            namegen=prefix_name,  
        ) 
    }    
    
