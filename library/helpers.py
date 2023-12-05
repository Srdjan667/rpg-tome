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
