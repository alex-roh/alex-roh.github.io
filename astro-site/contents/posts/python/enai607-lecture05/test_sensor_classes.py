import unittest
from sensor_classes import Sensor, CalibratedSensor


class SensorTests(unittest.TestCase):
    def test_required_examples(self):
        before = Sensor.get_sensor_count()
        s1 = Sensor("Ava", [10, 20, 30])
        s2 = CalibratedSensor("Ben", [4, 6], 1.5, 2.0)
        self.assertEqual(s1.get_average(), 20.0)
        self.assertEqual(s2.get_average(), 9.5)
        s1.add_value(40)
        self.assertEqual(s1.get_average(), 25.0)
        self.assertEqual(Sensor.get_sensor_count(), before + 2)

    def test_private_list_copies(self):
        for factory in (lambda xs: Sensor("A", xs),
                        lambda xs: CalibratedSensor("B", xs, 2, 1)):
            source = [4, 6]
            sensor = factory(source)
            source[0] = 999
            returned = sensor.get_values()
            returned[1] = 999
            self.assertEqual(sensor.get_values(), [4, 6])
            self.assertIsNot(sensor.get_values(), sensor.get_values())

    def test_ids_across_subclasses(self):
        class ExtraSensor(Sensor):
            pass
        start = Sensor.get_sensor_count()
        objects = [Sensor("A", [0]), CalibratedSensor("B", [0], 1, 0),
                   ExtraSensor("C", [0]), Sensor("D", [0])]
        self.assertEqual([s.get_id() for s in objects], list(range(start, start + 4)))
        self.assertEqual(CalibratedSensor.get_sensor_count(), start + 4)
        self.assertIsInstance(Sensor.__dict__["get_sensor_count"], classmethod)

    def test_invalid_readings_and_names(self):
        for name, readings, error in [("", [1], ValueError), ("A", [], ValueError),
                                      ("A", [-1], ValueError), ("A", [1, "2"], TypeError),
                                      ("A", [True], TypeError)]:
            with self.subTest(name=name, readings=readings):
                count = Sensor.get_sensor_count()
                with self.assertRaises(error):
                    Sensor(name, readings)
                self.assertEqual(Sensor.get_sensor_count(), count)

    def test_invalid_calibration_does_not_count(self):
        for scale, offset, error in [(0, 0, ValueError), (-1, 0, ValueError),
                                    ("1", 0, TypeError), (1, "0", TypeError),
                                    (True, 0, TypeError)]:
            with self.subTest(scale=scale, offset=offset):
                count = Sensor.get_sensor_count()
                with self.assertRaises(error):
                    CalibratedSensor("B", [1], scale, offset)
                self.assertEqual(Sensor.get_sensor_count(), count)

    def test_rejected_add_keeps_state(self):
        sensor = Sensor("A", [0, 2])
        for value, error in [(-1, ValueError), ("3", TypeError)]:
            with self.assertRaises(error):
                sensor.add_value(value)
            self.assertEqual(sensor.get_values(), [0, 2])

    def test_child_methods_and_dynamic_string(self):
        sensor = CalibratedSensor("Ben", [4, 6], 1.5, 2)
        sensor.add_value(8)
        self.assertEqual(sensor.get_values(), [4, 6, 8])
        self.assertEqual(sensor.get_average(), 11.0)
        self.assertIn("average = 11.00", str(sensor))
        self.assertIn("Ben", str(sensor))
        self.assertIn(str(sensor.get_id()), str(sensor))
        self.assertIn("count = 3", str(sensor))

    def test_independent_objects_and_negative_offset(self):
        a = Sensor("A", [10, 20])
        b = CalibratedSensor("B", [0], 1, -2)
        self.assertEqual(b.get_average(), -2)
        b.add_value(4)
        self.assertEqual(a.get_values(), [10, 20])
        self.assertEqual(a.get_average(), 15)
        self.assertEqual(b.get_name(), "B")


if __name__ == "__main__":
    unittest.main(verbosity=2)
