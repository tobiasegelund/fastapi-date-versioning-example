import datetime
import typing as t

API_VERSIONS: dict[datetime.date, t.Callable] = {
    datetime.date(2023, 1, 1): hello_version_v1,
    datetime.date(2023, 6, 1): hello_version_v1,
    datetime.date(2024, 1, 1): hello_version_v2,
    datetime.date(2024, 6, 1): hello_version_v2,
}
