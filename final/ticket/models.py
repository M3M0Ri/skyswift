from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from flight.models import Flight
# from flight.models import normal_user   #-----> ??
from user.models import MyUserModel
from .manager import TicketManger


class Ticket(models.Model):
    user = models.ForeignKey(MyUserModel, on_delete=models.CASCADE, related_name="tickets")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    seat_number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], null=False,
                                              blank=False)
    price = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999999)], null=True,
                                        blank=True)
    unique_id = models.CharField(max_length=100, default='', blank=True, null=True)
    active = models.BooleanField(default=True, verbose_name="being status : ")
    tickets = TicketManger()
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.unique_id = f"{self.user}-{self.flight.id}-{self.flight.__str__()}-{self.seat_number}"

        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return f"Ticket ( {self.id} ) for {self.user} with sent number : {self.seat_number} on flight {self.flight}"
