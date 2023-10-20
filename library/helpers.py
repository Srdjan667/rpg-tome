"""
All helper functions for library are stored here
"""


def get_sort_parameters(request, get_criteria, l):
    parameters = {}
    for i in l:
        if i != request.GET.get(get_criteria, None):
            parameters[i] = None
        else:
            parameters[i] = i

    return parameters


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


def get_rarity_checkboxes(request, RARITIES):
    rarity_dict = {}

    # Make a dict of all checked out rarity checkboxes
    for r in RARITIES:
        rarity_dict[r] = request.GET.get(r, None)
    return rarity_dict
