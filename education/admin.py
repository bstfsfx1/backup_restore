from django.contrib import admin
from .models import Tutor, School, Course # Adjust names

class TutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'course_subject')  # Adjust fields

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'district')  # Adjust fields

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor', 'school')  # Adjust fields


admin.site.register(Course, CourseAdmin)
admin.site.register(Tutor, TutorAdmin)
admin.site.register(School, SchoolAdmin)
