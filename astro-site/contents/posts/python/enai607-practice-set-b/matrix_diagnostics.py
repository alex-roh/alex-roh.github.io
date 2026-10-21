"""문제 6: 행별 2차원 점의 변환·복원, 산점도와 범주별 막대그래프."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def create_arrays():
    # [P6.1-A] 한 행이 점 하나, 열 0이 x, 열 1이 y다. 지정 순서를 유지한다.
    points = np.array([[1, 0], [0, 1], [1, 1], [2, 1], [-1, 1]], dtype=int)
    # [P6.1-B] 변환 결과를 별도 변수에 받아 원래 정수 배열을 유지한다.
    points_float = points.astype(float)
    # [P6.1-C] 시작 0, 끝 10 제외, 간격 2. 직접 [0,2,4,6,8]을 쓰지 않는다.
    even_values = np.arange(0, 10, 2)
    return points, points_float, even_values


def transform_points(points_float):
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    # [P6.2-A] (5,2) @ (2,2) -> (5,2). 각 행의 점을 같은 순서로 변환.
    transformed = points_float @ A
    determinant = np.linalg.det(A)  # 결과 3을 코드에 직접 대입하지 않는다.
    inverse_A = np.linalg.inv(A)
    identity = np.eye(2)
    # [P6.2-B] 행벡터에 A를 오른쪽에서 곱했으므로 역행렬도 오른쪽에 곱한다.
    recovered = transformed @ inverse_A
    return A, transformed, determinant, inverse_A, identity, recovered


def make_scatter(points_float, transformed):
    fig = plt.figure(figsize=(7, 6))
    # [P6.3-A] [:,0]은 모든 점의 x, [:,1]은 모든 점의 y를 꺼낸다.
    plt.scatter(points_float[:, 0], points_float[:, 1], color="royalblue",
                marker="o", s=90, label="Original")
    plt.scatter(transformed[:, 0], transformed[:, 1], color="darkorange",
                marker="x", s=110, linewidths=2, label="Transformed")
    plt.title("Original and transformed points")
    plt.xlabel("x coordinate")
    plt.ylabel("y coordinate")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis("equal")  # x와 y의 한 단위를 같은 길이로 보여 준다.
    fig.tight_layout()
    return fig


def make_bar():
    # [P6.4-A] scatter와 다른 figure를 만들어 그래프가 섞이지 않게 한다.
    fig = plt.figure(figsize=(7, 5))
    category_labels = ["Low", "Medium", "High"]
    category_counts = [12, 7, 15]
    positions = np.arange(3)  # 막대의 중심 위치: 0, 1, 2
    # [P6.4-B] 이미 센 빈도를 높이로 쓰므로 hist가 아니라 bar다.
    plt.bar(positions, category_counts, width=0.35, edgecolor="black", color="steelblue")
    plt.xticks(positions, category_labels)
    plt.title("Category counts")
    plt.xlabel("Category")
    plt.ylabel("Count")
    fig.tight_layout()
    return fig


def main():
    np.set_printoptions(precision=4, suppress=True)
    points, points_float, even_values = create_arrays()
    print("ndim:", points.ndim)
    print("size:", points.size)
    print("shape:", points.shape)
    print("original dtype:", points.dtype)
    print("converted dtype:", points_float.dtype)
    print("arange:", even_values)

    A, transformed, determinant, inverse_A, identity, recovered = transform_points(points_float)
    print("transformed:")
    print(transformed)
    print("transformed shape:", transformed.shape)
    print(f"determinant: {determinant:.4f}")
    print("inverse_A:")
    print(inverse_A)
    # [P6.2-C] ==가 아니라 부동소수점 허용 오차를 고려해 수치적으로 비교한다.
    print("A @ inverse_A is identity:", np.allclose(A @ inverse_A, identity))
    print("recovered agrees with original:", np.allclose(recovered, points_float))

    folder = Path(__file__).resolve().parent
    scatter = make_scatter(points_float, transformed)
    scatter.savefig(folder / "points_scatter.png", dpi=160, bbox_inches="tight")
    plt.show()  # [P6.3-B] 첫 번째 그림도 먼저 저장한 뒤 보여 준다.
    plt.close(scatter)

    bar = make_bar()
    bar.savefig(folder / "categories_bar.png", dpi=160, bbox_inches="tight")
    plt.show()  # [P6.4-C] 두 번째 그림도 저장 후 표시한다.
    plt.close(bar)
    print("Saved: points_scatter.png, categories_bar.png")


if __name__ == "__main__":
    main()
