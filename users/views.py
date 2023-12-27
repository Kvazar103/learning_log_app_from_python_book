from django.shortcuts import render,redirect
from django.contrib.auth import login # импортируем функцию login() для выполнения входа пользователя, если регистрационная информация верна.
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register(request):
    #Регистрирует нового пользователя.
    if request.method!='POST':
        # Выводит пустую форму регистрации
        form=UserCreationForm
    else:
        # Обработка заполненной формы.
        form=UserCreationForm(data=request.POST) #В случае ответа на запрос POST создается экземпляр UserCreationForm, основанный на отправленных данных
        
        if form.is_valid():
            new_user=form.save() #ы вызываем метод save() формы для со- хранения имени пользователя и хеша пароля в базе данных
            # Выполнение входа и перенаправление на домашнюю страницу.
            login(request,new_user) #мы вы- полняем вход; этот процесс состоит из двух шагов: сначала вызывается функция login() с объектами request и new_user, которая создает действительный сеанс для нового пользователя.
            return redirect('learning_logs:index') #пользователь перенаправляется на домашнюю страницу, где приветствие в заголовке сообщает о том, что регистрация прошла успешно.
    # Вывести пустую или недействительную форму.
    context={'form':form}
    return render(request,'registration/register.html',context)
