from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404 #мы импортируем исключение Http404, которое будет выдаваться программой при запросе пользователем темы, которую ему видеть не положено.

# Create your views here.
# Создайте здесь свои представления.

def index(request):
    #Домашняя страница приложения Learning Log
    return render(request,'learning_logs/index.html')

#Сначала импортируется функция login_required(). Мы применяем login_ required() как декоратор для функции представления topics(), для чего перед именем login_required() ставится знак @; он сообщает Python, что этот код должен выполняться перед кодом topics().
#Код login_required() проверяет, вошел ли пользователь в систему, и Django за- пускает код topics() только при выполнении этого условия. Если же пользователь не выполнил вход, он перенаправляется на страницу входа.
#Чтобы перенаправление работало, необходимо внести изменения settings .py и сообщить Django, где искать страницу входа.
@login_required
#Функция topics() должна получать данные из базы данных и отправлять их шаблону.
def topics(request): #Функции topics() необходим один параметр: объект request, полученный Django от сервера 
    #Выводит список тем.
    topics=Topic.objects.filter(owner=request.user).order_by('date_added') #выдается запрос к базе данных на получение объектов Topic, отсортированных по атрибуту date_added
    #Если пользователь выполнил вход, в объекте запроса устанавливается атрибут request.user с информацией о пользователе. Фрагмент кода Topic.objects. filter(owner=request.user) приказывает Django извлечь из базы данных только те объекты Topic, у которых атрибут owner соответствует текущему пользователю.
    context={'topics':topics}#определяется контекст, который будет передаваться шаблону
    return render(request,'learning_logs/topics.html',context)#использующей данные, функции render() передается переменная context, а также объект request и путь к шаблону

#Представление отдельной темы
#Функция topic() должна получить тему и все связанные с ней записи из базы данных
@login_required
def topic(request,topic_id):
    #Выводит одну тему и все ее записи.
    topic=Topic.objects.get(id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    if topic.owner!=request.user: #Если тема не принадлежит текущему пользователю, выдается исключение Http404, а Django возвращает страницу с ошибкой 404.
        raise Http404
    entries=topic.entry_set.order_by('-date_added') #знак «минус» перед date_added сортирует результаты в обратном порядке, то есть самые последние записи будут находиться на первых местах.
    context={'topic':topic,'entries':entries} #Тема и записи сохраняются в словаре context, который передается шаблону topic .html
    return render(request,'learning_logs/topic.html',context)

# Функция new_topic() должна обрабатывать две разные ситуации: исходные запросы страницы new_topic 
# (в этом случае должна отображаться пустая форма) и обработка данных, отправленных на форме. 
# Затем она должна перенаправить пользователя обратно на страницу topics:
@login_required
def new_topic(request):
    #Определяет новую тему.
    if request.method!='POST': #Если метод запроса отличен от POST, вероятно, используется запрос GET, поэтому необходимо вернуть пустую форму (даже если это запрос другого типа, это все равно безопасно)
        #Данные не отправлялись; создается пустая форма
        form=TopicForm() #Мы создаем экземпляр TopicForm, сохраняем его в переменной form и отправляем форму шаблону в словаре context
        #Так как при создании TopicForm аргументы не передавались, Django создает пустую форму, которая заполняется пользователем.
    else: #Если используется метод запроса POST, выполняется блок else, который обрабатывает данные, отправленные в форме
        #Отправлены данные POST; обработать данные.
        form=TopicForm(data=request.POST) #создаем экземпляр TopicForm и передаем ему данные, введенные пользователем, хранящиеся в request.POST.
        #Отправленную информацию нельзя сохранять в базе данных до тех пор, пока она не будет проверена. 
        # Функция is_valid() проверяет, что все обязательные поля были заполнены (все поля формы по умолчанию 
        # являются обязательными), а вве- денные данные соответствуют типам полей — например, 
        # что длина текста меньше 200 символов, как было указано в файле models .py в главе 18. 
        # Автоматическая проверка избавляет нас от большого объема работы. Если все данные действительны, 
        # можно вызвать метод save() , который записывает данные из формы в базу данных.
        if form.is_valid():
            new_topic = form.save(commit=False) # Save topic in a variable. При первом вызове form.save() передается аргумент commit=False, потому что новая тема должна быть изменена перед сохранением в базе данных
            new_topic.owner = request.user # Set topics owner attribute to current user. Атрибуту owner новой темы присваивается текущий пользователь
            new_topic.save() # Save the changes to the database.
            return HttpResponseRedirect(reverse('learning_logs:topics'))
            #form.save()
            #return redirect('learning_logs:topics') #После того как данные будут сохранены, страницу можно покинуть. Мы используем вызов redirect() для перенаправления браузера на страницу topics, на которой пользователь увидит только что введенную им тему в общем списке тем
    # Вывести пустую или недействительную форму.
    context={'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    #Добавляет новую запись по конкретной теме.
    topic=Topic.objects.get(id=topic_id)
    
    if request.method!='POST':
        #Данные не отправлялись; создается пустая форма.
        form=EntryForm()
    else:
        #Отправлены данные POST; обработать данные.
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            # При вызове save() мы включаем аргумент commit=False для того, чтобы создать новый объект записи 
            # и сохранить его в new_entry, не сохраняя пока в базе данных. Мы присваиваем атрибуту topic объекта 
            # new_entry тему, прочитанную из базы данных в начале функции, после чего вызываем save() 
            # без аргументов. В результате запись сохраняется в базе данных с правильно ассоциированной темой.
            return redirect('learning_logs:topic',topic_id=topic_id)
            #Вызов redirect() получает два аргумента — имя представления, которому передается управление, 
            # и аргумент для функции представления. В данном случае происходит перенаправление функции topic(), 
            # которой должен переда- ваться аргумент topic_id. Вызов перенаправляет пользователя на страницу темы, 
            # для которой была создана запись, и пользователь видит новую запись в списке записей.
    # Вывести пустую или недействительную форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)    

@login_required
def edit_entry(request,entry_id):
    #Редактирует существующую запись.
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    
    if topic.owner != request.user:
        raise Http404
    
    if request.method!='POST':
        #Исходный запрос; форма заполняется данными текущей записи.
        form=EntryForm(instance=entry)
        #В блоке if, который выполняется для запроса GET, создается экземпляр EntryForm с аргументом 
        # instance=entry. Этот аргумент приказывает Django создать форму, заранее заполненную информацией из 
        # существующего объекта записи. Пользова- тель видит свои существующие данные и может отредактировать их.
    else:
        #Отправка данных POST; обработать данные.
        form=EntryForm(instance=entry,data=request.POST)
        #При обработке запроса POST передаются аргументы instance=entry и data=request.POST. Они приказывают 
        # Django создать экземпляр формы на основании информации существующего объекта записи, обновленный 
        # данными из request.POST.
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)
    
    # Если отображается исходная форма для редактирования записи или если отправленная форма недействительна, 
    # создается словарь context, а страница строится на базе шаблона edit_entry.html.
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

        
        
    

    
    
    