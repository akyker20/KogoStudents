from django import template
from django.utils import timezone
import datetime

register = template.Library()

@register.inclusion_tag('drivers/location_groups.html')
def get_groups(location):
	groups = location.pickup_groups.filter(status='w').all()
	context = {'groups': groups, 'location': location}
	return context