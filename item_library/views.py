from django.shortcuts import render, redirect
from .models import Item
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import CreateItemForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from functools import reduce
from operator import or_

FILTERS = ["title", "min_value", "max_value"]
RARITIES = ['common', 'uncommon', 'rare', 'very rare', 'legendary']


@login_required
def check_for_session_errors(request):
	# sets empty strings as a default values to avoid KeyError
	for i in range(len(FILTERS)):
		request.session.setdefault(FILTERS[i], '')

	request.session.setdefault('rarity_list', '')
	request.session.setdefault('filter_entry', '')


@login_required
def order_items(request, items):
	order = request.GET.get('order', None)
	try:
		items = items.order_by(order)
		request.session['order'] = order
	except:
		try:
			items = items.order_by(request.session.get('order'))
		except:
			items = items.order_by('-date_created')

	return items


@login_required
def filter_items(request):
	user_id = request.user
	items = Item.objects.filter(author=user_id)
	template_filters = {}

	if request.method == "POST":
		for i in range(len(FILTERS)):
			template_filters[FILTERS[i]] = request.POST.get(FILTERS[i])

	else:
		for i in range(len(FILTERS)):
			template_filters[FILTERS[i]] = request.session[FILTERS[i]]

	if template_filters["title"]:
		items = items.filter(title__icontains=template_filters["title"])
		request.session["title"] = template_filters["title"]
	if template_filters["min_value"]:
		items = items.filter(value__gte=template_filters["min_value"])
		request.session["min_value"] = template_filters["min_value"]
	if template_filters["max_value"]:
		items = items.filter(value__lte=template_filters["max_value"])
		request.session["max_value"] = template_filters["max_value"]

	rarity_filters = [Q(rarity=request.POST.get(r, None)) for r in RARITIES if request.POST.get(r, None)]

	if rarity_filters:
		items = items.filter(reduce(or_, rarity_filters))

	return items


@login_required
def index(request):
	rarity_list = []
	filter_entry = {}

	check_for_session_errors(request)

	for i in range(len(RARITIES)):
		rarity_list.append({"is_checked": request.POST.get(RARITIES[i])})
		rarity_list[i]['rarity'] = RARITIES[i]

	if request.method == 'POST':
		if 'filter' in request.POST:
			items = filter_items(request)

			for i in range(len(FILTERS)):
				filter_entry[FILTERS[i]] = request.POST.get(FILTERS[i])

		elif 'reset' in request.POST:
			items = Item.objects.filter(author=request.user)

			for i in range(len(rarity_list)):
				rarity_list[i]['is_checked'] = None

			for i in range(len(FILTERS)):
				request.session[FILTERS[i]] = None

	else:
		items = filter_items(request)

	if request.session["filter_entry"] != filter_entry:
		request.session["filter_entry"] = filter_entry
	if request.session["rarity_list"] != rarity_list:
		request.session["rarity_list"] = rarity_list

	items = order_items(request, items)

	context = {
	'items': items,
	}

	return render(request, "item_library/index.html", context)


@login_required
def new_item(request):
	if request.method == 'POST':
		form = CreateItemForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = request.user
			item.save()
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
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Item
	context_object_name = 'item'
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return True