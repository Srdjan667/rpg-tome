from functools import reduce
from operator import or_

from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.generic import DetailView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .helpers import get_sort_criteria, get_sort_direction
from .forms import CreateItemForm
from .models import Item

ITEMS_PER_PAGE = 10
FILTERS = ["title", "min_value", "max_value"]
RARITIES = {'common': 1, 
			'uncommon': 2, 
			'rare':3, 
			'very rare':4, 
			'legendary':5}

def order_items(request, items):
	direction_mapping = {"ascending":"", "descending":"-"}

	# Gets order criteria from URL
	order = request.GET.get("order", "date_created")
	order_direction = request.GET.get("direction", "descending")

	order = order.replace(" ", "_")
	order_direction = direction_mapping[order_direction]

	# Combines direction_mapping with ordering criteria
	items = items.order_by(order_direction + order)

	return items


def filter_items(request):
	items = Item.objects.filter(
            	author=request.user, 
	            date_created__lte=timezone.now())

	template_filters = {}

	if request.method == "GET":
		for i in FILTERS:
			template_filters[i] = request.GET.get(i)
 
	if template_filters["title"]:
		items = items.filter(title__icontains=template_filters["title"])
	if template_filters["min_value"]:
		items = items.filter(value__gte=template_filters["min_value"])
	if template_filters["max_value"]:
		items = items.filter(value__lte=template_filters["max_value"])

	rarity_filters = [Q(
		rarity=RARITIES[r]) 
		for r in RARITIES if request.GET.get(r, None) == "on"]

	if rarity_filters:
		items = items.filter(reduce(or_, rarity_filters))

	return items


@login_required
def index(request):
	rarity_dict = {}

	if request.method == 'GET':
		# Filter items based on GET criteria
		items = filter_items(request)

	# Make a dict of all checked out rarity checkboxes
	for r in RARITIES.keys():
		rarity_dict[r] = request.GET.get(r, None)

	items = order_items(request, items)

	paginator = Paginator(items, ITEMS_PER_PAGE)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	context = {
	'page_obj': page_obj,
	'rarity_dict': rarity_dict,
	'sorting_dict': get_sort_criteria(request),
	'sort_direction': get_sort_direction(request)
	}	

	return render(request, "item_library/index.html", context)


@login_required
def new_item(request):
	if request.method == 'POST':
		form = CreateItemForm(request.POST)
		# If everything is fine, show success message
		if form.is_valid():
			item = form.save(commit=False)
			item.author = request.user
			item.save()
			messages.success(request, f"Item successfully created")
		# Return error
		else:
			messages.error(request, f"Item is not valid")

		return redirect('item_library:index')
	else:
		form = CreateItemForm()

	return render(request, 'item_library/new.html', {'form':form})


class ItemDetailView(LoginRequiredMixin, DetailView):
	model = Item
	template_name = 'item_library/item_detail.html'


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Item
	form_class = CreateItemForm
	success_url = '/'


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Item
	context_object_name = 'item'
	success_url = '/'