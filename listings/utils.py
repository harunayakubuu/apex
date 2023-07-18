from .models import Listing


def get_locations(self):
    listings = Listing.objects.all()
    locations = []
    for listing in listings:
        locations.append(listing.location)
