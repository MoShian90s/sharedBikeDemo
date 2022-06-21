from django.db import models
from django.utils import timezone
import pygeohash as gh
import random, math, string


# Table that carries all initial information of the bikes when registered to the system
class Bike_Info(models.Model):
    Insurance_id = models.CharField(max_length=100)
    Brand = models.CharField(max_length=100)
    Original_loc_lat = models.CharField(max_length=100)
    Original_loc_long = models.CharField(max_length=100)
    Original_geo_loc = models.CharField(max_length=100)

    def __str__(self):
        return self.Insurance_id


# Table that shows the status of all bikes in the system; on road -> used, idle -> can be rented, out of service -> defected and yet to be repaired
class Bike_Status(models.Model):
    Bike_id = models.ForeignKey(Bike_Info, on_delete=models.CASCADE)

    class Status_Options(models.TextChoices):
        ON_ROAD = 'On Road',
        IDLE = 'Idle',
        Out_Of_Service = 'Out of Service'

    Status = models.CharField(
        max_length=20,
        choices=Status_Options.choices,
        default=Status_Options.IDLE
    )

    def __str__(self):
        return self.Bike_id


# Table that contains all initial information of the customer when registered to the system
# Customer_login_status indicates if the customer can rent a bike or not
class CustomerInfo(models.Model):
    Customer_id = models.CharField(max_length=100)
    Customer_first_name = models.CharField(max_length=100)
    Customer_last_name = models.CharField(max_length=100)
    Customer_password = models.CharField(max_length=100)
    Customer_phone_num = models.CharField(max_length=100)
    Customer_gender = models.CharField(max_length=100)
    Customer_age = models.IntegerField()
    Customer_login_status = models.BooleanField(default=True)
    Customer_wallet = models.FloatField(default=20.00)
    Customer_cardNumber = models.CharField(max_length=100)

    def __str__(self):
        return self.Customer_id


