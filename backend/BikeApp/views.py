import json
import random
import time
import datetime

from django.db.models import fields
import pygeohash as gh
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from passlib.context import CryptContext
from random import choice
from string import ascii_letters, digits
from math import ceil
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models.aggregates import Count
from django.db import connection
from .models import Bike_Info, Bike_Location, Bike_Status, Operator_Info, Changing_Bikes_Location, Repair_Bikes
from .models import CustomerInfo, PaymentInformation, CustomerLocation, OrderHistory, CustomerComplaints, ManagerInfo

# Password Encryption Schemes
myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])


# This function is used to encrypt passwords before saving to the database
def encrypt_password(password):
    return myctx.hash(password)


# Registration and sign in Methods for all users
# Customer should have a separate Signup method since we are expecting more fields during sign up than the manager
@api_view(('POST',))
def customer_signup(request):
    # Customer Info
    username = request.POST.get("username")
    password = request.POST.get("password")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone_num = request.POST.get("phone_number")
    gender = request.POST.get("gender")
    age = int(request.POST.get("age"))
    card_num = request.POST.get("cardNumber")
    user = ""
    try:
        # Create new customer object
        user = CustomerInfo(Customer_id=username, Customer_first_name=first_name, Customer_last_name=last_name,
                            Customer_password=encrypt_password(password),
                            Customer_phone_num=phone_num, Customer_gender=gender, Customer_age=age,
                            Customer_wallet=10, Customer_cardNumber = card_num)  # save password encrypted
        # Check for the uniqueness of the username
        get_object_or_404(CustomerInfo, Customer_id=username)
        return Response("Username already exists")
    except:
        # Successfully created a new customer entry and returned the ID
        user.save()
        user_record = CustomerInfo.objects.all().filter(Customer_id=username)
        user_record_json = serializers.serialize('json', user_record)
        return HttpResponse(user_record_json, content_type='application/json')


# Manager and Operator sign up method
@api_view(('POST',))
def sign_up(request):
    # user info
    username = request.POST.get("username")
    password = request.POST.get("password")
    user_type = request.POST.get("user_type")
    user = ""
    try:
        # according to the user type, create a new user object respectively and check if the user already exists or not
        if user_type == "Operator":
            user = Operator_Info(Username=username, Password=encrypt_password(password),
                                 Login_status=False)  # save password encrypted
            get_object_or_404(Operator_Info, Username=username)
        elif user_type == "Manager":
            user = ManagerInfo(Username=username, Password=encrypt_password(password),
                               Login_status=False)  # save password encrypted
            get_object_or_404(ManagerInfo, Username=username)
        # username already exists
        return Response("Username already exists")
    except:
        # Successfully created a new user entry and returned the user ID
        user.save()
        if user_type == "Operator":
            user_record = Operator_Info.objects.all().filter(Username=username)
        elif user_type == "Manager":
            user_record = ManagerInfo.objects.all().filter(Username=username)
        user_record_json = serializers.serialize('json', user_record, fields='Username')
        return HttpResponse(user_record_json, content_type='application/json')

# simple session key generation
def get_session_key(max):
    timestamp = str(int(time.time()))
    for i in range(0, max):
        timestamp = timestamp + str(random.randint(0, 10))

    return timestamp

# user login function; this function is generic for all users
@api_view(('POST',))
def sign_in(request):
    # User info
    username = request.POST.get("username")
    password = request.POST.get("password")
    user_type = request.POST.get("user_type")
    user_password = ""
    # response data format
    data={}
    try:
        # retrieve record from the corresponding table
        if user_type == "Operator":
            already_a_user_flag = get_object_or_404(Operator_Info, Username=username)
            already_a_user_flag.Login_status = True
            user_password = already_a_user_flag.Password
            
            data['id']=get_object_or_404(Operator_Info, Username=username).__getattribute__('id')
        elif user_type == "Customer":
            already_a_user_flag = get_object_or_404(CustomerInfo,
                                                    Customer_id=username)  # customer has a special definition for login status
            user_password = already_a_user_flag.Customer_password
            
            customer_result=CustomerInfo.objects.filter(Customer_id=username).values()
        else:
            already_a_user_flag = get_object_or_404(ManagerInfo, Username=username)
            already_a_user_flag.Login_status = True
            user_password = already_a_user_flag.Password
            
            data['id']=get_object_or_404(ManagerInfo, Username=username).__getattribute__('id')
        # Password verification
        if myctx.verify(password, user_password):
            # Sucessfully verified the user, update the login status if needed and return the user ID.
            already_a_user_flag.save()
            # Session generation
            request.session['session_key']=get_session_key(32) #  key produced by django
            request.session.set_expiry(0)
            # response data building
            if user_type=="Customer":
                customer_result_list=list(customer_result)[0]
                customer_result_list['session_key']=request.session['session_key']
                customer_result_list['pk']=customer_result_list['id']
                return HttpResponse(json.dumps(customer_result_list))
            else:
                data['session_key']=request.session['session_key']

            return HttpResponse(json.dumps(data))
        else:
            # Verification Error; incorrect password
            response = HttpResponse(username)
            response.status_code = 401
            return response
    except:
        # Username does not exist in the database
        response = HttpResponse()
        response.status_code = 404
        return response


