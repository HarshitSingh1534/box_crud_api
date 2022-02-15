from django.urls import path
from boxes.views import (
    BoxCreateView,
    BoxUpdateView,
    DestroyBoxView,
    ListAllBoxesView,
    ListMyBoxView,
)

urlpatterns = [
    path("list-all-boxes", ListAllBoxesView.as_view(), name="list-all-boxes"),
    path("create-box", BoxCreateView.as_view(), name="create-box"),
    path("update-box/<uuid:pk>", BoxUpdateView.as_view(), name="update-box"),
    path("list-my-boxes", ListMyBoxView.as_view(), name="list-my-boxes"),
    path("delete-box/<uuid:pk>", DestroyBoxView.as_view(), name="delete-box"),
]
