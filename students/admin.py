from django.contrib import admin
from models import StudentProfile, Request, RideGroup, Location


class RequestAdmin(admin.ModelAdmin):
	list_display = ('student', 'time', 'pickup_loc','dropoff_loc', 'group')

class RideGroupAdmin(admin.ModelAdmin):
	list_display = ('created_at', 'pickup_loc', 'dropoff_loc', 'riders', 'status')

	def riders(self, obj):
		return obj.__unicode__()

admin.site.register(StudentProfile)
admin.site.register(Request, RequestAdmin)
admin.site.register(RideGroup, RideGroupAdmin)
admin.site.register(Location)