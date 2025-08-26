# import graphene
# from crm.schema import Query as CRMQuery, Mutation as CRMMutation


# class Query(CRMQuery, graphene.ObjectType):
#     pass


# class Mutation(CRMMutation, graphene.ObjectType):
#     pass


# schema = graphene.Schema(query=Query, mutation=Mutation)

# class Query(graphene.ObjectType):
#     hello = graphene.String(default_value="Hello, GraphQL!")

# schema = graphene.Schema(query=Query)

import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

app = Celery('crm', broker='redis://localhost:6379/0')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()
class Query(CRMQuery, graphene.ObjectType):
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
