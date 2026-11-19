from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('animals.urls')),
    path('api/', include('applications.urls')),
    # Uploaded photos. On PythonAnywhere a static-files mapping for /media/ serves them
    # faster before the request reaches Django; this route is the fallback everywhere else.
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
