from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic import DeleteView, DetailView, UpdateView

from .forms import ItemFilterForm, ItemsForm, SpellFilterForm, SpellsForm
from .helpers import get_sort_parameters, path_without_page
from .models import Item, Spell

ITEMS_PER_PAGE = 10
SPELLS_PER_PAGE = 10
SORT_CRITERIA = ["date created", "title", "rarity", "value"]
SORT_DIRECTION = ["ascending", "descending"]


@login_required
def item_list(request):
    form = ItemFilterForm(request.GET)

    if form.is_valid():
        items = Item.get_queryset(request, form.cleaned_data)
        items = Item.sort_queryset(request, items)
    else:
        items = Item.objects.all()
        items = Item.sort_queryset(request, items)

    paginator = Paginator(items, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "page_obj": page_obj,
        "sorting_dict": get_sort_parameters(request, "order", SORT_CRITERIA),
        "sort_direction": get_sort_parameters(request, "direction", SORT_DIRECTION),
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
    form = SpellFilterForm(request.GET)

    if form.is_valid():
        spells = Spell.get_queryset(request, form.cleaned_data)
    else:
        spells = Spell.objects.all()

    spells = spells.order_by("-date_created")

    paginator = Paginator(spells, SPELLS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "page_obj": page_obj,
        "path_without_page": path_without_page(request),
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
