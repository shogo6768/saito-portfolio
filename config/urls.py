from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import TopPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TopPage.as_view(), name='toppage'),
    path('blog/', include('blogs.urls')),
    path('accounts/', include('accounts.urls')),
    path('qa/', include('QA.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