# user logout function; generic among all users
@api_view(('POST',))
def sign_out(request):
    # user info
    username = request.POST.get("username")
    user_type = request.POST.get("user_type")
    try:
        # retrieve user record from the table and change the login_status flag
        if user_type == "Operator":
            user = get_object_or_404(Operator_Info, Username=username)
            user.Login_status = False
            user.save()
        elif user_type == "Customer":
            get_object_or_404(CustomerInfo, Customer_id=username)
            # customer has a special definition for login_status
        else:
            user = get_object_or_404(ManagerInfo, Username=username)
            user.Login_status = False
            user.save()
        
        request.session.delete(request.session.session_key)
        request.session.flush()

        return Response("Successfully Logged out")
    except:
        # username does not exist in the database
        response = HttpResponse()
        response.status_code = 404
        return response


# Customer Functions
# Search the nearest bikes around customer
@api_view(('POST',))
def nearest_bike(request):
    lat = request.POST.get("latitude")
    long = request.POST.get("longitude")
    gh_userloc = gh.encode(float(lat), float(long), 5)
    # retrieve bikes near the customer
    nearest = Bike_Location.objects.all().filter(Geohash_loc=gh_userloc)
    # retrieve bikes which are free to use
    bike_free = Bike_Status.objects.all().filter(Status=Bike_Status.Status_Options.IDLE)
    list = []
    for i, free in enumerate(bike_free):
        dict = {}
        for j, near in enumerate(nearest):
            # bike near the customer and free to use
            if near.Bike_id_id == free.Bike_id_id:
                bike_info = get_object_or_404(Bike_Info, pk=near.Bike_id_id)
                brand = bike_info.Brand
                lat = near.Loc_lat
                long = near.Loc_long
                dict['bike_id'] = str(near.Bike_id_id)
                dict['Brand'] = brand
                dict['Latitude'] = lat
                dict['Longitude'] = long
        # add bike information to the list
        if dict:
            list.append(dict)
    return HttpResponse(json.dumps(list), content_type='application/json')

# Customer return bike function
@api_view(('POST',))
def rent_bike(request):
    user_id = request.POST.get("customer_id")
    bike_id = request.POST.get("bike_id")
    user_lat = request.POST.get("latitude")
    user_long = request.POST.get("longitude")
    # user info
    user_info = get_object_or_404(CustomerInfo, pk=int(user_id))
    # bike status info
    bike_status = get_object_or_404(Bike_Status, Bike_id_id=int(bike_id))
    # check if the customer have unpaid bill
    unpaid_order = OrderHistory.objects.all().filter(Customer_id_id=int(user_id), is_complete=False).count()
    # check if the user can rent bike or not
    if user_info.Customer_login_status and unpaid_order == 0:
        # record start time
        time = datetime.datetime.now()

        # change the bike status from idle to on-road
        bike_status.Status = Bike_Status.Status_Options.ON_ROAD
        bike_status.save()


        # retrieve customer location table
        loc = CustomerLocation.objects.filter(Customer_id_id=int(user_id))
        # check user location entry, if exists, update datea
        if loc.exists():
            user_loc = get_object_or_404(CustomerLocation, Customer_id_id=int(user_id))
            user_loc.Current_location_latitude = user_lat
            user_loc.Current_location_longitude = user_long
            user_loc.save()
        # if user location entry not exists, create a new entry
        else:
            user_loc = CustomerLocation.objects.create(Customer_id_id=int(user_id), Current_location_latitude=user_lat,
                                                       Current_location_longitude=user_long)

        # create a new order record
        user_history = OrderHistory.objects.create(Customer_id_id=user_info.pk, Bike_id_id=bike_status.Bike_id_id,
                                                   Start_location_latitude=user_lat,
                                                   Start_location_longitude=user_long, Start_time=time,
                                                   is_complete=False)
        return Response("Start riding.")
    else:
        return Response("Please pay your bill.")


# calculate the ride bill
def ride_bill(start_time, end_time):
    bill = ceil((end_time.timestamp() - start_time.timestamp()) / (60.0 * 60.0)) #how many hours
    bill = 0 if bill < 0 else bill #if negative, return zero
    bill += (end_time.date() - start_time.date()).days * 24
    return bill

# Customer return bike function
@api_view(('POST',))
def return_bike(request):
    user_id = request.POST.get("customer_id")
    user_lat = request.POST.get("latitude")
    user_long = request.POST.get("longitude")
    # user order info
    user_history = get_object_or_404(OrderHistory, Customer_id_id=int(user_id), is_complete=False)
    start_time = user_history.Start_time
    # record return bike time
    end_time = datetime.datetime.now()
    # update user location entry
    user_loc = get_object_or_404(CustomerLocation, Customer_id_id=int(user_id))
    user_loc.Current_location_latitude = user_lat
    user_loc.Current_location_longitude = user_long
    user_loc.save()

    # update order history entry
    user_history.End_time = end_time
    user_history.End_location_latitude = user_lat
    user_history.End_location_longitude = user_long
    user_history.Ride_Bill = ride_bill(start_time, end_time)
    user_history.save()

    # update bike status
    bike_status = get_object_or_404(Bike_Status, Bike_id_id=user_history.Bike_id_id)
    bike_status.Status = Bike_Status.Status_Options.IDLE
    bike_status.save()

    # update bike location
    bike_loc = get_object_or_404(Bike_Location, Bike_id_id=user_history.Bike_id_id)
    bike_loc.Loc_lat = user_lat
    bike_loc.Loc_long = user_long
    bike_loc.Geohash_loc = gh.encode(float(user_lat), float(user_long), 5)
    bike_loc.save()

    order_history = OrderHistory.objects.all().filter(Customer_id_id=int(user_id), is_complete=False)
    user_history_json = serializers.serialize('json', order_history,
                                              fields=('Start_time', 'End_time', 'Ride_Bill'))
    return HttpResponse(user_history_json, content_type='application/json')

# Customer report bike defective function
@api_view(('POST',))
def report_defective(request):
    user_id = request.POST.get('customer_id')
    bike_id = request.POST.get('bike_id')
    complaint = request.POST.get('complaint_description')
    # retrieve customer order history info
    order = OrderHistory.objects.all().filter(Customer_id_id=int(user_id), Bike_id_id=int(bike_id),
                                              is_complete=False)
    bike_status = get_object_or_404(Bike_Status, Bike_id_id=int(bike_id))

    # check if customer rented the bike or not
    # if rented, close the order
    if order.exists():
        user_history = get_object_or_404(OrderHistory, Customer_id_id=int(user_id), Bike_id_id=int(bike_id),
                                         is_complete=False)
        user_history.is_complete = True
        user_history.save()
    # check the bike status
    if bike_status.Status != Bike_Status.Status_Options.Out_Of_Service:
        # update bike status
        bike_status.Status = Bike_Status.Status_Options.Out_Of_Service
        bike_status.save()

        # create repair bike record
        bike_repair = Repair_Bikes.objects.create(Bike_id_id=int(bike_id), Repair_status=False)

        # create a new complaint record
        user_complaint = CustomerComplaints.objects.create(Customer_id_id=int(user_id), Bike_id_id=int(bike_id),
                                                           Complaint_Description=complaint,
                                                           Status=CustomerComplaints.ComplaintStatus.NEW)
        user_complaint.Complaint_id = user_complaint.pk
        user_complaint.save()

    return Response("We have received your report.")

# Customer add money to application account function
@api_view(('POST',))
def add_money(request):
    # customer info
    user = get_object_or_404(CustomerInfo, pk=int(request.POST.get("Customer_id")))
    password = request.POST.get('password')
    amount = float(request.POST.get('amount'))
    # customer password verification
    if myctx.verify(password, user.Customer_password):
        user.Customer_wallet += amount
        msg = 'Successfully added money in the wallet.'
        # unblocked the user account
        if user.Customer_wallet >= 0 and user.Customer_login_status == False:
            user.Customer_login_status = True
            msg = msg + " You are Unblocked"
        user.save()
        msg = 'Successfully added money in the wallet'
    else:
        msg = 'Incorrect password'
    return Response(msg)


# Get customer balance information
@api_view(('POST',))
def balance(request):
    # customer info
    user = get_object_or_404(CustomerInfo, Customer_id=request.POST.get("Customer_id"))
    return Response(user.Customer_wallet)

# Customer pay order bill function
@api_view(('POST',))
def pay_bill(request):
    user_id = request.POST.get("customer_id") #sending the PK
    # customer info
    user_info = get_object_or_404(CustomerInfo, pk=int(user_id))
    # customer order info
    user_history = get_object_or_404(OrderHistory, Customer_id_id=int(user_id), is_complete=False)
    bill = user_history.Ride_Bill
    user_info.Customer_wallet -= bill

    # check customer account money, if less than 0, block the user account
    if user_info.Customer_wallet < 0:
        user_info.Customer_login_status = False
        user_info.save()
        return Response("You don't have sufficient money in the wallet. You are blocked temporarily")
    # close the order
    else:
        user_history.is_complete = True
        # Create a new payment record to keep track of the payments taking place in the system
        user_payment = PaymentInformation(Payment_reference_number = ''.join([choice(ascii_letters + digits) for i in range(10)]),
                                          Card_Number=user_info.Customer_cardNumber, Payment_date =  datetime.datetime.today().strftime('%d-%m-%Y'),
                                          Payment_timestamp = datetime.datetime.now().timestamp(), Customer_id_id = user_info.pk,
                                          Customer_password_id = user_info.pk)
        # Save the Database
        user_history.save()
        user_payment.save()
        user_info.save()
        return Response("Payment successful.")


# Get customer payment history data
@api_view(('POST',))
def statistics(request):
    user_id = request.POST.get("customer_id")
    # user order info
    user_history = OrderHistory.objects.all().filter(Customer_id_id=int(user_id))
    user_history_json = serializers.serialize('json', user_history, fields='Ride_Bill')
    return HttpResponse(user_history_json, content_type='application/json')


# Operator Functions
# Operator profile editing function
@api_view(('POST',))
def edit_operator_profile(request):
    # Operator info
    username = request.POST.get("username")
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")
    try:
        # retrieve operator record from database if exists
        operator = get_object_or_404(Operator_Info, Username=username)
        # password verification
        if myctx.verify(old_password, operator.Password):
            # update profile and save to DB
            operator.Password = encrypt_password(new_password)
            operator.save()
            return Response("Successfully Updated Profile")
        else:
            # incorrect old password
            return Response("Incorrect Password")
    except:
        # user does not exist in our records
        return Response("User does not exist")


