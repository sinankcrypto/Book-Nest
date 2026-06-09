from .models import ReadingListBook

def reorder_positons(reading_list):
    books = (
        ReadingListBook.objects
        .filter(reading_list=reading_list)
        .order_by("position")
    )

    for index, item in enumerate(books, start=1):
        item.position = index
        item.save(update_fields=["position"])
