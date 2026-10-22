---
title: "[ENAI601] 03 — Convex Set, 제약조건을 공간의 모양으로 읽기"
description: "열린집합·닫힌집합·compact부터 affine/convex/conic combination과 hull, hyperplane·halfspace·polyhedron, affine image·preimage, supporting hyperplane까지 예제와 증명으로 복습한다."
date: 2026-10-21
publishedAt: "2026-10-21T01:28:45-04:00"
updatedAt: "2026-10-22T04:29:19+00:00"
tags:
  - ENAI601
  - convex-sets
  - optimization
series: "ENAI601 Numerical Methods"
seriesOrder: 3
---

최적화는 가능한 선택 중에서 가장 좋은 $x$를 찾는 문제다. 여기에는 두 질문이 함께 있다. <strong>무엇을 좋다고 평가할까? 어떤 $x$를 선택해도 될까?</strong> 첫 질문은 objective function, 두 번째 질문은 feasible set이 담당한다.

[앞 글의 행렬](/enai601-matrices-and-psd/)이 벡터를 변환하는 규칙이었다면, 이번에는 조건을 만족하는 벡터들을 모아 <strong>공간의 모양</strong>으로 읽는다. 여러 제약조건이 만드는 영역은 어떤 집합이고, 그 안의 두 점을 섞어도 여전히 조건을 만족할까? 이것이 convex set을 공부하는 출발점이다.

이 글은 개인 손글씨 노트 <strong>「3 Convex Set」의 내용이 있는 1–6페이지</strong>, <strong>ENAI601 Module 2 — Convex Sets 교안</strong>, <strong>2026년 9월 16일 수업</strong>을 대조해 작성했다. 원본을 펼치지 않고도 복습할 수 있도록 정의·예제·반례·짧은 증명을 본문에 담았다. Supporting hyperplane은 교안과 수업에서 보충했고, 최소값 존재 조건과 거리 공식의 유도 등은 개념을 연결하기 위한 보충 설명이다.

이 글의 공간은 유한차원 실수 공간 $\mathbb{R}^{n}$이다. interior·boundary·open·closed는 별도로 말하지 않으면 <strong>주변 공간 $\mathbb{R}^{n}$을 기준</strong>으로 한다. 내적과 거리는 표준 내적과 유클리드 노름을 사용한다.

| 먼저 붙잡을 질문 | 이어지는 개념 |
| --- | --- |
| 집합에 경계가 포함되는가? 끝없이 뻗는가? | open, closed, bounded, compact |
| 점들을 어떤 계수로 섞는가? | affine, convex, conic combination과 hull |
| 등식과 부등식은 어떤 모양을 만드는가? | hyperplane, halfspace, polyhedron, norm ball |
| 집합을 바꾸거나 제약을 결합해도 볼록한가? | intersection, affine image와 preimage |
| 경계를 한쪽에서 받치는 평면은 무엇인가? | supporting hyperplane과 최적점 |

## 1. Objective function과 feasible set은 따로 확인한다

다음은 최적화 문제의 기본 형태다.

$$
\underset{x\in C}{\operatorname{minimize}}\ f_0(x)
$$

$f_{0}(x)$는 평가할 값이고 $C$는 선택이 허용되는 $x$의 집합이다. 예를 들어

$$
C=\{(x_1,x_2):x_1\ge0,\ x_2\ge0,\ x_1+x_2\le6\}
$$

이면 두 변수는 음수가 될 수 없고 합이 6을 넘을 수 없다. 제약 세 개를 동시에 만족하는 점들이 feasible set을 만든다.

이 집합에서 $f_{0}(x)=x_{1}^{2}+x_{2}^{2}$를 최소화하는 문제와 $f_{0}(x)=- x_{1}- x_{2}$를 최소화하는 문제는 <strong>같은 feasible set, 다른 objective function</strong>을 갖는다. 첫 번째는 원점에서 최소가 되고, 두 번째는 $x_{1}+x_{2}=6$인 경계 선분 전체에서 같은 최소값 −6을 갖는다.

따라서 feasible set의 볼록성만으로 최적점의 유일성이나 목적함수의 볼록성까지 결론 내릴 수 없다. 수업에서 같은 단어 convex를 집합과 함수에 각각 사용한다고 주의를 준 이유다. 이 글에서는 우선 <strong>집합의 볼록성</strong>을 다룬다.

## 2. Open set: 모든 점 주변에 작은 여유가 있다

중심 $x$와 반지름 $\varepsilon >0$인 열린 공을 다음과 같이 쓰자.

$$
B_\varepsilon(x)=\{z\in\mathbb R^n:\|z-x\|_2<\varepsilon\}
$$

집합 $C$가 <strong>open(열린집합)</strong>이라는 것은 다음 뜻이다.

$$
\forall x\in C,\quad\exists\varepsilon>0
\quad\text{such that}\quad B_\varepsilon(x)\subseteq C
$$

집합 안의 점을 <strong>어느 것으로 골라도</strong>, 그 점을 중심으로 충분히 작은 공을 그려 집합 안에 넣을 수 있어야 한다. 반지름 $\varepsilon$는 점마다 달라도 된다. 모든 점에서 같은 $\varepsilon$ 하나를 쓸 필요는 없다.

1차원 구간 $C=(0,1)$에서 $x=0.5$라면 $\varepsilon =0.1$을 선택할 수 있다. $x=0.001$처럼 끝에 가까운 점에서도 더 작은 $\varepsilon =0.0005$를 쓰면 된다. 끝점 0과 1은 집합에 없으므로 그 점들에서 공을 넣을 필요는 없다.

반대로 $[0,1]$에서는 $x=0$ 주변의 어떤 양의 반지름 구간도 음수를 포함한다. 따라서 $\mathbb R$에서 열린집합이 아니다.

교안은 작은 공을 닫힌 공, 즉 거리 $\le \varepsilon$로 써서 열린집합을 정의한다. 여기서는 표준적인 열린 공 표기를 사용했다. <strong>적당한 양의 반지름이 존재한다</strong>는 조건에서는 두 방식이 동치다. 열린 공이 들어가면 반지름을 절반으로 줄인 닫힌 공도 들어간다.

## 3. Closed set: 극한으로 도달하는 점을 빠뜨리지 않는다

집합 $C$가 <strong>closed(닫힌집합)</strong>라는 정의는 여집합이 열린집합이라는 것이다.

$$
C\text{ is closed}\quad\Longleftrightarrow\quad
\mathbb R^n\setminus C\text{ is open}
$$

$\mathbb{R}^{n}$에서는 수열로도 이해할 수 있다. $C$ 안의 점들로 이루어진 수열이 어떤 점으로 수렴하면 그 극한점도 $C$ 안에 있어야 한다.

$$
x_k\in C,\quad x_k\to x\quad\Longrightarrow\quad x\in C
$$

$[0,1]$은 이 성질을 만족한다. $(0,1)$은 $x_{k}=1/(k+1)$이 0으로 수렴하지만 0을 포함하지 않으므로 닫혀 있지 않다.

