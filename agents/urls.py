from django.urls import path
from . import views


app_name = 'agents'


urlpatterns = [
    path('list/', views.all_agents, name = 'agents-list'),

    path('all/', views.public_agents_list, name = 'public-agents-list'),
    path('<int:id>/agent/', views.public_agent_details, name = 'public-agent-details'),

    path('agent/user/<int:id>/update/form/', views.agency_agent_user_update, name = 'agency-agent-user-update'),
    path('agent/user/<int:id>/details/', views.agency_agent_user_details, name = 'agency-agent-user-details'),
    path('agent/user/<int:pk>/delete/', views.AgencyAgentUserDeleteView.as_view(), name = 'agency-agent-user-delete'),
    path('agency/agent/user/create/form/', views.agency_agent_user_create, name = 'agency-agent-user-create'),
    
    path('agency/agents/list/', views.agency_agents_list, name = 'agency-agents-list'),

    path('create/', views.agent_create, name = 'agent-create'),
    path('update/', views.agent_update, name = 'agent-update'),
    
]