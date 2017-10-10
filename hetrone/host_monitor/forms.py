from django.forms import ModelForm
from django.forms import Form

def __new__(cls, *args, **kwargs):

    for field_name in cls.base_fields:
        field = cls.base_fields[field_name]
        # print("field repr",field_name,field.__repr__())
        attr_dic = { 'class': 'form-control'}

        field.widget.attrs.update(attr_dic)

    return ModelForm.__new__(cls)

def create_dynamic_modelform(model_class):
    class Meta:
        model = model_class

        fields = "__all__"



    dynamic_modelform = type("DynamicModelForm",
                             (ModelForm,),
                             {'Meta':Meta,'__new__':__new__})
    return dynamic_modelform