### Open과 closed는 양자택일이 아니다

| $\mathbb R$의 부분집합 | open | closed | 이유 |
| --- | --- | --- | --- |
| $(0,1)$ | O | X | 모든 점에 작은 여유가 있고, 끝점 극한은 빠짐 |
| $[0,1]$ | X | O | 끝점은 내부점이 아니지만 극한을 모두 포함 |
| [0,1) | X | X | 0 때문에 open이 아니고 1을 빠뜨려 closed도 아님 |
| $\mathbb R$, $\varnothing$ | O | O | 둘 다 open이고 closed |

수업에서는 단위원 내부와 원 둘레를 구별했다. <strong>원 둘레만 있는 집합도 closed</strong>다. 원 내부를 채워야 closed가 되는 것이 아니다. closed는 집합의 두께나 구멍의 유무를 뜻하지 않는다.

## 4. Interior, closure, boundary를 한 예제로 정리하기

세 개념은 “완전히 안쪽”, “극한까지 포함한 전체”, “안과 밖이 만나는 부분”을 구분한다.

### Interior: 작은 공을 넣을 수 있는 점들

$$
\operatorname{int}C
=\{x\in C:\exists\varepsilon>0,\ B_\varepsilon(x)\subseteq C\}
$$

### Closure: C 안의 점들로 임의로 가깝게 접근할 수 있는 점들

$$
\operatorname{cl}C
=\{x:\text{there exists }x_k\in C\text{ with }x_k\to x\}
$$

상수 수열도 허용하므로 $C$ 자체도 closure에 들어간다. “빠진 경계를 채운다”는 직관과 연결된다.

### Boundary: 작은 공마다 안과 밖을 모두 만나는 점들

$$
\partial C=\operatorname{cl}C\setminus\operatorname{int}C
$$

경계점은 원래 집합에 포함될 수도, 포함되지 않을 수도 있다.

| $C$ | int $C$ | cl $C$ | $\partial C$ |
| --- | --- | --- | --- |
| $(0,1)$ | $(0,1)$ | $[0,1]$ | {0,1} |
| $[0,1]$ | $(0,1)$ | $[0,1]$ | {0,1} |
| [0,1) | $(0,1)$ | $[0,1]$ | {0,1} |

세 집합의 interior·closure·boundary가 같아도 원래 집합은 다르다. 경계의 어느 점을 포함하는지는 원래 집합의 정의를 읽어야 한다.

$$
C\text{ open}\iff C=\operatorname{int}C,\qquad
C\text{ closed}\iff C=\operatorname{cl}C
$$

### 낮은 차원의 집합에서는 “안쪽”의 기준이 중요하다

$\mathbb{R}^{2}$ 안의 선분 $L=\{(t,0):0\le t\le1\}$을 생각하자. 중간점 $(0.5,0)$ 주변에 아무리 작은 <strong>2차원 공</strong>을 그려도 선분 밖으로 나간다. 따라서 $\mathbb{R}^{2}$ 기준 int $L=\varnothing$다. $L$은 닫혀 있으므로 $\partial L=L$이다.

그렇다고 선분이 볼록하지 않다는 뜻은 아니다. 선분이 놓인 직선 안에서만 여유를 따지는 <strong>relative interior(상대적 내부)</strong>는 $\{(t,0):0<t<1\}$이다. 일반적으로 상대적 내부는 그 집합의 affine hull을 주변 공간으로 삼아 내부를 구한다. 상대적 내부는 보충 개념이며, 이후 “차원”과 “경계”를 혼동하지 않기 위해 함께 기억해 두면 좋다.

## 5. Bounded와 compact: 최솟값을 실제로 얻을 수 있을까?

$C$가 <strong>bounded(유계)</strong>라는 것은 어떤 유한한 반지름의 공 안에 $C$ 전체를 넣을 수 있다는 뜻이다.

$$
\exists R<\infty\quad\text{such that}\quad
C\subseteq\{x:\|x\|_2\le R\}
$$

중심이 다른 공으로 정의해도 동치다. 모든 방향으로 무한히 뻗지 않는다고 이해할 수 있다.

$\mathbb{R}^{n}$에서는 <strong>compact ⇔ closed이고 bounded</strong>가 성립한다. 이 동치는 유한차원 유클리드 공간을 전제로 한다.

| 집합 | closed | bounded | compact |
| --- | --- | --- | --- |
| $(0,1)$ | X | O | X |
| $[0,1]$ | O | O | O |
| [0,∞) | O | X | X |
| 단위원 둘레 | O | O | O |
| 원점을 지나는 전체 직선 | O | X | X |

### 보충: continuous + nonempty compact가 주는 보장

<strong>연속인 실수값 함수는 비어 있지 않은 compact 집합에서 최솟값과 최댓값을 실제로 갖는다.</strong> 점들을 더 좋은 값으로 계속 접근시키는 것과, 그 값을 달성하는 점이 존재하는 것은 다르다.

예를 들어 $f(x)=x$를 $(0,1)$에서 최소화하면 0에 한없이 가까워질 수 있지만 $x=0$은 허용되지 않는다. infimum은 0이지만 minimum은 없다. 집합을 $[0,1]$로 바꾸면 $x=0$에서 최소값 0을 얻는다.

closed만으로도 부족하다. [0,∞)에서 $f(x)=e^{-x}$는 0으로 가까워지지만 어떤 유한한 $x$에서도 0이 되지 않는다.

반대로 compact가 최솟값 존재의 필요조건인 것은 아니다. $f(x)=x^{2}$는 compact가 아닌 $\mathbb R$ 전체에서도 $x=0$에서 최소값을 갖는다. 또 compact하다고 최적점이 유일한 것도 아니다. 상수함수는 집합의 모든 점에서 같은 값을 갖는다.

## 6. Affine combination: 점 하나에서 출발해 방향으로 이동하기

선형결합에 <strong>계수의 합이 1</strong>이라는 조건을 붙이면 affine combination이다.

$$
x=\sum_{i=1}^k\theta_i x_i,\qquad
\sum_{i=1}^k\theta_i=1,\qquad\theta_i\in\mathbb R
$$

계수는 음수여도 된다. 두 점에서는 다음과 같이 쓸 수 있다.

$$
x=(1-t)x_1+tx_2=x_1+t(x_2-x_1),\qquad t\in\mathbb R
$$

<strong>기준점 $x_{1}$에서 방향 $x_{2}- x_{1}$로 $t$배 이동한다</strong>는 뜻이다. 두 점이 다르면 $t$를 모든 실수로 바꾸어 두 점을 지나는 직선 전체를 얻는다.

예를 들어 $x_{1}=(1,1)$, $x_{2}=(3,2)$이면

$$
x=(1+2t,\ 1+t)
$$

이다. $t=0$이면 (1,1), $t=1$이면 (3,2), $t=1/2$이면 중간점 (2,1.5), $t=2$이면 선분 밖의 (5,3)을 얻는다.

계수 합 1의 의미는 좌표 원점을 옮길 때도 드러난다. 모든 점에 같은 벡터 $c$를 더하면

