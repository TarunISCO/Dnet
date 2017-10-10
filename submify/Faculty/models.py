# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinLengthValidator
from allauth.socialaccount.models import SocialAccount
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

from helper import file_hash
from django.conf import settings
import os


class FacultyModel(models.Model):
    """Model representation for the Faculty
    :var name : Name of the Faculty
    :var email : Email of the Faculty
    :var department : Department of the Faculty
    """

    DEPARTMENTS = (
        ("CS", "Computer Science"),
        ("IT", "Information Technology")
    )

    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    department = models.CharField(max_length=2, choices=DEPARTMENTS, default="IT")

    def __str__(self):
        return self.name + ' ' + str(self.id)


def validate_batch(value):
    if len(str(value)) != 4:
        raise ValidationError('Batch is not of length 4')


class Course(models.Model):
    """Model representation for the courses
    :var courseID : Course Id of the course
    :var courseName : Name of the course
    :var instructor : Instructor (faculty)
    """

    courseId = models.CharField(max_length=5, null=False, blank=False, validators=[MinLengthValidator(5)])
    courseName = models.CharField(max_length=20, null=False, blank=False)
    batch = models.IntegerField(default=2013, validators=[validate_batch], null=False, blank=False)
    instructor = models.ForeignKey(FacultyModel)

    def __str__(self):
        return self.courseId

    @staticmethod
    def get_course_by_id(cid):
        return Course.objects.filter(courseId=cid)

    @staticmethod
    def get_courses_by_instructor(instructor_id):
        return Course.objects.filter(instructor=instructor_id)


class TitleFormat(models.Model):
    """Model for title format for the problem
    :var courseCode : Course Code for the program
    :var titleName : title Name for the problem
    :var instituteId : Need Institute id in the title
    :var groupId : Group ID Flag for getting group id (specific)
    :var groupInitial : Group Initials to follow for renaming
    """

    courseCode = models.ForeignKey(Course)
    titleName = models.CharField(max_length=20, null=False, blank=False)
    instituteId = models.BooleanField(default=False)
    groupId = models.BooleanField(default=True)
    groupInitial = models.CharField(max_length=20, null=False, blank=True)

    def __str__(self):
        return self.titleName + ' ' + str(self.courseCode)


def validate_late_submission(value):
    if value.time.hour > 60:
        raise ValidationError('Maximum extension can be of only one hour')


class Submission(models.Model):
    """Model representation for the submission
    :var course : Course for which submission have to be done
    :var startDate : start date for the submission
    :var endDate : Ending date for submission
    :var hashString : hash generated for the submission (used by endpoints)
    :var lateSubmission : Flag for allowing late Submission
    :var lateSubmissionPeriod : Limit for late submission
    :var reviewType : Method for gettign submissions
    """

    OPTIONS = (
        (0, "Email"),
        (1, "Zip/Tar archive"),
        (2, "API Endpoint")
    )

    course = models.ForeignKey(Course)
    startDate = models.DateTimeField(default=datetime.datetime.now)
    endDate = models.DateTimeField(null=False, blank=False)
    hashString = models.IntegerField(null=False)
    lateSubmission = models.BooleanField(null=False, blank=True, default=True)
    lateSubmissionPeriod = models.IntegerField('Late submission period (in minutes)', blank=True,
                                               validators=[validate_late_submission], null=True)
    reviewType = models.IntegerField(choices=OPTIONS, blank=False, default=1)
    titleType = models.ForeignKey(TitleFormat)

    def __str__(self):
        return self.course.courseId + ' ' + str(self.startDate)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.hashString = file_hash.generate_hash_string(str(self.course.courseId) + ' ' + str(self.startDate.date) +
                                                         ' ' + str(self.endDate.date))
        super(Submission, self).save(force_insert, force_update)


class Submit(models.Model):
    """Model representation for all submit"""
    user = models.ForeignKey(SocialAccount)
    document = models.FileField(upload_to='docs/', blank=False)
    submission = models.ForeignKey(Submission)

    def __str__(self):
        return str(self.user.id) + ' ' + str(self.submission.id)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        for field in self._meta.fields:
            if field.name == 'document':
                data = self.user.extra_data
                extension = str(self.document).split('.')[-1]
                name = self.submission.titleType.titleName + '_' + data['email'][0:4] + '.' + extension
                path = 'documents/%d' % self.submission.hashString
                field.upload_to = path
                abs_path = settings.BASE_DIR + '/' + path
                #print abs_path + '/' + str(self.document)
                #print os.path.join(os.path.dirname(abs_path), name)
                # os.rename(abs_path + '/' + str(self.document), os.path.join(os.path.dirname(abs_path), name))
        super(Submit, self).save()


@receiver(post_save, sender=Submit)
def rename_file(sender, instance, created, **kwargs):
    data = instance.user.extra_data
    id_data = str(data['email']).split('@')[0]
    #print id_data
    extension = str(instance.document).split('.')[-1]
    name = instance.submission.titleType.titleName + '_' + id_data + '.' + extension
    path = 'documents/%d' % instance.submission.hashString
    abs_path = settings.BASE_DIR + '/' + str(instance.document)
    #print abs_path
    #print os.path.join(os.path.dirname(abs_path), name)
    os.rename(abs_path, os.path.join(os.path.dirname(abs_path), name))
