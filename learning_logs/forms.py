from django import forms
from .models import Topic,Entry

class TopicForm(forms.ModelForm):# определяется класс с именем TopicForm, наследующий от forms. ModelForm.
    class Meta: #ModelForm состоит из вложенного класса Meta, который сообщает Django, на какой модели должна базироваться форма и какие поля на ней должны находиться.
        model=Topic #форма создается на базе модели Topic
        fields=['text'] #на ней размещается только полеtext
        labels={'text':''} #приказывает Django не генерировать подпись для текстового поля
        
class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['text']
        labels={'text':'Entry:'}
        widgets={'text':forms.Textarea(attrs={'cols':80})} 
        # включается атрибут widgets. Виджет (widget) представляет собой элемент формы HTML: однострочное 
        # или многострочное текстовое поле, раскрываю- щийся список и т. д. Включая атрибут widgets, 
        # вы можете переопределить виджеты, выбранные Django по умолчанию. Приказывая Django использовать 
        # элемент forms. Textarea, мы настраиваем виджет ввода для поля 'text', чтобы ширина текстовой 
        # области составляла 80 столбцов вместо значения по умолчанию 40. У пользователя будет достаточно 
        # места для создания содержательных записей.
        
        