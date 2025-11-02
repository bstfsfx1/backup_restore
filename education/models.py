from django.db import models
from .choices import district_choices, subject_choices

#from .models import Course
#from .models import School, Tutor

# Create your models here.
class School(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    district = models.CharField(max_length=50)
    room_num = models.IntegerField(default=0)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    office_hr = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
    # class Meta:
    #     db_table = 'schools_school'


class Tutor(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20, default='00000000')
    email = models.EmailField(max_length=50, unique=False, blank=True)
    is_mvp = models.BooleanField(default=True)
    hire_date = models.DateTimeField(auto_now_add=True)
    course_subject = models.CharField(max_length=50,choices=subject_choices, default='Chinese', help_text='Subject taught by the tutor')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, help_text='Average rating from 0.0 to 5.0')
    experience = models.CharField(max_length=20, default=1, help_text='Years of experience')
    taught_students = models.PositiveIntegerField(default=100, help_text='Number of students taught')
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'tutors_tutor'


class Course(models.Model): 
    #syllabus = models.ManyToManyField(Curriculum, blank=True)

    CLASS_TYPE_CHOICES = [
        ('live', 'Live'),
        ('video', 'Video'),
    ]

    title = models.CharField(
        max_length=200,
        help_text='Name of the course'
    )
    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.DO_NOTHING,
        related_name='courses',
        help_text='Tutor teaching this course'
    )
    school = models.ForeignKey(
        School,
        on_delete=models.DO_NOTHING,
        related_name='courses',
        help_text='School offering the course',
        blank=True,
        null=True,
    )
    district = models.CharField(
        max_length=50,
        choices=district_choices,
        default='Sha Tin',
        help_text='District where the course is offered'
    )
    subject = models.CharField(
        max_length=50,
        choices=subject_choices,
        default='Chinese',
        help_text='Subject matter of the course'
    )
    students_enrolled = models.PositiveIntegerField(
        default=0,
        help_text='Current number of students enrolled'
    )
    max_students = models.PositiveIntegerField(
        default=20,
        help_text='Maximum number of students allowed'
    )
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        help_text='Average rating from 0.0 to 5.0'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Course price in HKD'
    )
    duration = models.PositiveIntegerField(
        default=1,
        help_text='Course duration in hours'
    )
    total_classes = models.PositiveIntegerField(
        default=4,
        help_text='Total number of classes in the course'
    )
    class_time = models.CharField(
        max_length=50,
        default='Wed 4 p.m.',
        help_text='Scheduled time for the class (e.g., Wed 4 p.m.)'
    )
    class_type = models.CharField(
        max_length=5,
        choices=CLASS_TYPE_CHOICES,
        default='live',
        help_text='Delivery format of the course'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    description = models.TextField(
        help_text='Detailed description of the course',
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'courses_course'

        
# class Curriculum(models.Model):
#     name = models.CharField(max_length=50,
#                         choices=subject_choices,
#                         default='Chinese',
#                         help_text='Subject matter of the curriculum'
#                         )
# text = models.TextField(blank=True,
#                         null=True,
#                         help_text='Detailed syllabus of the curriculum'
#                         )
# def __str__(self):
#     return self.name