# Operator registers a new bike to the system
@api_view(("POST",))
def register_new_bike(request):
    # new bike info
    brand = request.POST.get("brand")
    insurance_id = request.POST.get("insurance_id")
    loc_lat = request.POST.get("latitude")
    loc_long = request.POST.get("longitude")
    try:
        # check if a bike already exists with the same insurance id; it must be unique
        bike = get_object_or_404(Bike_Info, Insurance_id=insurance_id)
        return Response("A bike with the same Insurance ID already exists")
    except:
        # Add to bike_info table a new record
        bike = Bike_Info(Insurance_id=insurance_id, Brand=brand, Original_loc_lat=loc_lat,
                         Original_loc_long=loc_long, Original_geo_loc=gh.encode(float(loc_lat), float(loc_long), 5))
        bike.save()
        print("HELLO")
        # Add to bike_location table a new record
        bike_loc = Bike_Location(Loc_lat=loc_lat, Loc_long=loc_long,
                                 Geohash_loc=gh.encode(float(loc_lat), float(loc_long), 5),
                                 Bike_id=Bike_Info.objects.get(pk=bike.pk))
        bike_loc.save()
        # Add this bike to the bike_status table with an idle status
        bike_status = Bike_Status(Status=Bike_Status.Status_Options.IDLE, Bike_id=Bike_Info.objects.get(pk=bike.pk))
        bike_status.save()
        return Response("Successfully registered a new bike to the system")


# Track all bikes information to help the operator monitor the bikes in the system
@api_view(('GET',))
def track(request):
    # retrieve all current bikes locations from the Bike_location table
    bikes_loc = Bike_Location.objects.all()
    bikes_loc_json = serializers.serialize('json', bikes_loc, fields=('Loc_lat', 'Loc_long'))
    return HttpResponse(bikes_loc_json, content_type='application/json')


# Live tracking for a single bike in the system
@api_view(('POST',))
def track_bike(request):
    # bike info to track
    bike_id = request.POST.get("bike_id")
    lat = request.POST.get("Latitude")
    long = request.POST.get("Longitude")
    # update the Bike_location table with the final destination location of the bike
    bike_loc = get_object_or_404(Bike_Location, pk=int(bike_id))
    bike_loc.Loc_lat = lat
    bike_loc.Loc_long = long
    bike_loc.Geohash_loc = gh.encode(float(lat), float(long), 5)
    bike_loc.save()
    return Response("Updated final location after tracking")


# Defected Bikes retrieval function
@api_view(('GET',))
def retrieve_defected_bikes(request):
    # select the unrepaired bikes to return them to the operator
    bikes_to_repair = Repair_Bikes.objects.all().filter(Repair_status=False)
    list = []
    # retrieve the user complaint descrition from the CustomerComplaints table to show the operator what the problem is
    for i, bike in enumerate(bikes_to_repair):
        dict = {}
        complaint = get_object_or_404(CustomerComplaints, Bike_id=bike.Bike_id_id,
                                      Status=CustomerComplaints.ComplaintStatus.NEW)
        print(bike.Bike_id_id)
        description = complaint.Complaint_Description
        complaint_id = complaint.Complaint_id
        dict['bike_id'] = str(bike.Bike_id_id)
        dict['Description'] = description
        dict['Complaint_id'] = complaint_id
        if dict:
            list.append(dict)
    # return a list of defected bikes and their corresponding complaints to the operator
    return HttpResponse(json.dumps(list), content_type='application/json')


# Mark a bike to be repaired and save the operator ID of the operator who did the repair
@api_view(('POST',))
def repair_bike(request):
    bike_id = request.POST.get("bike_id")
    operator_id = request.POST.get("operator_id")
    # change defected bike repair status to become repaired
    bike_repair_status = get_object_or_404(Repair_Bikes, Bike_id_id=int(bike_id))
    bike_repair_status.Repair_status = True
    bike_repair_status.Operator_id = get_object_or_404(Operator_Info, pk=operator_id)
    bike_repair_status.save()
    # Update Bike_Status Table from out of service -> idle
    bike_status = get_object_or_404(Bike_Status, pk=int(bike_id))
    bike_status.Status = Bike_Status.Status_Options.IDLE
    bike_status.save()
    # Update CustomerComplaint Status to resolved
    complaint_status = get_object_or_404(CustomerComplaints, Bike_id=int(bike_id))
    complaint_status.Status = CustomerComplaints.ComplaintStatus.RESOLVED
    complaint_status.save()
    return Response("Updated Repair Status Successfully.")


