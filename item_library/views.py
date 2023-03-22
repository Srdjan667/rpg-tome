from django.shortcuts import render, redirect
from .models import Item
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import CreateItemForm
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


@login_required
def index(request):
	order = request.GET.get('order', None)
	try:
		items = Item.objects.filter(author=request.user.id).order_by(order)
	except:
		items = Item.objects.filter(author=request.user.id).order_by('-date_created')
		
	context = {
	'items': items
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


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Item
	success_url = '/'