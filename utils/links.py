from flask_admin.menu import MenuLink
from flask_login.utils import current_user

class LoginMenuLink(MenuLink):
    def is_accessible(self):
        return not current_user.is_authenticated 

class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated      