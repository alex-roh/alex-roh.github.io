---
title: "[ENAI601] 02 — 행렬에서 PSD까지, 사라지는 방향과 복원하는 방법"
description: "직접 쓴 행렬 노트로 복습하는 행·열 관점, rank와 null space, 왼쪽 역행렬·최소제곱·의사역행렬, 고유기저와 PSD. 대칭행렬 조건과 각도 해석까지 연결한다."
date: 2026-10-21
publishedAt: "2026-10-21T00:25:14-04:00"
updatedAt: "2026-10-21T17:36:03Z"
update: 2026-10-21
tags:
  - ENAI601
  - linear-algebra
  - optimization
series: "ENAI601 Numerical Methods"
seriesOrder: 2
---

행렬에 벡터를 곱하면 새로운 벡터가 나온다. 계산은 행과 열을 곱해서 더하면 되지만, 그 결과를 이해하려면 다른 질문이 필요하다. <strong>입력의 어떤 방향이 출력에 남고, 어떤 방향이 사라질까? 출력만 보고 입력을 되찾을 수 있을까?</strong>

이번 글은 직접 작성한 <strong>「2 Matrix」 손글씨 노트 8페이지</strong>를 중심으로, <strong>ENAI601 Module 1 — Linear Algebra 교안</strong>, <strong>9월 9일 수업</strong>, <strong>9월 16일 도입부 복습</strong>을 대조해 정리했다. [앞 글의 벡터·정사영](/enai601-vectors-and-projection/)에서 출발해, 행렬을 선형변환으로 읽고 복원·근사·이차형식으로 이어 간다. 이 글에서는 실수 벡터와 실수 행렬을 사용한다.

왼쪽 역행렬과 Moore–Penrose 의사역행렬, PSD의 대칭성에 관한 설명은 필기에 적어 둔 질문을 풀어 쓴 <strong>보충 학습</strong>이다. 교안에서 직접 다룬 범위와 구분해 표시했다.

| 필기의 출발점 | 이 글에서 확인할 것 |
| --- | --- |
| 1쪽: 행과 열의 관점 | 출력 하나를 계산하는 방법과 가능한 출력 전체의 관계 |
| 2–3쪽: rank·null space·inverse | pivot, 자유변수, 복원 가능성의 연결 |
| 4쪽: left inverse·least squares | 정확한 복원과 가장 가까운 근사의 차이 |
| 5–6쪽: eigenvector·spectral theorem | 고유방향을 검사하는 것으로 모든 방향을 설명하는 이유 |
| 7–8쪽: PSD·PD·outer product·각도 | 대칭성, 영벡터 예외, 행렬식 판정의 한계 |

## 1. 행 관점과 열 관점은 서로 다른 질문에 답한다

필기의 첫 행렬은 출력 두 개와 입력 세 개를 연결한다.

$$
A=\begin{bmatrix}2&-1&5\\0&3&4\end{bmatrix},\qquad
x=\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix},\qquad
Ax=\begin{bmatrix}2x_1-x_2+5x_3\\3x_2+4x_3\end{bmatrix}
$$

### 행 관점: 출력 하나를 어떻게 계산하는가?

첫 번째 출력은 첫 번째 행과 입력 전체의 내적이다. 두 번째 출력은 두 번째 행과 입력 전체의 내적이다.

$$
A=\begin{bmatrix}a_1^T\\a_2^T\end{bmatrix}
\quad\Longrightarrow\quad
Ax=\begin{bmatrix}a_1^Tx\\a_2^Tx\end{bmatrix}
$$

각 행은 하나의 출력을 만들기 위한 가중치 묶음이다. 예를 들어 입력 $x=(1,2,- 1)$이면 첫 번째 출력은 −5, 두 번째 출력은 2다.

### 열 관점: 입력 하나가 출력 전체에 어떻게 기여하는가?

이번에는 입력 성분별로 항을 모아 보자.

$$
Ax=x_1\begin{bmatrix}2\\0\end{bmatrix}
+x_2\begin{bmatrix}-1\\3\end{bmatrix}
+x_3\begin{bmatrix}5\\4\end{bmatrix}
$$

각 열벡터는 해당 입력 성분이 출력 공간에 더하는 방향이다. $x_{1}$, $x_{2}$, $x_{3}$는 그 방향들의 계수다. 일반적으로는

$$
A=[a_1\ a_2\ \cdots\ a_n]
\quad\Longrightarrow\quad Ax=\sum_{j=1}^{n}x_ja_j
$$

이다. 수업에서 강조한 “행렬 곱은 열의 선형결합”이라는 설명이 여기서 나온다. 행 관점은 <strong>출력 성분 하나의 계산</strong>, 열 관점은 <strong>가능한 출력들의 공간</strong>을 이해할 때 유용하다.

### Shape를 먼저 확인한다

$$
A\in\mathbb R^{m\times n},\quad x\in\mathbb R^n,
\quad Ax\in\mathbb R^m,\qquad A:\mathbb R^n\to\mathbb R^m
$$

입력 차원은 열의 개수 $n$이고 출력 차원은 행의 개수 $m$이다. 벡터의 shape를 열로 쓰면 $n\times 1$에서 $m\times 1$로 바뀐다.

행렬 $C$에 대해서도 각 열을 하나씩 입력하면 된다.

$$
A\in\mathbb R^{m\times n},\quad C\in\mathbb R^{n\times p}
\quad\Longrightarrow\quad AC\in\mathbb R^{m\times p},
\qquad (AC)_{ij}=\sum_{k=1}^n a_{ik}c_{kj}
$$

AC는 먼저 $C$, 다음 $A$를 적용하는 합성이다. 일반적으로 AC와 CA는 다르며, 한쪽만 정의될 수도 있다. 행렬 덧셈은 두 행렬의 shape가 같을 때 같은 위치의 원소끼리 더한다.

