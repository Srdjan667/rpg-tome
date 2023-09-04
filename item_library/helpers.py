"""
All helper functions for item_library are stored here
"""

SORTING_CRITERIA = ["date created", "title", "rarity", "value"]
SORTING_DIRECTIONS = ["ascending", "descending"]

def get_sort_criteria(request):
	sorting_dict = {}

	for i in SORTING_CRITERIA:
		if i != request.GET.get("order", None):
			sorting_dict[i] = None
		else:
			sorting_dict[i] = i

	return sorting_dict


def get_sort_direction(request):
	sort_direction = {}
	for i in SORTING_DIRECTIONS:
		if i != request.GET.get("direction", None):
			sort_direction[i] = None
		else:
			sort_direction[i] = i

	return sort_direction