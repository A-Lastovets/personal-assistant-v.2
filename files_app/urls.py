from django.contrib.auth.decorators import login_required
from django.urls import path
from files_app import views
from files_app.views import FileListView

urlpatterns = [
    path('upload/', login_required(views.upload_file), name='upload_file'),
    path('files/', login_required(FileListView.as_view()), name='file_list'),
    path('download/<int:file_id>/',
         login_required(views.download_file), name='download_file'),
    path('delete/<int:file_id>/',
         login_required(views.delete_file), name='delete_file'),
]
