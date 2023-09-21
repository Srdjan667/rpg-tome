from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic import DeleteView, DetailView, UpdateView

from .forms import CreateItemForm
from .helpers import get_sort_criteria, get_sort_direction
from .models import Item

ITEMS_PER_PAGE = 10
RARITIES = {
    "common": 1,
    "uncommon": 2,
    "rare": 3,
    "very rare": 4,
    "legendary": 5,
    "artifact": 6,
}


@login_required
def index(request):
    rarity_dict = {}

    # Make a dict of all checked out rarity checkboxes
    for r in RARITIES:
        rarity_dict[r] = request.GET.get(r, None)

    items = Item.get_queryset(request)
    items = Item.sort_queryset(request, items)

    paginator = Paginator(items, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "rarity_dict": rarity_dict,
        "sorting_dict": get_sort_criteria(request),
        "sort_direction": get_sort_direction(request),
    }

    return render(request, "item_library/index.html", context)


@login_required
def new_item(request):
    if request.method == "POST":
        form = CreateItemForm(request.POST)
        # If everything is fine, show success message
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.save()

            messages.success(request, "Item successfully created")

        # Return error
        else:
            messages.error(request, "Item is not valid")

        return redirect("item_library:index")

    else:
        form = CreateItemForm()

    return render(request, "item_library/new.html", {"form": form})


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "item_library/item_detail.html"


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = CreateItemForm
    success_url = "/"


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    context_object_name = "item"
    success_url = "/"
