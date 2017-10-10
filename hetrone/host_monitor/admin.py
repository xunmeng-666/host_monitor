from django.contrib import admin
from django import forms
from host_monitor.admin_base import site
# Register your models here.
from host_monitor import models
from host_monitor.admin_base import site,BaseAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField




class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.Account
        fields = ('email', 'name','is_active','is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.Account
        fields = ('email', 'password', 'name', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class AccountAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email', 'name','is_active')
    list_filter = ('id','邮箱','姓名','是否激活')
    fieldsets = (
        ('test', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active',)}),
        ('AuditPermission', {'fields': ('bind_host_users','host_groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('user_permissions','groups','bind_host_users','host_groups')


# class HostUserAdmin(BaseAdmin):
#     list_display = ['username','auth_type','password']

class HostInfoAdmin(BaseAdmin):
    list_display = ('id','hostname', 'ip_address', 'port', 'idc',)
    list_filter = ('id','主机名','IP地址','端口号','机房')
    search_fields = ['hostname', 'ip_address']
    list_per_page = 5
    filter_horizontal = ('hostname', 'ip_address', 'port', 'idc','system_user', )

    def test(self,*args,**kwargs):
        print('admin',self,args,kwargs)

class HostGroupAdmin(BaseAdmin):
    list_display = ('group_name','accounts')
    list_filter = ('主机组名','所属用户')
    search_fields = ['group_name', 'accounts']
# Now register the new UserAdmin...

class MonitorInfo():
    list_display = ('主机地址','CPU使用率','内存使用率','硬盘使用率','入口流量','出口流量',)
    list_filter = ('ip_address','cpu_use','ram_use','disk_use','host_input','host_output')
    list_per_page = 50

class IDCInfo(BaseAdmin):
    list_display = ('name','address')
    list_filter = ('机房名称','所在位置')
    search_fields = ['name','address']

class EmailAdmin(BaseAdmin):
    list_display = ('账号','密码','发件服务器','SSL','端口','TLS','收件人')
    list_filter = ('user','password','host','ssl','ssl_port','tls','from_user')

site.register(models.Host,HostInfoAdmin)
site.register(models.HostGroup,HostGroupAdmin)
site.register(models.Account, AccountAdmin)
site.register(models.HostUser,)
site.register(models.IDC,IDCInfo)
site.register(models.AuditLog)
site.register(models.BindHostUser)
site.register(models.Monitor,MonitorInfo)
site.register(models.Email,EmailAdmin)


