from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import itertools


class CalendarPeriod(models.Model):
    calendar_period_id = models.IntegerField(primary_key=True)
    calendar_period_name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return '%s' % self.calendar_period_name

    class Meta:
        permissions = {('view_calendarperiod', 'Can view calendar period'), }
        ordering = ['calendar_period_id']


class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    calendar_period = models.ForeignKey(CalendarPeriod, related_name='semesters', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return '%s-%s' % (self.year, self.calendar_period.calendar_period_name)

    def get_absolute_url(self):
        return reverse('courseinfo:semester_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('courseinfo:semester_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('courseinfo:semester_remove', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        unique_slug = slugify(self)
        for x in itertools.count(1):
            if not Semester.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = '%s-%d' % (unique_slug, x)
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

    class Meta:
        permissions = {('view_semester', 'Can view semester'), }
        ordering = ['year', 'calendar_period__calendar_period_id']
        unique_together = ('year', 'calendar_period')


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_number = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return '%s' % self.course_name

    def get_absolute_url(self):
        return reverse('courseinfo:course_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('courseinfo:course_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('courseinfo:course_remove', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        unique_slug = slugify(self.course_name)
        for x in itertools.count(1):
            if not Course.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = '%s-%d' % (unique_slug, x)
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

    class Meta:
        permissions = {('view_course', 'Can view course'), }
        ordering = ['course_number']


class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return '%s , %s' % (self.last_name, self.first_name)

    def get_absolute_url(self):
        return reverse('courseinfo:instructor_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('courseinfo:instructor_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('courseinfo:instructor_remove', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        unique_slug = slugify('%s--%s' % (self.last_name, self.first_name))
        for x in itertools.count(1):
            if not Instructor.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = '%s-%d' % (unique_slug, x)
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

    class Meta:
        permissions = {('view_instructor', 'Can view instructor'), }
        ordering = ['last_name', 'first_name']


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    nick_name = models.CharField(max_length=45, default='', blank=True)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        if self.nick_name == "":
            return '%s , %s' % (self.last_name, self.first_name)
        else:
            return '%s , %s (%s)' % (self.last_name, self.first_name, self.nick_name)

    def get_absolute_url(self):
        return reverse('courseinfo:student_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('courseinfo:student_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('courseinfo:student_remove', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        unique_slug = slugify('%s--%s' % (self.last_name, self.first_name))
        for x in itertools.count(1):
            if not Student.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = '%s-%d' % (unique_slug, x)
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

    class Meta:
        permissions = {('view_student', 'Can view student'), }
        ordering = ['last_name', 'first_name']


class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=10)
    semester = models.ForeignKey(Semester, related_name='sections', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)
    instructors = models.ManyToManyField(Instructor, related_name='sections')
    students = models.ManyToManyField(Student, related_name='sections')
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return '%s - %s (%s)' % (self.course.course_number, self.section_name, self.semester)

    def get_absolute_url(self):
        return reverse('courseinfo:section_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('courseinfo:section_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('courseinfo:section_remove', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        unique_slug = slugify(self.section_name)
        for x in itertools.count(1):
            if not Section.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = '%s-%d' % (unique_slug, x)
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

    class Meta:
        permissions = {('view_section', 'Can view section'), }
        ordering = ['course__course_number', 'section_name', 'semester']
