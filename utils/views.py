from flask import url_for, redirect
from flask_admin.contrib.sqla import ModelView
from flask_login.utils import current_user
from wtforms.fields import TextField, DateTimeField 
from utils.fields import MultipleImageUploadField
from path import FILE_UPLOAD_DIR

class AdminView(ModelView):  
    def is_accessible(self):  
        return current_user.is_authenticated 
            
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login')) 
         
class BlogView(AdminView):   
    def prefix_name(obj, file_data):
        return file_data.filename
           
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
        