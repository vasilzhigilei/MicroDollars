from django.shortcuts import render
from django.views.generic import CreateView
from .models import Donation, OrganizationModel, Search
from .tables import DonationTable
from django.contrib.auth.models import User
from microdollars.forms import ProfileForm, DonationForm, SearchForm, Search
from django.core.exceptions import ObjectDoesNotExist
from django_tables2.config import RequestConfig
from collections import Counter
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from collections import Counter
import statistics
# Create your views here.


def index(request):
    form = DonationForm(request.POST or None)
    if form.is_valid():
        tempForm = form.save(commit=False)
        if request.user and not request.user.is_anonymous:
            tempForm.user = request.user
        else:
            tempForm.user = None
        tempForm.save()
        messages.success(
            request, "Successfully completed transaction!")
        return redirect(reverse('index'))

    if request.user.is_anonymous:
        messages.warning(
            request, "You're not logged in, so your donation will be anonymous. It won't show up on leaderboards, or on any profile!")

    # generate string for top banner display
    banner = {'text': ""}
    if request.user.is_authenticated:
        # get total donation amount
        sum = 0
        try:
            for donation in Donation.objects.filter(user=request.user.id):
                sum += donation.amount
        except:
            pass
        text = ""
        if sum == 0:
            emoji = 128578
            tolevelup = 10
            text = "Your level is &#" + \
                str(emoji) + ", donate $" + \
                str(tolevelup) + " more to level up!"
        elif sum < 10:
            emoji = 128513
            tolevelup = 10 - sum
            text = "Your level is &#" + \
                str(emoji) + ", donate $" + \
                str(tolevelup) + " more to level up!"
        elif sum < 100:
            emoji = 129297
            tolevelup = 100 - sum
            text = "Your level is &#" + \
                str(emoji) + ", donate $" + \
                str(tolevelup) + " more to level up!"
        elif sum < 1000:
            emoji = 129321
            tolevelup = 1000 - sum
            text = "Your level is &#" + \
                str(emoji) + ", donate $" + \
                str(tolevelup) + " more to level up!"
        else:
            emoji = 128081
            text = "Your level is &#" + \
                str(emoji) + ", you are at the max level!"
        banner['text'] = text
    context = {
        'form': form,
        'donation_list': Donation.objects,
        'organizations': OrganizationModel.objects.all(),
        'banner': banner,
    }
    return render(request, "microdollars/index.html", context)


def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    message = ""
    if form.is_valid():
        form.save()
        message = '<div class="alert alert-success" role="alert">Successfully updated profile!</div>'
    context = {
        'form': form,
        'message': message,
    }
    return render(request, "microdollars/profile.html", context)


def usernameToUserDonations(username):
    try:
        uid = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return None
    print("test")
    return Donation.objects.filter(user=uid)


def lookup(request):
    print("form")
    form = SearchForm(request.GET or None)
    donationTable = None
    data = None
    labels = None
    donationsEmpty = False
    average = None
    mode = None
    median = None
    username = None

    def calcDonationsPerOrg(username):
        userDonations = usernameToUserDonations(username)
        orgToTotalDonations = dict()
        for donation in userDonations:
            orgName = donation.donateto.organization_name
            orgToTotalDonations[orgName] = orgToTotalDonations.get(
                orgName, 0) + donation.amount
        return orgToTotalDonations

    def calcAvgDonationAmount(userDonations):
        print(userDonations)
        return round(statistics.mean(userDonations), 2)

    def calcModeAmount(userDonations):
        return max(userDonations, key=userDonations.count)

    def calcMedianAmount(userDonations):
        return statistics.median(userDonations)

    if form.is_valid():
        username = form.cleaned_data['user_search']
        donations = usernameToUserDonations(username)
        donationTable = DonationTable(donations)
        donationsEmpty = (donations.count() == 0)
        RequestConfig(request).configure(donationTable)

        if not donationsEmpty:
            # calc total donations
            orgToTotalDonations = calcDonationsPerOrg(username)
            data = [float(val)
                    for val in list(orgToTotalDonations.values())]
            labels = list(orgToTotalDonations.keys())
            donationsList = [d['amount'] for d in donations.values()]
            average = calcAvgDonationAmount(donationsList)
            mode = calcModeAmount(donationsList)
            median = calcMedianAmount(donationsList)
    context = {
        'form': form,
        'donationsEmpty':  donationsEmpty,
        'donationTable': donationTable,
        'data': data,
        'labels': labels,
        'average': average,
        'mode': mode,
        'median': median,
        'username': username,
    }
    return render(request, "microdollars/lookup.html", context)


def gamify(request):
    donations = None

    def usernameToUserDonations(username):
        try:
            uid = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        return Donation.objects.filter(user=uid)

    def exponential(user, donation):
        if(donation == 0):
            return (user, donation, 128578)
        elif(donation < 10):
            return (user, donation, 128513)
        elif(donation < 100):
            return (user, donation, 129297)
        elif(donation < 1000):
            return (user, donation, 129321)
        else:
            return (user, donation, 128081)

    def getAllDonations():
        userList = User.objects.all()
        sum = 0
        leaderboard = []
        for user in userList:
            getUserDonations = usernameToUserDonations(user.username)
            for donation in getUserDonations:
                sum += donation.amount
            leaderboard.append(exponential(user.username, sum))
            sum = 0
        return leaderboard

    def sortThis():
        return sorted(getAllDonations(), key=lambda x: x[1], reverse=True)

    def numberList(rankingslist):
        finallist = []
        i = 1
        for rankings in rankingslist:
            finallist.append((i, rankings[0], rankings[1], rankings[2]))
            i += 1
        return finallist

    context = {
        'leaderboard': numberList(sortThis()),
    }

    return render(request, "microdollars/leaderboard.html", context)


def about(request):
    return render(request, "microdollars/about.html")
