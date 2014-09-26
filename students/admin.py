from django.contrib import admin
from models import StudentProfile, Request, RideGroup, Location


class RequestAdmin(admin.ModelAdmin):
	list_display = ('student', 'time', 'starting_loc','ending_loc', 'group')

class RideGroupAdmin(admin.ModelAdmin):
	list_display = ('created_at', 'starting_loc', 'ending_loc', 'students', 'status')

	def students(self, obj):
		return obj.__unicode__()

admin.site.register(StudentProfile)
admin.site.register(Request, RequestAdmin)
admin.site.register(RideGroup, RideGroupAdmin)
admin.site.register(Location)