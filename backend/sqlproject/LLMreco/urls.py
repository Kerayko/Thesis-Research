from django.urls import path
from . import views

urlpatterns = [
    path('recommendations/', views.get_recommendations, name='get-recommendations'),
    path('process-input/', views.process_input, name='process-input'),
    path('realtime-completion/', views.get_realtime_completion, name='realtime-completion'),
    path('chat/', views.chat_response, name='chat_response'),
    path('db-structure/', views.get_db_structure, name='get-db-structure'),
] 