# The operator can invalidate a complaint if he/she believes it is unreasonable.
@api_view(('POST',))
def invalidate_complaint(request):
    complaint_id = request.POST.get("complaint_id")
    resolution = request.POST.get("resolution")
    operator_id = request.POST.get("operator_id")
    # change CustomerComplaint status to invalid and save the reason the operator gave to invalidate it in the resolution field
    customer_complaint = get_object_or_404(CustomerComplaints, Complaint_id=complaint_id)
    customer_complaint.Status = CustomerComplaints.ComplaintStatus.INVALID
    customer_complaint.Complaint_Resolution = resolution
    customer_complaint.save()
    # change the bike_status from out of service -> idle
    bike_status = get_object_or_404(Bike_Status, pk=int(customer_complaint.Bike_id_id))
    bike_status.Status = Bike_Status.Status_Options.IDLE
    bike_status.save()
    # change the repair status of the bike to become repaired
    bike_repair_status = get_object_or_404(Repair_Bikes, Bike_id_id=customer_complaint.Bike_id_id, Repair_status=False)
    bike_repair_status.Repair_status = True
    bike_repair_status.Operator_id = get_object_or_404(Operator_Info, pk=operator_id)
    bike_repair_status.save()
    return Response("Complaint Status has been successfully updated to invalid")


# This function returns all the repairing an operator has done.
@api_view(('GET',))
def repair_history(request, operator_id):
    # retrieve the repaired bikes with the assigned operator_id
    history = Repair_Bikes.objects.all().filter(Operator_id=operator_id, Repair_status=True)
    history_json = serializers.serialize('json', history)
    return HttpResponse(history_json, content_type='application/json')


# This function changes the locations of the selected bikes to the new locations according to the operator's request
@api_view(('POST',))
def move_bikes(request):
    operator_id = int(request.POST.get("operator_id"))
    bike_ids = request.POST.getlist("bike_ids")
    lat = request.POST.get("latitude")
    long = request.POST.get("longitude")
    start_lat = ""
    start_long = ""
    loc_bias = 0  # this bias is added for the purpose of visualization on the map to avoid having all bikes displayed as one icon
    # we take the bike_ids as a string so we need to parse it into a list of bike_ids
    for bike_id in bike_ids:
        # update locations table with new location for each bike
        bike_current_location = get_object_or_404(Bike_Location, pk=int(bike_id))
        start_lat = bike_current_location.Loc_lat
        start_long = bike_current_location.Loc_long
        bike_current_location.Loc_lat = str(float(lat) + loc_bias)
        bike_current_location.Loc_long = long
        bike_current_location.Geohash_loc = gh.encode(float(lat), float(long), 5)
        bike_current_location.save()
        loc_bias += 0.0001  # minimal change in the location for better visualization
    # keep record of this change in the changing_bikes_location table; this would help in the history of movement
    bike_moving = Changing_Bikes_Location(From_loc=start_lat + " " + start_long,
                                          To_loc=str(lat) + " " + str(long),
                                          Number_bikes_moved=len(bike_ids), Moving_status=True,
                                          Operator_id=get_object_or_404(Operator_Info, pk=operator_id))
    bike_moving.save()
    return Response("Bikes moved successfully.")


# retrieve the moving actions an operator has done
@api_view(('GET',))
def move_bikes_history(request, operator_id):
    # retrieve the records that have moved bikes and operator_id equivalent to the parameter
    history = Changing_Bikes_Location.objects.all().filter(Operator_id=operator_id, Moving_status=True)
    history_json = serializers.serialize('json', history)
    return HttpResponse(history_json, content_type='application/json')


# Retrieve all information about the bikes in the system
@api_view(('GET',))
def retrieve_bikes_info(request):
    bikes_info = Bike_Info.objects.all()
    bikes_info_json = serializers.serialize('json', bikes_info)
    return HttpResponse(bikes_info_json, content_type='application/json')


# Retrieve information about a single bike in the system
@api_view(('GET',))
def retrieve_bike_info(request, bike_id):
    bike_info = Bike_Info.objects.all().filter(pk=bike_id)
    bike_info_json = serializers.serialize('json', bike_info)
    return HttpResponse(bike_info_json, content_type='application/json')


# Manager Functions
# Manager Functions for customer
# Manager search for customer info; search customers according to a condition
@api_view(('POST',))
def search_customer_info(request):
    condition = request.POST.get("keyword")
    type = request.POST.get("type")
    if condition=='':
        customer_details = CustomerInfo.objects.all()
        customer_details_json = serializers.serialize('json', customer_details, fields=(
            'Customer_id', 'Customer_first_name', 'Customer_last_name', 'Customer_phone_num', 'Customer_gender',
            'Customer_age'))
        return HttpResponse(customer_details_json, content_type='application/json')
    # Return all customers fitting the filtering condition
    if type == "Customer_id":
        cus_info = CustomerInfo.objects.all().filter(Customer_id=condition)
    elif type == "Customer_first_name":
        cus_info = CustomerInfo.objects.all().filter(Customer_first_name=condition)
    elif type == "Customer_last_name":
        cus_info = CustomerInfo.objects.all().filter(Customer_last_name=condition)
    elif type == "Customer_age":
        cus_info = CustomerInfo.objects.all().filter(Customer_age=condition)
    elif type == "Customer_gender":
        cus_info = CustomerInfo.objects.all().filter(Customer_gender=condition)
    elif type == "Customer_phone_num":
        cus_info = CustomerInfo.objects.all().filter(Customer_phone_num=condition)

    if len(cus_info) == 0:
        # No customers meeting these filtering conditions
        response = HttpResponse()
        response.status_code = 400
        return response
    else:
        #  return the customers found
        cus_info_json = serializers.serialize('json', cus_info)
        return HttpResponse(cus_info_json, content_type='application/json')