$$
\sum_i\theta_i(x_i+c)
=\sum_i\theta_i x_i+c
$$

이다. 각 점을 $c$만큼 옮긴 조합은 원래 조합을 $c$만큼 옮긴 것과 같다. affine geometry가 원점을 꼭 지나야 할 필요가 없는 이유다.

세 점도 기준점을 분리하면 이해하기 쉽다.

$$
x=x_1+\theta_2(x_2-x_1)+\theta_3(x_3-x_1)
$$

세 점이 한 직선에 있지 않으면 두 차이 벡터가 독립이어서 평면을 만든다. 한 직선에 있으면 affine hull은 여전히 직선이다.

## 7. Convex combination과 convex set

affine combination에 <strong>모든 계수가 0 이상</strong>이라는 조건을 더한다.

$$
x=\sum_{i=1}^k\theta_i x_i,\qquad
\theta_i\ge0,\quad\sum_{i=1}^k\theta_i=1
$$

이것이 <strong>convex combination(볼록결합)</strong>이다. 두 점에서는

$$
x=(1-t)x_1+tx_2,\qquad 0\le t\le1
$$

이므로 두 점 사이의 <strong>끝점을 포함한 선분</strong>만 얻는다. affine combination은 직선 전체, convex combination은 선분이다.

집합 $C$가 convex라는 정의는 다음과 같다.

$$
\boxed{
x_1,x_2\in C,\quad t\in[0,1]
\quad\Longrightarrow\quad (1-t)x_1+tx_2\in C
}
$$

어떤 두 점을 골라도, 선분 위의 어떤 비율을 골라도 $C$ 안에 남아 있어야 한다. 두 점의 조건을 반복 적용하면 임의의 <strong>유한 개 점</strong>의 볼록결합도 $C$ 안에 들어간다.

![채워진 원판은 두 점 사이 선분을 포함하지만 원 둘레만 있는 집합은 중간점 원점을 포함하지 않는다.](disk-and-circle.svg)

### 볼록성을 증명할 때와 반증할 때

증명하려면 <strong>임의의</strong> $x_{1},x_{2}$와 $t$를 잡고 정의를 만족함을 보여야 한다. 몇 쌍의 점이나 중간점만 확인해서는 증명이 되지 않는다.

반증은 단 하나의 반례로 충분하다. 단위원 둘레에서 (1,0), (−1,0)을 고르면 중간점 (0,0)은 원 둘레에 없다. 따라서 원 둘레는 nonconvex다. 원 내부를 채운 원판은 convex다.

### Open/closed와 convexity는 다른 성질이다

$(0,1)$, $[0,1]$, [0,1)은 모두 convex다. 경계를 포함하는 방식은 달라도, 두 허용점 사이가 빠져 있지 않기 때문이다.

반면 원 둘레는 closed이고 bounded여서 compact지만 convex는 아니다. 서로 떨어진 두 열린 원판의 합집합은 open이지만 일반적으로 nonconvex다. <strong>경계의 포함 여부와 선분의 포함 여부를 따로 확인한다.</strong>

## 8. Conic combination과 세 가지 hull

교안에는 affine·convex combination과 함께 conic combination도 등장한다.

$$
x=\sum_{i=1}^k\theta_i x_i,\qquad\theta_i\ge0
$$

conic combination은 계수를 음수가 아닌 값으로 제한하지만 <strong>합을 1로 고정하지 않는다.</strong> 따라서 방향뿐 아니라 전체 배율도 자유롭다.

| 결합 | 계수 조건 | 두 점 $e_{1}=(1,0)$, $e_{2}=(0,1)$에서 얻는 집합 |
| --- | --- | --- |
| linear | 제한 없음 | 평면 $\mathbb{R}^{2}$ 전체 |
| affine | 합이 1 | $x_{1}+x_{2}=1$인 직선 전체 |
| conic | 각각 0 이상 | $x_{1}\ge 0$, $x_{2}\ge 0$인 사분면 전체 |
| convex | 각각 0 이상, 합이 1 | 사분면 안의 (1,0)과 $(0,1)$ 사이 선분 |

집합 $S$의 점들을 재료로 <strong>가능한 모든 유한 결합</strong>을 모은 것이 해당 hull이다.

$$
\operatorname{aff}S=\left\{\sum_i\theta_i x_i:
x_i\in S,\ \sum_i\theta_i=1\right\}
$$

$$
\operatorname{cone}S=\left\{\sum_i\theta_i x_i:
x_i\in S,\ \theta_i\ge0\right\}
$$

$$
\operatorname{conv}S=\left\{\sum_i\theta_i x_i:
x_i\in S,\ \theta_i\ge0,\ \sum_i\theta_i=1\right\}
$$

여기서는 $S$가 비어 있지 않다고 하자. affine hull은 $S$를 포함하는 가장 작은 affine set이고, convex hull은 $S$를 포함하는 가장 작은 convex set이다. conic hull은 $S$를 포함하는 가장 작은 <strong>convex cone</strong>이다. 예를 들어 세 비공선 점의 convex hull은 꼭짓점·변·내부를 모두 포함한 삼각형이다.

계수 제한을 비교하면 다음 포함관계를 얻는다.

$$
\operatorname{conv}S\subseteq\operatorname{aff}S,
\qquad\operatorname{conv}S\subseteq\operatorname{cone}S
$$

affine hull과 conic hull 사이에는 일반적인 포함관계가 없다. 표의 직선과 사분면은 서로를 포함하지 않는다.

## 9. Affine set, subspace, dimension을 연결하기

<strong>Affine set</strong>은 그 안의 서로 다른 두 점을 지나는 <strong>직선 전체</strong>를 포함한다.

$$
x_1,x_2\in C,\quad t\in\mathbb R
\quad\Longrightarrow\quad(1-t)x_1+tx_2\in C
$$

convex set보다 $t$의 범위가 넓다. 따라서 <strong>affine set은 convex지만, convex set이 모두 affine인 것은 아니다.</strong> 선분과 원판은 convex지만 affine은 아니다.

비어 있지 않은 affine set은 어떤 부분공간 $V$와 점 $x_{0}$에 대해 $x_{0}+V$로 나타낼 수 있다. 선형방정식의 해집합이 대표적이다.

$$
C=\{x:Ax=b\}
$$

해 $x_{0}$가 하나 있으면 다른 모든 해는 $x_{0}$에 null space 벡터를 더한 형태다.

$$
C=x_0+\mathcal N(A)
$$

앞 글의 null space가 여기서는 <strong>해집합 안에서 움직일 수 있는 방향</strong>을 뜻한다. $b=0$이면 해집합이 null space 자체여서 원점을 포함하는 subspace다. $b\ne 0$인 해집합은 원점을 지나지 않을 수 있다. 해가 없으면 집합은 공집합이다.

### Convex set의 차원은 affine hull의 차원이다

$\mathbb{R}^{3}$ 속 삼각형은 성분을 세 개로 적지만, 한 평면 안에서만 움직이므로 자체 차원은 2다.

