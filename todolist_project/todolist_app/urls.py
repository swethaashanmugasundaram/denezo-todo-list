from django.urls import path
from . import views
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete
urlpatterns = [
    path('',TaskList.as_view(),name="tasklist"),
    path('taskdetail/<int:pk>/',TaskDetail.as_view(),name="taskdetail"),
    path('task-create/',TaskCreate.as_view(),name="task-create"),
    path('task-upate/<int:pk>/',TaskUpdate.as_view(),name="task-upate"),
    path('task-delete/<int:pk>/',TaskDelete.as_view(),name="task-delete"),
    path('register/',views.register,name="register"),
    path('login/',views.login_page,name="login"),
    path('logout/',views.logout_page,name="logout")
]
