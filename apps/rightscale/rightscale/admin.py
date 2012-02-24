from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import UserRightScaleProfile
from django.forms.widgets import PasswordInput

admin.site.unregister(User)


class UserRightScaleProfileInline(admin.StackedInline):
    model = UserRightScaleProfile
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name =='rightscale_password':
            kwargs['widget'] = PasswordInput
        return super(UserRightScaleProfileInline, self).formfield_for_dbfield(db_field,**kwargs)
        
    
class UserRightScaleProfileAdmin(UserAdmin):
    inlines = [UserRightScaleProfileInline]
    
admin.site.register(User, UserRightScaleProfileAdmin)