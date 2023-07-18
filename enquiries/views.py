from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Enquiry
from django.conf import settings

from .forms import EnquiryStatusUpdateForm


@login_required
def all_enquiries(request):
    enquiries = Enquiry.objects.all()    
    context = {
        'enquiries': enquiries,
    }
    return render(request, 'enquiries/all-enquiries.html', context)


def enquiry_form(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing_slug = request.POST['listing_slug']
        listing = request.POST['listing']
        listing_address = request.POST['listing_address']
        listing_location = request.POST['listing_location']
        user_id = request.POST['user_id']
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        user_phone = request.POST['user_phone']
        message = request.POST['message']
        agent_email = request.POST['agent_email']

        listing_owner = request.POST['listing_owner']

        # print(agent_email)
        
        
        if not user_phone:
            messages.error(request, 'Phone number is required.')
            return redirect("/properties/"+listing_slug+"/"+listing_id)

        # if len(user_phone) != 11 or len(user_phone) != 15:
        #         messages.error(request, 'Invalid phone number, correct it and try again.')
        #         return redirect("/properties/"+listing_slug+"/"+listing_id)

        # if not user_phone.isdigit():
        #         messages.error(request, 'Invalid phone number, correct it and try again.')
        #         return redirect("/properties/"+listing_slug+"/"+listing_id)

        if request.user.is_authenticated:
            if user_id == listing_owner:
                messages.error(request, 'You can not make enquiries on your OWN properties')
                return redirect("/properties/"+listing_slug+"/"+listing_id)


        if request.user.is_authenticated:
            user_id = request.user.id
            if not user_phone:
                messages.error(request, 'Phone number is required.')
                return redirect("/properties/"+listing_slug+"/"+listing_id)

            has_contacted = Enquiry.objects.all().filter(listing_id = listing_id, user_id = user_id)
            if has_contacted:
                messages.error(request, 'You have already sent enquiry for this property.')
                return redirect("/properties/"+listing_slug+"/"+listing_id)

        enquiry = Enquiry(
            listing_id = listing_id,
            listing = listing,
            user_id = user_id,
            user_name = user_name,
            user_email = user_email,
            user_phone = user_phone,
            message = message
        )
        # print(agent_email)

        enquiry.save()
        
        send_mail(
            subject = f'Enquiry in Respect of { listing }',
            message = f'There has been an enquiry in respect of { listing }. Sign into the admin panel for more information.',
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [agent_email,],
            fail_silently = False
        )
        messages.success(request, 'We have recieved your message, our agent shall get back to you soon.')
        return redirect("/properties/"+listing_slug+"/"+listing_id)

    context = {
        
    }
    return render(request, 'enquiries/enquiries.html', context)


@login_required
def my_enquiries(request):
    my_enquiries = Enquiry.objects.order_by('-created_at').filter(user_id=request.user.id)
    context = {
        'my_enquiries':my_enquiries
    }
    return render(request, 'enquiries/my-enquiries.html', context)


@login_required
def enquiry_status_update(request, id):
    enquiry = get_object_or_404(Enquiry, id=id)
    form = EnquiryStatusUpdateForm(instance=enquiry)
    if request.method=="POST":
        form = EnquiryStatusUpdateForm(request.POST, instance = enquiry)
        if form.is_valid():
            form.save()
            messages.success(request, "Status updated.")
            # return redirect("enquiries:")

    context = {
        'form':form
    }
    return render(request, 'enquiries/enquiry-status-update.html', context)