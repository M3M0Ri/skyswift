from django.db.models import Manager


class TicketManger(Manager):
    def get_ticket_id(self, id):
        return self.filter(unique_id=id)

    def find_by_seat_number(self, seat_number):
        return self.filter(seat_number=seat_number)

    def get_most_expensive_ticket(self):
        return self.order_by('-price').first()

    def current_price(self):
        if self.price.all():
            return self.price.order_by('-created')[0].price

    def cheapest_ticket(self):
        return self.order_by('price').first()