# Manager retrieval for all customer information
@api_view(('GET',))
def retrieve_customer_info(request):
    # returns all needed customer information for all customers
    customer_details = CustomerInfo.objects.all()
    customer_details_json = serializers.serialize('json', customer_details, fields=(
        'Customer_id', 'Customer_first_name', 'Customer_last_name', 'Customer_phone_num', 'Customer_gender',
        'Customer_age'))
    return HttpResponse(customer_details_json, content_type='application/json')


## Manager deleting customer information
@api_view(('POST',))
def delete_customer_info(request):
    customer_id = request.POST.get("customer_id")
    try:
        # delete the customer with the given customer_id
        already_a_user_flag = get_object_or_404(CustomerInfo, Customer_id=customer_id)
        already_a_user_flag.delete()
        return Response("Customer details removed successfully.")
    except:
        # no customer found with this id
        response = HttpResponse()
        response.status_code = 400
        return response


# Manager editing customer information
# Note: customer id should not be changed
@api_view(('POST',))
def edit_customer_info(request):
    # retrieve new info
    customer_id = request.POST.get("customer_id")
    customer_first_name = request.POST.get("customer_first_name")
    customer_last_name = request.POST.get("customer_last_name")
    customer_phone_num = request.POST.get("customer_phone_num")
    customer_age = request.POST.get("customer_age")
    customer_gender = request.POST.get("customer_gender")

    try:
        # make sure the customer exists
        already_a_user_flag = get_object_or_404(CustomerInfo, Customer_id=customer_id)
    except:
        # customer does not exist
        response = HttpResponse()
        response.status_code = 400
        return response
    # updating customer record in the database
    CustomerInfo.objects.filter(Customer_id=customer_id).update(
                                                                Customer_first_name=customer_first_name,
                                                                Customer_last_name=customer_last_name,
                                                                Customer_phone_num=customer_phone_num,
                                                                Customer_age=customer_age,
                                                                Customer_gender=customer_gender)
    return Response("Customer details updated successfully.")


# Manager adding new customer information
@api_view(('POST',))
def add_customer_info(request):
    # Customer Info
    username = request.POST.get("username")
    password = request.POST.get("password")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone_num = request.POST.get("phone_number")
    gender = request.POST.get("gender")
    age = int(request.POST.get("age"))
    card_num = request.POST.get("cardNumber")
    user = ""
    try:
        # check if the customer exists
        flag = CustomerInfo.objects.get(Customer_id=username)
        response = HttpResponse()
        response.status_code = 404
        return response
    except:
        try:
            # Create new customer object
            user = CustomerInfo(Customer_id=username, Customer_first_name=first_name, Customer_last_name=last_name,
                                Customer_password=encrypt_password(password),
                                Customer_phone_num=phone_num, Customer_gender=gender, Customer_age=age,
                                Customer_wallet=10, Customer_cardNumber = card_num)  # save password encrypted
            # Check for the uniqueness of the username
            get_object_or_404(CustomerInfo, Customer_id=username)
            return Response("Username already exists")
        except:
            # Successfully created a new customer entry and returned the ID
            user.save()
            user_record = CustomerInfo.objects.all().filter(Customer_id=username)
            user_record_json = serializers.serialize('json', user_record)
            return HttpResponse(user_record_json, content_type='application/json')


# Manager Functionality for operator
# Manager retrieval for all operator information
@api_view(('GET',))
def retrieve_operator_info(request):
    operator_details = Operator_Info.objects.all()
    operator_details_json = serializers.serialize('json', operator_details, fields=('id', 'Username', 'Login_status'))
    return HttpResponse(operator_details_json, content_type='application/json')


# Manager deleting for operator information
@api_view(('POST',))
def delete_operator_info(request):
    operator_id = request.POST.get("operator_id")
    Operator_Info.objects.filter(id=operator_id).delete()
    return Response("Operator details removed successfully.")


# Manager search for operator information
@api_view(('POST',))
def search_operator_info(request):
    condition = request.POST.get("keyword")
    type = request.POST.get("type")
    if condition=='':
        operator_details = Operator_Info.objects.all()
        operator_details_json = serializers.serialize('json', operator_details, fields=('id', 'Username', 'Login_status'))
        return HttpResponse(operator_details_json, content_type='application/json')
    # condition to retrieve information accordingly
    if type == "id":
        op_info = Operator_Info.objects.all().filter(id=condition)
    elif type == "Username":
        op_info = Operator_Info.objects.all().filter(Username=condition)
    elif type == "Login_status":
        op_info = Operator_Info.objects.all().filter(Login_status=condition)
    # check if any operators were found given the conditions
    if len(op_info) == 0:
        # no operators found to meet the conditions
        response = HttpResponse()
        response.status_code = 400
        return response
    else:
        # return operators found that meet the conditions
        op_info_json = serializers.serialize('json', op_info)
        return HttpResponse(op_info_json, content_type='application/json')


