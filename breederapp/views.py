from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from django.contrib.auth import authenticate
from datetime import date,datetime
from django.contrib import messages
from .models import *
from django.db.models import F,Q
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login

# Create your views here.
def index(request):
    return render(request,'index.html')
def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        print(username, "######################", password)
        user = authenticate(username=username, password=password) # Retrieve the user object
        print(user)
        
        if user is not None:
            auth_login(request, user)   # cycles the session key
            request.session['uid'] = user.id
            request.session['type'] = user.usertype
            if user.usertype == 'admin':
                request.session['uid'] = user.id
                request.session['type'] = 'admin'
                print("Admin login success")
                messages.info(request, "Admin login success")
                return redirect('/adminhome')
            elif user.usertype == 'breeder':
                request.session['uid'] = user.id
                request.session['type'] = 'breeder'
                print("breeder login success")
                messages.info(request, "breeder login success")
                return redirect('/breederhome')

            elif user.usertype == 'customer':
                request.session['uid'] = user.id
                request.session['type'] = 'customer'
                print("customer login success")
                messages.info(request, "customer login success")
                return redirect('/customerhome')

            elif user.usertype == 'physician':

                print("Physician login success")
                messages.info(request, "Physician login success")
                return redirect('/phyHome')
        else:
            print("Login Failed")
            messages.info(request, " login Failed")
    return render(request,'login.html')
def adminhome(request):
    return render(request,'admin/adminhome.html')
def customerhome(request):
    return render(request,'customer/customerhome.html')
def breederhome(request):
    return render(request,'breeder/breederhome.html')

def registercustomer(request):
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST['password']
        phone = request.POST['phone']
        place = request.POST.get('place')
        district=request.POST.get('district')
        if Customer.objects.filter(email=email,phone=phone).exists():
            print("User already exists")
            messages.info(request, "already exists")
        else:
            loginqry=Login.objects.create_user(username=email,is_active=0,password=password,viewpassword=password,usertype='customer')
            loginqry.save()

            reg = Customer.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    password=password,
                    user=loginqry,
                    place=place,
                    district=district,
                )
            reg.save()
            messages.info(request, "Registered successfully")
            return redirect('/login')
    return render(request, 'registercustomer.html')
def registerbreeder(request):
         if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST['password']
            phone = request.POST['phone']
            place = request.POST.get('place')
            district=request.POST.get('district')

            if Breeder.objects.filter(email=email,phone=phone).exists():
                print("User already exists")
                messages.info(request, "already exists")
            else:
                loginqry=Login.objects.create_user(username=email,is_active=0,password=password,viewpassword=password,usertype='breeder')
                loginqry.save()

                ex = Breeder.objects.create(
                    name=name,
                    email=email,
                    password=password,
                    phone=phone,
                    place=place,
                    user=loginqry,
                    district=district,
                
                )
                ex.save()
                messages.info(request, "Registered successfully")

                return redirect('/login')

         return render(request, 'registerbreeder.html')
def loginrequest(request):
    res=Customer.objects.filter(status='pending')
    resu=Breeder.objects.filter(status='pending')
    return render(request,'admin/loginrequest.html',{"res":res,"resu":resu})

def updatebr(request):
    status=request.GET['status']
    id=request.GET.get('id')

    if status=='1':
        Login.objects.filter(id=id).update(is_active=1)
        Breeder.objects.filter(user_id=id).update(status='approved')
        messages.info(request,'approved')
    else:
        Login.objects.filter(id=id).update(is_active=0)
        Breeder.objects.filter(user_id=id).delete()
        messages.info(request,'rejected')
    return HttpResponseRedirect('/loginrequest')
def updatecus(request):
    status=request.GET['status']
    id=request.GET.get('id')

    if status=='1':
        Login.objects.filter(id=id).update(is_active=1)
        Customer.objects.filter(user_id=id).update(status='approved')

        messages.info(request,'approved')
    else:
        Login.objects.filter(id=id).update(is_active=0)
        Customer.objects.filter(user_id=id).delete()

        messages.info(request,'rejected')
    return HttpResponseRedirect('/loginrequest')

