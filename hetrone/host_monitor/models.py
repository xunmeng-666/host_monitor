from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,PermissionsMixin)

# Create your models here.

class IDC(models.Model):
    name = models.CharField(max_length=64,unique=True)
    address = models.CharField(max_length=64,blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "机房信息"
        verbose_name_plural = "机房信息"

class Host(models.Model):
    """主机表"""

    hostname = models.CharField("主机名",unique=True,max_length=64)
    ip_address = models.GenericIPAddressField("IP地址", unique=True)
    idc = models.ForeignKey("IDC")
    port = models.IntegerField("端口",default=22)
    enabled = models.BooleanField('连接状态',default=False)
    date = models.DateField(auto_now_add=True)
    username = models.CharField('系统用户',default='root',max_length=64)
    auth_type_choices = ((0, 'ssh-password'), (1, 'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choices, default=0)
    password = models.CharField( max_length=128, blank=True, null=True, )
    host_group = models.ForeignKey('HostGroup',blank=True,null=True)
    # user = models.ManyToManyField("HostUser")

    def __str__(self):
        return "%s %s %s %s" %(self.hostname,self.ip_address,self.idc,self.port)
    class Meta:
        verbose_name = '主机信息表'
        verbose_name_plural = '主机信息表'

class HostGroup(models.Model):
    """主机组"""
    group_name = models.CharField(max_length=64,unique=True)
    accounts =  models.ForeignKey("Account",blank=True,null=True)

    def __str__(self):
        return self.group_name
    class Meta:
        verbose_name = '主机组'
        verbose_name_plural = '主机组'

class HostUser(models.Model):
    """主机用户"""
    username = models.CharField('系统用户',max_length=64)
    auth_type_choices = ((0,'ssh-password'),(1,'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choices,default=0)
    password = models.CharField(max_length=128,blank=True,null=True,)

    class Meta:
        unique_together  = ('username','password')
        verbose_name = '系统用户'
        verbose_name_plural = '系统用户'

    def __str__(self):
        return "%s-%s-%s" %(self.username,self.get_auth_type_display(),self.password)
        #root `123
        # root

class BindHostUser(models.Model):
    """实现主机与主机用户的关联，最小粒度的权限"""
    host = models.ForeignKey("Host")
    host_user = models.ForeignKey("HostUser")

    class Meta:
        unique_together = ("host",'host_user')

    def __str__(self):
        return "%s-%s"%(self.host,self.host_user)

class SessionLog(models.Model):
    account = models.ForeignKey("Account")
    bind_host_user = models.ForeignKey("BindHostUser")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return "%s-%s" %(self.account,self.bind_host_user)

class AuditLog(models.Model):
    """审计日志"""
    session = models.ForeignKey("SessionLog")
    cmd = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s-%s" %(self.session,self.cmd)

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Email(models.Model):
    host = models.CharField(max_length=32)
    user = models.EmailField(max_length=32)
    password = models.CharField(max_length=128)
    tls = models.BooleanField(default=False)
    ssl = models.BooleanField(default=True)
    ssl_port = models.IntegerField
    from_user = models.EmailField(max_length=32)





class Monitor(models.Model):
    hostname = models.ForeignKey(Host ,on_delete=models.CASCADE)
    cpu_use = models.CharField(max_length=12)
    cpu_total = models.CharField(max_length=12)
    ram_use = models.CharField(max_length=12)
    ram_total = models.CharField(max_length=12)
    disk_use = models.CharField(max_length=12)
    disk_total=models.CharField(max_length=12)
    host_input = models.CharField(max_length=12)
    host_output = models.CharField(max_length=12)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # unique_together = ("hostname",'cpu_use','cpu_total','ram_use','ram_total','disk_use','disk_total','host_input','host_output')
        verbose_name = '主机监控'
        verbose_name_plural = '主机监控'

# class Groups(models.Model):
#     name = models.CharField(max_length=12,default='系统管理员')

class Account(AbstractBaseUser,PermissionsMixin):
    '''平台用户'''
    email = models.EmailField(
        verbose_name='邮件地址',
        max_length=255,
        unique=True,
    )
    name = models.CharField('姓名',max_length=32)
    is_active = models.BooleanField('激活',default=True)
    is_staff = models.BooleanField(
        'staff status',
        default=True,
        help_text='Designates whether the user can log into this admin site.',
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email
    class Meta:
        permissions = (
            ('crm_table_index','可以查看所有的项目'),
            ('crm_table_list','可以查看每张表里所有的数据'),
            ('crm_table_list_view','可以访问表里每条数据的修改页'),
            ('crm_table_list_change','可以对表里的每条数据进行修改'),
        )

        verbose_name = '用户列表'
        verbose_name_plural = '用户管理'





