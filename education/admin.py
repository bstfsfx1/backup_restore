from django.contrib import admin
#from .models import Curriculum
from .models import Tutor, School, Course # Adjust names

#@admin.site.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'course_subject')  # Adjust fields
    # search_fields = ('name', 'email')
    # list_filter = ('course_subject',)
    # ordering = ('name',)

#@admin.site.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'district')  # Adjust fields
    # search_fields = ('title', 'district')
    # list_filter = ('district',)
    # ordering = ('title',)
    
#@admin.site.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor', 'school')  # Adjust fields
    # search_fields = ('title', 'tutor__name', 'school__title')
    # list_filter = ('school', 'tutor')
    # ordering = ('title',)

# class CurriculumAdmin(admin.ModelAdmin):
#     list_display = ('name', 'text',)
#     list_display_links = ('name',)
#     list_editable = ()

admin.site.register(Course, CourseAdmin)
admin.site.register(Tutor, TutorAdmin)
admin.site.register(School, SchoolAdmin)
#admin.site.register(Curriculum, CurriculumAdmin)