def breederadddog(request):
    uid=request.session['uid']
    if request.POST:
        name=request.POST['name']
        price=request.POST['price']
        description=request.POST['description']
        img=request.FILES['image']
        breed = request.POST.get('breed')
        gender = request.POST.get('gender')
        medication = request.POST.get('medication')
        certificate=request.POST.get('certificate')

        age = request.POST['age']
        expert=Breeder.objects.get(user_id=uid)
        if Breederdog.objects.filter(name=name,breeder_id__user_id=uid).exists():
            print("User already exists")
            messages.info(request, "dog already exists")
        else:
            registerqry=Breederdog.objects.create(name=name,gender=gender,price=price,breed=breed,description=description,age=age,image=img,breeder=expert,medication=medication,certificate=certificate)
            registerqry.save()
            messages.info(request, "added successfully")
    return render(request,'breeder/breederadddog.html')
def customeradddog(request):
    uid=request.session['uid']
    if request.POST:
        name=request.POST['name']
        description=request.POST['description']
        img=request.FILES['image']
        breed = request.POST.get('breed')
        medication = request.POST.get('medication')
        gender = request.POST.get('gender')
        age = request.POST['age']
        expert=Customer.objects.get(user_id=uid)
        if Customerdog.objects.filter(name=name,customer_id__user_id=uid).exists():
            print("User already exists")
            messages.info(request, "dog already exists")
        else:
            registerqry=Customerdog.objects.create(name=name,gender=gender,breed=breed,description=description,age=age,image=img,customer=expert,medication=medication)
            registerqry.save()
            messages.info(request, "added successfully")
    return render(request,'customer/customeradddog.html')

def breederviewdog(request):
    uid=request.session['uid']
    res=Breederdog.objects.filter(Q(breeder_id__user_id=uid)& Q(status='pending'))
    resu=Breederdog.objects.filter(Q(breeder_id__user_id=uid) & Q(status='requested'))

    return render(request,'breeder/breederviewdog.html',{"res":res,"resu":resu})

def deletedogbybreeder(request):
    id=request.GET.get('id')
    Breederdog.objects.filter(id=id).delete()
    messages.info(request, "deleted successfully")

    return HttpResponseRedirect('/breederviewdog')
def updatedogbybreeder(request):
    id=request.GET.get('id')
    qy=Breederdog.objects.filter(id=id)
    if request.POST:
        name=request.POST['name']
        price=request.POST['price']
        description=request.POST['description']
        img=request.FILES['image']
        breed = request.POST.get('breed')
        medication = request.POST.get('medication')
        gender = request.POST.get('gender')
        age = request.POST['age']
        certificate=request.POST['certficate']

        registerqry = Breederdog.objects.get(id=id)  
        registerqry.name = name
        registerqry.price = price
        registerqry.description = description
        registerqry.gender = gender
        registerqry.medication = medication
        registerqry.breed=breed
        registerqry.image = img
        registerqry.age = age
        registerqry.certificate=certificate

        registerqry.save()
        messages.info(request, "updated successfully")

        return redirect('/breederviewdog')
    return render(request,'breeder/updatebreederdog.html',{"qy":qy})

def customerviewdog(request):
    uid=request.session['uid']
    res=Customerdog.objects.filter(Q(customer_id__user_id=uid) & Q(status='pending'))
    resu=Customerdog.objects.filter(Q(customer_id__user_id=uid) & Q(status='requested'))

    return render(request,'customer/customerviewdog.html',{"res":res,"resu":resu})

def deletedogbycustomer(request):
    id=request.GET.get('id')
    Customerdog.objects.filter(id=id).delete()
    messages.info(request, "deleted successfully")

    return HttpResponseRedirect('/customerviewdog')
def updatedogbycustomer(request):
    id=request.GET.get('id')
    qy=Customerdog.objects.filter(id=id)
    if request.POST:
        name=request.POST['name']
        price=request.POST['price']
        description=request.POST['description']
        img=request.FILES['image']
        breed = request.POST.get('breed')
        medication = request.POST.get('medication')
        gender = request.POST.get('gender')
        age = request.POST['age']

        registerqry = Customerdog.objects.get(id=id)  
        registerqry.name = name
        registerqry.price = price
        registerqry.description = description
        registerqry.gender = gender
        registerqry.medication = medication
        registerqry.breed=breed
        registerqry.image = img
        registerqry.age = age

        registerqry.save()
        messages.info(request, "updated successfully")

        return redirect('/customerviewdog')
    return render(request,'customer/updatecustomerdog.html',{"qy":qy})

def viewmatch(request):
    uid=request.session['uid']
    did = request.GET.get('did')
    print(did)
    id = request.GET.get('did')
    cus = Customerdog.objects.get(id=id)
    cust=Customer.objects.get(user_id=uid)
    res = Breederdog.objects.filter(breed=cus.breed,  breeder_id__district=cust.district, breeder_id__place=cust.place,status='pending').exclude(gender=cus.gender)
    return render(request, 'customer/viewmatch.html', {'res': res,'did':did})

