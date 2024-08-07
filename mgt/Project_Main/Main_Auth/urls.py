from django.urls import path
from .views import RegisterUser,LoginUser,ProtectedView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('pv/',ProtectedView.as_view()),
    
]