## 2. 선형변환: 덧셈과 스칼라배를 보존한다

행렬 $A$로 정의한 변환은 선형이다.

$$
A(\alpha x+\beta y)=\alpha Ax+\beta Ay
$$

입력을 먼저 조합하고 변환하든, 각각 변환한 뒤 같은 계수로 조합하든 결과가 같다. 따라서 원점은 반드시 원점으로 간다.

$$
A0=0
$$

고정된 벡터 $b$를 더하는 변환은 $b$가 0이 아닌 경우 affine transformation이다.

$$
T(x)=Ax+b
$$

이 변환은 일반적으로 원점을 보존하지 않는다. 나중에 제약식을 볼 때 선형 부분공간과 원점에서 이동한 집합을 구별하는 데 도움이 된다.

## 3. Range는 가능한 출력 전체다

입력을 자유롭게 바꿀 때 만들 수 있는 출력의 집합이 <strong>range</strong>, 또는 column space다.

$$
\mathcal R(A)=\{Ax:x\in\mathbb R^n\}
=\operatorname{span}\{a_1,\ldots,a_n\}\subseteq\mathbb R^m
$$

필기의 예제처럼 두 열이 종속인 행렬을 생각하자.

$$
B=\begin{bmatrix}1&2\\2&4\end{bmatrix},\qquad
Bx=(x_1+2x_2)\begin{bmatrix}1\\2\end{bmatrix}
$$

두 번째 열은 첫 번째 열의 2배다. 어떤 입력을 넣어도 출력은 (1,2) 방향의 직선에 놓인다.

$$
\mathcal R(B)=\operatorname{span}\left\{\begin{bmatrix}1\\2\end{bmatrix}\right\}
$$

출력 성분은 두 개지만 독립적인 출력 방향은 하나다. 예를 들어 $b=(1,0)$은 이 직선 밖에 있으므로 $Bx=b$를 만족하는 입력이 없다.

range가 부분공간인 이유도 선형성으로 확인할 수 있다. 가능한 두 출력 $Ax$, $Ay$를 선형결합하면 다시 $A(\alpha x+\beta y)$라는 가능한 출력이 된다. 영벡터 A0도 포함한다.

## 4. Null space는 사라지는 입력 전체다

<strong>Null space</strong>, 또는 kernel은 출력이 영벡터가 되는 입력들의 집합이다.

$$
\mathcal N(A)=\{x\in\mathbb R^n:Ax=0\}\subseteq\mathbb R^n
$$

range는 <strong>출력 공간</strong>, null space는 <strong>입력 공간</strong>에 놓인다. $Ax=Ay$일 때 $A(x- y)=0$이므로, null space는 같은 출력을 만드는 입력들의 차이도 설명한다.

위의 $B$에서는 다음이 성립한다.

$$
z=\begin{bmatrix}-2\\1\end{bmatrix},\qquad Bz=0,
\qquad B(x+tz)=Bx\quad(t\in\mathbb R)
$$

원래 입력에 $z$ 방향을 얼마나 더해도 출력이 바뀌지 않는다. 출력만으로 그 방향의 입력 정보를 복원할 수 없다.

### 필기의 2×3 예제: 자유변수로 모든 해를 표현하기

$$
C=\begin{bmatrix}1&0&1\\0&1&1\end{bmatrix},\qquad Cx=0
$$

연립방정식으로 쓰면 $x_{1}+x_{3}=0$, $x_{2}+x_{3}=0$이다. 세 번째 성분을 $t$로 놓으면

$$
x=\begin{bmatrix}-t\\-t\\t\end{bmatrix}
=t\begin{bmatrix}-1\\-1\\1\end{bmatrix},\qquad
\mathcal N(C)=\operatorname{span}\left\{\begin{bmatrix}-1\\-1\\1\end{bmatrix}\right\}
$$

이다. 자유변수가 하나이므로 null space의 차원은 1이다. 여기서 null space는 “입력 벡터 하나”가 아닌 <strong>그런 입력들의 집합</strong>이다. 또한 선형결합해도 여전히 0으로 가므로 부분공간이다.

## 5. Rank는 pivot의 개수이자 독립적인 출력 방향의 수다

rank는 range의 차원이다.

$$
\operatorname{rank}(A)=\dim\mathcal R(A)\le\min(m,n)
$$

열벡터가 $n$개이므로 독립적인 방향은 $n$개를 넘을 수 없고, 그 열들이 사는 출력 공간이 $m$차원이므로 $m$개도 넘을 수 없다. 영행렬의 rank는 0이며, 가능한 최대값 $\min(m,n)$을 가지면 <strong>full rank</strong>다.

필기에서는 행 소거 후 pivot을 세는 계산으로 연결했다.

$$
D=\begin{bmatrix}1&2&1\\1&2&2\end{bmatrix}
\xrightarrow{R_2\leftarrow R_2-R_1}
R=\begin{bmatrix}1&2&1\\0&0&1\end{bmatrix}
$$

첫 번째 열과 세 번째 열에 pivot이 있으므로 rank는 2다. 두 번째 열은 첫 번째 열의 2배다. range의 기저를 원래 행렬에서 고르면

$$
\left\{\begin{bmatrix}1\\1\end{bmatrix},
\begin{bmatrix}1\\2\end{bmatrix}\right\}
$$

가 된다. <strong>행 소거는 pivot 열의 위치를 알려 주지만, 원래 column space의 기저는 원래 행렬의 그 열에서 가져온다.</strong>

