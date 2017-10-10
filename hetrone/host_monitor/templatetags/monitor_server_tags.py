from django.template import Library
from django.utils.safestring import mark_safe
from host_monitor.admin import site
import redis

#标签文件


register = Library()




@register.simple_tag
def get_model_verbose_name(admin_class):
    print('admin_class-get',admin_class)
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_user_info(request):
    print('request--getuser',)







@register.simple_tag
def get_hostinfo_obj(monitor_id):
    str = "<tr>"
    for host_info in monitor_id:

        std = "<th><a href='#'>%s</a></th>" %host_info.hostname.ip_address
        std += "<th>%s</th>" %host_info.cpu_use
        std += "<th>%s</th>" %host_info.ram_use
        std += "<th>%s</th>" %host_info.disk_use
        std += "<th>%s</th>" %host_info.host_input
        std += "<th>%s</th>" %host_info.host_output
        str += std

        str +="</tr>"
    print('str',str)
    #
    return mark_safe(str)




@register.simple_tag
def get_js_ip_data(redis_data):

    ip_addr = {'ip_address':redis_data.get("ip_address")}
    for ip in ip_addr:
        js_ip = ip_addr[ip]
        return js_ip
@register.simple_tag
def get_js_net_data(redis_data):
    net_data_list = []
    network = {'host_input':redis_data.get('host_input')}
    for net in network:
        input_data = int(network[net][0])
        net_input = net_data_list.append(input_data)
    return net_data_list

@register.simple_tag
def get_filter_condtions_string(filter_conditions,q_val):
    print('filter_conditi---',filter_conditions)
    print('q_val---',q_val)
    condtion_str = ""
    for k,v in filter_conditions.items():
        condtion_str += "&%s=%s" %(k,v)
        print('11--1',condtion_str)
    if q_val:#拼接search 字段
        condtion_str += "&_q=%s" % q_val
        print('condtion_str-23--get--',condtion_str)
    print('condtion_str---get--',condtion_str)
    return mark_safe(condtion_str)

@register.simple_tag
def generate_orderby_icon(new_order_key):
    if new_order_key.startswith('-'):
        icon_ele = """<i class="fa fa-angle-down" aria-hidden="true"></i>"""
    else:
        icon_ele = """<i class="fa fa-angle-up" aria-hidden="true"></i>"""
    return mark_safe(icon_ele)

@register.simple_tag
def build_filter_ele(filter_column,admin_class,filter_conditions):
    """
    1.拿到要过滤字段的对象field_obj
    2. 调用field_obj.get_choices()
    3. 生成select元素
    4.循环choices列表，生成option元素
    :param filter_column:
    :param model_class:
    :return:
    """
    print('filter_column',filter_column)
    print('admin_class',admin_class)
    print('filter_conditions',filter_conditions)
    print('filter_conditions---',dir(filter_conditions))
    field_obj = admin_class.model._meta.get_field(filter_column)
    print('field_obj****',field_obj.get_choices)
    select_ele = "<select class='form-control' name=%s>"% filter_column
    print('sele')
    # filter_option = filter_conditions.get(filter_column) #1.None 代表没有对这个字段过滤，2.有值，选中的具体的option的val
    filter_option = filter_conditions.get(filter_column)
    print('filter_option',filter_option)
    if filter_option:#代表此字段过滤了
        for choice in field_obj.get_choices():
            print('choice---',choice)
            if filter_option == str(choice[0]):
                selected = 'selected'
            else:
                selected = ''
            option_ele = "<option value=%s  %s>%s</option>" % (choice[0],selected,choice[1])
            select_ele += option_ele
    else:
        print('field_obj---',field_obj.get_choices)
        print('field_obj---',dir(field_obj))
        print('field_obj.get_choices',field_obj.get_choices)
        for choice in field_obj.get_choices():
            option_ele = "<option value=%s >%s</option>" % (choice[0],choice[1])
            select_ele += option_ele


    select_ele += "</select>"
    return mark_safe(select_ele)


@register.simple_tag
def get_enable_objects (row,app_name,model_name,admin_class):

    row_str = "<td id='conn-status' class='text-center' data-editable='false'>"
    if row.enabled is False:
        pass
    else:
        row_str += "<a style='color:#1CD61C'> 已连接 </a></td>"
    row_str += "<form method='POST'>"

    row_str += "<td class='text-center' data-editable='false'>" \
               "<a href='/host_edit/{app_name}/{model_name}/{obj_host}' class='btn btn-primary btn-xs' data-toggle='modal' >" \
               "编辑</a>".format(app_name=app_name, model_name=model_name, obj_host=row.id, )

    # row_str += "<a href='/host_conn/{app_name}/{model_name}/{obj_id}/' class='conn btn-primary btn btn-xs btn-warning' />连接</a>".format(app_name=app_name, model_name=model_name, obj_id=row.id,)
    row_str += "<a  id='conn' class='conn btn-primary btn btn-xs btn-warning' />连接</a>".format(app_name=app_name, model_name=model_name, obj_id=row.id,)
    row_str += "<a href='/host_del/{app_name}/{model_name}/{obj_id}/' class='btn btn-xs btn-danger asset_del' value='2'>删除</a></td>"\
        .format(app_name=app_name, model_name=model_name, obj_id=row.id)
    row_str += "</form>"
    row_str += "</td>"
    return mark_safe(row_str)





