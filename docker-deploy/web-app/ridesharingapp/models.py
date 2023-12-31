from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class VehicleType(models.TextChoices):
    FOUR_SEATER = 'FOUR_SEATER', _('4 Seats')
    SIX_SEATER = 'SIX_SEATER', _('6 Seats')


class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=15,
                                    choices=VehicleType.choices,
                                    default=VehicleType.FOUR_SEATER, )
    license_no = models.CharField(max_length=500, blank=False, default=None)
    special_info = models.TextField(blank=True, null=True, default=None)


class Party(models.Model):
    owner = models.ForeignKey(User, related_name='party_owner', on_delete=models.CASCADE)
    passengers = models.IntegerField(default=1)


class Ride(models.Model):
    class RideStatus(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        CONFIRMED = 'CONFIRMED', _('Confirmed')
        COMPLETED = 'COMPLETED', _('Completed')

    rideId = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, related_name='driver', on_delete=models.CASCADE, blank=True, null=True)
    rideOwner = models.ForeignKey(Party, related_name='ride_owner', on_delete=models.CASCADE, blank=False, null=False)
    isSharable = models.BooleanField(default=False)
    rideShared = models.ManyToManyField(Party, blank=True)
    source = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)
    destinationArrivalTimeStamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=RideStatus.choices,
        default=RideStatus.OPEN,
    )
    availablePassengers = models.IntegerField(default=4,
                                        validators=[MaxValueValidator(8), MinValueValidator(1)])
    vehicleType = models.CharField(max_length=15, choices=VehicleType.choices, blank=True, null=True)
    specialRequests = models.TextField(blank=True, null=True, default=None)
    def isRideEditable(self):
        return self.status == self.RideStatus.OPEN
