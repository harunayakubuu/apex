from django.shortcuts import redirect, render, get_object_or_404
from .models import Client
from .forms import AdminClientUserUpdateForm, ClientCreateForm, ClientUpdateForm
from accounts.forms import UserUpdateForm
from django.contrib import messages

from django.urls import reverse, reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import DeleteView

from django.contrib.auth import get_user_model
User  = get_user_model()


@login_required
def client_list(request):
    clients = User.objects.order_by('date_joined').filter(is_client=True)
    context = {
        'clients': clients
    }
    return render(request, 'clients/clients-list.html', context)


@login_required
def client_create(request):
    user_obj = request.user

    user_form = UserUpdateForm(instance=request.user)
    client_form = ClientCreateForm()

    if request.method == 'POST':

        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        client_form = ClientCreateForm(request.POST, request.FILES)

        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_obj = client_form.save(commit = False)
            client_obj.user = user_obj
            client_obj.save()
            messages.success(request, 'Profile Updated.')

            # message = """
            # You have been added as an agent to join the {request.user.profile.agency.name}. 
            # Please go to the log in page, click the forget password link to reset your password to enable you log in to start working.
            # """
            # send_mail(
            #     subject = "Invitation as Agent.",
            #     message = message,
            #     from_email = settings.EMAIL_HOST_USER,
            #     recipient_list = [user.email,]
            # )
            return redirect('accounts:profile')
        else:
           messages.error(request, 'Check the form and try again.') 
    context = {
        'user_form': user_form,
        'client_form': client_form
    }
    return render(request, 'clients/client-create-form.html', context)


@login_required
def client_update(request):
    client_obj  = request.user.client

    user_form = UserUpdateForm(instance=request.user)
    client_update_form = ClientUpdateForm(instance = client_obj)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        client_update_form = ClientUpdateForm(request.POST, request.FILES or None, instance = client_obj)
        if client_update_form.is_valid() and user_form.is_valid():
            user_form.save()
            client_update_form.save()
            messages.success(request, 'Changes Saved.')
            # return redirect('accounts:profile')
        else:
           messages.error(request, 'Check the form and try again.') 
    context = {
        'user_form': user_form,
        'client_update_form': client_update_form,
        'client': client_obj
    }
    return render(request, 'clients/client-edit-form.html', context)



@login_required
def admin_client_user_details(request, id):
    client = get_object_or_404(User, id = id)
    context = {
        'client': client,
    }
    return render(request, 'clients/admin-client-user-details.html', context)


@login_required
def admin_client_user_update(request, id):
    user = get_object_or_404(User, id = id)
    form = AdminClientUserUpdateForm(instance=user)
    if request.method == 'POST':
        form = AdminClientUserUpdateForm(request.POST, request.FILES or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes Saved.')
            return redirect('clients:clients-list')
        else:
           messages.error(request, 'Check the form and try again.') 

    context = {
        'form': form,
    }
    return render(request, 'clients/admin-client-user-update.html', context)


class AdminClientUserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'clients/admin-client-user-delete.html'
    success_url = reverse_lazy('clients:clients-list')