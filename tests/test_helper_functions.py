import helper_functions
import pytest


@pytest.mark.parametrize(
    "month,year,expected_start,expected_end",
    [
        (12, 2023, "2023-12-01T00:00:00+10:00", "2024-01-01T00:00:00+10:00"),
        (2, 2024, "2024-02-01T00:00:00+10:00", "2024-03-01T00:00:00+10:00"),
    ],
)
def test_calc_start_end_strings_returns_rfc3339_datetime(
    month: int, year: int, expected_start: str, expected_end: str
) -> None:
    result = helper_functions.calc_start_end_strings(month, year)
    assert result[0] == expected_start
    assert result[1] == expected_end
