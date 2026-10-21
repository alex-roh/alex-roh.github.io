"""행렬 수치 결과와 두 그림의 실제 데이터·막대 속성을 검사한다."""
from pathlib import Path
import tempfile
import unittest
import matplotlib
matplotlib.use("Agg")  # 자동 테스트에서만 창을 띄우지 않는다.
import matplotlib.pyplot as plt
import numpy as np
import matrix_diagnostics as model


class MatrixTests(unittest.TestCase):
    def test_array_types_metadata_and_arange(self):
        points, floating, evens = model.create_arrays()
        self.assertEqual(points.ndim, 2)
        self.assertEqual(points.size, 10)
        self.assertEqual(points.shape, (5, 2))
        self.assertTrue(np.issubdtype(points.dtype, np.integer))
        self.assertTrue(np.issubdtype(floating.dtype, np.floating))
        self.assertFalse(np.shares_memory(points, floating))
        np.testing.assert_array_equal(evens, [0, 2, 4, 6, 8])

    def test_transform_values_and_row_order(self):
        _, points, _ = model.create_arrays()
        _, transformed, *_ = model.transform_points(points)
        self.assertEqual(transformed.shape, (5, 2))
        np.testing.assert_allclose(transformed, [[2, 1], [1, 2], [3, 3], [5, 4], [-1, 1]])

    def test_inverse_identity_and_recovery(self):
        _, points, _ = model.create_arrays()
        A, _, det, inverse, identity, recovered = model.transform_points(points)
        self.assertAlmostEqual(det, 3)
        np.testing.assert_allclose(A @ inverse, identity, atol=1e-12)
        np.testing.assert_allclose(recovered, points, atol=1e-12)

    def test_scatter_data_labels_and_no_lines(self):
        _, points, _ = model.create_arrays()
        _, transformed, *_ = model.transform_points(points)
        fig = model.make_scatter(points, transformed)
        try:
            ax = fig.axes[0]
            self.assertEqual(len(ax.collections), 2)
            self.assertEqual(len(ax.lines), 0)
            np.testing.assert_allclose(ax.collections[0].get_offsets(), points)
            np.testing.assert_allclose(ax.collections[1].get_offsets(), transformed)
            self.assertTrue(ax.get_title() and ax.get_xlabel() and ax.get_ylabel())
            self.assertIsNotNone(ax.get_legend())
        finally:
            plt.close(fig)

    def test_bar_heights_width_edges_and_ticks(self):
        fig = model.make_bar()
        try:
            ax = fig.axes[0]
            self.assertEqual([bar.get_height() for bar in ax.patches], [12, 7, 15])
            np.testing.assert_allclose([bar.get_width() for bar in ax.patches], 0.35)
            np.testing.assert_allclose([bar.get_x()+bar.get_width()/2 for bar in ax.patches], [0, 1, 2])
            for bar in ax.patches:
                np.testing.assert_allclose(bar.get_edgecolor(), [0, 0, 0, 1])
            self.assertEqual([tick.get_text() for tick in ax.get_xticklabels()], ["Low", "Medium", "High"])
        finally:
            plt.close(fig)

    def test_separate_figures_save_png_and_preserve_original(self):
        points, floating, _ = model.create_arrays()
        before = points.copy()
        _, transformed, *_ = model.transform_points(floating)
        scatter, bar = model.make_scatter(floating, transformed), model.make_bar()
        try:
            self.assertNotEqual(scatter.number, bar.number)
            with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as folder:
                for figure, name in [(scatter, "points_scatter.png"), (bar, "categories_bar.png")]:
                    output = Path(folder) / name
                    figure.savefig(output)
                    self.assertTrue(output.read_bytes().startswith(b"\x89PNG"))
            np.testing.assert_array_equal(points, before)
        finally:
            plt.close(scatter)
            plt.close(bar)


if __name__ == "__main__":
    unittest.main(verbosity=2)
