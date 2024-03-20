from django.contrib import admin
from django.urls import path, include
from home import views
from profiles import views
from account.views import register
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', views.profile_list),
    path('profiles/<str:username>/', views.profile_details),
    path('profiles/<str:username>/update/', views.profile_update, name='profile_update'),
    path('profiles/disconnect/<int:current_user_id>/<int:user_id>/', views.disconnect_user, name='disconnect_user'),
    path('waving/', include('waving.urls')),   
    path('block_profile/<int:sender_id>/<int:receiver_id>/', views.block_profile, name='block_profile'),
    path('unblock_profile/<int:sender_id>/<int:receiver_id>/', views.unblock_profile, name='unblock_profile'),
    path('profiles/search', views.profile_search),
    path('accounts/', include('account.urls')),
    path("register/", register, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

