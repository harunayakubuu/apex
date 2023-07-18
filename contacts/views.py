from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .forms import ContactForm, EmergencyContactForm, ContactUpdateForm
from .models import BranchOffice, Contact, EmergencyContact
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import DeleteView


def contact_form(request):
    offices = BranchOffice.objects.order_by('state').filter(is_active=True)
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "We've received your message. We shall get back to you shortly.")
            
            # send_mail(
            #     subject = "Contact Form.",
            #     message = "We've received your message. We shall get back to you shortly.",
            #     from_email = settings.EMAIL_HOST_USER,
            #     recipient_list = [user.email,]
            # )

            return redirect('contacts:contact-form')
    context = {
        'form': form,
        'offices': offices
    }
    return render(request, 'contacts/contact-form.html', context)


@login_required
def contact_messages(request):
    contact_messages = Contact.objects.order_by('-created_at')
    context = {
        'contact_messages': contact_messages
    }
    return render(request, 'contacts/contact-messages.html', context)


@login_required
def contact_message_detail(request, id):
    message = get_object_or_404(Contact, id=id)
    context = {
        'message': message
    }
    return render(request, 'contacts/contact-message-details.html', context)


@login_required
def contact_message_update(request, id):
    message = get_object_or_404(Contact, id = id)
    form = ContactUpdateForm(instance = message)
    if request.method == 'POST':
        form = ContactUpdateForm(request.POST, instance = message)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes saved.")
            return redirect('contacts:contact-messages')
    context = {
        'form': form,
        'message': message
    }
    return render(request, 'contacts/contact-message-update.html', context)


class ContactMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'contacts/contact-message-delete.html'
    success_url = reverse_lazy('contacts:contact-messages')


@login_required
def emergency_contact_create(request):
    form = EmergencyContactForm()
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form_data = form.save(commit = False)
            form_data.user = request.user
            form_data.save()
            messages.success(request, "Contact was saved.")
            
            message = """
            You have been added to serve as a contact person by {request.user.get_full_name} on Apex Estate Managers and Properties LTD. 
            <p>
                Kindly be informed that you will be contacted by our staff for details.
            </p>
            <p>
                Management,<br>
                Apex Estate Managers and Properties LTD
            </p>
            """
            send_mail(
                subject = "Contact Person Notification",
                message = message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [form_data.email,]
            )

            return redirect("contacts:emergency-contacts")
        else:
            messages.error(request, 'Check and correct the error below.')
    
    context = {
        'form': form
    }
    return render(request, 'contacts/emergency-contact-create.html', context)


@login_required
def emergency_contact_edit(request, id):
    instance = EmergencyContact.objects.get(id = id)
    form = EmergencyContactForm(instance = instance)
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST or None, request.FILES or None, instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Update saved.")
            return redirect("contacts:emergency-contacts")
        else:
            messages.error(request, 'Error. Check and correct the error below.')
    
    context = {
        'instance': instance,
        'form': form
    }
    return render(request, 'contacts/emergency-contact-edit.html', context)


@login_required
def emergency_contacts(request):
    emergency_contacts = EmergencyContact.objects.filter(user = request.user)
    context = {
        'emergency_contacts': emergency_contacts
    }
    return render(request, 'contacts/emergency-contacts.html', context)


@login_required
def emergency_contact_delete(request, id):
    emergency_contact = EmergencyContact.objects.get(id=id, user = request.user)
    emergency_contact.delete()
    messages.success(request, "Contact deleted.")
    return redirect('contacts:emergency-contacts')


def offices(request):
    offices = BranchOffice.objects.filter(is_active=True)
    context = {
        'offices': offices
    }
    return render(request, 'contacts/offices.html', context)