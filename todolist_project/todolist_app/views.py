from django.shortcuts import redirect,render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from todolist_app.form import customUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.

class TaskList(LoginRequiredMixin,ListView):
    # return render(request,"todolist/index.html")
    model = Task
    context_object_name = 'tasks_in_data'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context['tasks_in_data'] = context['tasks_in_data'].filter(user=self.request.user)
        context['count'] = context['tasks_in_data'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input :
            context['tasks_in_data'] = context['tasks_in_data'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context
        
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task_detail'


class  TaskCreate(LoginRequiredMixin,CreateView):
     model = Task
     fields = ['title','description','complete']
     success_url = reverse_lazy('tasklist')
     
     def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
 
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasklist')
  
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task_delete'
    success_url = reverse_lazy('tasklist')
   
def register(request):
    form= customUserForm()
    if request.method=='POST':
        form=customUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registeration successfully done you can login now !!!")
            return redirect('/login')
    return render(request,"todolist/register.html",{'form':form})


def login_page(request):
    if request.method=='POST':
        name=request.POST.get('username')
        pwd =request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in successfully !!!")           
        else:
            messages.error(request,'Invalid username or password')
            return redirect('/login')
    return render(request,"todolist/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully!!")
        return redirect("/")