def requestforbreeding(request):
    did = request.GET.get('did')
    print(did)
    uid=request.session['uid']

    customer=Customer.objects.get(user_id=uid)
    id = request.GET.get('id')
    Customerdog.objects.filter(id=did).update(status='requested')
    Breederdog.objects.filter(id=id).update(status='requested')
    bry=Breeding.objects.create(breederdog_id=id,customerdog_id=did,status='requested',customer=customer)
    bry.save()
    messages.info(request, "requested successfully")

    return redirect('/customerviewstatus')

def breederviewrequest(request):
    uid=request.session['uid']
    res=Breeding.objects.filter(Q(breederdog_id__breeder_id__user_id=uid) & Q(status='requested'))
    print(res)
    resu=Breeding.objects.filter(Q(breederdog_id__breeder_id__user_id=uid,status='approved') & Q(paymentstatus='paid'))
    resul=Breeding.objects.filter(Q(breederdog_id__breeder_id__user_id=uid) & Q(status='customer confirmed') & Q(paymentstatus='paid'))

    return render(request, 'breeder/breederviewrequest.html', {'res': res,'resu': resu,'resul': resul})
def deleterequest(request):
    id=request.GET.get('id')
    breeding=Breeding.objects.get(id=id)
    Customerdog.objects.filter(id=breeding.customerdog_id).update(status='pending')
    Breederdog.objects.filter(id=breeding.breederdog_id).update(status='pending')
    Breeding.objects.filter(id=id).delete()
    messages.info(request, "deleted successfully")
    return HttpResponseRedirect('/breederviewrequest')
def acceptrequest(request):
    uid=request.session['uid']
    id=request.GET.get('id')
    breeder=Breeder.objects.get(user_id=uid)
    breeding=Breeding.objects.get(id=id)
    Customerdog.objects.filter(id=breeding.customerdog_id).update(status='approved')
    Breederdog.objects.filter(id=breeding.breederdog_id).update(status='approved')
    Breeding.objects.filter(id=id).update(status='approved',breeder=breeder)
    messages.info(request, "accepted successfully")
    return HttpResponseRedirect('/breederviewrequest')
def customerviewstatus(request):
    uid=request.session['uid']
    # br=Breeding.objects.(customerdog_id__customer_id__user_id=uid,status='approved')
    id=request.GET.get('id')
    print(id,"hgfhjgjhkhjkjhhhhhhhhhhhhhhhh")

    res=Breeding.objects.filter(Q(customerdog_id__customer_id__user_id=uid) & Q(status='approved') & Q(paymentstatus='pending'))
    resu=Breeding.objects.filter(Q(customerdog_id__customer_id__user_id=uid) & Q(status='approved') & Q(paymentstatus='paid'))
    resul=Breeding.objects.filter(Q(customerdog_id__customer_id__user_id=uid) & Q(status='breeding completed') & Q(paymentstatus='paid'))

    if  request.POST:
        return redirect('/payment')

    return render(request, 'customer/customerviewstatus.html', {'res': res,'resu': resu,'resul': resul,'id':id})


def payment(request):
    today=date.today()
    id=request.GET.get('id')
    print(id,"hgfhjgjhkhjkjhhhhhhhhhhhhhhhh")
    uid=request.session['uid']
    res=Breeding.objects.filter(customerdog_id__customer_id__user_id=uid,status='approved',paymentstatus='pending')
    br=Breeding.objects.filter(customerdog_id__customer_id__user_id=uid,status='approved',paymentstatus='paid')

    if  request.POST:
        # price=request.POST['price']        
        price=request.POST['price']
        print(price)
        admincommission=(int(price)*(30))/100
        breederpayment=int(price)-int(admincommission)
        # Breeding.objects.filter(customer_id__user_id=uid,id=id,status='approved',paymentstatus='pending').update(amount=price,admincommission=admincommission,breederpayment=breederpayment)

        Breeding.objects.filter(customer_id__user_id=uid,id=id,status='approved',paymentstatus='pending').update(paymentstatus='paid',startdate=today,amount=price,admincommission=admincommission,breederpayment=breederpayment)
        messages.info(request, "payment success")

        return redirect('/customerviewstatus')
    return render(request,'customer/payment.html', {'res': res,'br':br,'id':id})
