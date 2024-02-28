from core import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

urlpatterns = [
    # path('api/token/create/',TokenObtainPairView.as_view()),
    path('api/token/refresh/',TokenRefreshView.as_view()),
    # path('api/token/verify/',TokenVerifyView.as_view()),
    path('api/auth/user/', include('accounts.urls')),
    path('api/company/',include('company.urls')),
    path('api/jobs/',include('jobs.urls')),
    path('api/notification/',include('notification.urls')),
    path('api/manager/',include('administrator.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)
