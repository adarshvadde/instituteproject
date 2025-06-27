from django.contrib import admin
from .models import StudentUser , AttendanceRecord,Application,AdminUser,WeeklyWorkReport,DailyEntry
class AdminUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(AdminUser, AdminUserAdmin)
class StudentUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentUser, StudentUserAdmin)
class AttendanceRecordAdmin(admin.ModelAdmin):
    pass
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)
class ApplicationFormAdmin(admin.ModelAdmin):
    pass
admin.site.register(Application,ApplicationFormAdmin)

class WeeklyWorkReportFormAdmin(admin.ModelAdmin):
    pass
admin.site.register(WeeklyWorkReport,WeeklyWorkReportFormAdmin)

class DailyEntryFormAdmin(admin.ModelAdmin):
    pass
admin.site.register(DailyEntry,DailyEntryFormAdmin)
