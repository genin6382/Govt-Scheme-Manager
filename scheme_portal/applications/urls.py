from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.ApplicationView.as_view(),name='applications'),
    path('check/<int:scheme_id>/', views.ApplicationStatusView.as_view(), name='application-status'),
    path('schemes/<int:scheme_id>/',views.ApplicationDetailListView.as_view(),name='application_manage'),
    path('<int:pk>/',views.ApplicationDetailManageView.as_view(),name='application_detail'),
   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)