행 연산을 가역행렬 $E$의 곱으로 쓰면 $R=ED$다. 따라서 rank와 열들 사이의 선형관계는 보존되지만, column space 자체는 $E$에 의해 바뀔 수 있다. 예를 들어 $B$의 두 번째 행에서 첫 번째 행의 2배를 빼면 range가 (1,2) 방향에서 (1,0) 방향으로 바뀐다. 두 경우 모두 차원은 1이다. 한편 $EDx=0$과 $Dx=0$은 동치이므로 null space는 그대로다.

### Rank–nullity는 입력 변수의 개수를 센다

$$
n=\operatorname{rank}(A)+\dim\mathcal N(A)
$$

피벗 변수의 수와 자유변수의 수를 더하면 전체 입력 변수의 수 $n$이다. $C$는 rank 2와 nullity 1로 3=2+1을 만족한다. 행의 수 $m$을 왼쪽에 넣으면 안 된다.

row rank와 column rank도 같다. 다만 <strong>행들이 사는 공간과 열들이 사는 공간이 같다</strong>는 뜻은 아니다. 행공간은 $\mathbb{R}^{n}$, 열공간은 $\mathbb{R}^{m}$의 부분공간이다.

| 조건 | $Ax=b$에서의 의미 |
| --- | --- |
| full column rank: rank = $n$ | null space가 {0}. 해가 존재하면 유일 |
| full row rank: rank = $m$ | range가 $\mathbb{R}^{m}$ 전체. 모든 $b$에 대해 해가 존재 |
| 정방행렬이고 rank = $n$ | 모든 $b$에 대해 유일한 해. 역행렬 존재 |

## 6. 역행렬과 행렬식: 되돌릴 수 있는 변환인가?

$n\times n$ 정방행렬 $A$에 대해 다음을 만족하는 행렬이 있으면 가역이라고 한다.

$$
AA^{-1}=A^{-1}A=I_n
$$

가역이면 출력 $b$로부터 입력을 되찾을 수 있다.

$$
Ax=b\quad\Longrightarrow\quad x=A^{-1}b
$$

교안의 예제는 다음과 같다.

$$
A=\begin{bmatrix}3&2\\1&4\end{bmatrix},\qquad
A^{-1}=\frac1{10}\begin{bmatrix}4&-2\\-1&3\end{bmatrix}
$$

$2\times 2$ 행렬의 determinant는 다음 식이다.

$$
\det\begin{bmatrix}a&b\\c&d\end{bmatrix}=ad-bc
$$

위의 $A$에서는 12−2=10이다. 정방행렬에서 다음 조건들은 동치다.

$$
\det(A)\ne0
\iff \operatorname{rank}(A)=n
\iff \mathcal N(A)=\{0\}
\iff A^{-1}\text{ exists}
$$

9월 9일 수업에서는 행렬식의 기하학적 의미도 설명했다. 2차원 단위 정사각형에 $A$를 적용하면 두 열벡터가 만드는 평행사변형이 된다. <strong>행렬식의 절댓값은 넓이의 배율</strong>이다. 더 높은 차원에서는 부피의 배율로 확장된다. 부호는 방향의 보존 또는 반전을 나타낸다.

행렬식이 0이면 차원이 눌려 넓이·부피가 0이 된다. 그러면 서로 다른 입력들이 겹쳐져 원래 입력을 유일하게 복원할 수 없다.

### 직사각형 행렬은 왜 따로 생각해야 할까?

필기에서 이어지는 질문은 “정방행렬이 아니어도 입력을 복구할 수 있을까?”다. 여기부터 왼쪽 역행렬·최소제곱 부분은 보충 학습이다.

행이 더 많은 <strong>tall matrix</strong>라도 full column rank이면 서로 다른 입력이 같은 출력으로 겹치지 않는다. 입력을 더 큰 출력 공간 안에 일대일로 넣는 것이다. 다만 출력 공간의 모든 벡터를 만들지는 못한다.

반대로 열이 더 많은 <strong>wide matrix</strong>는 $\operatorname{rank}\le m<n$이므로 nullity가 양수다. 입력 전체를 일대일로 복구할 수 없다. full row rank이면 모든 출력을 만들 수 있고 오른쪽 역행렬은 가질 수 있다.

## 7. 왼쪽 역행렬은 원래 만들어 낸 출력을 정확히 복원한다

full column rank인 $A$에 대해, $A$의 왼쪽에 곱해서 항등행렬을 만드는 $L$을 생각하자.

$$
A\in\mathbb R^{m\times n},\quad L\in\mathbb R^{n\times m},
\qquad LA=I_n
$$

그러면 실제로 $A$가 만든 출력 $y=Ax$에서는 Ly=x다. 이것이 <strong>left inverse(왼쪽 역행렬)</strong>의 복원 의미다.

하지만 임의의 $b$에 대해 $ALb=b$라고 결론 내릴 수는 없다. tall matrix에서 AL은 $m\times m$이고 rank가 최대 $n$이므로, $m>n$이면 $I$ₘ이 될 수 없다.

필기의 간단한 예제를 쓰면

$$
E=\begin{bmatrix}1&0\\0&1\\0&0\end{bmatrix},\qquad
Ex=\begin{bmatrix}x_1\\x_2\\0\end{bmatrix}
$$

이다. 입력은 두 성분인데 출력은 세 성분이다. 출력은 xy평면 안에만 놓이고, 그 평면 안에서는 입력을 잃지 않는다.

### 왼쪽 역행렬은 하나가 아닐 수 있다

임의의 c,d에 대해 다음 행렬은 모두 $E$의 왼쪽 역행렬이다.

$$
L_{c,d}=\begin{bmatrix}1&0&c\\0&1&d\end{bmatrix},
\qquad L_{c,d}E=I_2
$$

