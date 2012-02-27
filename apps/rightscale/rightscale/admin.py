import re

from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.widgets import PasswordInput
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

from righteous import api

from dateutil import parser

from models import UserRightScaleProfile, Deployment, Server

admin.site.unregister(User)
api.config.settings.logged_in = False


def rightscale_connect(user):
    profile = user.get_profile()
    if not api.config.settings.logged_in:
        api.init({'username': profile.rightscale_email,
                 'password': profile.rightscale_password,
                 'default_deployment_id': 222115001,
                 'account_id': 12211}, {}, True)
        if api.login():
            api.config.settings.logged_in = True
    return True
    
def rightscale_refresh_deployments(user):
    rightscale_connect(user)
    deployments = api.list_deployments()
    Deployment.objects.all().update(synced=False)
    Server.objects.all().update(synced=False)
    for deployment in deployments:
        dobj, created = Deployment.objects.get_or_create(href=deployment['href'],
                                                        defaults={
                                                            'nickname': deployment['nickname'],
                                                            'description': deployment['description'],
                                                            'created_at': parser.parse(deployment['created_at']),
                                                            'updated_at': parser.parse(deployment['updated_at']),
                                                            'synced': True
                                                        })
        dobj.synced = True
        dobj.save()
        for server in deployment['servers']:
            sobj, created = Server.objects.get_or_create(href=server['href'],
                                                        defaults={
                                                            'nickname': server['nickname'],
                                                            'created_at': parser.parse(server['created_at']),
                                                            'updated_at': parser.parse(server['updated_at']),
                                                            'server_type': server['server_type'],
                                                            'state': server['state'],
                                                            'deployment': dobj,
                                                            'synced': True
                                                        })
            sobj.synced = True
            sobj.save()

def rightscale_create_deployment(user, nickname, description):
    rightscale_connect(user)
    deployment = api.create_deployment(nickname, description)
    return api.find_deployment(nickname)

def rightscale_shutdown_deployment(request, nickname):
    rightscale_connect(request.user)
    deployment = api.find_deployment(nickname)
    if deployment:
        for server in deployment['servers']:
            if deployment['href']=='https://my.rightscale.com/api/acct/12211/deployments/222115001':
                if server['state']=='operational':
                    messages.add_message(request,
                                         messages.INFO,
                                         'Issuing shutdown (real) command on %s' % server['nickname'])
                    api.stop_server(server['href'])
                else:
                    messages.add_message(request,
                                         messages.INFO,
                                         'Server %s not in operational mode. Shutdown command not sent' % server['nickname'])
            else:
                messages.add_message(request,
                                     messages.INFO,
                                     'Issuing shutdown (simulated) command on %s. Server state is %s.' % (server['nickname'],
                                                                                                          server['state']))
    return True

def rightscale_start_deployment(request, nickname):
    rightscale_connect(request.user)
    deployment = api.find_deployment(nickname)
    if deployment:
        for server in deployment['servers']:
            if deployment['href']=='https://my.rightscale.com/api/acct/12211/deployments/222115001':
                if server['state']=='stopped':
                    messages.add_message(request,
                                         messages.INFO,
                                         'Issuing start (real) command on %s' % server['nickname'])
                    api.start_server(server['href'])
                else:
                    messages.add_message(request,
                                         messages.INFO,
                                         'Server %s is already started or is booting up. Start command not sent' % server['nickname'])
            else:
                messages.add_message(request,
                                     messages.INFO,
                                     'Issuing start (simulated) command on %s. Server state is %s' % (server['nickname'],
                                                                                                      server['state']
                                                                                                      ))
    return True

class UserRightScaleProfileInline(admin.StackedInline):
    model = UserRightScaleProfile
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name =='rightscale_password':
            kwargs['widget'] = PasswordInput
        return super(UserRightScaleProfileInline, self).formfield_for_dbfield(db_field,**kwargs)
        
    
class UserRightScaleProfileAdmin(UserAdmin):
    inlines = [UserRightScaleProfileInline]
    

class DeploymentAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'synced', 'view_servers_link', 'shutdown_link', 'start_link')
    readonly_fields = ('synced', 'created_at', 'updated_at', 'href')
    search_fields = ['nickname']
    
    def view_servers_link(self, obj):
        return mark_safe('<a href="%s/servers/">Go</a>' % obj.id)
    view_servers_link.allow_tags=True
    view_servers_link.short_description='View servers'
    
    def shutdown_link(self, obj):
        info = self.model._meta.app_label, self.model._meta.module_name
        return mark_safe('<a href="%s">Go</a>' % reverse('admin:%s_%s_shutdown' % info, args=(obj.id,)))
    shutdown_link.allow_tags=True
    shutdown_link.short_description='Shutdown'
    
    def start_link(self, obj):
        info = self.model._meta.app_label, self.model._meta.module_name
        return mark_safe('<a href="%s">Go</a>' % reverse('admin:%s_%s_start' % info, args=(obj.id,)))
    start_link.allow_tags=True
    start_link.short_description='Start'
    
    def save_model(self, request, obj, form, change):
        deployment = rightscale_create_deployment(request.user, obj.nickname, obj.description)
        if deployment:
            obj.created_at = parser.parse(deployment['created_at'])
            obj.updated_at = parser.parse(deployment['updated_at'])
            obj.href = deployment['href']
        return super(DeploymentAdmin, self).save_model(request, obj, form, change)
    
    def changelist_view(self, request, extra_context=None):
        #
        return super(DeploymentAdmin, self).changelist_view(request, extra_context=extra_context)
    
    def get_urls(self):
        urls = super(DeploymentAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.module_name
        
        my_urls = patterns('',
            (r'^refresh/$', self.get_all),
            url(r'^(.+)/shutdown/$', self.shutdown, name='%s_%s_shutdown' % info),
            url(r'^(.+)/start/$', self.start, name='%s_%s_start' % info),
            url(r'^(.+)/servers/$', self.servers, name='%s_%s_servers' % info),
        )
        return my_urls + urls
    
    def get_all(self, request):
        rightscale_refresh_deployments(request.user)
        return redirect(reverse('admin:rightscale_deployment_changelist'))
    
    def shutdown(self, request, obj):
        deployment = Deployment.objects.get(pk=obj)
        rs_depl = rightscale_shutdown_deployment(request, deployment.nickname)
        return redirect(reverse('admin:rightscale_deployment_changelist'))
        
    def start(self, request, obj):
        deployment = Deployment.objects.get(pk=obj)
        rs_depl = rightscale_start_deployment(request, deployment.nickname)
        return redirect(reverse('admin:rightscale_deployment_changelist'))
    
    def servers(self, request, obj):
        deployment = Deployment.objects.get(pk=obj)
        messages.add_message(request, messages.INFO, 'Unable to display arrays and RDS instances yet')
        return redirect('%s?q=%s' % (reverse('admin:rightscale_server_changelist'), deployment.nickname))

class ServerAdmin(admin.ModelAdmin):
    search_fields = ['=deployment__nickname']
    

admin.site.register(User, UserRightScaleProfileAdmin)
admin.site.register(Deployment, DeploymentAdmin)
admin.site.register(Server, ServerAdmin)