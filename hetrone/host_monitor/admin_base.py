class BaseAdmin(object):
    list_display = ()
    list_filter = ()
    list_per_page = 5
    default_actions = ["delete_obj"]


class AdminSite(object):
    def __init__(self):
        self.registered_admins = {}

    def register(self, model_or_iterable, admin_class=BaseAdmin, **options):
        '''
        负责把每个APP下的表注册到self.registered_admins集合里
        :param model_or_iterable:
        :param admin_class:
        :param options:
        :return:
        '''
        # admin_class = admin_class()
        admin_class.model = model_or_iterable  #把model撞倒admin——class，以供simple_tags模板调用
        app_label = model_or_iterable._meta.app_label
        if app_label not in self.registered_admins:
            self.registered_admins[app_label]= {}
        self.registered_admins[app_label][model_or_iterable._meta.model_name]=admin_class



site = AdminSite()