원래 $E$가 만드는 출력은 세 번째 성분이 0이므로 c,d가 무엇이든 복원값이 같다. 그러나 $b=(3,5,100)$처럼 range 밖의 벡터에 적용하면 결과가 달라진다.

$$
L_{c,d}b=\begin{bmatrix}3+100c\\5+100d\end{bmatrix}
$$

따라서 <strong>왼쪽 역행렬이라는 조건만으로 임의의 관측값에 대한 최소제곱해가 정해지지는 않는다.</strong> 그 역할을 하는 특별한 선택이 의사역행렬이다.

## 8. 최소제곱과 의사역행렬: 만들 수 없는 출력에 가장 가깝게 가기

현실의 관측값 $b$는 $A$의 range 밖에 있을 수 있다. 그때는 $Ax=b$의 정확한 해를 찾는 대신

$$
\min_x\|Ax-b\|_2^2
$$

를 푼다. 가능한 출력 중 $b$에 가장 가까운 점을 고르는 문제다. [벡터 글의 정사영](/enai601-vectors-and-projection/)이 여기서 다시 등장한다.

$$
\hat b=A\hat x=\operatorname{proj}_{\mathcal R(A)}b,\qquad
r=b-A\hat x,\qquad r\perp\mathcal R(A)
$$

잔차가 $A$의 각 열과 직교해야 하므로

$$
A^T(b-A\hat x)=0\quad\Longleftrightarrow\quad
A^TA\hat x=A^Tb
$$

를 얻는다. 이것이 <strong>normal equations(정규방정식)</strong>다. 잔차를 b−A $x$̂로 정의했으므로 부호도 이 식과 일치한다.

### Full column rank일 때의 공식

$$
x^TA^TAx=\|Ax\|_2^2
$$

$A$가 full column rank이면 0이 아닌 $x$에서 이 값이 양수다. 따라서 $A^{T}A$는 PD이자 가역이다. 이때

$$
A^+=(A^TA)^{-1}A^T,\qquad \hat x=A^+b,\qquad A^+A=I_n
$$

이다. $A^+$는 Moore–Penrose pseudoinverse이며, 이 경우에는 왼쪽 역행렬이기도 하다. 하지만 앞의 모든 $L$이 $A^+$인 것은 아니다.

### 필기의 b=(3,5,100) 예제

![E는 두 입력 좌표를 xy평면으로 보내고 E+는 관측값의 첫 두 좌표를 추출한다. E+E는 항등행렬이고 EE+는 xy평면으로의 정사영이다.](inverse-and-projection.svg)

$E$의 두 열은 이미 정규직교하므로 $E^{T}E=I_{2}$다.

$$
E^+=E^T=\begin{bmatrix}1&0&0\\0&1&0\end{bmatrix}
$$

$$
\hat x=E^+b=\begin{bmatrix}3\\5\end{bmatrix},\qquad
\hat b=E\hat x=\begin{bmatrix}3\\5\\0\end{bmatrix},\qquad
r=\begin{bmatrix}0\\0\\100\end{bmatrix}
$$

$b$ 자체를 복원한 것이 아니라, <strong>xy평면에서 $b$에 가장 가까운 출력의 두 좌표</strong>를 얻었다. 세 번째 성분 100은 $E$의 어떤 입력으로도 만들 수 없는 잔차다.

$$
EE^+=\begin{bmatrix}1&0&0\\0&1&0\\0&0&0\end{bmatrix}\ne I_3
$$

$E^+E$는 입력을 복원하는 $I_{2}$지만, $EE^+$는 출력 공간에서 xy평면으로 정사영하는 행렬이다.

### Rank가 부족해도 의사역행렬은 존재한다

일반 실수 행렬의 Moore–Penrose 의사역행렬은 유일하다. 다음 네 조건을 만족한다.

$$
AA^+A=A,\qquad A^+AA^+=A^+,
\qquad (AA^+)^T=AA^+,\qquad(A^+A)^T=A^+A
$$

rank가 부족하면 $(A^{T}A)^{-1}A^{T}$ 공식은 사용할 수 없다. 대신 SVD로 정의할 수 있다. $A=U\Sigma V^{T}$이면

$$
A^+=V\Sigma^+U^T
$$

이며, $\Sigma^+$는 0이 아닌 특이값만 역수로 바꾸고 전치한 크기에 배치한다. 0인 특이값은 0으로 남긴다.

<strong>$A^+ b$는 최소제곱해들 중 유클리드 노름이 가장 작은 해</strong>다. rank가 부족하면 계수는 여러 개일 수 있어도 정사영된 출력 $AA^+b$는 유일하다. 일반적으로 $A^+ A$는 입력 공간의 row space로의 정사영이며, 원래 입력 전체를 되돌리는 항등행렬은 아니다.

| 연산 | 의미 |
| --- | --- |
| $A^+ b$ | $b$에 대한 최소 노름 최소제곱 계수 |
| $AA^+b$ | $b$를 column space에 정사영한 출력 |
| $A^+ Ax$ | $x$를 row space에 정사영한 입력 성분 |

NumPy의 [`lstsq`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html)는 최소제곱해를, [`pinv`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.pinv.html)는 SVD를 이용한 의사역행렬을 계산한다. 실제 수치 계산에서는 정규방정식의 역행렬을 직접 만들기보다 이러한 수치 선형대수 루틴을 사용한다. 아주 작은 특이값을 0으로 취급할지에 따라 수치적 rank와 결과가 달라질 수 있으므로 임계값도 의미가 있다.

## 9. 고유벡터와 고유값: 특정 방향의 배율

정방행렬 $A$의 <strong>고유벡터</strong>는 다음을 만족하는 0이 아닌 벡터다.

$$
Av=\lambda v,\qquad v\ne0
$$