# Manager adding new operator information
@api_view(('POST',))
def add_operator_info(request):
    # user info
    username = request.POST.get("username")
    password = request.POST.get("password")
    user_type = request.POST.get("user_type")
    user = ""
    try:
        # according to the user type, create a new user object respectively and check if the user already exists or not
        user = Operator_Info(Username=username, Password=encrypt_password(password),
                                Login_status=False)  # save password encrypted
        get_object_or_404(Operator_Info, Username=username)
        return Response("Username already exists")
    except:
        # Successfully created a new user entry and returned the user ID
        user.save()
        user_record = Operator_Info.objects.all().filter(Username=username)
        user_record_json = serializers.serialize('json', user_record, fields='Username')
        return HttpResponse(user_record_json, content_type='application/json')

# Manager Functionality for bike
# Manager search for bike information
@api_view(('POST',))
def search_bike_info(request):
    condition = request.POST.get("keyword")
    type = request.POST.get("type")
    # condition on which we filter the bikes
    if type == "Brand":
        bike_info = Bike_Info.objects.all().filter(Brand=condition)
    else:
        bike_info = Bike_Info.objects.all().filter(Insurance_id=condition)
    # check if there were any bikes that meet the conditions
    if len(bike_info) == 0:
        # no bikes meeting the conditions
        response = HttpResponse()
        response.status_code = 400
        return response
    else:
        # return bikes meeting the conditions
        bike_info_json = serializers.serialize('json', bike_info)
        return HttpResponse(bike_info_json, content_type='application/json')


# Manager Visualization
# Manager Visualisation for customer gender
@api_view(('GET',))
def customer_gender(request):
    # retrieve all customers gender info
    customer_details = CustomerInfo.objects.values('Customer_gender').annotate(Count=Count('Customer_id'))
    customer_details_json = json.dumps(list(customer_details))
    return HttpResponse(customer_details_json, content_type='application/json')


# Manager Visualisation for customer age
def customer_age(request):
    response = []
    for i in range(10, 60, 10):
        item = {}
        item['name'] = str(i) + ' to ' + str(i + 10)
        item['value'] = CustomerInfo.objects.filter(Customer_age__range=[i, i + 9]).count()
        response.append(item)
    customer_details_json = json.dumps(response)
    return HttpResponse(customer_details_json, content_type='application/json')


# Manager Visualisation for customer order history
@api_view(('GET',))
def customer_order_history(request):
    cursor = connection.cursor()
    cursor.execute("""SELECT  1 as id,'inside 5 minutes' as name,count(*) as value FROM (SELECT id,(julianday(End_time)-julianday(Start_time))*24*3600 as Service_time,Bike_id_id,Start_time,End_time FROM BikeApp_orderhistory WHERE is_complete=True) WHERE Service_time BETWEEN 0 AND 300
        UNION
        SELECT  2 as id,'inside 10 minutes' as name,count(*) as value FROM (SELECT id,(julianday(End_time)-julianday(Start_time))*24*3600 as Service_time,Bike_id_id,Start_time,End_time FROM BikeApp_orderhistory WHERE is_complete=True) WHERE Service_time BETWEEN 300 AND 600
        UNION
        SELECT  3 as id,'inside 30 minutes' as name,count(*) as value FROM (SELECT id,(julianday(End_time)-julianday(Start_time))*24*3600 as Service_time,Bike_id_id,Start_time,End_time FROM BikeApp_orderhistory WHERE is_complete=True) WHERE Service_time BETWEEN 600 AND 1800
        UNION
        SELECT  4 as id,'over 30 minutes' as name,count(*) as value FROM (SELECT id,(julianday(End_time)-julianday(Start_time))*24*3600 as Service_time,Bike_id_id,Start_time,End_time FROM BikeApp_orderhistory WHERE is_complete=True) WHERE Service_time > 1800""")
    raw = cursor.fetchall()
    customer_order_history_json = json.dumps(raw)
    return HttpResponse(customer_order_history_json, content_type='application/json')


# Manager Visualisation for operator-Complaint status
@api_view(('GET',))
def operator_complaint_status(request):
    operator_complaint_status = CustomerComplaints.objects.values('Status').annotate(Count=Count('Complaint_id'))
    operator_complaint_status_json = json.dumps(list(operator_complaint_status))
    return HttpResponse(operator_complaint_status_json, content_type='application/json')


# Manager Visualisation for operator-Login status
@api_view(('GET',))
def operator_login_status(request):
    operator_details = Operator_Info.objects.values('Login_status').annotate(Count=Count('id'))
    operator_details_json = json.dumps(list(operator_details))
    return HttpResponse(operator_details_json, content_type='application/json')


# Manager Visualisation for Bike-Brand
@api_view(('GET',))
def bike_brand(request):
    bike_details = Bike_Info.objects.values('Brand').annotate(Count=Count('id'))
    bike_details_json = json.dumps(list(bike_details))
    return HttpResponse(bike_details_json, content_type='application/json')


# Manager Visualisation for Bike-Status
@api_view(('GET',))
def bike_status(request):
    bike_details = Bike_Status.objects.values('Status').annotate(value=Count('id'))
    bike_details_json = json.dumps(list(bike_details))
    return HttpResponse(bike_details_json, content_type='application/json')

