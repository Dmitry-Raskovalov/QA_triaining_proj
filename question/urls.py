from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('questions/<int:pk>', views.QuestionView.as_view(), name='question'),
    path('ask-question', views.AskQuestionView.as_view(), name='ask_question'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('add-question', views.AddQuestion.as_view(), name='add_question'),
    path('search', views.SearchView.as_view(), name='search'),
    path('tags-index', views.TagIndexView.as_view(), name='tags_index'),
    path('tag/<slug:slug>', views.TagView.as_view(), name='tag'),
]