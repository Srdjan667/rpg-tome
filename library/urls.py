from django.urls import path

from library import views

app_name = "library"

urlpatterns = [
    path("", views.index, name="index"),  # home page
    path("items/", views.item_list, name="item-list"),
    path("item/new/", views.new_item, name="item-create"),
    path("item/<int:pk>/", views.ItemDetailView.as_view(), name="item-detail"),
    path("item/<int:pk>/update/", views.ItemUpdateView.as_view(), name="item-update"),
    path("item/<int:pk>/delete/", views.ItemDeleteView.as_view(), name="item-delete"),
    path("spells/", views.spell_list, name="spell-list"),
    path("spell/new", views.new_spell, name="spell-create"),
    path("spell/<int:pk>/", views.SpellDetailView.as_view(), name="spell-detail"),
    path(
        "spell/<int:pk>/update/", views.SpellUpdateView.as_view(), name="spell-update"
    ),
    path(
        "spell/<int:pk>/delete/", views.SpellDeleteView.as_view(), name="spell-delete"
    ),
]