실수 고유벡터와 실수 고유값을 생각하면, 변환 결과가 원래 벡터와 같은 직선 위에 있다. 양의 고유값은 같은 방향의 배율, 음의 고유값은 방향 반전까지 포함한 배율이고, 0이면 그 방향이 사라진다.

영벡터는 어떤 행렬에서도 위 식을 만족하므로 고유벡터에서 제외한다. 또 일반 실수 행렬의 고유값·고유벡터는 복소수가 될 수도 있다. 이때는 실수 평면의 화살표 그림만으로 해석하기 어렵다.

### 왜 특성방정식이 null space 문제일까?

$$
Av=\lambda v\quad\Longleftrightarrow\quad(A-\lambda I)v=0
$$

고유벡터는 0이 아니므로 $A- \lambda I$의 null space에 영벡터 이외의 벡터가 있어야 한다. 즉 $A- \lambda I$가 특이행렬이어야 한다. 따라서 고유값을 찾는 식은 특성방정식이다.

$$
\det(\lambda I-A)=0
$$

교안의 대칭행렬을 예로 들면

$$
S=\begin{bmatrix}1&-2\\-2&6\end{bmatrix}
$$

이고 특성다항식은

$$
\det(\lambda I-S)=(\lambda-1)(\lambda-6)-4
=\lambda^2-7\lambda+2
$$

이다. 따라서

$$
\lambda_1=\frac{7-\sqrt{41}}2\approx0.2984,\qquad
\lambda_2=\frac{7+\sqrt{41}}2\approx6.7016
$$

두 배율 모두 양수지만 방향별로 크기가 꽤 다르다. 고유값의 합과 곱으로 계산을 검산할 수도 있다. 고유값은 대수적 중복도를 포함해서 센다.

$$
\lambda_1+\lambda_2=7=\operatorname{tr}(S),\qquad
\lambda_1\lambda_2=2=\det(S)
$$

$\lambda$를 찾은 뒤에는 $(A- \lambda I)v=0$을 풀어 고유벡터를 구한다. 고유벡터의 0이 아닌 스칼라배도 같은 고유값의 고유벡터다. 특정 길이 하나로 유일하게 정해지는 것이 아니라, 그 방향을 나타낸다.

특성다항식은 $\det (\lambda I- A)$ 또는 $\det (A- \lambda I)$로 쓸 수 있다. 둘은 $(- 1)^{n}$ 배 차이이므로 근은 같다. 다만 최고차항과 상수항의 부호를 계산할 때는 어느 쪽을 썼는지 일관되게 유지한다.

## 10. 대칭행렬: 직교하는 고유방향으로 좌표를 바꾸기

실수 대칭행렬은 전치해도 같다.

$$
S=S^T
$$

교안에서 강조하는 성질은 다음과 같다.

- 고유값이 모두 실수다.
- 서로 다른 고유값에 대응하는 고유벡터들은 직교한다.
- 고유값이 중복되어도, 각 고유공간에서 적절히 기저를 고르면 전체 공간의 정규직교 고유기저를 만들 수 있다.

마지막 성질까지 포함한 spectral theorem을 행렬로 쓰면 다음과 같다.

$$
S=Q\Lambda Q^T,\qquad Q^TQ=QQ^T=I
$$

$Q$의 열은 정규직교 고유벡터이고, $\Lambda$의 대각선에 대응 고유값들이 놓인다. $Q$의 열들이 전체 공간의 기저이므로 임의의 $x$를 이 좌표로 표현할 수 있다.

$$
c=Q^Tx,\qquad x=Qc
$$

앞 글에서 본 “정규직교기저와 내적하면 계수를 얻는다”는 계산이 그대로 다시 나온다.

중복 고유값에 속하는 벡터들이 <strong>처음부터 모두 직교한다</strong>는 뜻은 아니다. 그 고유공간 안에서 직교기저를 선택할 수 있다는 뜻이다.

### “고유벡터끼리는 직교한다”의 정확한 조건

실수 대칭행렬 $S$에 대해 Sv=λv, Sw=μw라 하자. 그러면

$$
\lambda v^Tw=(Sv)^Tw=v^TSw=\mu v^Tw
$$

이므로 $(\lambda - \mu )v^{T}w=0$이다. $\lambda \ne \mu$이면 $v^{T}w=0$을 얻는다. 대칭성으로 $S^{T}=S$를 쓸 수 있었던 것이 핵심이다.

같은 고유값의 고유벡터들은 임의로 골랐을 때 직교할 필요가 없다. 예를 들어 $I_{2}$에서는 모든 0이 아닌 벡터가 고유값 1의 고유벡터다. 그중 (1,0), (1,1)은 직교하지 않는다. spectral theorem은 이런 고유공간 안에서도 <strong>정규직교기저를 선택할 수 있다</strong>는 정리다.

일반 행렬의 대각화는 고유벡터를 충분히 확보했을 때 $A=P\Lambda P^{-1}$로 쓴다. 실수 대칭행렬에서는 $P$를 정규직교행렬 $Q$로 고를 수 있어 $Q^{-1}=Q^{T}$라는 추가 이점이 생긴다.

## 11. 이차형식: 고유방향별 제곱 크기에 가중치를 주기

필기 5–6페이지에서 PSD를 이해하기 위해 전개한 식이다.

$$
f(x)=x^TSx
$$

$x$는 $n\times 1$, $S$는 $n\times n$이므로 결과는 $1\times 1$ 스칼라다. 행렬 곱 Sx가 벡터를 만들고, 여기에 $x$를 내적한다.

대칭행렬을 고유기저로 분해하면 이 식의 의미가 선명해진다.