$$
\dim C=\dim(\operatorname{aff}C)
$$

점들이 주어졌다면 기준점 하나를 빼서 만든 차이 벡터들의 rank로 affine hull의 차원을 구할 수 있다. 두 점이 다르면 1차원, 세 점이 비공선이면 2차원이다. 이 정의는 비어 있지 않은 집합을 기준으로 사용한다.

## 10. Hyperplane: 선형 등식 하나가 만드는 집합

0이 아닌 벡터 $a$와 실수 $b$에 대해

$$
H=\{x\in\mathbb R^n:a^Tx=b\},\qquad a\ne0
$$

를 <strong>hyperplane(초평면)</strong>이라고 한다. $\mathbb{R}^{2}$에서는 직선, $\mathbb{R}^{3}$에서는 평면이며 일반적으로 차원은 n−1이다. $\mathbb{R}^{1}$에서는 점 하나다.

필기의 예제는

$$
x_1+x_2=6,\qquad a=\begin{bmatrix}1\\1\end{bmatrix},\quad b=6
$$

이다. (0,6), (2,4), (3,3), (6,0)은 모두 이 직선 위에 있다.

### 왜 a가 normal vector일까?

$p,q$가 같은 초평면 위에 있으면 $a^{T}p=b$, $a^{T}q=b$다. 두 식을 빼면

$$
a^T(p-q)=0
$$

이다. p−q는 초평면을 따라 이동하는 방향이다. 따라서 <strong>$a$는 초평면 안의 모든 이동 방향에 수직</strong>이다. 이것이 normal vector(법선벡터)의 의미다.

(2,4)에서 (3,3)으로 가는 방향은 (1,−1)이고 (1,1)과의 내적은 0이다. $a$가 초평면 위의 점이라는 뜻이 아니라, 초평면에 수직인 방향을 나타낸다는 뜻이다.

### 왜 hyperplane은 affine이고 convex일까?

$p,q\in H$이면, 모든 실수 $t$에 대해

$$
a^T((1-t)p+tq)=(1-t)b+tb=b
$$

다. 직선 전체가 $H$에 있으므로 affine이고, 특히 $0\le t\le 1$에서도 성립하므로 convex다. 등식 오른쪽에 $b$가 남는 것은 <strong>계수의 합이 1</strong>이기 때문이다.

$a=0$은 정의에서 제외한다. 이때 식은 $b=0$이면 전체 공간, $b\ne 0$이면 공집합을 나타내므로 보통의 초평면이 아니다.

### 초평면을 여러 개 교차시키면 내부가 채워질까?

<strong>교집합은 각 집합에 공통으로 속하는 점만 남기는 연산이다.</strong> 얇은 경계들을 겹쳐서 그 사이 공간을 채우는 연산이 아니다. 예를 들어 다음 두 직선을 동시에 만족하는 점은 원점 하나뿐이다.

$$
\{x:x_1=0\}\cap\{x:x_2=0\}=\{(0,0)\}
$$

같은 직선을 반복하면 그대로 그 직선이 남고, 서로 다른 평행선을 교차시키면 공집합이다. 따라서 등식을 추가할 때마다 반드시 차원이 하나씩 줄어드는 것도 아니다. <strong>독립적인 제약인지, 중복인지, 서로 모순되는지</strong>에 따라 결과가 달라진다.

여러 선형 등식을 행렬로 묶어 보면 구조가 더 분명해진다. 해가 하나라도 존재하고 그중 하나를 기준점으로 잡으면,

$$
Cx=d,\qquad Cx_0=d
\quad\Longrightarrow\quad
\{x:Cx=d\}=x_0+\mathcal N(C)
$$

이다. 해집합은 Null Space를 기준점만큼 평행이동한 <strong>affine set</strong>이고, 차원은 입력 차원에서 행렬의 rank를 뺀 값이다.

$$
\dim\{x:Cx=d\}=n-\operatorname{rank}(C)
\qquad\text{(해집합이 비어 있지 않을 때)}
$$

방향 하나가 허용되면 그 방향으로 양쪽 끝없이 이동할 수 있으므로, 이 집합은 유한한 길이의 선분이나 채워진 삼각형이 될 수 없다. 비어 있지 않은 bounded affine set은 점 하나뿐이다. 또한 <strong>원점을 지나지 않는 affine set을 선형 subspace라고 부르면 안 된다.</strong> 예를 들어 `x₁+x₂=6`은 affine set이지만 원점이 없어 선형 부분공간은 아니다.

다음에 배울 부등식 제약은 경계 위만 남기는 대신, <strong>경계의 한쪽에 있는 점들도 허용</strong>한다. 이것이 초평면과 halfspace의 중요한 차이다.

## 11. a와 b는 방향과 위치를 정하지만, b 자체가 거리는 아니다

필기에서 “원점에서 이 초평면까지 얼마나 떨어져 있을까?”라는 질문이 이어진다. $a$는 법선 방향을 정하고, <strong>고정된 $a$에 대해</strong> $b$가 법선 방향의 위치를 정한다. 실제 거리를 얻으려면 $a$의 길이도 보정해야 한다.

원점에서 가장 가까운 점 $x^*$는 $a$ 방향에 있다. $x^*=\alpha a$를 $a^Tx^*=b$에 넣으면

$$
\alpha\|a\|_2^2=b
\quad\Longrightarrow\quad
\boxed{x^*=\frac{b}{\|a\|_2^2}a}
$$

이다. 그 점에서 초평면 안의 다른 점으로 가는 방향은 $a$에 수직이므로, 피타고라스 정리에 의해 $x^*$가 가장 가깝다. 따라서 거리는

$$
\boxed{\operatorname{dist}(0,H)=\|x^*\|_2=\frac{|b|}{\|a\|_2}}
$$

다. $b$가 음수일 수도 있으므로 거리는 절댓값을 쓴다. $a$를 단위 법선으로 정규화했을 때만 $b$를 부호 있는 거리로 바로 읽을 수 있다.

$x_{1}+x_{2}=6$에서는 $a$의 노름이 $\sqrt{2}$이므로

$$
x^*=\begin{bmatrix}3\\3\end{bmatrix},\qquad
\operatorname{dist}(0,H)=\frac6{\sqrt2}=3\sqrt2
$$

다. 거리 6이 아니다. 식을 $2x_{1}+2x_{2}=12$로 바꾸어도 같은 초평면이고 거리는 변하지 않는다. $a$와 $b$를 함께 같은 0이 아닌 배수로 바꾸면 같은 등식을 나타내기 때문이다.

보충으로, 임의의 점 $q$에서 초평면으로의 정사영과 거리는 다음과 같다.

$$
\operatorname{proj}_H(q)=q-\frac{a^Tq-b}{\|a\|_2^2}a,
\qquad\operatorname{dist}(q,H)=\frac{|a^Tq-b|}{\|a\|_2}
$$

이동량이 법선 방향이고, 결과를 $a$와 내적하면 $b$가 되는지 확인하면 공식을 검산할 수 있다.

