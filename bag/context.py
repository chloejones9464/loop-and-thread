

def bag_content(request):

    bag_items = []
    total = 0
    pattern_count = 0

    context = {
        'bag_items': bag_items,
        'total': total,
        'pattern_count': pattern_count,
    }

    return context
