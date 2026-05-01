from django import forms
from tasks.models import Task,TaskDetail

#Django Form that is basic ata future a kaje tmn lage na

class TaskForm(forms.Form):
    title=forms.CharField(max_length=100,label='Task Title')
    description=forms.CharField(widget=forms.Textarea,label='Task Description')
    due_date=forms.DateField(widget=forms.SelectDateWidget,label='Due Date')
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label='Assigned To')


    def __init__(self, *args, **kwargs):
        #arg=tuple and kargs= dictionary

        employees=kwargs.pop("employees",[])
       #print(employees)
        #why super()
        #because we need to first our parent that's why super inside init
        #here parent is Form..if we click Form then we see form field that is in built 
        #title,descripton etc will perform first then perform --init-- class that retrive data from database
        super().__init__(*args,**kwargs)
        #suoer class auto (self.fields) make kore
        #self.fields is basically a dictionary of all form fields

        self.fields['assigned_to'].choices=[(emp.id,emp.name)for emp in employees]
        #assigned_to is key and self.fields['assinged_to'] is value
        #Database → (id, name) → choices → form field → checkbox show
        #choice is a property of fields that tell which thing it will show for user


#mixin ar maddhome amra form er style set korte pari and onek line code ke kom kore dite pari
class djangoFormMixin:
    default_css_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring-rose-600"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': self.default_css_classes, 'name': field_name, 'placeholder': f'Enter a descriptive {field_name}'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': self.default_css_classes, 'name': field_name, 'placeholder': f'Provide a detailed description of the {field_name} ', 'rows': 4})
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({'class': "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring-rose-600", 'name': field_name})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': "space-y-2", 'name': field_name})



#Django Model Form ata future a kaje lagbe
class TaskModelForm(djangoFormMixin,forms.ModelForm):
    class Meta:
        model=Task #kon model ar jonne form make korte chai ata dte hoi
        fields = ['title','description','due_date','assigned_to'] # oi model ar kon kon field use korte chai ata
        widgets={
            'due_date':forms.SelectDateWidget,
            'assigned_to':forms.CheckboxSelectMultiple
        }
        
        """Manual style form er jonno amra widget use korte pari but eta onek line code hobe and jodi onek field thake tahole aro besi line code hobe tai amra style form er jonno mixin use korbo"""
        # widgets={#css ar kaj kore
        #     'title':forms.TextInput(attrs={'class':"border border-purple-500-300 rounded-lg p-3 w-full mb-4 shadow-sm focus:border-rose-600 ",'name':'title','placeholder':'Enter a descriptive task title'}),
        #     'description':forms.Textarea(attrs={'class':"border border-purple-500 rounded-lg p-2 w-full h-24 mb-4 shadow-sm focus:border-rose-600 ",'name':'description','placeholder':'Provide a detailed description of the task ','rows':4   }),
        #     'due_date':forms.SelectDateWidget(attrs={'class':"border border-purple-500-300 rounded-lg p-2 gap-1 mb-4 bg-purple-300 text-black shadow-sm focus:border-rose-600 ",'name':'due_date'}),
        #     'assigned_to':forms.CheckboxSelectMultiple(attrs={'class':" rounded-lg p-2 mb-4 shadow-sm focus:border-rose-600 ",'name':'assigned_to'}),
        # }
    '''using mixin for styling form eta onek line code ke kom kore dey and amra jodi aro besi field add kori taholeo amader code onek clean thakbe'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()



class TaskDetailModelForm(djangoFormMixin,forms.ModelForm):
    class Meta:
        model=TaskDetail
        fields = ['priority','notes']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()    