$$
\begin{aligned}
x^TSx
&=(Qc)^T(Q\Lambda Q^T)(Qc)\\
&=c^T\Lambda c\\
&=\sum_{i=1}^n\lambda_i c_i^2
\end{aligned}
$$

<strong>정규직교 고유방향별 성분의 제곱에 고유값을 가중치로 곱한 합</strong>이다. 직교하는 좌표를 선택해서 교차항을 없앤 것이다.

원래 좌표에서 $S$의 예제를 전개하면 다음과 같다.

$$
x^TSx=x_1^2-4x_1x_2+6x_2^2
=(x_1-2x_2)^2+2x_2^2
$$

교차항은 있지만 완전제곱으로 정리하면 0이 아닌 $x$에서 항상 양수임을 알 수 있다. 원래 좌표에서 교차항이 있다는 사실만으로 이차형식의 부호를 판단하면 안 된다.

고유벡터 하나에만 $x$를 대입하면 그 방향의 부호를 검사한다. 그러나 PSD 정의는 <strong>모든 $x$</strong>에 관한 것이다. spectral theorem 덕분에 모든 $x$를 이 고유기저의 선형결합으로 표현할 수 있고, 교차항이 사라진 가중 제곱합으로 계산할 수 있다. 그래서 모든 고유값이 0 이상이라는 조건이 모든 $x$에서의 부호 조건으로 확장된다.

## 12. PSD와 PD: 모든 방향에서의 부호 조건

이 수업에서는 실수 대칭행렬에 대해 PSD와 PD를 정의한다.

$$
S\succeq0\quad\Longleftrightarrow\quad
x^TSx\ge0\quad\text{for every }x\in\mathbb R^n
$$

$$
S\succ0\quad\Longleftrightarrow\quad
x^TSx>0\quad\text{for every }x\ne0
$$

첫 번째가 <strong>positive semidefinite(양의 준정부호)</strong>, 두 번째가 <strong>positive definite(양의 정부호)</strong>다. PD에서도 $x=0$을 넣으면 결과는 0이므로 정의에서 제외한다.

고유방향의 제곱합 표현으로부터 판정 조건을 얻는다.

$$
S\succeq0\iff\lambda_i\ge0\ (\text{all }i),\qquad
S\succ0\iff\lambda_i>0\ (\text{all }i)
$$

| 행렬 | 이차형식 | 판정 |
| --- | --- | --- |
| $\operatorname{diag}(3,1)$ | $3x_{1}^{2}+x_{2}^{2}$ | PD |
| $\operatorname{diag}(3,0)$ | $3x_{1}^{2}$ | PSD, PD는 아님 |
| $\operatorname{diag}(1,-1)$ | $x_{1}^{2}- x_{2}^{2}$ | indefinite: 방향에 따라 양수·음수 |

PSD는 <strong>원소들이 모두 0 이상</strong>이라는 조건이 아니다. 위에서 계산한 $S$는 음수 원소 −2를 포함하지만 PD다. 반대로 모든 원소가 양수여도 다음 행렬은 PSD가 아니다.

$$
H=\begin{bmatrix}1&2\\2&1\end{bmatrix},\qquad
\begin{bmatrix}1&-1\end{bmatrix}H\begin{bmatrix}1\\-1\end{bmatrix}=-2
$$

또한 행렬식이 양수라는 조건만으로도 부족하다. 예를 들어 $- I_{2}$는 행렬식이 1이지만 모든 0이 아닌 방향에서 이차형식이 음수다.

PD이면 고유값이 모두 양수이므로 행렬식도 양수이고 역행렬이 존재한다. 반대로 <strong>PSD이면서 가역이면 PD</strong>다. PSD의 고유값들은 0 이상이고, 가역성은 그중 0이 없다는 뜻이기 때문이다. 가역이라는 조건만으로 PD가 되는 것은 아니다.

## 13. 왜 BᵀB와 outer product는 PSD일까?

교안의 마지막 연결은 행렬을 특정 형태로 만들면 PSD임을 바로 보일 수 있다는 것이다. 임의의 실수 행렬 $B$에 대해

$$
x^TB^TBx=(Bx)^T(Bx)=\|Bx\|_2^2\ge0
$$

이므로 $B^{T}B$는 대칭 PSD다. $B$가 <strong>full column rank</strong>이면 0이 아닌 $x$를 영벡터로 보내지 않으므로 PD다. $BB^{T}$도 같은 방식으로 PSD이며, PD가 되려면 $B$가 full row rank여야 한다.

열벡터 $a$로 만든 outer product는 그 특수한 경우다.

$$
aa^T\in\mathbb R^{n\times n},\qquad
x^Taa^Tx=(a^Tx)^2\ge0
$$

내적 $a^{T}a$는 스칼라지만 외적 $aa^T$는 행렬이다. 여기서 outer product는 3차원 cross product와 다른 연산이다.

$a$가 0이 아니면 $aa^T$의 rank는 1이다. $n$이 2 이상이면 $a$에 수직인 0이 아닌 방향이 존재하므로 그 방향에서 이차형식은 0이다. 따라서 보통 PSD이며, $n\ge 2$에서는 PD가 될 수 없다.

필기의 $u=(1,2)$를 실제로 곱하면

$$
uu^T=\begin{bmatrix}1&2\\2&4\end{bmatrix}=B,
\qquad x^TBx=(x_1+2x_2)^2
$$

이다. 처음 range와 null space를 설명할 때 사용한 $B$가 다시 나온다. 가능한 출력은 $u$ 방향 하나뿐이고, $u$에 수직인 (−2,1) 방향은 사라진다. 그 방향에서 이차형식도 0이므로 PSD지만 PD는 아니다. 이 행렬의 고유값은 5와 0이다.

## 14. 왜 PSD를 대칭행렬에 대해 정의할까?

