from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standard shape for every paginated list endpoint: the current page's
    items, the total count across ALL matching rows (not just this page),
    and the limit/offset that produced this page. Declaring this as the
    route's response_model (e.g. response_model=PaginatedResponse[ProductRead])
    is what makes the OpenAPI docs show the real shape instead of an
    untyped dict.
    """

    items: list[T]
    total: int
    limit: int
    offset: int
