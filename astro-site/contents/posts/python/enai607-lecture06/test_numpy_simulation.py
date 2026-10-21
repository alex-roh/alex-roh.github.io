from pathlib import Path
import tempfile
import unittest
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy_simulation import (create_curves, make_slice_examples, solve_system,
                              generate_rayleigh, make_figure)


class SimulationTests(unittest.TestCase):
    def test_grid_endpoints_and_spacing(self):
        x, f, g = create_curves()
        self.assertEqual(x.shape, (500,))
        self.assertEqual(f.shape, x.shape)
        self.assertEqual(g.shape, x.shape)
        self.assertEqual(x[0], 0)
        self.assertEqual(x[-1], 10)
        np.testing.assert_allclose(np.diff(x), 10 / 499)

    def test_functions_and_maximum_coordinate(self):
        x, f, g = create_curves()
        np.testing.assert_allclose(f, np.sin(3 * x) * np.exp(-x / 2))
        np.testing.assert_allclose(g, np.cos(2 * x) * np.exp(-x / 2))
        self.assertEqual(f[np.argmax(f)], f.max())
        self.assertGreater(x[np.argmax(f)], 0)
        self.assertTrue(np.isfinite(f.std()))

    def test_view_copy_and_original_curve(self):
        _, f, _ = create_curves()
        before = f.copy()
        initial, transpose, matrix, view, independent, copied = make_slice_examples(f)
        self.assertEqual(initial.shape, (3, 4))
        self.assertEqual(transpose.shape, (4, 3))
        self.assertEqual(view.shape, (2, 2))
        self.assertTrue(np.shares_memory(matrix, view))
        self.assertEqual(matrix[1, 0], -1)
        self.assertFalse(np.shares_memory(independent, copied))
        np.testing.assert_array_equal(independent, initial)
        np.testing.assert_array_equal(f, before)
        np.testing.assert_array_equal(transpose, initial.T)

    def test_linear_system(self):
        A, b, solution = solve_system()
        np.testing.assert_allclose(solution, [2, 3])
        np.testing.assert_allclose(A @ solution, b)

    def test_complex_magnitudes_and_shapes(self):
        real, imag, z, magnitude = generate_rayleigh()
        self.assertEqual(real.shape, (10_000,))
        self.assertEqual(imag.shape, real.shape)
        self.assertTrue(np.iscomplexobj(z))
        np.testing.assert_array_equal(z.real, real)
        np.testing.assert_array_equal(z.imag, imag)
        np.testing.assert_allclose(magnitude, np.sqrt(real**2 + imag**2))
        self.assertTrue(np.all(magnitude >= 0))

    def test_random_parameters_sanity(self):
        real, imag, _, magnitude = generate_rayleigh(seed=607)
        self.assertLess(abs(real.mean()), 0.03)
        self.assertLess(abs(imag.mean()), 0.03)
        self.assertAlmostEqual(real.std(), 1 / np.sqrt(2), delta=0.03)
        self.assertAlmostEqual(imag.std(), 1 / np.sqrt(2), delta=0.03)
        self.assertLess(abs(np.corrcoef(real, imag)[0, 1]), 0.05)
        self.assertAlmostEqual(np.mean(magnitude**2), 1, delta=0.05)

    def test_histogram_and_saved_figure(self):
        x, f, g = create_curves()
        *_, magnitude = generate_rayleigh()
        fig, axes, counts, edges = make_figure(x, f, g, magnitude)
        try:
            self.assertEqual(len(fig.axes), 2)
            self.assertEqual(len(axes[0].lines), 2)
            self.assertEqual(counts.shape, (100,))
            self.assertEqual(edges.shape, (101,))
            self.assertEqual(counts.sum(), 10_000)
            with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as folder:
                output = Path(folder) / "test.png"
                fig.savefig(output)
                self.assertGreater(output.stat().st_size, 0)
        finally:
            plt.close(fig)

    def test_invalid_sample_count(self):
        with self.assertRaises(ValueError):
            generate_rayleigh(0)
        with self.assertRaises(ValueError):
            generate_rayleigh(-1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