## Manager Visualisation for Bike-month-distribution
@api_view(('POST',))
def bike_hours_status(request):
    flag = datetime.datetime.strptime(request.POST.get('Day'),"%Y-%m-%d")
    grained = request.POST.get('grainedLevel')
    intervals = int(request.POST.get('intervals'))

    if grained=='1':
        order = OrderHistory.objects
    else:
        order = OrderHistory.objects.filter(Start_time__year=flag.year).filter(Start_time__month=flag.month).filter(Start_time__day=flag.day)

    day = []
    for hour in range(0,24,intervals):
        element = order.filter(Start_time__hour__gte=hour).filter(Start_time__hour__lt=(hour+intervals)).aggregate(value=Count('Bike_id'))
        element['name'] = str(hour)+'-'+str(hour+intervals)
        day.append(element)

    result={}
    result['name']=request.POST.get('Day')
    result['value']=day

    customer_order_history_json = json.dumps(result)
    return HttpResponse(customer_order_history_json, content_type='application/json')

## Manager Visualisation for Bike-weeks-distribution
@api_view(('POST',))
def bike_weeks_status(request):
    flag = datetime.datetime.strptime(request.POST.get('StartDay'),"%Y-%m-%d")
    grained = request.POST.get('grainedLevel')
    intervals = int(request.POST.get('intervals'))

    results=[]
    currentTime = flag
    for i in range(7):
        currentTime = currentTime + datetime.timedelta(days=1)
        if grained=='1':
            order = OrderHistory.objects.filter(Start_time__week_day=i+1)
        else:
            order = OrderHistory.objects.filter(Start_time__year=currentTime.year).filter(Start_time__month=currentTime.month).filter(Start_time__day=currentTime.day)

        day = []
        for hour in range(0,24,intervals):
            element = order.filter(Start_time__hour__gte=hour).filter(Start_time__hour__lt=(hour+intervals)).aggregate(value=Count('Bike_id'))
            element['name'] = str(hour)+'-'+str(hour+intervals)
            day.append(element)

        eachday={}
        eachday['name']='day '+str(i)
        eachday['value']=day

        results.append(eachday)

    order_history_json = json.dumps(results)
    return HttpResponse(order_history_json, content_type='application/json')

## Manager Visualisation for Bike-month-distribution
@api_view(('POST',))
def bike_years_status(request):
    Start_Year=request.POST.get('Start_Year')
    Start_Month=request.POST.get('Start_Month')
    End_Year=request.POST.get('End_Year')
    End_Month=request.POST.get('End_Month')
    grained = request.POST.get('grainedLevel')
   
    yearsOrderList = []

    if grained=='1':
        monthRange=range(1,13)
        monthOrderList = []
        for month in monthRange:
            monthOrder = OrderHistory.objects.filter(Start_time__month=month).aggregate(value=Count('Bike_id'))
            monthOrder['name']=str(month)
            monthOrderList.append(monthOrder)
        item={}
        item['name']=str('year')
        item['value']=monthOrderList
        yearsOrderList.append(item)
    else:
        for year in range(int(Start_Year),int(End_Year)+1):
            monthOrderList = []
            
            monthRange = []
            if int(Start_Year)==int(End_Year):
                monthRange=range(int(Start_Month),int(End_Month)+1)
            elif year==int(Start_Year):
                monthRange=range(int(Start_Month),13)
            elif year==int(End_Year):
                monthRange=range(1,int(End_Month)+1)
            else:
                monthRange=range(1,13)

            for month in monthRange:
                monthOrder = OrderHistory.objects.filter(Start_time__year=year).filter(Start_time__month=month).aggregate(value=Count('Bike_id'))
                monthOrder['name']=str(year) + '-' + str(month)
                monthOrderList.append(monthOrder)

            item={}
            item['name']=str(year)
            item['value']=monthOrderList
            yearsOrderList.append(item)
        
    # customer_order_history_json = serializers.serialize('json', results)
    customer_order_history_json = json.dumps(yearsOrderList)
    return HttpResponse(customer_order_history_json, content_type='application/json')

@api_view(['POST'])
def get_condition_bike(request):
    start=datetime.datetime.strptime(request.POST.get('start'),"%Y-%m-%d %H:%M:%S")
    end=datetime.datetime.strptime(request.POST.get('end'),"%Y-%m-%d %H:%M:%S")
    
    bike_location_json=json.dumps(list(OrderHistory.objects.filter(Start_time__range=(start,end)).values('Start_location_latitude','Start_location_longitude')))
    return HttpResponse(bike_location_json)

@api_view(['POST'])
def random_order_data(request):
    num=int(request.POST.get('max'))
    for i in range(num):
        time=datetime.datetime.now()
        StartTime=time+datetime.timedelta(days=random.randint(0,200),minutes=random.randint(0,72000))
        EndTime=StartTime+datetime.timedelta(minutes=random.randint(10,100))
        OrderHistory.objects.create(Customer_id_id=6, 
                                        Bike_id_id=5,
                                        Start_location_latitude=random.random()*0.1+55.811936,
                                        Start_location_longitude=random.random()*0.3-4.343057, 
                                        End_location_latitude=random.random()*0.1+55.811936,
                                        End_location_longitude=random.random()*0.3-4.343057,
                                        Start_time=StartTime,
                                        End_time=EndTime,
                                        is_complete=True)

    return HttpResponse('😀')