"""예상문제 3: 벡터화 계산, 배열 복사, 연립방정식, 난수와 그래프."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def create_curves():
    # 끝점 0과 10을 모두 포함하는 부동소수점 값 500개.
    x = np.linspace(0, 10, 500)
    # 배열 전체에 함수를 적용한다. 원소별 Python for문은 사용하지 않는다.
    f = np.sin(3 * x) * np.exp(-x / 2)
    g = np.cos(2 * x) * np.exp(-x / 2)
    return x, f, g


def make_slice_examples(f):
    # reshape만 하면 f와 메모리를 공유할 수 있다.
    # f의 통계·그래프를 오염시키지 않도록 실습용 행렬을 먼저 독립 복사한다.
    matrix = f[:12].reshape(3, 4).copy()
    initial = matrix.copy()       # 변경 전 출력용 스냅샷
    transpose = matrix.T.copy()   # 전치 결과도 변경 전 상태를 보존

    view = matrix[-2:, :2]        # 마지막 두 행, 처음 두 열: shape (2, 2)
    view[0, 0] = -1.0
    # 기본 슬라이스는 메모리를 공유하므로 matrix[1, 0]도 -1.0이 된다.

    independent = f[:12].reshape(3, 4).copy()
    copied = independent[-2:, :2].copy()
    copied[0, 0] = -999.0
    # .copy() 결과는 별도 데이터를 가지므로 independent는 변하지 않는다.
    return initial, transpose, matrix, view, independent, copied


def solve_system():
    A = np.array([[3.0, 1.0], [1.0, 2.0]])
    b = np.array([9.0, 8.0])
    solution = np.linalg.solve(A, b)  # 해를 직접 계산; [2, 3]을 대입하지 않음
    return A, b, solution


def generate_rayleigh(sample_count=10_000, seed=607):
    # 10_000은 숫자를 읽기 쉽게 쓴 정수 10000과 같다.
    if sample_count <= 0:
        raise ValueError("표본 수는 양수여야 함")
    np.random.seed(seed)  # 재현을 위해 두 난수 배열 생성 전에 한 번만 설정
    sigma = 1 / np.sqrt(2)  # scale에 넣는 값은 분산이 아니라 표준편차
    real = np.random.normal(0.0, sigma, sample_count)
    imag = np.random.normal(0.0, sigma, sample_count)
    z = real + 1j * imag    # 원소별 복소수 생성; j라는 별도 변수를 만들지 않음
    magnitude = np.abs(z)   # sqrt(real**2 + imag**2)와 같은 원소별 크기
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

    # 요구사항은 도수(count). density=True나 정규화 weights를 쓰지 않는다.
    counts, edges, _ = axes[1].hist(
        magnitude, bins=100, density=False,
        color="steelblue", edgecolor="white", linewidth=0.3
    )
    axes[1].set_title("Rayleigh-distributed magnitudes")
    axes[1].set_xlabel("Magnitude")
    axes[1].set_ylabel("Number of occurrences")
    axes[1].grid(True, alpha=0.3)
    fig.tight_layout()  # 제목과 축 이름의 겹침 조정
    return fig, axes, counts, edges


def main():
    np.set_printoptions(precision=4, suppress=True)
    x, f, g = create_curves()
    peak_index = np.argmax(f)  # 최댓값 자체가 아니라 위치
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
    print("view 변경 후 matrix[1, 0]:", changed[1, 0])
    print("view 메모리 공유:", np.shares_memory(changed, view))
    print("copy 메모리 공유:", np.shares_memory(independent, copied))
    print("copy 변경 후 원본 유지:", np.array_equal(independent, initial))

    A, b, solution = solve_system()
    print("solution:", solution)
    print("A @ solution:", A @ solution)
    print("system verified:", np.allclose(A @ solution, b))

    real, imag, z, magnitude = generate_rayleigh()
    # shape가 잘못된 상태로 그래프를 그리지 않도록 수치 결과를 검사한다.
    assert x.shape == f.shape == g.shape == (500,)
    assert real.shape == imag.shape == z.shape == magnitude.shape == (10_000,)
    assert np.all(magnitude >= 0)
    assert np.allclose(magnitude, np.sqrt(real**2 + imag**2))
    assert np.allclose(A @ solution, b)

    fig, axes, counts, edges = make_figure(x, f, g, magnitude)
    assert len(counts) == 100 and len(edges) == 101
    assert np.isclose(counts.sum(), magnitude.size)
    print("random array shape:", magnitude.shape)
    print("histogram bins:", len(counts))
    print("histogram total count:", int(counts.sum()))

    output = Path(__file__).resolve().parent / "simulation.png"
    fig.savefig(output, dpi=160, bbox_inches="tight")  # show보다 먼저 저장
    print("Saved:", output.name)
    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
