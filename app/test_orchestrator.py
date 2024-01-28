from unbabel_cli import sma_orchestrator
from tempfile import TemporaryFile
import pytest

config_data = {
    "test_case_events_test": {
        "input_file": "events_test.json",
        "window_size": 10,
        "output_file": "output_events_test.json"
    },
    "test_case_events_test2": {
        "input_file": "events_test2.json",
        "window_size": 1,
        "output_file": "output_events_test2.json"
    },
    "test_case_events_test3": {
        "input_file": "events_test.json",
        "window_size": 0,
        "output_file": "output_events_test3.json"
    },
}

@pytest.mark.parametrize("test_case, input_file, window_size, output_file", [
    (test_name, test_data["input_file"], test_data["window_size"], test_data["output_file"])
    for test_name, test_data in config_data.items()
])
def test_orchestrator(test_case, input_file, window_size, output_file):
    with open(f"app/fixtures/{input_file}", "r", encoding="utf-8") as input_io:
        with TemporaryFile("w+") as output_io:
            sma_orchestrator(input_io, window_size, output_io)
            output_io.seek(0)

            with open(f"app/fixtures/{output_file}", "r", encoding="utf-8") as comp_io:
                assert comp_io.read() == output_io.read(), f"Test {test_case} failed"
