from django.contrib import admin
from django.urls import path, include  # Import include here
from home import views
from profiles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', views.profile_list),
    path('profiles/<int:id>/', views.profile_details),
    path('profiles/<int:pk>/update/', views.profile_update, name='profile-update'),
    path('profiles/disconnect/<int:current_user_id>/<int:user_id>/', views.disconnect_user, name='disconnect_user'),
    path('waving/', include('waving.urls')), 
]
