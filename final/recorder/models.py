from django.db import models

from ticket.models import Ticket


# Create your models here.

class recordOfTickets(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING, verbose_name="Field of ticket")
    time_creation = models.DateTimeField(verbose_name="time creation of record")
