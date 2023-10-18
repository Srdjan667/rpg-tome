"""
All helper functions for library are stored here
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


# Avoids ?page duplication in URL
def url_strip_page_number(request):
    request = request.GET.copy()
    request.pop("page", None)

    return request.urlencode()


def path_without_page(request):
    return f"{request.path}?{url_strip_page_number(request)}"


# Populate dict for filtering based on GET criteria
def prep_filters(FILTERS):
    filters = {}
    for k, v in FILTERS.items():
        if v:
            filters[k] = v
    return filters


# All rarities that are unchecked in HTML form should be exluded from final query
def exclude_unchecked_rarities(items, rarity_dict):
    rarity_value = {
        "common": 1,
        "uncommon": 2,
        "rare": 3,
        "very rare": 4,
        "legendary": 5,
        "artifact": 6,
    }

    for k, v in rarity_dict.items():
        if v is None:
            items = items.exclude(rarity=rarity_value[k])
    return items
