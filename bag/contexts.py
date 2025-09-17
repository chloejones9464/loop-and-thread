from patterns.models import Pattern
from decimal import Decimal


def bag_contents(request):
    bag = request.session.get("bag", {})

    bag_items = []
    total = Decimal("0.00")
    pattern_count = 0

    ids = bag.keys()
    patterns = Pattern.objects.filter(pk__in=ids)

    for pattern in patterns:
        total += pattern.price
        bag_items.append({
            "item_id": pattern.id,
            "pattern": pattern,
        })

    pattern_count = len(patterns)

    grand_total = total

    context = {
        "bag_items": bag_items,
        "total": total,
        "pattern_count": pattern_count,
        "grand_total": grand_total,
    }

    return context
