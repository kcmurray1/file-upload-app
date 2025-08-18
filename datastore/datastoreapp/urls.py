from django.urls import path
from datastoreapp.views import FileCollection, FileRecord

urlpatterns = [
    path("files", FileCollection.as_view(), name='file-collection'),
    path("file/<int:pk>", FileRecord.as_view(), name='file-record'),
]