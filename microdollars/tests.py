from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from .models import OrganizationModel, Donation, Search
from .forms import DonationForm, SearchForm, ProfileForm
from http import HTTPStatus
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime
from django.test import Client

class OrganizationTest(TestCase):
    # Donation.objects.create()
    # assertEquals("RequiredOutput", This DonationModel.str())
    def create_org(self):
        return OrganizationModel.objects.create()

    def test_about_me(self):
        item = self.create_org()
        self.assertEquals("INFO ON THIS ORGANIZATION", item.about_me)

    def test_organization_name(self):
        item = self.create_org()
        self.assertEquals(item.organization_name, "")

    def test_false_name(self):
        item = self.create_org()
        self.assertNotEqual(item.organization_name, "Anything")

    def test_false_about_me(self):
        item = self.create_org()
        self.assertNotEqual(item.about_me, "INFO ON THIS ORGANIZATIO")


class DonationFormTests(TestCase):
    # check whether form properly pulls orgs from the DB and displays in the form
    def test_donateto_field_contains_all_orgnizations(self):
        OrganizationModel.objects.create(
            organization_name="Org 1", about_me="I'm Org 1!")
        form = DonationForm()
        OrganizationModel.objects.create(
            organization_name="Org 2", about_me="I'm Org 2!")
        self.assertQuerysetEqual(
            form.fields['donateto'].queryset, OrganizationModel.objects.all(), transform=lambda x: x, ordered=False)

    def test_success_donation_form(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        formData = {
            'donateto': org,
            'amount': 55,
            'comment': "55 bucks for Org 1, enjoy",
        }
        form = DonationForm(data=formData)
        self.assertTrue(form.is_valid())

    def test_improperOrg_donation_from(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        uncontainedOrg = OrganizationModel(
            organization_name="Org 2", about_me="I'm Org 2!")

        formData = {
            'donateto': uncontainedOrg,
            'amount': 55,
            'comment': "55 bucks for Org 1, enjoy",
        }
        form = DonationForm(data=formData)
        self.assertFalse(form.is_valid())

    def test_improperAmountString_donation_from(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        formData = {
            'donateto': org,
            'amount': "not a number",
            'comment': "55 bucks for Org 1, enjoy",
        }
        form = DonationForm(data=formData)
        self.assertFalse(form.is_valid())

    def test_improperAmountNegative_donation_from(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        formData = {
            'donateto': org,
            'amount': -1,
            'comment': "-1 bucks for Org 1, enjoy",
        }
        form = DonationForm(data=formData)
        self.assertFalse(form.is_valid())

    def test_improperAmountZero_donation_from(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        formData = {
            'donateto': org,
            'amount': 0,
            'comment': "-1 bucks for Org 1, enjoy",
        }
        form = DonationForm(data=formData)
        self.assertFalse(form.is_valid())

# Integration test: submit with the form & view

class DonationFormAndViewTest(TestCase):
    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, '<label for="id_donateto">Donate to:</label>', html=True)

    def test_submitForm(self):
        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        user.save()

        self.assertEqual(Donation.objects.count(), 0)
        response = self.client.post(
            "/", data={"user": user.id, "donateto": org.id, "amount": 50, "comment": "Here's 50 dollars"}
        )
        self.assertEqual(Donation.objects.count(), 1)

class UserLookupTest(TestCase):
    def test_get(self):
        response = self.client.get("/lookup")
        self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_InputDoesNotExist(self):

        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        user.save()

        formData = {
            'donateto': org,
            'amount': 55,
            'comment': "55 bucks for Org 1, enjoy",
        }
        form = DonationForm(data=formData)
        form.user = user
        form.save()

        
        #search_look = Search("jacob")
        #search_look = Search(user_search= "jacob")
        formData = {
            'user_search': "jacob",
        }
        
        self.assertTrue(SearchForm(data=formData).is_valid())
    def test_InputDoesNotExist(self):

        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        user.save()

        formData = {
            'donateto': org,
            'amount': 55,
            'comment': "55 bucks for Org 1, enjoy",
        }
        form_donation = DonationForm(data=formData)
        form_donation.user = user
        form_donation.save()
       
        formData = {
            'user_search': "notjacob",
        }
        form_search = SearchForm(data=formData)
        
       
        self.assertEquals(
            form_search.errors["user_search"], ['Username ' + formData['user_search'] + ' does not exist'])
     
    def test_forCapital(self):

        org = OrganizationModel(
            organization_name="Org 1", about_me="I'm Org 1!")
        org.save()

        user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        user.save()

        formData = {
            'donateto': org,
            'amount': 55,
            'comment': "55 bucks for Org 1, enjoy",
        }
        form_donation = DonationForm(data=formData)
        form_donation.user = user
        form_donation.save()

        formData = {
            'user_search': "Jacob",
        }
        form_search = SearchForm(data=formData)
        
        self.assertEquals(
            form_search.errors["user_search"], ['Username ' + formData['user_search'] + ' does not exist'])

        


class LeaderboardTest(TestCase):
    def create_org(self):
        return OrganizationModel.objects.create()
    def create_donation(self):
        return Donation.objects.create()
    def exponential(self, user, donation):
        if(donation == 0):
            return (user, donation, 128578)
        elif(donation < 10):
            return (user, donation, 128513)
        elif(donation < 100):
            return (user, donation, 129297)
        elif(donation < 1000):
            return (user, donation, 129321)
        else:
            return (user, donation, 129332)

    def getAllDonations(self):
        userList = User.objects.all()
        sum = 0
        leaderboard = []
        for user in userList:
            getUserDonations = self.usernameToUserDonations(user.username)
            for donation in getUserDonations:
                sum += donation.amount
            leaderboard.append(self.exponential(user.username.capitalize(), sum))
            sum = 0
        return leaderboard

    def sortThis(self):
        return sorted(self.getAllDonations(), key=lambda x: x[1], reverse=True)

    def numberList(self, rankingslist):
        finallist = []
        i = 1
        for rankings in rankingslist:
            finallist.append((i, rankings[0], float(rankings[1]), rankings[2]))
            i+=1
        return finallist
    def usernameToUserDonations(self, username):
        try:
            uid = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        return Donation.objects.filter(user=uid)


    def test_empty(self):
        user = User.objects.create_user(
            username='FirstUser', email='jacob@…', password='top_secret')
        user2 = User.objects.create_user(
            username='SecondUser', email='jacob@…', password='top_secret')
        user3 = User.objects.create_user(
            username='ThirdUser', email='jacob@…', password='top_secret')
        user.save()
        user2.save()
        user3.save()

        org = OrganizationModel(organization_name="One", about_me="This is the first organization")
        org2 = OrganizationModel(organization_name="Two", about_me="This is the second organization")
        org.save()
        org2.save()

        emptyList = self.numberList(self.sortThis())
        empty = [(1, 'Firstuser', 0.0, 128578),
                (2, 'Seconduser', 0.0, 128578),
                (3, 'Thirduser', 0.0, 128578)]
        self.assertEquals(emptyList, empty)
    def test_createLeaderboardBeforeChange(self):
        user = User.objects.create_user(
            username='FirstUser', email='jacob@…', password='top_secret')
        user2 = User.objects.create_user(
            username='SecondUser', email='jacob@…', password='top_secret')
        user3 = User.objects.create_user(
            username='ThirdUser', email='jacob@…', password='top_secret')
        user.save()
        user2.save()
        user3.save()

        org = OrganizationModel(organization_name="One", about_me="This is the first organization")
        org2 = OrganizationModel(organization_name="Two", about_me="This is the second organization")
        org.save()
        org2.save()


        donationFromFirstUser1 = Donation(user=user, donateto=org, amount=2, comment="")
        donationFromSecondUser1 = Donation(user=user2, donateto=org2, amount=30, comment="")
        donationFromThirdUser1 = Donation(user=user3, donateto=org, amount=3000, comment="")

        donationFromFirstUser1.save()
        donationFromSecondUser1.save()
        donationFromThirdUser1.save()

        listOfDonations = self.numberList(self.sortThis())
        listOfTestDonations = []
        listOfTestDonations.append((1, user3.username.capitalize(), float(3000), 129332))
        listOfTestDonations.append((2, user2.username.capitalize(), float(30), 129297))
        listOfTestDonations.append((3, user.username.capitalize(), float(2), 128513))

        self.assertEquals(listOfDonations, listOfTestDonations)
        
    def test_createLeaderboard(self):
        user = User.objects.create_user(
            username='FirstUser', email='jacob@…', password='top_secret')
        user2 = User.objects.create_user(
            username='SecondUser', email='jacob@…', password='top_secret')
        user3 = User.objects.create_user(
            username='ThirdUser', email='jacob@…', password='top_secret')
        user.save()
        user2.save()
        user3.save()

        org = OrganizationModel(organization_name="One", about_me="This is the first organization")
        org2 = OrganizationModel(organization_name="Two", about_me="This is the second organization")
        org.save()
        org2.save()


        donationFromFirstUser1 = Donation(user=user, donateto=org, amount=2, comment="")
        donationFromSecondUser1 = Donation(user=user2, donateto=org2, amount=30, comment="")
        donationFromThirdUser1 = Donation(user=user3, donateto=org, amount=3000, comment="")

        donationFromFirstUser1.save()
        donationFromSecondUser1.save()
        donationFromThirdUser1.save()

        listOfDonations = self.numberList(self.sortThis())
        listOfTestDonations = []
        listOfTestDonations.append((1, user3.username.capitalize(), float(3000), 129332))
        listOfTestDonations.append((2, user2.username.capitalize(), float(30), 129297))
        listOfTestDonations.append((3, user.username.capitalize(), float(2), 128513))

        self.assertEquals(listOfDonations, listOfTestDonations)
        donationFromSecondUser2 = Donation(user=user2, donateto=org, amount=2971, comment="")
        donationFromSecondUser2.save()

        listOfDonations = self.numberList(self.sortThis())
        listOfTestDonations2 = []
        listOfTestDonations2.append((1, user2.username.capitalize(), float(3001), 129332))
        listOfTestDonations2.append((2, user3.username.capitalize(), float(3000), 129332))
        listOfTestDonations2.append((3, user.username.capitalize(),  float(2),    128513))
        self.assertEquals(listOfDonations, listOfTestDonations2)


class ProfileUpdateTest(TestCase):
    def test_invalidUsernameSpace(self):
        user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        user.save()

        formData = {
            'username': 'A Space',
            'first_name': 'Jacob',
            'last_name': 'ALastName',
        }
        form = ProfileForm(data=formData)
        
        self.assertFalse(form.is_valid())
        self.assertEquals(
            form.errors["username"], ['Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'])
    
    def test_invalidUsernameChar(self):
        user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        user.save()

        formData = {
            'username': 'Jacob!!!',
            'first_name': 'Jacob',
            'last_name': 'ALastName',
        }
        form = ProfileForm(data=formData)
        
        self.assertFalse(form.is_valid())
        self.assertEquals(
            form.errors["username"], ['Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'])

    def test_validProfileUpdate(self):
        user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        user.save()

        formData = {
            'username': 'Jacob',
            'first_name': 'Jacob',
            'last_name': 'ALastName',
            'date_joined': timezone.now(),
        }

        form = ProfileForm(data=formData)
        self.assertTrue(form.is_valid())

    def test_submitForm(self):
        user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        user.set_password('top_secret')
        user.save()

        formData = {
            'username': 'Jacob',
            'first_name': 'Jacob',
            'last_name': 'ALastName',
            'date_joined': timezone.now(),
        }

        client = Client() 
        client.login(username=user.username, password='top_secret')
        response = client.post("/profile", data=formData)
        
        self.assertEquals(User.objects.get(username='Jacob').username, 'Jacob')