from django.shortcuts import render
from django.views import View
from collections import deque
from django.views.generic import TemplateView
from django.http import HttpResponse


# Create your views here.


class WelcomeView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'tickets/index.html', context)


MENU = {
    'Change oil': '/get_ticket/change_oil',
    'Inflate tires': '/get_ticket/inflate_tires',
    'Get diagnostic test': '/get_ticket/diagnostic',
}

SERVICE_TIME = {
    'change_oil': 2,
    'inflate_tires': 5,
    'diagnostic': 30,
}

LINE_OF_CARS = {
    'change_oil': deque(),
    'inflate_tires': deque(),
    'diagnostic': deque(),
}


def calculate_waiting(no_of_customers, constant):
    if no_of_customers == 1:
        waiting_period = 0
    else:
        waiting_period = constant * (no_of_customers - 1)
    return waiting_period


def calculate_wait_time(service):
    priority_list = ['change_oil', 'inflate_tires', 'diagnostic']
    index = priority_list.index(service)
    wait_time = 0
    position = 0
    for service in priority_list[:index + 1]:
        people_queued = len(LINE_OF_CARS[service])
        position += people_queued
        wait_time += SERVICE_TIME[service] * people_queued
    return position, wait_time


class MenuView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'menus': MENU
        }
        return render(request, 'tickets/menu_page.html', context)


class TicketView(TemplateView):
    template_name = 'tickets/ticket_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = kwargs['service']
        context['ticket_number'], context['minutes_to_wait'] = calculate_wait_time(service)
        LINE_OF_CARS[service].append(1)
        return context


class RedirectView(View):

    def get(self, request, *args, **kwargs):
        line_of_cars = {'Change oil queue:': len(LINE_OF_CARS['change_oil']),
                        'Inflate tires queue:': len(LINE_OF_CARS['inflate_tires']),
                        'Get diagnostic queue:': len(LINE_OF_CARS['diagnostic'])}
        context = {
            'queues': line_of_cars
        }
        return render(request, 'tickets/operator_menu.html', context)