필기 마지막 페이지에 남겨 둔 질문이다. 여기서는 수업의 정의에서 출발해 보충해서 생각해 본다.

임의의 실수 정방행렬 $M$은 대칭 부분 $S$와 반대칭 부분 $K$로 나눌 수 있다.

$$
M=S+K,\qquad S=\frac{M+M^T}{2},\qquad K=\frac{M-M^T}{2},
\qquad S^T=S,\quad K^T=-K
$$

$x^TKx$는 스칼라이므로 전치해도 같아야 한다. 그런데 $K^{T}=- K$를 쓰면 부호가 반대가 된다.

$$
x^TKx=(x^TKx)^T=x^TK^Tx=-x^TKx
\quad\Longrightarrow\quad x^TKx=0
$$

따라서

$$
\boxed{x^TMx=x^T\left(\frac{M+M^T}{2}\right)x=x^TSx}
$$

이다. <strong>이차형식은 반대칭 부분을 보지 못한다.</strong> 이차형식의 부호를 설명하는 대표 행렬을 대칭 부분으로 잡으면 실수 고유값·정규직교 고유기저·곡률을 일관되게 연결할 수 있다. 이것이 이번 수업의 PSD 정의에서 대칭성을 명시하는 이유다.

### 비대칭행렬의 고유값만 검사하면 안 되는 이유

$$
M=\begin{bmatrix}1&4\\0&1\end{bmatrix}
$$

은 두 고유값이 모두 1이다. 하지만 $x=(1,- 1)$을 넣으면

$$
x^TMx=1-4+1=-2
$$

가 된다. “고유값이 모두 양수이므로 PD”라는 판정은 여기서 적용할 수 없다. 앞에서 사용한 판정의 조건은 <strong>실수 대칭행렬</strong>이었다.

반대로 대칭이 아니어도 이차형식이 항상 양수인 경우는 있다.

$$
N=\begin{bmatrix}1&-1\\1&1\end{bmatrix},\qquad
x^TNx=x_1^2+x_2^2
$$

이 경우 대칭 부분이 $I_{2}$다. 이번 글에서는 교안의 관례에 따라 $N$ 자체를 PSD/PD 행렬로 분류하지 않고, <strong>$N$의 이차형식은 $I_{2}$의 이차형식과 같다</strong>고 표현한다. 부호 부등식 자체와 대칭행렬을 대상으로 한 용어의 정의를 구분한다.

## 15. x와 Ax의 각도로 PSD를 읽을 때의 주의점

9월 9일 수업은 이차형식을 $x$와 $Ax$ 사이의 내적으로 해석했다. 필기 7–8페이지도 이 설명을 따라간다.

$$
x^TAx=\langle x,Ax\rangle
=\|x\|_2\|Ax\|_2\cos\theta
$$

$x$와 $Ax$가 모두 0이 아닌 경우, 내적이 음수가 아니면 둘 사이의 각도는 90도를 넘지 않는다. 즉 출력이 입력의 정반대쪽으로 크게 꺾이는 방향이 없다는 직관이다. 행렬이 모든 벡터를 같은 각도로 회전시킨다는 뜻은 아니다.

단, <strong>$Ax=0$이면 각도는 정의되지 않는다.</strong> PSD 행렬은 null space를 가질 수 있으므로 이 예외를 반드시 포함해야 한다. 예를 들어 $\operatorname{diag}(2,0)$에 $x=(0,1)$을 넣으면 $Ax=0$이다. 내적은 0이지만 이를 “각도가 90도”라고 읽으면 안 된다.

실수 대칭 PSD에서는 더 강한 사실도 성립한다.

$$
x^TAx=\sum_i\lambda_i c_i^2=0
\quad\Longleftrightarrow\quad Ax=0
$$

모든 항이 0 이상이므로 합이 0이려면 양의 고유값에 해당하는 계수가 모두 0이어야 한다. 따라서 <strong>$Ax$가 0이 아닌 PSD의 경우에는 실제로 각도가 90도보다 작다.</strong> 수업의 “90도를 넘지 않는다”는 설명은 맞는 필요조건이며, 영벡터 예외를 보완하면 더 정확해진다.

또 이 각도 조건만으로 대칭성을 유도할 수는 없다. 앞 절의 $N$은 비대칭이지만 0이 아닌 모든 $x$에서 $x^TNx>0$이다. 각도는 이차형식의 부호를 설명하는 직관이고, PSD의 전체 정의를 대체하지 않는다.

## 16. 최적화로 이어지는 이차함수

대칭행렬 $S$를 사용한 이차함수에서는

$$
f(x)=x^TSx,\qquad \nabla f(x)=2Sx,\qquad \nabla^2f(x)=2S
$$

이다. $S$가 PSD이면 convex, PD이면 strictly convex다. 이 이차함수에서 PSD는 아래로 휘는 고유방향이 없다는 뜻이고, PD는 모든 0이 아닌 방향에서 양의 곡률을 갖는다는 뜻이다.

최소제곱 목적함수도 같은 구조다.

$$
g(x)=\|Ax-b\|_2^2
=x^TA^TAx-2b^TAx+b^Tb,\qquad
\nabla^2g(x)=2A^TA\succeq0
$$

$A$가 full column rank이면 $A^{T}A$가 PD여서 최소제곱 계수는 유일하다. rank가 부족하면 null space 방향으로 움직여도 $Ax$가 같아서 목적함수 값이 변하지 않는다. <strong>rank, 복원 가능성, 최소제곱해의 유일성, PSD/PD가 같은 구조를 다른 관점에서 설명하고 있다.</strong>

## 17. 계산으로 확인하기

