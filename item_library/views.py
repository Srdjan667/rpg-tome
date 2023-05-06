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

RARITIES = ['common', 'uncommon', 'rare', 'very rare', 'legendary']

def order_items(request, items):
	order = request.GET.get('order', None)
	try:
		items = items.order_by(order)

		request.session['order'] = order
		request.session.save()
	except:
		try:
			items = items.order_by(request.session.get('order'))
		except:
			items = items.order_by('-date_created')

	return items


def filter_items(request):
	user_id = request.user
	items = Item.objects.filter(author=user_id)

	title = request.POST.get('title')
	min_value = request.POST.get('min_value')
	max_value = request.POST.get('max_value')

	if title != "":
		items = items.filter(title__icontains=title)
	if min_value != "":
		items = items.filter(value__gte=min_value)
	if max_value != "":
		items = items.filter(value__lte=max_value)

	rarity_filters = [Q(rarity=request.POST.get(r, None)) for r in RARITIES if request.POST.get(r, None)]

	if rarity_filters:
		items = items.filter(reduce(or_, rarity_filters))

	return items


@login_required
def index(request):
	rarity_list = []
	filter_entry = {}

	if request.method == 'POST':
		if 'filter' in request.POST:
			items = filter_items(request)

			filters = ["title", "min_value", "max_value"]

			for i in range(len(filters)):
				filter_entry[filters[i]] = request.POST.get(filters[i])

		elif 'reset' in request.POST:
			items = Item.objects.filter(author=request.user)

	else:
		items = Item.objects.filter(author=request.user)

	items = order_items(request, items)

	for i in range(len(RARITIES)):
		rarity_list.append({"is_checked": request.POST.get(RARITIES[i])})
		rarity_list[i]['rarity'] = RARITIES[i]

	context = {
	'items': items,
	'filter_entry': filter_entry,
	'rarity_list': rarity_list,
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