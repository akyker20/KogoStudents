from django import template
import datetime
from django.utils import timezone
from students.models import Location, Request

register = template.Library()

@register.filter
def num_active_requests(location):
	return Request.objects.filter(starting_loc=location, group__status='w').count()