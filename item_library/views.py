from django.shortcuts import render, redirect
from .models import Item
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import CreateItemForm

@login_required
def index(request):
	current_user_id = request.user.id
	items = Item.objects.filter(author=current_user_id).order_by("-date_created")
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
