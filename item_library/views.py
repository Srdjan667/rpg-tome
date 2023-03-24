from django.shortcuts import render, redirect
from .models import Item
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import CreateItemForm
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


@login_required
def index(request):
	order = request.GET.get('order', None)
	user_id = request.session.get('_auth_user_id')
	try:
		items = Item.objects.filter(author=user_id).order_by(order)

		request.session['order'] = order
		request.session.save()
	except:
		try:
			items = Item.objects.filter(author=user_id).order_by(request.session.get('order'))
		except:
			items = Item.objects.filter(author=user_id).order_by('-date_created')

	context = {
	'items': items
	}
	return render(request, "item_library/index.html", context)


@login_required
def new_item(request):
	user_id = request.session.get('_auth_user_id')
	if request.method == 'POST':
		form = CreateItemForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = user_id
			item.save()
			return redirect('item_library:index')
	else:
		form = CreateItemForm()
	return render(request, 'item_library/new.html', {'form':form})


class ItemDetailView(LoginRequiredMixin, DetailView):
	model = Item
	template_name = 'item_library/item_detail.html'


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Item
	context_object_name = 'item'
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return True