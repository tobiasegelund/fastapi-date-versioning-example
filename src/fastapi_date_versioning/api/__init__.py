import datetime
import typing as t

from fastapi_date_versioning.api.home import hello_version_v1, hello_version_v2

HOME_API_VERSIONS: dict[datetime.date, t.Callable] = {
    datetime.date(2023, 6, 1): hello_version_v1,
    # datetime.date(2024, 6, 1): hello_version_v2,
}
