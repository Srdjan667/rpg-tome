from django.urls import path

from . import views
from .views import ItemDeleteView, ItemDetailView, ItemUpdateView

app_name = "library"

urlpatterns = [
    # path("", views.index, name="index"), # home page
    path("items/", views.item_list, name="item-list"),
    path("item/new/", views.new_item, name="item-create"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("item/<int:pk>/update/", ItemUpdateView.as_view(), name="item-update"),
    path("item/<int:pk>/delete/", ItemDeleteView.as_view(), name="item-delete"),
    # path("test/", views.render_test_form, name="library:test"),# third argument is not right
]
