"""Lecture 06 / Practice Problem 3: vectorized NumPy and Matplotlib."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def create_curves():
    x = np.linspace(0, 10, 500)
    f = np.sin(3 * x) * np.exp(-x / 2)
    g = np.cos(2 * x) * np.exp(-x / 2)
    return x, f, g


def make_slice_examples(f):
    # Keep the original f intact for statistics and plotting.
    matrix = f[:12].reshape(3, 4).copy()
    initial = matrix.copy()
    transpose = matrix.T.copy()

    view = matrix[-2:, :2]
    view[0, 0] = -1.0
    # A basic slice shares storage: matrix[1, 0] also becomes -1.0.

    independent_matrix = f[:12].reshape(3, 4).copy()
    copied_slice = independent_matrix[-2:, :2].copy()
    copied_slice[0, 0] = -999.0
    # The copied slice owns separate data; independent_matrix is unchanged.
    return initial, transpose, matrix, view, independent_matrix, copied_slice


def solve_system():
    A = np.array([[3.0, 1.0], [1.0, 2.0]])
    b = np.array([9.0, 8.0])
    solution = np.linalg.solve(A, b)
    return A, b, solution


def generate_rayleigh(sample_count=10_000, seed=607):
    if sample_count <= 0:
        raise ValueError("sample_count must be positive")
    # The practice problem explicitly requests np.random.normal or randn.
    np.random.seed(seed)
    sigma = 1 / np.sqrt(2)
    real = np.random.normal(0.0, sigma, sample_count)
    imag = np.random.normal(0.0, sigma, sample_count)
    z = real + 1j * imag
    magnitude = np.abs(z)
    return real, imag, z, magnitude


def make_figure(x, f, g, magnitude):
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    axes[0].plot(x, f, color="royalblue", label=r"$f(x)=\sin(3x)e^{-x/2}$")
    axes[0].plot(x, g, color="darkorange", linestyle="--",
                 label=r"$g(x)=\cos(2x)e^{-x/2}$")
    axes[0].set_title("Damped sinusoidal functions")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("Function value")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    counts, edges, _ = axes[1].hist(magnitude, bins=100, density=False,
                                   color="steelblue", edgecolor="white",
                                   linewidth=0.3)
    axes[1].set_title("Rayleigh-distributed magnitudes")
    axes[1].set_xlabel("Magnitude")
    axes[1].set_ylabel("Number of occurrences")
    axes[1].grid(True, alpha=0.3)
    fig.tight_layout()
    return fig, axes, counts, edges


def main():
    np.set_printoptions(precision=4, suppress=True)
    x, f, g = create_curves()
    peak_index = np.argmax(f)
    print("shape:", f.shape)
    print(f"mean: {f.mean():.6f}")
    print(f"std (ddof=0): {f.std():.6f}")
    print(f"maximum: {f.max():.6f}")
    print("maximum index:", int(peak_index))
    print(f"x at maximum: {x[peak_index]:.6f}")

    initial, transpose, changed, view, independent, copied = make_slice_examples(f)
    print("matrix shape:", initial.shape)
    print(initial)
    print("transpose shape:", transpose.shape)
    print(transpose)
    print("view shape:", view.shape)
    print("matrix[1, 0] after view edit:", changed[1, 0])
    print("view shares memory:", np.shares_memory(changed, view))
    print("copy shares memory:", np.shares_memory(independent, copied))
    print("independent matrix unchanged:", np.array_equal(independent, initial))

    A, b, solution = solve_system()
    print("solution:", solution)
    print("A @ solution:", A @ solution)
    print("system verified:", np.allclose(A @ solution, b))

    real, imag, z, magnitude = generate_rayleigh()
    assert x.shape == f.shape == g.shape == (500,)
    assert real.shape == imag.shape == z.shape == magnitude.shape == (10_000,)
    assert np.all(magnitude >= 0)
    assert np.allclose(magnitude, np.sqrt(real**2 + imag**2))

    fig, axes, counts, edges = make_figure(x, f, g, magnitude)
    assert len(counts) == 100
    assert len(edges) == 101
    assert np.isclose(counts.sum(), magnitude.size)
    print("random array shape:", magnitude.shape)
    print("histogram bins:", len(counts))
    print("histogram total count:", int(counts.sum()))

    output = Path(__file__).resolve().parent / "simulation.png"
    fig.savefig(output, dpi=160, bbox_inches="tight")
    print("Saved:", output.name)
    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