def chat(request):
    id=request.GET.get('id')
    print(id)
    uid = request.session['uid']
    bb = Breeding.objects.get(customer_id__user_id=uid,id=id, status='approved', paymentstatus='paid')

    br = Breeding.objects.filter(customer_id__user_id=uid,id=id, status='approved', paymentstatus='paid')
    res=Chat.objects.filter(breeding=id)

    if request.method == 'POST':
        bid = request.POST['id']
        msg = request.POST['msg']
        expert = Customer.objects.get(user_id=uid)
        resu = Chat.objects.create(breeding_id=bid,breeder_id=bb.breederdog.breeder_id, message=msg, customer=expert)
        resu.save()
        res=Chat.objects.filter(breeding=id)
    return render(request, 'customer/chat.html', {'br': br, 'res': res,'bb':bb,'id':id})


def viewchat(request):
    uid = request.session['uid']
    id=request.GET.get('id')
    print(id)
    res=Chat.objects.filter(breeder_id__user_id=uid,reply=None)
    if request.POST:
        reply=request.POST['reply']
        id=request.POST['did']
        print(reply,"riojegoijhohomhhkgnhnrohrotjhrihhjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjt")
        Chat.objects.filter(breeder_id__user_id=uid,reply=None,id=id).update(reply=reply)
    return render(request, 'breeder/viewchat.html', { 'res': res})


def customerend(request):
    id=request.GET.get('id')
    print(id)
    Breeding.objects.filter(id=id).update(status='customer confirmed')
    messages.info(request, "customer confirmed")

    return HttpResponseRedirect('/customerviewstatus')
def breederend(request):
    today=date.today()

    id=request.GET.get('id')
    print(id)
    Breeding.objects.filter(id=id).update(status='breeding completed',enddate=today)
    messages.info(request, "breeder confirmed")

    return HttpResponseRedirect('/breederviewrequest')
def breederrestart(request):
    today=date.today()

    id=request.GET.get('id')
    print(id)
    Breeding.objects.filter(id=id).update(status='approved')
    messages.info(request, "restarting breeding process")
    return HttpResponseRedirect('/breederviewrequest')
def feedback(request):
    uid = request.session['uid']
    uuid=Customer.objects.get(user_id=uid)
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        user = Feedback(
            feedback=feedback,
            customer=uuid
        )
        user.save()
        messages.info(request, "feedback added")    

    return render(request, 'customer/feedback.html')
def viewfeedback(request):
    res=Feedback.objects.all()
    return render(request, 'admin/viewfeedback.html',{'res':res})
def paymentdetails(request):
    res=Breeding.objects.filter(status='breeding completed')
    return render(request, 'admin/paymentdetails.html',{'res':res})
def offspring(request):
    id=request.GET.get('id')
    uid = request.session['uid']
    customer=Customer.objects.get(user_id=uid)
    
    if request.POST:
        name=request.POST['name']
        description=request.POST['description']
        img=request.FILES['image']
        breed = request.POST.get('breed')
        medication = request.POST.get('medication')
        gender = request.POST.get('gender')
        expert=Breeding.objects.get(id=id)
        if Offspring.objects.filter(name=name,id=id).exists():
            print("User already exists")
            messages.info(request, "offspring already exists")
        else:
            registerqry=Offspring.objects.create(name=name,gender=gender,breed=breed,description=description,image=img,breeding=expert,breeder=expert.breeder,customer=customer,medication=medication)
            registerqry.save()
            messages.info(request, "offspring added")

            return redirect('/viewoffspring')
        
    return render(request,'customer/offspring.html',{'id':id})
def viewoffspring(request):
    uid = request.session['uid']

    res=Offspring.objects.filter(customer_id__user_id=uid)
    return render(request, 'customer/viewoffspring.html',{'res':res})
def viewoffspringadmin(request):

    res=Offspring.objects.all()
    return render(request, 'admin/viewoffspringadmin.html',{'res':res})
def viewoffspringbreeder(request):
    uid = request.session['uid']

    res=Offspring.objects.filter(breeder_id__user_id=uid)
    return render(request, 'breeder/viewoffspring.html',{'res':res})

