from functools import reduce
from operator import or_

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django import forms

from .forms import CreateItemForm
from .models import Item


FILTERS = ["title", "min_value", "max_value"]
RARITIES = ['common', 'uncommon', 'rare', 'very rare', 'legendary']
DEFAULT_SESSION_KEYS = {"rarity_list": "", 
						"filter_entry": "", 
						"order": "date_created", 
						"direction": "desc"}


def initialize_session(request):
	# Sets empty strings as a default values to avoid KeyError
	for i in FILTERS:
		request.session.setdefault(i, '')

	for k, v in DEFAULT_SESSION_KEYS.items():
		request.session.setdefault(k, v)


def order_items(request, items):
	direction_mapping = {"asc":"", "desc":"-"}

	order = request.GET.get("order", request.session["order"])

	# Uses URL parameter if avaiable, if not session is used instead
	order_direction = request.GET.get("direction", request.session["direction"])

	if order_direction is None:
		order_direction = "desc"

	order_direction = direction_mapping[order_direction]

	# Combines direction_mapping with ordering criteria
	items = items.order_by(order_direction + order)
	request.session["order"] = order

	if request.session["direction"] != request.GET.get("direction"):
		request.session["direction"] = request.GET.get("direction")

	return items


def filter_items(request):
	items = Item.objects.filter(
            	author=request.user, 
	            date_created__lte=timezone.now())

	template_filters = {}

	if request.method == "POST":
		for i in FILTERS:
			template_filters[i] = request.POST.get(i)
	else:
		for i in FILTERS:
			template_filters[i] = request.session[i]

	if template_filters["title"]:
		items = items.filter(title__icontains=template_filters["title"])
		request.session["title"] = template_filters["title"]
	if template_filters["min_value"]:
		items = items.filter(value__gte=template_filters["min_value"])
		request.session["min_value"] = template_filters["min_value"]
	if template_filters["max_value"]:
		items = items.filter(value__lte=template_filters["max_value"])
		request.session["max_value"] = template_filters["max_value"]

	rarity_filters = [Q(
		rarity=request.POST.get(r, None)) 
		for r in RARITIES if request.POST.get(r, None)]

	if rarity_filters:
		items = items.filter(reduce(or_, rarity_filters))

	return items


@login_required
def index(request):
	rarity_list = []
	filter_entry = {}

	initialize_session(request)

	# For each rarity check whether is checkbox active or not
	for i in range(len(RARITIES)):
		rarity_list.append({"is_checked": request.POST.get(RARITIES[i])})
		rarity_list[i]['rarity'] = RARITIES[i]

	if request.method == 'POST':
		# Saves user input so it can be filled from the session
		if 'filter' in request.POST:
			items = filter_items(request)

			for i in FILTERS:
				filter_entry[i] = request.POST.get(i)

		# Clears all previously filled fields
		elif 'reset' in request.POST:
			items = Item.objects.filter(
            	author=request.user, 
	            date_created__lte=timezone.now())

			for i in range(len(rarity_list)):
				rarity_list[i]['is_checked'] = None

			for i in FILTERS:
				request.session[i] = None
	else:
		items = filter_items(request)

	if request.session["filter_entry"] != filter_entry:
		request.session["filter_entry"] = filter_entry
	if request.session["rarity_list"] != rarity_list:
		request.session["rarity_list"] = rarity_list

	items = order_items(request, items)

	paginator = Paginator(items, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	context = {
	'page_obj': page_obj
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

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		entry = self.get_object()
		if self.request.user == entry.author:
			return True
		return False


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Item
	context_object_name = 'item'
	success_url = '/'

	def test_func(self):
		entry = self.get_object()
		if self.request.user == entry.author:
			return True
		return False