# Talbe that contains order information of customer rent a bike
class OrderHistory(models.Model):
    Customer_id = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    Bike_id = models.ForeignKey(Bike_Info, on_delete=models.CASCADE, default=0)
    Start_location_latitude = models.CharField(max_length=100)
    Start_location_longitude = models.CharField(max_length=100)
    End_location_latitude = models.CharField(max_length=100, null=True)
    End_location_longitude = models.CharField(max_length=100, null=True)

    Ride_Bill = models.FloatField(default=0.00, null=True)
    Start_time = models.DateTimeField(default=timezone.now)
    End_time = models.DateTimeField(null=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.Customer_id


# Table that contains customer bank card information and payment details
class PaymentInformation(models.Model):
    Customer_id = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    Payment_reference_number = models.CharField(max_length=100)
    Card_Number = models.CharField(max_length=100)
    Customer_password = models.ForeignKey(CustomerInfo, related_name="password", null=True, on_delete=models.CASCADE)
    Payment_date = models.CharField(max_length=100)
    Payment_timestamp = models.CharField(max_length=100)

    def __str__(self):
        return self.Payment_reference_number


# Table that records customer location information
class CustomerLocation(models.Model):
    Customer_id = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    Current_location_latitude = models.CharField(max_length=100)
    Current_location_longitude = models.CharField(max_length=100)

    def __str__(self):
        return self.Customer_id


# Table that contains customer complaint information and which bike is complaint about, having four complaint status:
# In progress -> operator is checking the bike, New -> operator havn't checked the bike, Resolved -> operator have checked the bike, Invalid -> bike is fine
class CustomerComplaints(models.Model):
    Customer_id = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    Complaint_id = models.CharField(max_length=100, null=True)
    Bike_id = models.ForeignKey(Bike_Info, related_name='Bike_ID', null=True, on_delete=models.CASCADE)
    Complaint_Description = models.CharField(max_length=1000)
    Complaint_Resolution = models.CharField(max_length=1000, null=True)

    # customer complaint status
    class ComplaintStatus(models.TextChoices):
        IN_PROGRESS = 'In Progress',
        NEW = 'New',
        RESOLVED = 'Resolved',
        INVALID = 'Invalid'

    Status = models.CharField(
        max_length=20,
        choices=ComplaintStatus.choices,
        default=ComplaintStatus.NEW
    )

    def __str__(self):
        return self.Complaint_id


# Table to keep track of updated bike locations in the system
class Bike_Location(models.Model):
    Bike_id = models.ForeignKey(Bike_Info, on_delete=models.CASCADE)
    Customer_id = models.ForeignKey(CustomerInfo, related_name='Customer_ID', null=True, on_delete=models.CASCADE)
    Loc_lat = models.CharField(max_length=100)
    Loc_long = models.CharField(max_length=100)
    Geohash_loc = models.CharField(max_length=100)

    def __str__(self):
        return self.Bike_id


# Table containing operator's credentials
class Operator_Info(models.Model):
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Login_status = models.BooleanField(default=False)

    def __str__(self):
        return self.Username


# Table containing moving history of bikes to keep track of the movements in the system
class Changing_Bikes_Location(models.Model):
    Operator_id = models.ForeignKey(Operator_Info, on_delete=models.CASCADE)
    From_loc = models.CharField(max_length=100)
    To_loc = models.CharField(max_length=100)
    Number_bikes_moved = models.IntegerField()
    Moving_status = models.BooleanField(default=False)

    def __str__(self):
        return self.Operator_id


# Table containing all bikes reported to be defected in the system and whether they have been repaired or not
class Repair_Bikes(models.Model):
    Bike_id = models.ForeignKey(Bike_Info, on_delete=models.CASCADE)
    Operator_id = models.ForeignKey(Operator_Info, on_delete=models.CASCADE, null=True)
    Repair_status = models.BooleanField(default=False)

    def __str__(self):
        return self.Bike_id


# Table containing manager's credential
class ManagerInfo(models.Model):
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Login_status = models.BooleanField(default=False)

    def __str__(self):
        return self.Username

# Populate the needed tables in the DB
# THIS SECTION IS COMMENTED TO AVOID REPOPULATING. BE CAREFUL IF YOU UNCOMMENT IT :)
# # BIKE INFO TABLE
# def create_random_point(x0, y0, distance):
#     r = distance / 111300
#     u = random.uniform(0, 1)
#     v = random.uniform(0, 1)
#     w = r * math.sqrt(u)
#     t = 2 * math.pi * v
#     x = w * math.cos(t)
#     x1 = x / math.cos(y0)
#     y = w * math.sin(t)
#     return (str(x0 + x1), str(y0 + y))
#
#
# letters = list(string.ascii_uppercase)
# bike_brands = ["Raleigh", "Focus", "Felt", "Specialized", "Trek", "Pinarello", "Eddy Merchx", "BMC", "Giant", "GT"]
# for i in range(1,101):
#     lat, long = create_random_point(55.8724, -4.2891, random.randrange(1000, 10000, 100))
#     bike = Bike_Info(Insurance_id=random.choice(letters) + str(random.randint(100, 1000)),
#                   Brand=random.choice(bike_brands), Original_loc_lat=lat,
#                   Original_loc_long=long, Original_geo_loc=gh.encode(float(lat), float(long), 5))
#     bike.save()
#     # BIKE LOCATION TABLE
#     bike_loc = Bike_Location(Loc_lat=lat, Loc_long=long, Geohash_loc=gh.encode(float(lat), float(long), 5),
#                              Bike_id=Bike_Info.objects.get(pk=i))
#     bike_loc.save()
# # BIKE STATUS TABLE
# status = ["Idle", "On Road", "Out of Service"]
# for i in range(1, 101):
#     m = Bike_Status(Bike_id=Bike_Info.objects.get(pk=i), Status=random.choice(status))
#     m.save()
