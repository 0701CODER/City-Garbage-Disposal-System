from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'index.html')
    # return render(request,'index.html')

#for showing signup/login button for NGO
def ngoclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'ngoclick.html')

#for showing signup/login button for Disposal
def disposalclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'disposalclick.html')

def ngo_signup_view(request):
    form1=forms.NGOUserForm()
    form2=forms.NGOExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.NGOUserForm(request.POST)
        form2=forms.NGOExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_ngo_group = Group.objects.get_or_create(name='NGO')
            my_ngo_group[0].user_set.add(user)

        return HttpResponseRedirect('ngologin')
    return render(request,'ngosignup.html',context=mydict)

def disposal_signup_view(request):
    form1=forms.DisposalUserForm()
    form2=forms.DisposalExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.DisposalUserForm(request.POST)
        form2=forms.DisposalExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_disposal_group = Group.objects.get_or_create(name='Disposal')
            my_disposal_group[0].user_set.add(user)

        return HttpResponseRedirect('disposallogin')
    return render(request,'disposalsignup.html',context=mydict)

#for checking user is NGO or Disposal
def is_ngo(user):
    return user.groups.filter(name='NGO').exists()
def is_disposal(user):
    return user.groups.filter(name='Disposal').exists()

def afterlogin_view(request):
    if is_ngo(request.user):
        return redirect('ngo-dashboard')
    elif is_disposal(request.user):
        return redirect('disposal-dashboard')

#for NGO LOGIN SECTION
@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def ngo_dashboard_view(request):
    ngodata=models.NGOExtra.objects.all().filter(user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'address':ngodata[0].address,
        'mobile':ngodata[0].mobile,
        'date':ngodata[0].joindate,
        'notice':notice
    }
    return render(request,'ngo_dashboard.html',context=mydict)

@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def ngo_collection_view(request):
    collections = models.Collection.objects.all()
    claimed=models.NGOExtra.objects.all().filter(user_id=request.user.id)

    context = {'collections':collections, 'id':claimed[0].id}
    return render(request,'ngo_collection.html', context)

@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def claim_collection_view(request, pk1, pk2, pk3):
    # print(don.status)
    don = models.Collection.objects.get(id=pk1)
    ngo = models.NGOExtra.objects.get(id=pk2)
    cla = models.Claim()
    # print(don.status)
    # if request.method == "POST":
    cla.ngoname=request.user.first_name
    cla.garbageName=pk3
    cla.mobile=ngo.mobile
    cla.address=ngo.address    

    don.status=True
    # ngo.claimed=True

    don.save()
    ngo.save()
    cla.save()
    messages.success(request, "Claimed Successfully!!")
    # return render(request,'student-attendance')
    return redirect(reverse('ngo-collection'))

@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def ngo_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('ngo-dashboard')
        else:
            print('form invalid')
    return render(request,'ngo_notice.html',{'form':form})

#for Disposal LOGIN SECTION
@login_required(login_url='disposallogin')
@user_passes_test(is_disposal)
def disposal_dashboard_view(request):
    disposaldata=models.DisposalExtra.objects.all().filter(user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'address':disposaldata[0].address,
        'mobile':disposaldata[0].mobile,
        'company_name':disposaldata[0].company_name,
        'notice':notice
    }
    return render(request,'disposal_dashboard.html',context=mydict)

@login_required(login_url='disposallogin')
@user_passes_test(is_disposal)
def disposal_collection_view(request):
    if request.method == "POST":
        don = models.Collection()
        don.username = request.POST.get('username')
        don.companyName = request.POST.get('companyName')
        don.number = request.POST.get('number')
        don.address = request.POST.get('address')
        don.garbageName = request.POST.get('garbageName')
        don.inputState = request.POST.get('inputState')
        don.quantity = request.POST.get('quantity')
        don.hours = request.POST.get('hours')
        don.description = request.POST.get('description')

        if len(request.FILES) != 0:
            don.garbageImage = request.FILES['garbageImage']

        don.save()
        messages.success(request, "Collection Listed Successfully!!")
    return render(request,'disposal_collection.html')

@login_required(login_url='disposallogin')
@user_passes_test(is_disposal)
def claimed_collection_view(request):
    # claims=models.NGOExtra.objects.all().filter(claimed=True)
    claims=models.Claim.objects.all()
    return render(request,'claimed_collection.html',{'claims':claims})

@login_required(login_url='disposallogin')
@user_passes_test(is_disposal)
def disposal_collection_history_view(request):
    collections = models.Collection.objects.all()

    context = {'collections':collections}
    return render(request,'disposal_collection_history.html', context)

# @login_required(login_url='disposallogin')
# @user_passes_test(is_ngo)
# def disposal_notice_view(request):
#     return render(request,'ngo_notice.html')

#for about us and contact us
def aboutus_view(request):
    return render(request,'aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'contactussuccess.html')
    return render(request, 'contactus.html', {'form':sub})
