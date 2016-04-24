from timeleft import timeleft
import pytest


VALID_SPEED_MEASUREMENT_BASE_AMOUNT = 838860800.0
VALID_SPEED_MEASUREMENT_NUMBER = "100"
VALID_SPEED_MEASUREMENT_PREFIX = "M"

VALID_SIZE_MEASUREMENT_BASE_AMOUNT = VALID_SPEED_MEASUREMENT_BASE_AMOUNT
VALID_SIZE_MEASUREMENT_NUMBER = VALID_SPEED_MEASUREMENT_NUMBER
VALID_SIZE_MEASUREMENT_PREFIX = VALID_SPEED_MEASUREMENT_PREFIX


class TestMeasurment:
    @pytest.fixture(autouse=True)
    def setup(self):
        """
        CaseInsensitiveDict instance with "Accept" header.
        """
        self.valid_speed_measurement = timeleft.Measurement(VALID_SPEED_MEASUREMENT_NUMBER +
                                                            VALID_SPEED_MEASUREMENT_PREFIX + "Bps")
        self.valid_size_measurement = timeleft.Measurement(VALID_SIZE_MEASUREMENT_NUMBER +
                                                           VALID_SIZE_MEASUREMENT_PREFIX + "B")

    def test_speed_measurement_base_amount(self):
        assert self.valid_speed_measurement.get_base_amount() == VALID_SPEED_MEASUREMENT_BASE_AMOUNT

    def test_size_measurement_base_amount(self):
        assert self.valid_size_measurement.get_base_amount() == VALID_SIZE_MEASUREMENT_BASE_AMOUNT

    def test_speed_measurement_get_type(self):
        assert self.valid_speed_measurement.get_type() == timeleft.SPEED

    def test_size_measurement_get_type(self):
        assert self.valid_size_measurement.get_type() == timeleft.SIZE

    @pytest.mark.parametrize("input_string", [
        VALID_SPEED_MEASUREMENT_NUMBER + "MBPs",
        VALID_SPEED_MEASUREMENT_NUMBER + "MBps",
        VALID_SPEED_MEASUREMENT_NUMBER + "MB/S",
        VALID_SPEED_MEASUREMENT_NUMBER + "MB/s",
    ])
    def test_speed_measurement_input_variations(self, input_string):
        speed_measurement = timeleft.Measurement(input_string)
        assert speed_measurement == self.valid_speed_measurement

    def test_bit_versus_byte_awareness(self):
        speed_bit_measurement = timeleft.Measurement("10Mbps")
        speed_byte_measurement = timeleft.Measurement("10MBps")
        size_bit_measurement = timeleft.Measurement("10Mb")
        size_byte_measurement = timeleft.Measurement("10MB")
        assert speed_bit_measurement.get_base_amount() * 8.0 == speed_byte_measurement.get_base_amount() and \
            size_bit_measurement.get_base_amount() * 8.0 == size_byte_measurement.get_base_amount()

    def test_invalid_measurement_input(self):
        with pytest.raises(RuntimeError):
            timeleft.Measurement("")


class TestTimeleft:
    def test_valid_get_measurements_input(self):
        args = ["100MBps", "100MB"]
        test_measurements = tuple(timeleft.get_measurements(args))
        comparison_measurements = (timeleft.Measurement("100MBps"), timeleft.Measurement("100MB"))
        assert test_measurements == comparison_measurements

    def test_get_measurements_too_many_inputs(self):
        with pytest.raises(RuntimeError):
            args = ["100MBps", "100MB", "100MB"]
            timeleft.get_measurements(args)

    def test_get_measurements_too_few_inputs_1(self):
        with pytest.raises(RuntimeError):
            args = ["100MBps"]
            timeleft.get_measurements(args)

    def test_get_measurements_too_few_inputs_0(self):
        with pytest.raises(RuntimeError):
            timeleft.get_measurements([])

    def test_get_duration_seconds(self):
        valid_speed_measurement = timeleft.Measurement(VALID_SPEED_MEASUREMENT_NUMBER +
                                                       VALID_SPEED_MEASUREMENT_PREFIX + "Bps")
        valid_size_measurement = timeleft.Measurement(VALID_SIZE_MEASUREMENT_NUMBER +
                                                      VALID_SIZE_MEASUREMENT_PREFIX + "B")
        assert timeleft.get_duration_seconds([valid_speed_measurement, valid_size_measurement]) == 1.0
