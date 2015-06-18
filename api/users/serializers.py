from rest_framework import serializers as ser

from api.base.serializers import JSONAPISerializer, JSONAPIListSerializer, LinksField, Link
from website.models import User
from django.db import models
from jsonfield import JSONField
from django.utils import six, timezone
import inspect
from rest_framework.utils import html


class JobsSerializer(JSONAPISerializer):
    startYear = ser.CharField(allow_blank=True)
    title = ser.CharField()
    startMonth = ser.IntegerField(max_value=12, min_value=1, allow_null=True)
    endMonth = ser.IntegerField(max_value=12, min_value=1, allow_null=True)
    endYear = ser.CharField(allow_blank=True)
    ongoing = ser.BooleanField()
    department = ser.CharField()
    institution = ser.CharField()

    class Meta:
        type_ = 'jobs'

# class SocialSerializer(JSONAPISerializer):
#     github = ser.CharField(allow_blank=True, source='social.github')
#     title = ser.CharField()
#     startMonth = ser.IntegerField(max_value=12, min_value=1, allow_null=True)
#     endMonth = ser.IntegerField(max_value=12, min_value=1, allow_null=True)
#     endYear = ser.CharField(allow_blank=True)
#     ongoing = ser.BooleanField()
#     department = ser.CharField()
#     institution = ser.CharField()
#
#     class Meta:
#         type_ = 'social'


class empty:
    """
    This class is used to represent no data being provided for a given input
    or output value.

    It is required because `None` may be a valid input or output value.
    """
    pass

class APIDictField(ser.DictField):

    def get_value(self, dictionary):
        # We override the default field access in order to support
        # dictionaries in HTML forms.
        if html.is_html_input(dictionary):
            return html.parse_html_dict(dictionary, prefix=self.field_name)
        return dictionary.get(self.field_name, empty)

    def to_internal_value(self, data):
        """
        Dicts of native values <- Dicts of primitive datatypes.
        """
        if html.is_html_input(data):
            data = html.parse_html_dict(data)
        if not isinstance(data, dict):
            self.fail('not_a_dict', input_type=type(data).__name__)
        return dict([
            (six.text_type(key), self.child.run_validation(value))
            for key, value in data.items()
        ])

    def to_representation(self, value):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        return dict([
            (six.text_type(key), self.child.to_representation(val))
            for key, val in value.items()
        ])



class UserSerializer(JSONAPISerializer):
    filterable_fields = frozenset([
        'fullname',
        'given_name',
        'middle_name',
        'family_name',
        'id'
    ])

    id = ser.CharField(read_only=True, source='_id')
    fullname = ser.CharField(help_text='Display name used in the general user interface')
    given_name = ser.CharField(required=False, help_text='For bibliographic citations')
    middle_name = ser.CharField(required=False, source='middle_names', help_text='For bibliographic citations')
    family_name = ser.CharField(required=False, help_text='For bibliographic citations')
    suffix = ser.CharField(required=False, help_text='For bibliographic citations')
    date_registered = ser.DateTimeField(read_only=True)
    gravatar_url = ser.CharField(required=False, help_text='URL for the icon used to identify the user. Relies on http://gravatar.com ')
    # employment_institutions = ser.ListField(child=JobsSerializer(), required=False, source='jobs', help_text='An array of dictionaries representing the '
    #                                         'places the user has worked')
    # employment_institutions = ser.ListField(child=ser.CharField(), required=False, source='jobs', help_text='An array of dictionaries representing the '
    #                                                                  'places the user has worked')
    # educational_institutions = ser.ListField(child=ser.CharField(), required=False, source='schools', help_text='An array of dictionaries representing the '
    #                                                                      'places the user has attended school')
    # social_accounts = ser.DictField(allow_null=True, child=ser.CharField(), source='social', help_text='A dictionary of various social media account '
    #                                                            'identifiers including an array of user-defined URLs')
    # social_accounts = APIDictField(source='social')
    # social_accounts = APIDictField(allow_null=True, child=ser.CharField(), required=False, source='social', help_text='A dictionary of various social media account '
    #                                                            'identifiers including an array of user-defined URLs')
    github = ser.CharField(required=False, source='social.github', help_text='Github Handle')
    scholar = ser.CharField(required=False, source='social.scholar', help_text='Google Scholar Account')
    personal = ser.CharField(required=False, source='social.personal', help_text='Personal Website')
    twitter = ser.CharField(required=False, source='social.twitter', help_text='Twitter Handle')
    linkedIn = ser.CharField(required=False, source='social.linkedIn', help_text='LinkedIn Account')
    impactStory = ser.CharField(required=False, source='social.impactStory', help_text='ImpactStory Account')
    orcid = ser.CharField(required=False, source='social.orcid', help_text='orcid Account Number ex 1111 1111 1111 1111')
    researcherId = ser.CharField(required=False, source='social.researcherId', help_text='ResearcherId Account')

    links = LinksField({
        'html': 'absolute_url',
        'nodes': {
            'relation': Link('users:user-nodes', kwargs={'user_id': '<pk>'})
        }
    })

    class Meta:
        type_ = 'users'
        fields = ('id', 'fullname', 'given_name', 'middle_name', 'family_name', 'suffix', 'date_registered', 'gravatar_url', 'employment_institutions', 'social_accounts')

    def absolute_url(self, obj):
        return obj.absolute_url

    def update(self, instance, validated_data):
        # jobs_data = validated_data.pop('jobs')
        # jobs = instance.jobs
        assert isinstance(instance, User), 'instance must be a User'
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # jobs.save()
        instance.save()
        return instance


class ContributorSerializer(UserSerializer):

    local_filterable = frozenset(['bibliographic'])
    filterable_fields = frozenset.union(UserSerializer.filterable_fields, local_filterable)

    bibliographic = ser.BooleanField(help_text='Whether the user will be included in citations for this node or not')
