import random
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from django.contrib import messages
from django.core.mail import send_mail

from django.urls import reverse, reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import DeleteView

from listings.models import Listing

from .models import Agent

from .forms import(
    AgentCreateForm, AgentUpdateForm,
    AgencyAgentUserCreateForm, AgencyAgentUserUpdateForm
)
from accounts.forms import UserUpdateForm
from django.conf import settings

User  = get_user_model()

# Public
# This function lists all active agents
def public_agents_list(request):
    agents = Agent.objects.order_by('-user').filter(user__is_active = True, is_active = True).filter(user__is_organisor = False)
    paginator = Paginator(agents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj
    }
    return render(request, 'agents/agents/public-agents-list.html', context)


# Public
# This function returns the details of active agent
def public_agent_details(request, id):
    agent = Agent.objects.get(user__id=id, user__is_active = True)
    agent_listings = Listing.objects.order_by('-created_at').filter(listing_agent = agent.id)
    agent_sale_listings = Listing.objects.order_by('-created_at').filter(status = 'sale').filter(listing_agent = agent.id)
    agent_rent_listings = Listing.objects.order_by('-created_at').filter(status = 'rent').filter(listing_agent = agent.id)
    context = {
        'agent': agent,
        'agent_listings': agent_listings,
        'agent_sale_listings': agent_sale_listings,
        'agent_rent_listings': agent_rent_listings,
    }
    return render(request, 'agents/agents/public-agent-details.html', context)


# Private Agent Create
@login_required
def agency_agent_user_create(request):
    form = AgencyAgentUserCreateForm()
    if request.method == 'POST':
        form = AgencyAgentUserCreateForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_client = False
            user.is_agent = True
            user.is_organisor = False
            user.set_password(f'{random.randint(0, 1000000000)}')
            # user.organization = request.user.profile
            user.save()
            Agent.objects.create(user=user, organization = request.user.profile)

            message = """
            You have been added as an agent to join the {request.user.agency.name}. 
            Please go to the log in page, click the forget password link to reset your password to enable you log in to start working.
            """
            send_mail(
                subject = "Invitation as Agent.",
                message = message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [user.email,]
            )
            messages.success(request, 'Saved.')
            return redirect('agents:agency-agents-list')
        else:
           messages.error(request, 'Check the form and try again.') 

    context = {
        'form': form,
        # 'user_form': user_form,
    }
    return render(request, 'agents/agency-agents/agency-agent-user-create-form.html', context)


# Private Agents List
@login_required
def agency_agents_list(request):
    agency = request.user.profile.agency
    agents = Agent.objects.filter(organization=request.user.profile)

    context = {
        'agents': agents,
        'agency': agency
    }
    return render(request, 'agents/agency-agents/agency-agents-list.html', context)


# Private Agent Details
@login_required
def agency_agent_user_details(request, id):
    agent = get_object_or_404(Agent, id = id)
    context = {
        'agent': agent,
    }
    return render(request, 'agents/agency-agents/agency-agent-user-details.html', context)


@login_required
def agency_agent_user_update(request, id):
    user = get_object_or_404(User, id = id)
    form = AgencyAgentUserUpdateForm(instance=user)
    if request.method == 'POST':
        form = AgencyAgentUserUpdateForm(request.POST, request.FILES or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved.')
            return redirect('agents:agency-agents-list')
        else:
           messages.error(request, 'Check the form and try again.') 

    context = {
        'form': form,
    }
    return render(request, 'agents/agency-agents/agency-agent-user-update.html', context)


class AgencyAgentUserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'agents/agency-agents/agency-agent-user-delete.html'
    success_url = reverse_lazy('agents:agency-agents-list')


# Accessible by Super Admin
@login_required
def all_agents(request):

    all_agents = User.objects.order_by('date_joined').filter(is_agent=True)

    context = {
        'all_agents': all_agents
    }
    return render(request, 'agents/agents/all-agents-list.html', context)


# User Agent to create their agent profile themselves
@login_required
def agent_create(request):
    user_obj  = request.user

    user_form = UserUpdateForm(instance=request.user)
    agent_create_form = AgentCreateForm()

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        agent_create_form = AgentCreateForm(request.POST, request.FILES or None, instance = agent_obj)
        if user_form.is_valid() and agent_create_form.is_valid():
            user_form.save()
            agent_obj = client_form.save(commit = False)
            agent_obj.user = user_obj
            agent_obj.save()
            messages.success(request, 'Changes Saved.')
            return redirect('accounts:profile')
        else:
           messages.error(request, 'Check the form and try again.') 
    context = {
        'user_form': user_form,
        'agent_create_form': agent_create_form,
        'user': user_obj
    }
    return render(request, 'agents/agents/agent-create-form.html', context)


@login_required
def agent_update(request):
    agent_obj  = request.user.agent

    user_form = UserUpdateForm(instance=request.user)
    agent_update_form = AgentUpdateForm(instance = agent_obj)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        agent_update_form = AgentUpdateForm(request.POST, request.FILES or None, instance = agent_obj)
        if user_form.is_valid() and agent_update_form.is_valid():
            user_form.save()
            agent_update_form.save()
            messages.success(request, 'Changes Saved.')
            return redirect('accounts:profile')
        else:
           messages.error(request, 'Check the form and try again.') 
    context = {
        'user_form': user_form,
        'agent_update_form': agent_update_form,
        'agent': agent_obj
    }
    return render(request, 'agents/agents/agent-update-form.html', context)