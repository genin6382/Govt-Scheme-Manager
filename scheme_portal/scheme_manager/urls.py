from django.urls import path
from . import views

urlpatterns = [
    path('', views.SchemeList.as_view(), name='scheme'),
    path('eligible/', views.EligibleSchemeList.as_view(), name='eligible-schemes'),
    path('<int:pk>/', views.SchemeDetail.as_view(), name='scheme_detail'),
    path('<int:pk>/can-feedback/', views.CanGiveFeedbackView.as_view(), name='can-user-feedback'),
    path('<int:pk>/feedbacks/',views.FeedbackView.as_view(),name='feedback_view'),
    path('<int:scheme_id>/feedbacks/<int:pk>',views.FeedbackDetail.as_view(),name='feedback_detail'),
]