아래 코드는 필기의 null space·왼쪽 역행렬·의사역행렬 예제와 비대칭 반례를 확인한다. NumPy가 설치된 Python에서 독립적으로 실행할 수 있다. 부동소수점 계산이므로 0인지 검사할 때는 근사 비교를 쓴다.

```python
import numpy as np

np.set_printoptions(precision=4, suppress=True)

# 1. Full row rank지만 입력 방향 하나를 잃는 2x3 행렬
C = np.array([[1., 0., 1.], [0., 1., 1.]])
z = np.array([-1., -1., 1.])
print("C rank / nullity:", np.linalg.matrix_rank(C),
      C.shape[1] - np.linalg.matrix_rank(C))
print("C @ z:", C @ z)
assert np.allclose(C @ z, 0)

# 2. 정확한 복원과 range 밖의 최소제곱 근사
E = np.array([[1., 0.], [0., 1.], [0., 0.]])
b = np.array([3., 5., 100.])
E_plus = np.linalg.pinv(E)
x_hat, _, _, _ = np.linalg.lstsq(E, b, rcond=None)
p = E @ x_hat
r = b - p
print("x_hat:", x_hat)
print("projection:", p)
print("residual:", r)
print("E+ E is identity:", np.allclose(E_plus @ E, np.eye(2)))
print("E E+ is identity:", np.allclose(E @ E_plus, np.eye(3)))
assert np.allclose(E.T @ r, 0)
assert np.allclose(E_plus @ b, x_hat)

# 3. 다른 왼쪽 역행렬은 range 밖의 b에서 결과가 다르다
L = np.array([[1., 0., 1.], [0., 1., 0.]])
assert np.allclose(L @ E, np.eye(2))
print("another left inverse applied to b:", L @ b)

# 4. Outer product는 PSD이며, 직교하는 입력 방향을 지운다
u = np.array([1., 2.])
B = np.outer(u, u)
print("outer-product eigenvalues:", np.linalg.eigvalsh(B))
assert np.allclose(B @ np.array([-2., 1.]), 0)

# 5. 비대칭행렬에서는 양의 고유값만으로 충분하지 않다
M = np.array([[1., 4.], [0., 1.]])
x = np.array([1., -1.])
print("nonsymmetric eigenvalues:", np.linalg.eigvals(M))
print("x^T M x:", x @ M @ x)
assert np.isclose(x @ M @ x, -2)
```

출력은 다음과 같다. 매우 작은 반올림 오차의 부호 표시는 환경에 따라 달라질 수 있다.

```text
C rank / nullity: 2 1
C @ z: [0. 0.]
x_hat: [3. 5.]
projection: [3. 5. 0.]
residual: [  0.   0. 100.]
E+ E is identity: True
E E+ is identity: False
another left inverse applied to b: [103.   5.]
outer-product eigenvalues: [0. 5.]
nonsymmetric eigenvalues: [1. 1.]
x^T M x: -2.0
```

## 18. 다시 풀어 볼 질문

1. 행 소거 후의 열벡터를 그대로 원래 column space의 기저로 써도 될까?
2. $3\times 2$ full column rank 행렬은 모든 3차원 출력을 만들 수 있을까?
3. $LA=I$를 만족하는 $L$은 항상 Moore–Penrose 의사역행렬일까?
4. 최소제곱 계수 $x$̂가 여러 개이면 정사영된 출력도 여러 개일까?
5. 대칭 PSD 행렬에서 $x^{T}Ax=0$이면 $x$가 반드시 영벡터일까?
6. 고유값이 모두 1인 비대칭행렬은 반드시 이차형식이 양수일까?

<strong>해설:</strong> 1. 일반적으로 안 된다. pivot 위치를 찾고 원래 행렬의 해당 열을 선택한다. 2. 안 된다. range는 3차원 공간 안의 2차원 부분공간이다. 3. 아니다. 왼쪽 역행렬은 여러 개일 수 있다. 4. 아니다. 출력은 유일하며 계수 차이가 null space에 있다. 5. 아니다. $x$가 null space에 있을 수 있다. 다만 $Ax=0$은 성립한다. 6. 아니다. 본문의 $M$과 $x=(1,- 1)$이 반례다.

## 참고한 자료와 보충 설명의 범위

- 개인 손글씨 노트 <strong>「2 Matrix」 1–8페이지</strong>: 행·열 해석, pivot과 rank, null space 예제, 왼쪽 역행렬·최소제곱·의사역행렬, PSD·PD, 마지막의 대칭성과 각도 질문.
- ENAI601, <strong>Module 1 — Linear Algebra</strong> 접근성 버전 교안: Matrices부터 Range and Nullspace, Inverse, Determinant, Eigenvalues & Eigenvectors, Symmetric Matrices, PSD/PD, outer product까지.
- <strong>2026-09-09 수업</strong>: 열의 선형결합, rank–nullity, 행렬식·고유값, 대칭행렬과 PSD/PD, $x$와 $Ax$의 내적을 통한 기하학적 해석.
- <strong>2026-09-16 수업 도입부</strong>: 행렬 연산·range·null space·역행렬·PD의 복습.
- [NumPy `lstsq` 공식 문서](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html), [NumPy `pinv` 공식 문서](https://numpy.org/doc/stable/reference/generated/numpy.linalg.pinv.html): 보충 계산 예제의 API와 최소 노름 해·SVD 계산 방식 확인.

왼쪽 역행렬의 비유일성 반례, Moore–Penrose 조건, 이차형식의 대칭 부분, 각도의 영벡터 예외와 엄밀한 조건, 최적화 연결은 필기의 질문을 바탕으로 보강했다. 예제의 차원·기호는 교안과 직접 계산으로 확인했다. 그림은 예제의 좌표와 행렬에서 새로 작성했으며, 필기·강의자료 원문을 첨부하지 않았다.
