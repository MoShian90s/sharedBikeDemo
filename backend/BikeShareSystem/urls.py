"""BikeShareSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from BikeApp import views
from django.views.generic.base import TemplateView
urlpatterns = {
    path('',TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('signin/', views.sign_in, name='signIn'),
    path('signup/', views.sign_up, name='signUp'),  # for operator and manager only
    path('signout/', views.sign_out, name='signOut'),

    #Customer
    path('nearestbike/', views.nearest_bike, name='nearestBike'),
    path('customer/signup/', views.customer_signup, name="customerSignUp"),
    path('customer/rentbike/', views.rent_bike, name='rentBike'),
    path('customer/returnbike/', views.return_bike, name='returnBike'),
    path('customer/paybill/', views.pay_bill, name='payBill'),
    path('customer/addmoney/', views.add_money, name='addMoney'),
    path('customer/balance/', views.balance, name='balance'),
    path('customer/reportdefective/', views.report_defective, name='reportDefective'),
    path('customer/statistics/', views.statistics, name='statistics'),

    #Operator
    path('operator/editprofile/', views.edit_operator_profile, name='editOperatorProfile'),
    path('operator/registerbike/', views.register_new_bike, name = 'registerNewBike'),
    path('operator/track/', views.track, name='trackBikes'),
    path('operator/trackbike/', views.track_bike, name='trackBike'),
    path('operator/defectedbikes/', views.retrieve_defected_bikes, name='defectedBikes'),
    path('operator/repairbike/', views.repair_bike, name='repairBike'),
    path('operator/<int:operator_id>/repairhistory/', views.repair_history, name='repairHistory'),
    path('operator/movebikes/', views.move_bikes, name='moveBikes'),
    path('operator/<int:operator_id>/movinghistory/', views.move_bikes_history, name='movingHistory'),
    path('operator/invalidatecomplaint/', views.invalidate_complaint, name = 'InvalidateComplaint'),

    #Operator and Manager
    path('bikesinfo/', views.retrieve_bikes_info, name='bikesInfo'), #this retrieves all bikes
    path('<int:bike_id>/bikeinfo/', views.retrieve_bike_info, name='bikeInfo'), #this retrieves only one

    #Manager
    ## customer
    path('manager/searchcustomerinfo/', views.search_customer_info, name='searchCustomerInfo'),
    path('manager/retrievecustomerinfo/', views.retrieve_customer_info, name='retrieveCustomerInfo'),
    path('manager/deletecustomerinfo/', views.delete_customer_info, name='DeleteCustomerInfo'),
    path('manager/editcustomerinfo/', views.edit_customer_info, name='EditCustomerInfo'),
    path('manager/addcustomerinfo/', views.add_customer_info, name='AddCustomerInfo'),
    ## operator
    path('manager/deleteoperatorinfo/', views.delete_operator_info, name='DeleteOperatorInfo'),
    path('manager/retrieveoperatorinfo/', views.retrieve_operator_info, name='RetrieveOperatorInfo'),
    path('manager/addoperatorinfo/', views.add_operator_info, name='AddOperatorInfo'),
    path('manager/searchoperatorinfo/', views.search_operator_info, name='SearchOperatorInfo'),
    ## bikes
    path('manager/retrievebikeinfo/', views.retrieve_bikes_info, name='RetrieveBikeInfo'),
    path('manager/searchbikeinfo/', views.search_bike_info, name='SearchBikeInfo'),

    # Manager Visualisations
    ## customer
    path('manager/customer_gender/', views.customer_gender, name='customer_gender'),
    path('manager/customer_age/', views.customer_age, name='customer_age'),
    path('manager/customer_order_history/', views.customer_order_history, name='customer_order_history'),
    ## operator
    path('manager/operator_complaint_status/', views.operator_complaint_status, name='operator_complaint_status'),
    path('manager/operator_login_status/', views.operator_login_status, name='operator_login_status'),
    ## bike
    path('manager/bike_brand/', views.bike_brand, name='bike_brand'),
    path('manager/bike_status/', views.bike_status, name='bike_status'),
    path('manager/bike_hours_status/', views.bike_hours_status, name='bike_hours_status'),
    path('manager/bike_weeks_status/', views.bike_weeks_status, name='bike_weeks_status'),
    path('manager/bike_years_status/', views.bike_years_status, name='bike_years_status'),
    path('manager/get_condition_bike/', views.get_condition_bike, name='get_condition_bike'),
    
    # test
    path('manager/random_order_data/', views.random_order_data, name='random_order_data'),
}