def endprocess(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        
        breeding = Breeding.objects.get(id=id)
        bdid = breeding.breederdog.id
        crid = breeding.customerdog.id
        brdog = Breederdog.objects.get(id=bdid)
        crdog = Customerdog.objects.get(id=crid)
        brdog.status = "pending"
        brdog.save()
        crdog.status = "pending"
        crdog.save()
        breeding.customerdog.status = 'pending'
        breeding.save()   

        breeding.breederdog.status = 'pending'
        breeding.save()   
 
  
        # Breeding.objects.filter(id=id).update(customerdog__status ='pending',breederdog__status='pending',status='end')
        return HttpResponseRedirect(f'/breedingend?id={id}')
def  breedingend(request):
        id = request.GET.get('id')
        
        Breeding.objects.filter(id=id).update(status = 'end')
        messages.info(request, "Process end")

        return HttpResponseRedirect('/customerviewstatus')



def viewpayment(request):
    uid = request.session['uid']

    res=Breeding.objects.filter(status='end',breeder_id__user_id=uid)
    return render(request, 'breeder/viewpayment.html',{'res':res})

def logout(request):
    auth_logout(request)   # clears request.session entirely
    return redirect('/index')




# def phyHome(request):
#     return render(request,"phyHome.html")

# def phyVDogs(request):
#     return render(request,"phyVDogs.html")

# def phyAddp(request):
#     if request.POST:
#         name = request.POST["name"]
#         price = request.POST["price"]
#         desc = request.POST["desc"]
#         img = request.FILES["img"]
#         p = Products.objects.create(name = name, price = price, desc = desc,img = img)
#         p.save()
#         messages.info(request,"Added successfully")
#     return render(request,"phyAddp.html")

# def phyVp(request):
#     data = Products.objects.all()
#     return render(request,"phyVp.html",{"data":data})


# def pRem(request):
#     id = request.GET.get('id')
#     p = Products.objects.get(id=id).delete()
#     return redirect("/phyVp")

# def phyVOrders(request):
#     data = Cart.objects.all()
#     return render(request,"phyVOrders.html",{"data":data})

# def phyPayments(request):
#     data=Payment.objects.all()
#     return render(request,"phyVPayments.html",{"data":data})


# def cusCart(request):
#     uid = request.session["uid"]
#     data = Cart.objects.filter(Q(uid__user__id = uid) & Q(status = "inCart")).order_by("-id")
#     amt = 0
#     for d in data:
#         at = int(d.amt)

#         print(at)
#         amt = int(amt) + int(at)
#     print(amt)

#     return render(request,"cusCart.html",{"data":data,"amt":amt})

# def cusOrder(request):
#     id = request.session["uid"]
#     data = Cart.objects.filter(uid__user__id=id).order_by("-id")
#     return render(request,"cusOrder.html",{"data":data})

# def cusStore(request):
#     data =Products.objects.all()
#     uid = request.session["uid"]
#     u = Customer.objects.get(user__id=uid)
#     if request.POST:
#         qty = request.POST["qty"]
#         pid = request.POST["pid"]
#         p = Products.objects.get(id=pid)
#         qty = int(qty)
#         pr = int(p.price)
#         amt = pr * qty
#         c = Cart.objects.create(pid = p,uid = u,qty = qty,amt = amt,status = "inCart")
#         c.save()
#         messages.info(request,"Added to Cart")
        
#     return render(request,"cusStore.html",{"data":data})


# def cartRem(request):
#     id = request.GET.get("id")
#     c = Cart.objects.get(id=id).delete()
#     return redirect("/cusCart")

# def userpay(request):

#     amt = request.GET.get("amt")
#     if amt == 0:
#         messages.info(request, "Add items in the cart")
#         return redirect("/cusStore")
#     uid = request.session["uid"]
#     u = Customer.objects.get(user__id=uid)
#     if request.POST:
#         p = Payment.objects.create(uid = u,amt = amt)
#         p.save()
#         c = Cart.objects.filter(Q(uid__user__id=uid) & Q(status="inCart"))
#         for ci in c:
#             ci.status = "Completed"
#             ci.save()
#         return redirect("/cusOrder")
#     return render(request,"userpay.html",{"amt":amt})

# def cusPayments(request):
#     id = request.session["uid"]
#     data = Payment.objects.filter(uid__user__id = id).order_by("-id")
#     return render(request,"cusPayments.html",{"data":data})
# def addvet(request):
#     if request.POST:
#             name = request.POST['name']
#             qualification= request.POST['degree']
#             clinic = request.POST['clinic']
#             contact = request.POST['phone']
#             exp = request.POST['experience']
#             vet=Veterinarian.objects.create(name=name,qualification=qualification,clinic=clinic,contact=contact,exp=exp)
#             vet.save()
            
#     return render(request,"admin/addvet.html")

# def vetlist(request):

#     v=Veterinarian.objects.all()

#     return render(request,"customer/vetlist.html",{'vet':v})