@register.simple_tag
def get_edite_objects (row,app_name,model_name,admin_class):

    print("hosts-group-appname",app_name)
    print("hosts-group-model-name",model_name)
    print("hosts-group-admin_class",admin_class)
    row_str = "<form method='POST'>"

    row_str += "<td class='text-center' data-editable='false'>" \
               "<a href='/host_group_edit/{app_name}/{admin_class}/{obj_host}/' class='btn btn-primary btn-xs' data-toggle='modal' >" \
               "编辑</a>".format(app_name=app_name, admin_class=admin_class, obj_host=row.id, )

    row_str += "<a href='/host_group_del/{app_name}/{admin_class}/{obj_id}/' class='btn btn-xs btn-danger asset_del' value='2'>删除</a></td>"\
        .format(app_name=app_name, admin_class=admin_class, obj_id=row.id)
    row_str += "</form>"
    return mark_safe(row_str)

@register.simple_tag
def get_abs_value(loop_num , curent_page_number):
    """返回当前页与循环loopnum的差的绝对值"""
    return abs(loop_num - curent_page_number)




@register.simple_tag
def build_table_row(row, admin_class, app_name, model_name):
    # print('row--',row)
    # print('row-get--',row.get_username)
    # print('row-id--',row.id)
    # print('dir(row)---',dir(row))
    # print('host_group-admin',admin_class)
    row_ele = ""
    row_ele += "<td class='text-center'><input type='checkbox'  class='row-obj' name ='_selected_obj'  value='{obj_id}'></td>".format(obj_id=row.id)
    for index, column_name in enumerate(admin_class.list_display):
        print('host-group-column_name',column_name)
        field_obj = row._meta.get_field(column_name)
        if field_obj.choices:
            column_display_func = getattr(row, 'get_%s_display' % column_name)
            column_val = column_display_func()
        else:
            column_val = getattr(row, column_name)
        if index == 0:
            td_ele = "<td class='text-center'><a id='row-obj' href='/host_edit/{app_name}/{model_name}/{obj_id}'>{column_val}</a></td>".format(
                app_name=app_name, model_name=model_name,obj_id=row.id ,column_val=column_val)
        else:
            td_ele = "<td class='text-center'>{column_val}</td>".format(column_val=column_val)
        row_ele += td_ele

    return mark_safe(row_ele)



@register.simple_tag
def build_account_row(row,admin_display,app_name):
    row_ele = ""
    row_ele += "<td class='text-center'><input type='checkbox'  class='row-obj' name ='_selected_obj'  value='{obj_id}'></td>".format(
        obj_id=row.id)
    for index,column_name in enumerate(admin_display):
        print('column_name',column_name)
        field_obj = row._meta.get_field(column_name)
        if field_obj.choices:
            column_display_func = getattr(row,'get_%s_display'%column_name)
            column_val = column_display_func()
        else:
            column_val = getattr(row,column_name)
        if index == 0:
            td_ele = "<td class='text-center'><a id='row-obj' href='/host_edit/{app_name}/account/{obj_id}'>{column_val}</a></td>".format(
                app_name=app_name,obj_id=row.id ,column_val=column_val)
        else:
            td_ele = "<td class='text-center'>{column_val}</td>".format(column_val=column_val)
        row_ele += td_ele

    return mark_safe(row_ele)



@register.simple_tag
def get_m2m_objects(admin_class,field_name,selected_objs):
    """
    1.根据field_name从admin_class.model反射出字段对象
    2.拿到关联表的所有数据
    3.返回数据
    :param admin_class:
    :param field_name:
    :return:
    """


    field_obj = getattr(admin_class.model,'%s'%field_name)
    all_objects = field_obj.rel.to.objects.all()
    return set(all_objects) - set(selected_objs)

@register.simple_tag
def get_selected_m2m_objects(form_obj,field_name):
    """
    1.根据field_name反射出form_obj.instance里的字段对象
    2. 拿到字段对象关联的所有数据
    :param form_obj:
    :param field:
    :return:
    """

    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance, field_name)
        return field_obj.all()
    else:
        return []

@register.simple_tag
def build_user_row(row,admin_class,app_name):
    print('row',row)
    print('admin_class',admin_class)
    print('app_name',app_name)

@register.simple_tag
def get_host_group_name(host_group):
    print('host_group',host_group)
    print('host_group-dir',dir(host_group))
    return host_group.model._meta.verbose_name
