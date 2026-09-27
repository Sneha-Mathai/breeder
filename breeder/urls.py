"""
URL configuration for breeder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from breederapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login/',views.login),
    path('index/',views.index),
    path('adminhome/',views.adminhome),
    path('registercustomer/',views.registercustomer),
    path('registerbreeder/',views.registerbreeder),
    path('loginrequest/',views.loginrequest),
    path('loginrequest/updatecus/',views.updatecus),
    path('loginrequest/updatebr/',views.updatebr),
    path('customerhome/',views.customerhome),
    path('breederhome/',views.breederhome),
    path('breederadddog/',views.breederadddog),
    path('customeradddog/',views.customeradddog),
    path('breederviewdog/',views.breederviewdog),
    path('updatedogbybreeder/',views.updatedogbybreeder),
    path('deletedogbybreeder/',views.deletedogbybreeder),
    path('customerviewdog/',views.customerviewdog),
    path('updatedogbycustomer/',views.updatedogbycustomer),
    path('deletedogbycustomer/',views.deletedogbycustomer),
    path('viewmatch/',views.viewmatch),
    path('requestforbreeding/',views.requestforbreeding),
    path('breederviewrequest/',views.breederviewrequest),
    path('acceptrequest/',views.acceptrequest),
    path('deleterequest/',views.deleterequest),
    path('customerviewstatus/',views.customerviewstatus),
    path('payment/',views.payment),
    path('chat/',views.chat),
    path('viewchat/',views.viewchat),
    path('breederrestart/',views.breederrestart),
    path('breederend/',views.breederend),
    path('customerend/',views.customerend),
    path('feedback/',views.feedback),
    path('viewfeedback/',views.viewfeedback),
    path('paymentdetails/',views.paymentdetails),
    path('offspring/',views.offspring),
    path('viewoffspring/',views.viewoffspring),
    path('viewoffspringadmin/',views.viewoffspringadmin),
    path('endprocess/',views.endprocess),
    path('viewpayment/',views.viewpayment),
    path('viewoffspringbreeder/',views.viewoffspringbreeder),
    path('breedingend/',views.breedingend),
    path('phyHome',views.phyHome),
    path('phyVp',views.phyVp),
    path('phyVOrders',views.phyVOrders),
    path('phyVDogs',views.phyVDogs),
    path('phyAddp',views.phyAddp),
    path('phyHome',views.phyHome),
    path('phyVPayments',views.phyPayments),
    path('cusStore',views.cusStore),
    path('cusOrder',views.cusOrder),
    path('cusPayments',views.cusPayments),
    path('cusCart',views.cusCart),
    path('cartRem',views.cartRem),
    path('userpay',views.userpay),
    path('pRem',views.pRem),
    path('addvet',views.addvet),
    path('vetlist',views.vetlist),


]

