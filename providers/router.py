from config import DEFAULT_PROVIDER
from providers.models import MODEL_MAP


def get_model(provider=None):

    provider = provider or DEFAULT_PROVIDER

    return MODEL_MAP[provider]