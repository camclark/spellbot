from functools import wraps
from typing import Any, Callable, Optional

from datadog import initialize
from datadog.api.events import Event
from ddtrace import tracer

from . import __version__
from .environment import running_in_pytest
from .settings import Settings

settings = Settings()
IS_RUNNING_IN_PYTEST = running_in_pytest()
CTX_PROPS = {
    "author_id",
    "channel_id",
    "command_id",
    "component_id",
    "custom_id",
    "guild_id",
    "interaction_id",
    "kwargs",
    "origin_message_id",
    "values",
}


def no_metrics() -> bool:
    return IS_RUNNING_IN_PYTEST or not settings.DD_API_KEY or not settings.DD_APP_KEY


def skip_if_no_metrics(f) -> Callable[..., None]:  # pragma: no cover
    @wraps(f)
    def wrapper(*args, **kwargs) -> None:
        return None if no_metrics() else f(*args, **kwargs)

    return wrapper


@skip_if_no_metrics
def setup_metrics() -> None:  # pragma: no cover
    initialize(api_key=settings.DD_API_KEY, app_key=settings.DD_APP_KEY)


@skip_if_no_metrics
def alert_error(
    title: str,
    text: str = "",
    tags: Optional[list[str]] = None,
) -> None:  # pragma: no cover
    tags = tags or []
    tags.append(f"version:{__version__}")
    Event.create(alert_type="error", title=title, text=text, tags=tags)  # type: ignore


@skip_if_no_metrics
def add_span_context(ctx: Any):
    span = tracer.current_span()
    for prop in CTX_PROPS:
        if value := getattr(ctx, prop, None):
            span.set_tag(prop, value)
