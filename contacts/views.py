from django.core.mail import send_mail
from django.shortcuts import render, redirect

from contacts.models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check if user have made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                message.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listing/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email,
                          phone=phone, message=message, user_id=user_id)

        contact.save()

        # send mail
        send_mail(
            'Property Listing Inquiry',
            'There has been an inquiry for' + listing + '. sign into the admin panel for more info',
            'mirabohuche@gmail.com',
            [realtor_email, 'myrabohuche@gmail.com'],
            fail_silently=False
        )

        message.success(request, 'Your request has been submitted, a realtor will get back to you very soon')
        return redirect('/listings/' + listing_id)