## 12. Halfspace와 polyhedron: 선형 부등식들을 동시에 만족하기

초평면의 등식을 부등식으로 바꾸면 한쪽 영역 전체를 얻는다.

$$
H_-=\{x:a^Tx\le b\},\qquad
H_+=\{x:a^Tx\ge b\},\qquad a\ne0
$$

이것이 경계를 포함하는 <strong>closed halfspace(닫힌 반공간)</strong>다. 등식은 경계 위의 점만, 부등식은 경계와 한쪽 영역의 점들을 허용한다. 경계를 제외하고 엄격한 부등호를 쓰면 open halfspace가 되지만, 아래 polyhedron의 정의에는 닫힌 반공간을 사용한다.

예를 들어 `x₁+x₂=6`은 직선 하나이고, `x₁+x₂≤6`은 그 직선과 합이 6보다 작은 모든 점이다. <strong>Halfspace가 내부를 나중에 채우는 것이 아니라, 처음부터 한쪽 영역 전체를 포함하는 집합</strong>인 것이다. 어느 쪽이 원점을 포함하는지는 부등호와 $b$의 부호에 따라 달라진다. 원점을 직접 대입해서 판단한다.

$H$₋ 안의 $p,q$를 볼록결합하면

$$
a^T((1-t)p+tq)
\le(1-t)b+tb=b,\qquad0\le t\le1
$$

이므로 halfspace는 convex다. (1−t),t가 음수가 아니어야 부등식 방향을 유지할 수 있다는 점이 중요하다. 일반적으로 affine set은 아니다.

### Polyhedron의 정의: 부피가 있어야 하는 것은 아니다

