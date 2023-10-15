from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic import DeleteView, DetailView, UpdateView

from .forms import ItemsForm, SpellsForm
from .helpers import get_sort_criteria, get_sort_direction, path_without_page
from .models import Item, Spell

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
def item_list(request):
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
        "path_without_page": path_without_page(request),
    }

    return render(request, "library/item_list.html", context)


@login_required
def new_item(request):
    if request.method == "POST":
        form = ItemsForm(request.POST)
        # If everything is fine, show success message
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.save()

            messages.success(request, "Item successfully created")

        # Return error
        else:
            messages.error(request, "Item is not valid")

        return redirect("library:item-list")

    else:
        form = ItemsForm()

    return render(request, "library/new.html", {"form": form})


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "library/item_detail.html"


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemsForm
    success_url = "/"

    def test_func(self):
        entry = self.get_object()
        if self.request.user == entry.author:
            return True
        return False


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    context_object_name = "item"
    success_url = "/"

    def test_func(self):
        entry = self.get_object()
        if self.request.user == entry.author:
            return True
        return False


@login_required
def spell_list(request):
    spells = Spell.objects.filter(author=request.user).order_by("-date_created")
    context = {
        "spells": spells,
    }

    return render(request, "library/spells/spell_list.html", context)


@login_required
def new_spell(request):
    if request.method == "POST":
        form = SpellsForm(request.POST)
        # If everything is fine, show success message
        if form.is_valid():
            spell = form.save(commit=False)
            spell.author = request.user
            spell.save()

            messages.success(request, "Spell successfully created")

        # Return error
        else:
            messages.error(request, "Spell is not valid")

        return redirect("library:spell-list")

    else:
        form = SpellsForm()

    return render(request, "library/spells/new_spell.html", {"form": form})


class SpellDetailView(LoginRequiredMixin, DetailView):
    model = Spell
    template_name = "library/spells/spell_detail.html"


class SpellUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Spell
    template_name = "library/spells/spell_form.html"
    form_class = SpellsForm
    success_url = "/spells/"

    def test_func(self):
        entry = self.get_object()
        if self.request.user == entry.author:
            return True
        return False


class SpellDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Spell
    template_name = "library/spells/spell_confirm_delete.html"
    context_object_name = "spell"
    success_url = "/spells/"

    def test_func(self):
        entry = self.get_object()
        if self.request.user == entry.author:
            return True
        return False
