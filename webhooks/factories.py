""""""

import abc

from webhooks.interfaces import IssueWebhook, Webhook, SGWebhook


class WebhookFactory(metaclass=abc.ABCMeta):
    """
    Declare an interface for operations that create abstract product objects.
    """

    @abc.abstractmethod
    def createWebhook(self, customization) -> 'Webhook':
        return customization()

    @staticmethod
    def getWebhookFactory(factoryType) -> 'WebhookFactory':
        return factoryType()


class IssueWebhookFactory(WebhookFactory):
    def createWebhook(self, name: str, **attributes) -> 'IssueWebhook':
        return type(name+'IssueWebhook', (IssueWebhook,Webhook,), attributes)

class PRWebhookFactory(WebhookFactory):
    ...

class ProjectsWebhookFactory(WebhookFactory):
    ...


issueWebhookFactory = IssueWebhookFactory()

# prWebhookFactory = PRWebhookFactory()
# projectsWebhookFactory = ProjectsWebhookFactory()



class SendGridWebhookFactory(WebhookFactory):
    def createWebhook(self, customization) -> 'SGWebhook':
        return customization()

    @staticmethod
    def getWebhookFactory(factoryType) -> 'WebhookFactory':
        return factoryType()


class UniversalSGWebhookFactory(SendGridWebhookFactory):
    def createWebhook(self, name: str, **attributes) -> 'SGWebhook':
        return type(name+'SGWebhook', (SGWebhook,), attributes)

sgWebhookFactory = UniversalSGWebhookFactory()