최적화에서 <strong>polyhedron(다면체)</strong>은 유한 개 선형 부등식과 선형 등식의 공통 해집합이다. [Boyd·Vandenberghe §2.2.4](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf#page=45)에서도 이 정의를 사용한다. 여기서 다면체는 일상적으로 떠올리는 입체 덩어리보다 넓은 용어다. <strong>직선·초평면·점·선분·반공간도 polyhedron에 포함</strong>되며, 내부나 부피가 반드시 존재해야 하는 것은 아니다.

$$
P=\{x:Ax\preceq b,\ Cx=d\}
$$

여기서 ≼는 성분별 부등식이다. 행벡터가 0이 아닌 경우, `Ax≼b`의 각 행은 halfspace를, `Cx=d`의 각 행은 hyperplane을 나타낸다. 0인 행은 항상 참인 조건이거나 불가능한 조건으로 따로 처리한다. 모든 조건을 동시에 만족시키므로 <strong>이 집합들의 교집합</strong>을 취한다. 부등식이나 등식 중 어느 한 종류의 제약은 없어도 된다.

이 표현에서는 두 종류의 역할을 다음처럼 읽으면 된다.

- <strong>등식:</strong> 점이 놓일 수 있는 affine 공간을 지정한다. 예를 들어 평면 전체에서 특정 직선 위로 선택을 제한한다.
- <strong>부등식:</strong> 각 경계의 어느 쪽을 허용할지 정한다. 여러 조건을 동시에 적용해 선택 가능한 영역을 제한한다.

다만 부등식끼리 맞물려 차원을 줄일 수도 있으므로, 이것을 두 종류의 절대적인 역할 분담으로 외우면 안 된다. 다음 예제들을 비교해 보자.

![비음수 제약과 x1+x2≤6의 교집합은 세 꼭짓점 (0,0), (6,0), (0,6)의 삼각형이다. 법선 (1,1)과 가장 가까운 경계점 (3,3)을 함께 표시했다.](halfspace-and-polyhedron.svg)

$$
P=\{x:x_1\ge0,\ x_2\ge0,\ x_1+x_2\le6\}
$$

는 꼭짓점 (0,0), (6,0), (0,6)을 포함하는 채워진 삼각형이다. 예를 들어 (1,1)은 세 부등식을 모두 엄격하게 만족하고, 그 주변의 충분히 작은 원판도 삼각형 안에 들어간다. 따라서 2차원 공간에서 interior가 존재하고 넓이가 양수다. closed이고 bounded이므로 compact이며 convex다.

반대로 세 경계선을 모두 <strong>등식</strong>으로 바꾸면 어떻게 될까?

$$
x_1=0,\qquad x_2=0,\qquad x_1+x_2=6
$$

앞의 두 식은 원점을 요구하지만, 원점은 마지막 식을 만족하지 않는다. 결과는 삼각형도, 삼각형의 테두리도 아닌 <strong>공집합</strong>이다. 삼각형의 세 변을 모아 놓은 테두리는 또 다른 집합이며, 이는 변들의 합집합으로 표현한다. 경계들의 교집합과 혼동하지 않는다.

### 같은 경계라도 등호와 부등호에 따라 결과가 달라진다

| 동시에 적용하는 조건 | 남는 집합 | 2차원 공간에서 interior |
| --- | --- | --- |
| `x₁+x₂=6` | 끝없이 이어지는 직선 | 없음 |
| `x₁=0`, `x₂=0` | 원점 하나 | 없음 |
| `x₁≥0`, `x₂≥0`, `x₁+x₂≤6` | 채워진 삼각형 | 있음 |
| `x₁≥0`, `x₂≥0`, `x₁+x₂=6` | (0,6)과 (6,0)을 잇는 선분 | 없음 |

마지막 선분은 길이가 0이 아니지만, 선분 위의 어느 점 주위에도 2차원 원판을 넣을 수 없다. 그래서 <strong>주변 공간에서의 interior</strong>는 비어 있다. 선분이 놓인 직선 안에서만 주변을 보면 양 끝을 제외한 점들은 <strong>relative interior(상대적 내부)</strong>에 속한다. “내부가 없다”는 말은 집합이 비어 있다는 뜻이 아니며, 어느 공간에서 내부를 보는지 구별해야 한다.

### Halfspace가 있어도 내부가 반드시 생기지는 않는다

반대 방향의 두 부등식을 동시에 만족시키면 등식이 된다.

$$
\{x:x_2\leq0\}\cap\{x:-x_2\leq0\}
=\{x:x_2=0\}
$$

왼쪽 두 집합은 각각 한쪽 영역 전체를 가진 halfspace지만, 교집합은 직선 하나다. 즉, <strong>halfspace 제약이 있다는 사실만으로 interior나 부피를 보장할 수는 없다.</strong> 교집합을 취하면 허용되는 점은 추가되지 않고 유지되거나 줄어든다.

더 일반적으로, 선형 등식 하나는 다음처럼 반대 방향의 선형 부등식 두 개와 완전히 동등하다.

$$
a^Tx=b
\quad\Longleftrightarrow\quad
\begin{cases}
a^Tx\leq b,\\
(-a)^Tx\leq-b.
\end{cases}
$$

따라서 모든 polyhedron은 <strong>유한 개 닫힌 halfspace만의 교집합</strong>으로도 표현할 수 있다. 등식을 함께 적는 정의는 다른 집합을 정의하는 것이 아니라, 같은 제약을 읽기 쉽게 표현한 것이다.

질문에 대한 정확한 답은 이렇다. <strong>채워진 삼각형 같은 영역을 초평면들의 교집합만으로 만들 수는 없다. 하지만 모든 polyhedron이 그런 영역이어야 하는 것은 아니므로, 다면체의 정의에 부등식이 반드시 하나 이상 있어야 한다고 요구하지는 않는다.</strong> 한편 halfspace들만 사용하더라도 결과가 직선·점·공집합으로 줄어들 수 있다.

모든 polyhedron이 bounded인 것은 아니다. $x_{1}\ge 0,x_{2}\ge 0$만 남기면 사분면 전체여서 unbounded다. 제약들이 모순이면 공집합일 수도 있고, 등식 때문에 직선이나 점만 남을 수도 있다.

또한 비선형 제약이라고 반드시 nonconvex인 것은 아니다. 다음 절의 노름 공도 convex다. 반대로 “등식이니까 affine”이라는 결론은 <strong>선형 등식</strong>일 때의 이야기다. $\lVert x\rVert_{2}=1$은 원 둘레여서 convex가 아니다.

## 13. Euclidean ball과 norm ball은 왜 convex일까?

중심 $c$와 반지름 $r>0$인 유클리드 닫힌 공은

$$
B(c,r)=\{x:\|x-c\|_2\le r\}
$$

이다. $\mathbb{R}^{2}$에서는 내부가 채워진 원판이고 $\mathbb{R}^{3}$에서는 내부를 채운 구다. 표면만 뜻하지 않는다.

$p,q\in B(c,r)$, $0\le t\le 1$이면 노름의 삼각부등식과 동차성으로

$$
\begin{aligned}
\|(1-t)p+tq-c\|
&=\|(1-t)(p-c)+t(q-c)\|\\
&\le(1-t)\|p-c\|+t\|q-c\|\\
&\le(1-t)r+tr=r
\end{aligned}
$$

이다. 따라서 convex다. 이 증명은 L2에만 의존하지 않는다. <strong>어떤 노름으로 정의한 공도 convex</strong>다.

| $\mathbb{R}^{2}$의 단위 norm ball | 조건 | 모양 |
| --- | --- | --- |
| L1 | $\lvert x_{1}\rvert+\lvert x_{2}\rvert\le 1$ | 꼭짓점이 축 위에 있는 마름모 |
| L2 | $\sqrt{x_{1}^{2}+x_{2}^{2}}\le 1$ | 채워진 원판 |
| $L_\infty$ | $\max (\lvert x_{1}\rvert,\lvert x_{2}\rvert)\le 1$ | $[- 1,1]^{2}$ 정사각형 |

거리 $<r$인 열린 공도 convex다. 반면 거리 $=r$인 표면은 차원에 따라 원 둘레나 구면이 되며, 일반적으로 두 점 사이의 선분을 포함하지 않는다.

## 14. Convexity를 보존하는 연산: 교집합

$C_{1},C_{2}$가 convex이고 $p,q\in C_1\cap C_2$이면 $p,q$는 두 집합 각각에도 속한다. 따라서 볼록결합은 각각의 집합에 남고, 결국 교집합에도 남는다.

$$
C_\alpha\text{ convex for every }\alpha
\quad\Longrightarrow\quad\bigcap_\alpha C_\alpha\text{ convex}
$$

볼록성 보존은 유한 개에 제한되지 않고 임의 개의 교집합에서도 성립한다. Polyhedron은 그중 <strong>유한 개 선형 제약</strong>으로 표현되는 경우이며, halfspace와 hyperplane이 각각 convex이므로 그 교집합도 convex다. 이 정리는 <strong>교집합에 내부나 부피가 생긴다는 정리</strong>가 아니다.

또 모든 convex set이 polyhedron인 것은 아니다. 예를 들어 닫힌 원판은 convex지만, 유한 개 halfspace의 교집합으로는 곡선 경계를 정확히 나타낼 수 없어 polyhedron이 아니다. 유한 개 직선 경계로 잘라 만든 다각형과 구별한다.

<strong>합집합에는 같은 결론이 없다.</strong> 두 집합 [−2,−1], [1,2]는 각각 convex지만 합집합에서는 −1과 1의 중간점 0이 빠진다.

### Open/closed를 보존하는 연산과 혼동하지 않기

| 성질 | 보존되는 연산 |
| --- | --- |
| open | 임의 합집합, 유한 교집합 |
| closed | 임의 교집합, 유한 합집합 |
| convex | 임의 교집합 |

예를 들어 열린 구간들의 무한 교집합 $\bigcap_{k=1}^{\infty}(-1/k,1/k)=\{0\}$은 open이 아니다. 닫힌 구간들의 무한 합집합 $\bigcup_{k=1}^{\infty}[1/k,1]=(0,1]$은 closed가 아니다. convexity의 교집합 정리는 이런 open/closed의 규칙과 별개다.

## 15. Affine image: 선분은 변환 후에도 선분으로 간다

affine function은 다음 형태다.

$$
f(x)=Ax+b,\qquad A\in\mathbb R^{m\times n},\quad b\in\mathbb R^m
$$

집합 $S$의 <strong>image(상)</strong>는 $S$의 모든 점을 변환해서 얻은 출력들의 집합이다.

$$
f(S)=\{f(x):x\in S\}
$$

$S$가 convex이면 $f(S)$도 convex다. 핵심은 계수 합이 1이어서 평행이동 $b$가 다음처럼 결합된다는 것이다.

$$
f((1-t)p+tq)=(1-t)f(p)+tf(q)
$$

$p$와 $q$ 사이의 입력 선분이 출력 $f(p),f(q)$ 사이의 선분을 만든다. $A$가 특이행렬이면 서로 다른 입력이 겹쳐 선분이 점으로 눌릴 수도 있다. 그래도 convexity는 보존된다.

### 수업 예제 1: 단위 정사각형이 평행사변형으로

$$
S=[0,1]^2,\qquad
f(x)=\begin{bmatrix}1&3\\0&2\end{bmatrix}x+\begin{bmatrix}1\\2\end{bmatrix}
$$

| 입력 꼭짓점 | 출력 |
| --- | --- |
| (0,0) | (1,2) |
| (1,0) | (2,2) |
| $(0,1)$ | (4,4) |
| (1,1) | (5,4) |

정사각형은 이 네 점의 convex hull이다. affine map은 볼록결합을 보존하므로, 출력도 네 출력 꼭짓점의 convex hull인 <strong>채워진 평행사변형</strong>이다. 꼭짓점 네 개만을 뜻하지 않는다.

행렬식이 2이므로 넓이는 원래 정사각형의 넓이 1의 2배다. 평행이동 $b$는 위치만 바꾸고 넓이는 바꾸지 않는다.

### 수업 예제 2: 같은 정사각형이 선분으로

$$
g(x)=\begin{bmatrix}1&2\\2&4\end{bmatrix}x+\begin{bmatrix}1\\2\end{bmatrix}
$$

$t=x_{1}+2x_{2}$라고 쓰면 $S$ 안에서 $0\le t\le 3$이다. 반대로 이 범위의 $t$에 대해 $x_{1}=x_{2}=t/3$을 선택하면 해당 $t$를 만들 수 있으므로 중간 값도 모두 포함한다.

$$
g(x)=\begin{bmatrix}1+t\\2+2t\end{bmatrix},\qquad0\le t\le3
$$

따라서 $g(S)$는 (1,2)와 (4,8)을 잇는 선분이다. 행렬의 rank가 1이고 행렬식이 0이라 넓이는 0으로 눌렸다. <strong>차원이 줄어도 볼록성은 남는다.</strong>

![단위 정사각형의 affine image는 full rank 변환에서 평행사변형이 되고 rank 1 변환에서는 선분이 된다.](affine-images.svg)

이 예제는 앞 글의 rank·range·행렬식이 집합의 변환에서도 그대로 쓰인다는 것을 보여 준다. 일반 비선형 함수에는 같은 보장이 없다. 예를 들어 $t\in [0,1]$을 $(t,t^{2})$로 보내면 포물선 조각이고, 양 끝 출력의 중간점 (0.5,0.5)은 그 조각에 없다.

## 16. Affine preimage: 출력 조건을 만족하는 입력들을 모으기

출력 공간의 집합 $C$를 정한 뒤, 그 안으로 들어가는 <strong>모든 입력</strong>을 모은다.

$$
f^{-1}(C)=\{x\in\mathbb R^n:f(x)\in C\}
$$

이것이 <strong>preimage(역상)</strong>다. 표기에 −1이 있어도 <strong>역함수가 존재해야 한다는 뜻이 아니다.</strong> $A$가 직사각형이거나 특이행렬이어도 정의할 수 있다.

$f$가 affine이고 $C$가 convex이면 $f^{-1}(C)$도 convex다. $p,q$가 역상에 있으면 $f(p),f(q)\in C$이고

$$
f((1-t)p+tq)=(1-t)f(p)+tf(q)\in C
$$

이므로 입력 볼록결합도 역상에 들어간다.

### 하나의 출력 구간이 입력 공간의 띠가 된다

$$
f(x_1,x_2)=x_1+x_2,\qquad C=[0,6]
$$

이면

$$
f^{-1}(C)=\{x:0\le x_1+x_2\le6\}
$$

이다. 두 평행한 직선 사이의 무한한 띠다. 출력의 compact 구간을 역상으로 가져왔다고 입력 집합까지 bounded가 되는 것은 아니다. (t,−t) 방향으로는 끝없이 움직일 수 있다.

norm ball의 역상을 사용하면 다음 집합의 볼록성도 바로 알 수 있다.

$$
\{x:\|Ax-b\|_2\le r\}
$$

$x$↦Ax−b가 affine이고, 출력의 닫힌 공이 convex이기 때문이다. $A$가 rank를 잃으면 이 집합은 null space 방향으로 unbounded일 수 있다. <strong>볼록성 보존은 유계성이나 차원까지 보존한다는 말이 아니다.</strong>

## 17. Supporting hyperplane: 경계를 한쪽에서 받치는 초평면

이 내용은 손필기의 범위 다음에 교안과 수업에서 이어진다. 집합 $C$의 경계점 $z$를 지나면서, $C$ 전체를 한쪽 반공간에 두는 초평면을 생각하자.

$$
H=\{x:a^Tx=b\},\qquad a\ne0,\quad b=a^Tz,
\qquad a^Tx\le b\quad\text{for all }x\in C
$$

이를 $z$에서의 <strong>supporting hyperplane(지지 초평면)</strong>이라고 한다. 평면이 $C$를 양쪽으로 가르면 지지 초평면이 아니다.

단위 닫힌 원판에서는 $z=(1,0)$에 대해 $x_{1}=1$인 직선이 한 예다. 원판 전체가 $x_{1}\le 1$ 쪽에 있고 $z$를 지난다.

수업과 교안의 <strong>supporting hyperplane theorem</strong>은 비어 있지 않은 convex set의 모든 경계점에 지지 초평면이 존재한다고 말한다. 같은 정리는 [Boyd·Vandenberghe의 공개 강의자료 §2.23](https://web.stanford.edu/~boyd/cvxbook/bv_cvxslides.pdf)에서도 확인할 수 있다.

### 경계점이 반드시 C 안에 있는 것은 아니다

$C$가 열린 단위원판이면 $z=(1,0)$은 $C$에 없지만 경계에는 있다. 여전히 $x_{1}=1$은 $C$를 한쪽에 두고 $z$를 지나는 지지 초평면이다. 이때 초평면은 $C$ 자체와 만나지 않고 closure의 경계에 닿는다. 따라서 “항상 원래 집합과 접한다”는 그림만으로 외우면 open set에서 혼동할 수 있다.

또 지지 초평면이 유일할 필요는 없다. 삼각형의 꼭짓점에서는 서로 다른 법선 방향의 지지선들을 고를 수 있다. 매끄러운 곡선의 접선만을 뜻하는 개념도 아니다.

### 선형 목적함수의 최적점과 연결하기

처음의 삼각형 $P$에서 $x_{1}+x_{2}$를 최대화하면 최대값은 6이고, $x_{1}+x_{2}=6$인 변 전체가 최적점이다. 이 직선은 $P$를 $x_{1}+x_{2}\le 6$ 쪽에 두는 지지 초평면이기도 하다.

일반적으로 $c\ne 0$이고 $z$가 $C$에서 $c^{T}x$의 최솟값을 실제로 달성하면

$$
c^Tx\ge c^Tz\quad(x\in C)
$$

이다. $a=- c$로 쓰면 $C$ 전체가 $a^{T}x\le a^{T}z$ 쪽에 놓인다. 목적함수의 같은 값들을 잇는 초평면이 최적점에서 feasible set을 한쪽으로 받친다고 볼 수 있다.

열린 원판에서 $x_{1}$의 supremum은 1이지만 이를 달성하는 점은 없다. 지지 초평면은 존재해도 최적점이 $C$ 안에 존재한다는 보장은 별도라는 점이 compact 이야기와 연결된다.

## 18. 정의로 판정하는 세 가지 예제

### 예제 A: 원점에서 멀리 떨어진 직선도 convex일까?

$$
C=\{x:x_1+x_2=6\}
$$

convex이고 affine이며 closed다. 원점을 포함하지 않으므로 subspace는 아니다. $\mathbb{R}^{2}$에서 bounded가 아니므로 compact도 아니다. <strong>원점 포함은 convex의 조건이 아니다.</strong>

### 예제 B: 띠에 비음수 제약을 더하면?

$$
D=\{x:0\le x_1+x_2\le6,\ x_1\ge0,\ x_2\ge0\}
$$

비음수 제약 때문에 $x_{1}+x_{2}\ge 0$은 자동으로 만족한다. 따라서 $D$는 처음의 삼각형 $P$와 같다. halfspace들의 교집합이므로 convex이고, 모든 좌표가 0 이상 6 이하라 bounded이며 closed이므로 compact다.

### 예제 C: 공에서 둘레만 남기면?

$$
E=\{x\in\mathbb R^2:\|x\|_2=1\}
$$

closed이고 bounded이므로 compact다. 하지만 (1,0),(−1,0)의 중간점이 빠져 있으므로 nonconvex다. $\mathbb{R}^{2}$에서 interior는 비어 있고 boundary는 $E$ 전체다. <strong>compact와 convex는 서로를 보장하지 않는다.</strong>

## 19. 복습할 때 자주 틀리는 구분

| 혼동하기 쉬운 생각 | 확인할 조건 |
| --- | --- |
| 집합은 open 또는 closed 둘 중 하나다 | 둘 다이거나 둘 다 아닐 수 있다 |
| closed이면 bounded다 | 직선·반공간은 closed지만 unbounded |
| compact이면 convex다 | 원 둘레가 반례 |
| convex이면 경계를 포함한다 | 열린 원판도 convex |
| convex set은 원점을 포함한다 | 원점에서 이동한 선분·삼각형도 convex |
| affine combination은 계수가 양수다 | 합만 1이며 음수도 허용 |
| $b$가 hyperplane까지의 거리다 | 거리는 $\lvert b\rvert/\lVert a\rVert_{2}$ |
| polyhedron은 반드시 닫힌 유한한 덩어리다 | closed이지만 unbounded·낮은 차원·공집합일 수 있음 |
| 초평면들을 교차시키면 그 사이의 내부가 채워진다 | 비어 있지 않으면 affine set이며, 채워진 삼각형은 만들 수 없음 |
| halfspace들의 교집합에는 반드시 내부가 있다 | 반대 방향 두 부등식만으로 직선 하나가 남을 수도 있음 |
| convex 집합 둘의 합집합도 convex다 | 교집합 보존 정리와 구별 |
| affine map은 차원을 보존한다 | 특이행렬은 차원을 줄일 수 있음 |
| preimage를 구하려면 $A^{-1}$이 필요하다 | 출력 조건을 만족하는 입력의 집합으로 정의 |
| 지지 초평면의 존재는 최적점 존재를 뜻한다 | 열린 원판에서는 경계값이 달성되지 않을 수 있음 |

## 20. 혼자 풀어 보는 확인 문제

1. $C=[0,1)$에서 int $C$, cl $C$, $\partial C$는 각각 무엇인가? $C$는 convex인가?
2. $x_{1}=(1,1)$, $x_{2}=(3,2)$일 때 $t=- 1$로 만든 affine combination은 무엇인가? 두 점의 convex combination인가?
3. 세 점 (0,0), (2,0), (0,2)의 affine hull과 convex hull은 무엇인가?
4. $2x_{1}+2x_{2}=12$의 법선, 원점에서 가장 가까운 점, 원점까지의 거리는?
5. $x_{1}+x_{2}\le 6$이 원점을 포함하는지 어떻게 판단하는가?
6. 단위 정사각형을 $g(x)=[[1,2],[2,4]]x+(1,2)$로 변환한 image의 차원과 양 끝점은?
7. $f(x)=x_{1}+x_{2}$일 때 $f^{-1}(\{3\})$는 무엇인가? 역함수가 필요할까?
8. $[0,1]^{2}$의 모든 점 중 $x_{1}+x_{2}$를 최대화하는 점은? 그 점을 지나는 지지선 하나는?
9. 단위 열린 원판에서 $x_{1}$을 최대화하는 점이 존재하는가? $x_{1}=1$은 지지선인가?
10. convex 집합의 볼록결합을 몇 개 계산해 모두 안에 있음을 확인하면 convexity의 증명이 될까?

<strong>해설</strong>

1. $(0,1)$, $[0,1]$, {0,1}이며 $C$는 convex다.
2. $x_{1}- (x_{2}- x_{1})=(- 1,0)$이다. $t$가 $[0,1]$ 밖이므로 두 점의 convex combination이 아니다.
3. affine hull은 $\mathbb{R}^{2}$ 전체, convex hull은 $x_{1}\ge 0,x_{2}\ge 0,x_{1}+x_{2}\le 2$인 채워진 삼각형이다.
4. 법선 (2,2), 가장 가까운 점 (3,3), 거리 $12/\sqrt{8}=3\sqrt{2}$다.
5. $x=0$을 부등식에 넣어 $0\le 6$임을 확인한다.
6. 1차원 선분이며 양 끝점은 (1,2),(4,8)이다.
7. $x_{1}+x_{2}=3$인 직선이다. 역함수는 필요하지 않다.
8. (1,1)에서 최대값 2. $x_{1}+x_{2}=2$가 지지선이다.
9. 최대값을 달성하는 점은 없다. supremum은 1이고 $x_{1}=1$은 경계점 (1,0)에서의 지지선이다.
10. 아니다. 정의는 모든 두 점과 모든 $t\in [0,1]$에 대한 조건이다. 반증에는 반례 하나로 충분하다.

## 다음 단원으로 이어 읽기

이번 글은 <strong>어떤 $x$를 선택할 수 있는가</strong>를 집합으로 설명했다. 다음 단원의 convex function은 그 집합 위에서 <strong>$x$의 값을 어떻게 평가하는가</strong>를 다룬다. convex set의 선분 조건과 convex function의 함수값 부등식은 서로 연결되지만 다른 정의다.

정사영에서 시작한 거리의 기하학, 행렬의 rank가 정하는 변환 후 차원, 제약조건의 교집합과 supporting hyperplane은 이후 최적화 문제의 해를 해석할 때 다시 등장한다.

## 참고한 자료와 보충 설명의 범위

- 개인 손글씨 노트 <strong>「3 Convex Set」 1–6페이지</strong>: open/closed/compact, interior·closure·boundary, affine/convex combination, convex set, hyperplane의 법선과 거리, halfspace·polyhedron·norm ball, affine image/preimage.
- ENAI601, <strong>Module 2 — Convex Sets</strong> 접근성 버전 교안: 최적화의 목적함수와 feasible set, 집합의 위상적 성질, combinations/hulls, affine·convex set, 볼록성을 보존하는 연산, supporting hyperplane.
- <strong>2026-09-16 수업</strong>: 원판과 원 둘레, open/closed의 반례, affine set, halfspace·polyhedron, 정사각형의 두 affine image 예제, supporting hyperplane.
- [Boyd·Vandenberghe, Convex Optimization 공개 강의자료 §2.23](https://web.stanford.edu/~boyd/cvxbook/bv_cvxslides.pdf): supporting hyperplane theorem의 조건 확인.

최소값 존재 조건, 상대적 내부, 거리와 정사영 공식의 유도, 볼록성 보존의 증명, 열린집합의 경계에서의 지지 초평면 예제는 복습을 위해 보강했다. 수식의 조건과 계산은 교안과 함께 확인했다. 그림은 본문 좌표로 새로 작성했으며 필기나 강의자료 원문을 전재하지 않았다.
