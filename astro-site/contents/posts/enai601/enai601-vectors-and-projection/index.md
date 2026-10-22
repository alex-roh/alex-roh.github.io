---
title: "[ENAI601] 01 — 벡터에서 정사영까지, 직교성이 계산을 바꾸는 이유"
description: "두 관측값을 하나의 예측으로 표현하는 문제에서 내적·노름·span·기저·정사영과 최소제곱의 의미를 연결한다."
date: 2026-10-21
publishedAt: "2026-10-21T00:25:14-04:00"
tags:
  - ENAI601
  - linear-algebra
  - optimization
series: "ENAI601 Numerical Methods"
seriesOrder: 1
updatedAt: "2026-10-22T17:44:41-04:00"
---

두 번 측정한 값이 3과 1이다. 이 둘을 숫자 하나 $a$로 요약하고, 두 측정값을 모두 $a$라고 예측한다고 하자. $a=1$이면 첫 측정값을 크게 틀리고, $a=3$이면 두 번째를 크게 틀린다. 그렇다면 어떤 값을 골라야 할까?

각 오차의 제곱을 더해 비교하면 $a=1$의 오차는 4, $a=2$의 오차는 2, $a=3$의 오차는 4다. 2가 좋아 보이지만 몇 가지 값만 비교해서는 모든 실수 중 가장 좋은 값이라고 증명할 수 없다. 이 작은 질문을 <strong>벡터와 정사영</strong>으로 풀면, 더 많은 관측값과 더 많은 변수를 쓰는 모델까지 같은 생각으로 확장할 수 있다.

관측값은 $v=(3,1)$이라는 점, 같은 값으로 예측한 결과는 $(a,a)$라는 점이다. 예측 가능한 점들은 직선 $x_2=x_1$ 위에 있다. 목표는 그 직선에서 관측값에 가장 가까운 점을 찾는 것이다. 이 글에서는 <strong>벡터로 값을 모으고→차이로 오차를 만들고→노름으로 오차를 재고→표현 가능한 공간에서 가장 가까운 점을 찾는 과정</strong>을 따라간다.

내적·span·기저·직교성은 이 과정에 각각 필요한 도구다. 뒤 단원을 먼저 알 필요는 없다. 마지막에는 왜 답이 $(2,2)$인지 미분 없이 증명하고, 행렬과 예측 모델에서 같은 계산이 어떻게 이어지는지 살펴본다. 여기서는 실수 벡터와 표준 내적, 유클리드 거리를 사용한다.

| 풀고 싶은 질문 | 필요한 개념 |
|---|---|
| 관측값과 예측값을 한꺼번에 적으려면? | 벡터 |
| 둘이 얼마나 다른지 숫자로 재려면? | 뺄셈·노름 |
| 모델이 어떤 예측들을 만들 수 있는가? | 선형결합·span·부분공간 |
| 필요한 방향만 남기려면? | 내적·정사영 |
| 방향이 서로 겹쳐 계산이 복잡해지면? | 직교기저·Gram–Schmidt |
| 찾은 점보다 더 좋은 점이 없다는 것을 보이려면? | 잔차의 직교성·피타고라스 정리 |

## Part A. 값을 벡터로 모으고 오차 재기

### 1. 벡터는 숫자 목록이면서 공간 속 이동이다

벡터(vector)는 여러 성분(component)을 순서대로 모아 놓은 대상이다. 예를 들어 2차원 벡터를 생각하자.

$$
v=\begin{bmatrix}3\\1\end{bmatrix}\in\mathbb{R}^2
$$

성분은 두 개이며, 기하학적으로는 원점에서 오른쪽으로 3, 위쪽으로 1만큼 향하는 화살표로 그릴 수 있다. 이런 관점에서 벡터에는 <strong>방향(direction)</strong>과 <strong>크기(magnitude)</strong>가 있다.

벡터의 성분이 반드시 물리적인 위치일 필요는 없다. 처음의 $v=(3,1)^T$에서는 첫 번째 축이 첫 관측값, 두 번째 축이 두 번째 관측값이다. $p(a)=(a,a)^T$는 그 두 관측값에 대한 예측을 모은 벡터다. 예를 들어 $a=1$이면 $p=(1,1)^T$, 차이 $v-p=(2,0)^T$는 관측별 오차를 모은 것이다. $\mathbb R^2$는 두 실수 성분을 갖는 공간, 위첨자 $T$는 행과 열을 바꾸는 전치(Transpose)다.

AI에서는 벡터를 하나의 데이터에 대한 <strong>feature vector</strong>로 생각할 수도 있다. 숫자 하나하나가 어떤 특징을 의미하는지에 따라 공간의 각 축이 정해진다. 그림의 좌표축이든 데이터의 특징축이든, 벡터 계산 자체는 같다.

#### 덧셈: 이동을 이어 붙이기

$$
u=\begin{bmatrix}2\\1\end{bmatrix},\qquad
v=\begin{bmatrix}1\\3\end{bmatrix}
$$

$$
u+v
=\begin{bmatrix}2+1\\1+3\end{bmatrix}
=\begin{bmatrix}3\\4\end{bmatrix}
$$

먼저 $u$만큼 움직이고, 그 끝점에서 $v$만큼 더 움직인다. 원점에서 최종 도착점으로 향하는 하나의 화살표가 합벡터다. 이를 <strong>head-to-tail rule</strong>이라고 한다. 두 벡터를 원점에서 그렸을 때 평행사변형의 대각선이 합벡터가 되는 <strong>parallelogram rule</strong>도 같은 이야기다.

#### 뺄셈: 한 위치에서 다른 위치까지의 이동

$$
x=\begin{bmatrix}1\\2\end{bmatrix},\qquad
y=\begin{bmatrix}4\\6\end{bmatrix}
$$

$$
y-x=\begin{bmatrix}3\\4\end{bmatrix}
$$

이 결과는 <strong>위치 $x$에서 위치 $y$로 향하는 displacement vector</strong>다. 화살표의 시작점은 $x$, 끝점은 $y$다. 역순으로 빼면 방향도 반대가 된다.

$$
x-y=-(y-x)
$$

덧셈이 연속된 이동을 합치는 작업이라면, 뺄셈은 두 위치 사이의 이동을 찾아내는 작업이다.

예측 벡터와 관측 벡터의 차이도 같은 연산이다. 이 글에서는 <strong>관측값−예측값</strong>을 잔차로 쓴다. 부호를 반대로 정의할 수도 있지만, 제곱해서 더한 오차는 같다. 중요한 것은 어떤 방향의 차이를 쓰는지 일관되게 정하는 것이다.

#### 스칼라배: 크기를 조절하거나 방향을 뒤집기

$$
cv=\begin{bmatrix}cv_1\\cv_2\end{bmatrix}
$$

양수인 스칼라를 곱하면 같은 방향으로 길이가 늘거나 줄어든다. 음수를 곱하면 반대 방향으로 뒤집힌다. 특히 스칼라가 0이면 영벡터가 된다.

---

### 2. 내적은 두 방향의 관계를 숫자로 만든다

내적(inner product), 또는 점곱(dot product)은 두 벡터에서 하나의 스칼라를 만든다.

$$
x=\begin{bmatrix}3\\4\end{bmatrix},\qquad
y=\begin{bmatrix}1\\2\end{bmatrix}
$$

$$
x^Ty=3\cdot1+4\cdot2=11
$$

하지만 <strong>왜 하필 곱해서 더할까?</strong> 기하학적인 의미를 보면 이해가 쉬워진다.

$$
x^Ty=\|x\|_2\|y\|_2\cos\theta
$$

여기서 각도는 두 벡터 사이의 각도다. 내적은 벡터의 길이뿐 아니라 <strong>얼마나 같은 방향을 향하는지</strong>도 반영한다.

- 예각이면 내적은 양수이고, <strong>두 벡터의 길이를 고정했을 때</strong> 각도가 0도이면 최대가 된다.
- 서로 수직이면 내적이 0이다.
- 서로 반대쪽으로 기울어 있으면 내적은 음수가 되고, 각도가 180도일 때 가장 작은 값이 된다.

단, 길이가 0인 벡터의 방향이나 두 벡터 사이의 각도는 정의하지 않는다.

이 사실은 AI에서도 익숙하다. 텍스트나 이미지의 feature embedding을 비교할 때, 벡터의 방향 관계를 이용해 유사성을 해석할 수 있다. 다만 단순 dot product는 벡터 길이에도 영향을 받으므로, 방향만 비교하고 싶을 때는 정규화한 벡터를 사용한다.

---

#### 내적이 어떻게 예측의 재료를 읽어 줄까?

같은 값으로 예측하는 방향 $u=(1,1)^T$와 관측값 $v=(3,1)^T$를 내적하면 $u^Tv=4$다. 두 관측값을 같은 비중으로 더한 값이다. 반면 $u^Tu=2$는 이 방향벡터의 길이 제곱이다. 뒤에서 두 값을 나눈 $4/2=2$가 가장 좋은 예측 계수가 된다.

내적의 결과 4 자체가 예측값 2는 아니다. 기준 방향의 길이까지 함께 보아야 한다. 이 구분이 정사영 공식의 분모를 이해하는 출발점이다.

### 3. 노름은 길이, 두 벡터의 차이는 거리다

벡터의 길이를 재는 함수가 <strong>norm</strong>이다. 여기서 주로 쓰는 것은 Euclidean norm 또는 L2 norm이다.

$$
\|x\|_2=\sqrt{x^Tx}
$$

예를 들어 다음 벡터의 길이는 피타고라스 정리로 계산된다.

$$
x=\begin{bmatrix}3\\4\end{bmatrix}
$$

$$
\|x\|_2=\sqrt{3^2+4^2}=5
$$

두 위치 사이의 <strong>distance</strong>는 먼저 두 벡터를 빼서 displacement를 만든 다음, 그 길이를 재는 것이다.

$$
d(x,y)=\|y-x\|_2
$$

앞에서 사용한 위치 벡터라면 결과는 다음과 같다.

$$
y-x=\begin{bmatrix}3\\4\end{bmatrix},\qquad
\|y-x\|_2=5
$$

즉 <strong>subtraction은 이동 벡터를 만들고, norm은 그 이동의 길이를 계산한다.</strong>

처음 문제를 노름으로 쓰면 오차를 한꺼번에 계산할 수 있다.

$$
v-p(a)=\begin{bmatrix}3-a\\1-a\end{bmatrix},\qquad
E(a)=\|v-p(a)\|_2^2=(3-a)^2+(1-a)^2.
$$

| 같은 값으로 예측 | 오차 벡터 | 제곱 오차의 합 |
|---|---|---:|
| $(1,1)$ | $(2,0)$ | 4 |
| $(2,2)$ | $(1,-1)$ | 2 |
| $(3,3)$ | $(0,-2)$ | 4 |

각 관측의 양·음 오차를 그대로 더하면 상쇄될 수 있지만, 제곱한 뒤 더하면 그런 상쇄가 없다. 거리는 $\sqrt{E(a)}$이고 제곱거리는 $E(a)$다. 둘 다 0 이상이며 제곱근은 크기 순서를 유지하므로, <strong>거리를 가장 작게 만드는 예측과 제곱거리를 가장 작게 만드는 예측은 같다.</strong>

#### 제곱 노름과 자기 자신과의 내적

노름을 제곱하면 제곱근이 사라진다.

$$
\|x\|_2^2=x^Tx=\sum_{i=1}^{n}x_i^2
$$

이것은 다음 장에서 계속 등장하는 <strong>quadratic form</strong>의 가장 기본적인 예다. 최적화에서는 제곱 노름을 목적함수로 사용하는 경우가 많다.

<span id="교수님-자료에서-강조한-노름의-성질"></span>

#### 노름 계산에서 지켜야 할 성질

스칼라배에 대해서는 길이의 배율만큼 변한다.

$$
\|cv\|_2=|c|\,\|v\|_2
$$

영벡터만 길이가 0이다.

$$
\|v\|_2=0\iff v=0
$$

<strong>Cauchy–Schwarz inequality</strong>는 내적의 절댓값이 두 벡터 길이의 곱보다 클 수 없다고 말한다.

$$
|u^Tv|\le\|u\|_2\|v\|_2
$$

이것은 내적의 각도 공식에서 코사인의 절댓값이 1 이하라는 사실로 이해할 수 있다.

<strong>Triangle inequality</strong>는 직접 가는 거리가 경유해서 가는 거리보다 길 수 없다는 뜻이다.

$$
\|u+v\|_2\le\|u\|_2+\|v\|_2
$$

나중에 어떤 norm 함수가 convex함을 보일 때 이 성질이 중요한 도구가 된다.

---

### 4. 정사영은 한 방향의 성분만 남긴다

![v=(3,1)을 y=x에 정사영하면 p=(2,2), 잔차는 r=(1,-1)이다.](projection.svg)

그림은 뒤에서 계산할 예제다. 파란 화살표가 원래 벡터, 초록 화살표가 정사영이고 점선이 잔차다.

어떤 벡터가 여러 방향으로 향하고 있을 때, 관심 있는 한 방향으로 얼마나 향하는지만 추출할 수 있을까? 이것이 <strong>projection</strong>의 출발점이다.

원래 벡터를 $v$, 기준 방향을 나타내는 0이 아닌 벡터를 $u$라고 하자. $v$를 $u$ 방향의 직선 위에 정사영하면 다음 결과를 얻는다.

$$
\operatorname{proj}_{u}(v)
=\frac{u^Tv}{u^Tu}u
=\frac{u^Tv}{\|u\|_2^2}u
$$

식의 역할을 나누면 다음과 같다.

- <strong>내적:</strong> 원래 벡터가 기준 방향과 얼마나 정렬되는지 확인한다.
- <strong>분모:</strong> 기준 벡터 자체의 길이 때문에 생기는 배율을 보정한다.
- <strong>마지막 벡터:</strong> 구한 양을 다시 실제 공간 속 화살표로 만든다.

#### 처음의 예측 문제에 적용하기

모든 예측은 $p=au$, $u=(1,1)^T$로 쓸 수 있다. 정사영 공식을 대입하면

$$
a=\frac{u^Tv}{u^Tu}=\frac{3+1}{1+1}=2,
\qquad p=au=\begin{bmatrix}2\\2\end{bmatrix}.
$$

오차는 $r=v-p=(1,-1)^T$다. 예측 직선의 방향과 내적하면 $u^Tr=1-1=0$이므로 오차는 그 직선에 수직이다. 왜 수직인 점이 가장 가까운지는 12절에서 증명한다.

공식을 얻는 과정도 이 관계에서 읽을 수 있다. $p=au$가 되도록 찾으면서 잔차가 $u$에 수직이라고 놓으면

$$
u^T(v-au)=0
\quad\Longrightarrow\quad u^Tv-a(u^Tu)=0
\quad\Longrightarrow\quad a=\frac{u^Tv}{u^Tu}.
$$

분모는 $u\ne0$이어서 양수다. 계수 $a$는 숫자 하나이고, $au$는 실제 예측 벡터다. $u$가 단위벡터가 아니면 $a$ 자체는 정사영의 길이가 아니다. 이 예에서는 $a=2$, 정사영 길이는 $\|p\|_2=2\sqrt2$다.

예를 들어 $x$축에 정사영하고 싶다면 기준 방향을 이렇게 고를 수 있다.

$$
u=\begin{bmatrix}1\\0\end{bmatrix},\qquad
v=\begin{bmatrix}3\\4\end{bmatrix}
$$

$$
\operatorname{proj}_{u}(v)
=\frac{3}{1}\begin{bmatrix}1\\0\end{bmatrix}
=\begin{bmatrix}3\\0\end{bmatrix}
$$

원래 벡터의 $y$방향 부분은 제거되고 $x$방향 부분만 남았다.

여기서 중요한 질문이 남는다. <strong>한 방향이 아니라 평면 전체에 정사영하고 싶다면 어떻게 해야 할까?</strong> 그러려면 먼저 공간과 기저를 이해해야 한다.

---

## Part B. 모델이 표현할 수 있는 공간

### 5. Linear combination과 span: 벡터들이 만들어 낼 수 있는 공간

벡터 덧셈과 스칼라배를 합친 연산이 <strong>linear combination(선형결합)</strong>이다.

$$
c_1v_1+c_2v_2+\cdots+c_kv_k
$$

각 계수를 바꾸면서 만들 수 있는 모든 결과를 모으면 <strong>span(생성공간)</strong>이 된다.

$$
\operatorname{span}\{v_1,\ldots,v_k\}
=\left\{\sum_{i=1}^{k}c_iv_i:c_i\in\mathbb R\right\}
$$

예를 들어 $x$축 방향과 $y$축 방향의 단위벡터가 있으면, 각각에 원하는 계수를 곱하고 더해서 평면의 모든 점에 도달할 수 있다.

$$
e_1=\begin{bmatrix}1\\0\end{bmatrix},\qquad
e_2=\begin{bmatrix}0\\1\end{bmatrix}
$$

$$
\operatorname{span}\{e_1,e_2\}=\mathbb R^2
$$

반면 두 벡터가 같은 직선을 가리킨다면 아무리 조합해도 그 직선 밖으로 나갈 수 없다.

$$
v_1=\begin{bmatrix}1\\1\end{bmatrix},\qquad
v_2=\begin{bmatrix}2\\2\end{bmatrix}=2v_1
$$

이것이 <strong>linear dependence(선형종속)</strong>이다. 두 번째 벡터가 새로운 방향 정보를 주지 않는다.

벡터들이 <strong>linearly independent(선형독립)</strong>라는 말은 영벡터를 만드는 선형결합이 자명한 경우밖에 없다는 뜻이다.

$$
c_1v_1+\cdots+c_kv_k=0
\quad\Longrightarrow\quad
c_1=\cdots=c_k=0
$$

> 선형독립은 각 벡터가 <strong>다른 벡터들의 조합으로 대체할 수 없는 새로운 방향 정보</strong>를 준다는 뜻이다.

---

#### Span은 모델이 만들 수 있는 예측의 범위다

처음의 모델은 $p=a(1,1)^T$만 만들 수 있다. 계수 $a$를 모든 실수로 바꾸면 직선 전체가 되므로 $W=\operatorname{span}\{(1,1)^T\}$다. 관측 벡터 $(3,1)^T$는 그 직선 밖이라 정확히 표현할 수 없다. 그래서 가능한 예측 중 가장 가까운 것을 찾았다.

이번에는 새 방향 $(1,0)^T$도 허용하자. $1(1,1)^T+2(1,0)^T=(3,1)^T$여서 관측값을 정확히 만들 수 있다. 두 방향은 독립이므로 평면 전체를 span한다. <strong>표현의 오차를 줄이는 일과, 어떤 방향들을 모델에 허용할지 정하는 일은 구별된다.</strong> 방향을 추가하면 표현 가능한 범위 자체가 달라진다.

### 6. Vector space, subspace, basis, dimension

여기서 <strong>vector space(벡터공간)</strong>를 생각해보자. 이 글에서 주로 다루는 표준적인 공간은 실수 성분을 갖는 다음 공간이다.

$$
\mathbb R^n
$$

벡터공간은 벡터 덧셈과 스칼라배가 정의되고 그 결과가 여전히 공간 안에 있으며, 그 밖의 벡터공간 공리도 만족하는 대상이다.

<strong>Subspace(부분공간)</strong>는 큰 벡터공간 안에 포함된 작은 벡터공간이다. 실수 벡터공간의 부분집합이 부분공간인지 확인할 때는 다음 조건이 핵심이다.

$$
0\in W
$$

$$
u,v\in W\implies u+v\in W
$$

$$
c\in\mathbb R,\ u\in W\implies cu\in W
$$

예를 들어 3차원 안의 xy평면은 부분공간이다.

$$
W=\left\{\begin{bmatrix}a\\b\\0\end{bmatrix}:a,b\in\mathbb R\right\}
$$

여기서는 더하고 배율을 바꿔도 세 번째 성분이 언제나 0이다. 반면 세 번째 성분이 항상 1인 평면은 영벡터가 포함되지 않으므로 부분공간이 아니다.

<strong>Basis(기저)</strong>는 공간 전체를 span하면서 동시에 linearly independent인 벡터들의 집합이다. 다시 말해 <strong>빠진 방향도 없고 불필요한 중복도 없는 좌표의 재료</strong>다.

<strong>Dimension(차원)</strong>은 기저에 포함된 벡터의 개수다.

$$
\dim(\mathbb R^2)=2,\qquad \dim(\mathbb R^3)=3
$$

특히 3개의 성분으로 적힌 벡터라도 그 벡터들이 움직이는 부분공간의 차원은 2일 수 있다. 예를 들어 위의 xy평면은 3차원 공간 안에 있지만 자체 차원은 2다.

---

#### 관측값 개수와 모델의 자유도는 다르다

$v=(3,1)^T$에는 성분이 두 개지만 $p=(a,a)^T$는 계수 하나만 선택한다. 예측들이 놓이는 직선의 차원은 1이다. 서로 독립인 방향 두 개를 허용하면 평면 안의 두 좌표를 자유롭게 선택할 수 있어 차원이 2가 된다.

같은 방향을 중복해서 늘리는 것으로는 자유도가 늘지 않는다. $(1,1)^T$와 $(2,2)^T$를 재료로 써도 $c_1(1,1)^T+c_2(2,2)^T=(c_1+2c_2)(1,1)^T$여서 같은 직선이다. $(2,2)^T$는 $(c_1,c_2)=(2,0)$으로도, $(0,1)$로도 표현된다. <strong>기저의 독립성은 같은 예측을 여러 계수로 중복 표현하지 않게 해 준다.</strong>

### 7. 직교성: 서로 다른 방향이 얼마나 겹치지 않는가

두 벡터가 <strong>orthogonal(직교)</strong>이라는 것은 내적이 0이라는 뜻이다.

$$
u^Tv=0
$$

0이 아닌 벡터끼리는 공간에서 90도를 이룬다. 이때 각 방향은 서로 간섭하지 않는 좌표축처럼 사용할 수 있다.

<strong>Orthogonal basis(직교기저)</strong>는 기저 벡터들이 서로 직교하는 경우다. <strong>Orthonormal basis(정규직교기저)</strong>는 여기에 각 기저 벡터의 길이가 1이라는 조건까지 더한 경우다.

$$
w_i^Tw_j=0\quad (i\ne j)
$$

$$
w_i^Tw_i=1
$$

여기서 주의할 점은 <strong>선형독립과 직교는 같지 않다</strong>는 것이다. 0이 아닌 직교 벡터들은 선형독립이지만, 선형독립인 벡터들이 모두 직교하는 것은 아니다.

그럼 왜 굳이 직교기저를 만들까? 답은 정사영을 평면이나 더 높은 차원으로 확장하면 분명해진다.

---

## Part C. 겹치지 않는 방향으로 계산하기

### 8. 한 방향의 정사영을 모으면 부분공간의 정사영이 된다

어떤 부분공간을 직교기저들이 생성한다고 하자.

$$
W=\operatorname{span}\{w_1,\ldots,w_m\}
$$

기저가 서로 직교한다면 <strong>부분공간 전체로의 정사영</strong>은 <strong>각 기저 방향으로의 정사영의 합</strong>으로 계산된다.

$$
\boxed{
\operatorname{proj}_W(v)
=\sum_{i=1}^{m}\operatorname{proj}_{w_i}(v)
}
$$

일반적인 직교기저에서는 다음처럼 계산한다.

$$
\operatorname{proj}_W(v)
=\sum_{i=1}^{m}\frac{w_i^Tv}{w_i^Tw_i}w_i
$$

#### 실제로 평면에 정사영해 보기

3차원 속 xy평면을 생각하자.

$$
w_1=\begin{bmatrix}1\\0\\0\end{bmatrix},\qquad
w_2=\begin{bmatrix}0\\1\\0\end{bmatrix}
$$

$$
v=\begin{bmatrix}3\\4\\5\end{bmatrix}
$$

$x$축 방향의 정사영은 다음과 같다.

$$
\operatorname{proj}_{w_1}(v)
=\begin{bmatrix}3\\0\\0\end{bmatrix}
$$

$y$축 방향도 별도로 계산한다.

$$
\operatorname{proj}_{w_2}(v)
=\begin{bmatrix}0\\4\\0\end{bmatrix}
$$

둘을 더하면 xy평면 위의 정사영이 된다.

$$
\operatorname{proj}_W(v)
=\begin{bmatrix}3\\0\\0\end{bmatrix}
+\begin{bmatrix}0\\4\\0\end{bmatrix}
=\begin{bmatrix}3\\4\\0\end{bmatrix}
$$

각 기저 방향이 90도로 분리되어 있으므로 <strong>하나의 방향 성분을 구해도 다른 방향 성분을 중복해서 세지 않는다.</strong> 바로 이 이유로 각 정사영을 독립적으로 계산해서 합칠 수 있다.

> 직교하지 않는 기저에 대해서도 부분공간으로의 정사영 자체는 존재한다. 다만 개별 기저벡터로 단순히 정사영한 결과들을 그냥 더하는 공식은 일반적으로 성립하지 않는다.

---

### 9. Orthonormal basis의 세 가지 이점

정규직교기저에서는 각 기저 벡터 길이의 제곱이 1이다. 따라서 정사영 공식의 분모가 사라진다.

$$
\operatorname{proj}_{w_i}(v)=(w_i^Tv)w_i
$$

이것은 단순히 계산이 짧아진다는 뜻이 아니다. <strong>좌표의 추출, 정사영의 재구성, 크기의 계산</strong>이 모두 간단해진다는 뜻이다.

#### 9.1 계수 추출: 내적 한 번으로 그 방향의 좌표를 안다

정규직교기저로 표현된 벡터를 생각하자.

$$
v=c_1w_1+\cdots+c_mw_m
$$

양변에 특정 기저 벡터를 내적하면 서로 다른 방향의 항들은 0이 된다.

$$
w_k^Tv
=\sum_{i=1}^{m}c_iw_k^Tw_i
=c_k
$$

따라서

$$
\boxed{c_k=w_k^Tv}
$$

이다. 이 값은 <strong>해당 기저 방향으로 얼마만큼 향하는지 나타내는 부호 있는 계수(signed coordinate)</strong>다. 계수가 음수라면 그 기저 벡터가 향하는 방향의 반대쪽 성분이라는 뜻이다.

예를 들어

$$
v=\begin{bmatrix}3\\-2\\4\end{bmatrix}
$$

라면 표준 정규직교기저에서 각 계수는 3, -2, 4다. 두 번째 계수 -2는 <strong>정의한 두 번째 축과 반대 방향</strong>의 성분을 뜻한다.

#### 9.2 부분공간 재구성: 필요한 좌표 성분만 추출한다

정규직교기저를 사용하면 부분공간 정사영 공식이 이렇게 단순해진다.

$$
\boxed{
\operatorname{proj}_W(v)
=\sum_{i=1}^{m}(w_i^Tv)w_i
}
$$

예를 들어 첫 번째와 세 번째 좌표만 남기고 싶다면 첫 번째와 세 번째 표준기저가 생성하는 부분공간에 정사영한다.

$$
W=\operatorname{span}\{e_1,e_3\}
$$

$$
\operatorname{proj}_W(v)
=3e_1+4e_3
=\begin{bmatrix}3\\0\\4\end{bmatrix}
$$

원래 벡터에서 선택한 부분공간에 속하는 성분만 남았다.

#### 9.3 제곱 노름: 피타고라스 정리가 고차원으로 확장된다

정규직교기저가 <strong>벡터 전체를 표현하는 공간</strong>의 기저라면,

$$
\boxed{\|v\|_2^2=\sum_{i=1}^{m}c_i^2}
$$

가 성립한다. 예시에서는 다음과 같다.

$$
\|v\|_2^2
=3^2+(-2)^2+4^2
=29
$$

서로 직교하는 성분에서는 교차항이 사라지므로, 각 좌표 성분의 제곱을 더해서 전체 길이의 제곱을 얻는다.

<strong>중요한 적용 조건:</strong> 기저가 작은 부분공간만 생성한다면, 위의 합은 <strong>그 부분공간으로 정사영한 벡터의 제곱 노름</strong>과 같다. 전체 벡터의 제곱 노름과는 구별한다.

$$
\boxed{
\|\operatorname{proj}_W(v)\|_2^2
=\sum_{i=1}^{m}c_i^2
}
$$

예를 들어 첫 번째와 세 번째 좌표만 남긴 결과라면

$$
\|\operatorname{proj}_W(v)\|_2^2
=3^2+4^2=25
$$

이고, 원래 전체 벡터의 제곱 노름 29와는 다르다.

---

### 10. 왜 직교하지 않으면 cross term이 나타날까?

여기서 선형독립과 직교를 혼동하기 쉽다.

<strong>“전체 크기의 제곱은 각 독립 성분의 크기 제곱을 더하면 되는 것 아닌가?”</strong>

정확히는 <strong>선형독립만으로는 부족하고, 서로 직교해야</strong> 단순히 더할 수 있다.

두 성분을 합친 벡터를 보자.

$$
v=c_1w_1+c_2w_2
$$

제곱 노름을 직접 전개하면

$$
\begin{aligned}
\|v\|_2^2
&=(c_1w_1+c_2w_2)^T(c_1w_1+c_2w_2)\\
&=c_1^2\|w_1\|_2^2+c_2^2\|w_2\|_2^2
+2c_1c_2w_1^Tw_2
\end{aligned}
$$

마지막 항이 <strong>cross term(교차항)</strong>이다.

$$
\boxed{2c_1c_2w_1^Tw_2}
$$

직교하면 내적이 0이므로 교차항이 사라진다.

$$
w_1^Tw_2=0
$$

그러나 선형독립이지만 직교하지 않는 경우에는 일반적으로 교차항이 남는다.

$$
w_1=\begin{bmatrix}1\\0\end{bmatrix},\qquad
w_2=\begin{bmatrix}1\\1\end{bmatrix}
$$

이 두 벡터는 선형독립이다. 그런데 두 벡터의 내적은 1이므로 직교하지 않는다. 계수를 모두 1로 선택하면

$$
v=w_1+w_2=\begin{bmatrix}2\\1\end{bmatrix}
$$

이고 실제 제곱 노름은 5다.

$$
\|v\|_2^2=2^2+1^2=5
$$

반면 각 성분의 제곱 노름만 더하면 3밖에 안 된다.

$$
\|w_1\|_2^2+\|w_2\|_2^2=1+2=3
$$

빠진 값 2가 바로 cross term이다.

$$
2w_1^Tw_2=2
$$

따라서

$$
5=1+2+2
$$

가 된다.

비직교 벡터여도 계수 중 하나가 0이면 해당 교차항은 0이다. 따라서 교차항의 존재는 기저의 관계와 실제 계수를 함께 보아야 한다.

> <strong>Linear independence</strong>는 정보가 중복되지 않는다는 조건이고, <strong>orthogonality</strong>는 제곱 노름을 계산할 때 서로 다른 방향의 교차항이 사라지는 조건이다. <strong>Orthonormality</strong>는 거기에 각 기저의 길이까지 1로 맞춘다.

---

### 11. Gram–Schmidt: 겹치는 방향을 빼서 정규직교기저 만들기

<blockquote class="lecture-excerpt">
<p class="lecture-excerpt-label">교안 발췌 · Module 1 — Projection / Gram–Schmidt</p>

Gram-Schmidt process: Starting with a basis $w_1,\ldots,w_m$, it constructs an orthonormal basis $b_1,\ldots,b_m$.

$$
b_1\leftarrow w_1,\qquad b_k\leftarrow w_k-\sum_{l=1}^{k-1}\frac{\langle w_k,b_l\rangle}{\langle b_l,b_l\rangle}b_l\quad(k=2,\ldots,m)
$$

</blockquote>

위 재귀식은 정사영을 빼서 <strong>직교벡터</strong>를 만드는 단계다. 정규직교기저를 얻으려면 마지막에 각 벡터를 자신의 노름으로 나누는 <strong>정규화</strong>까지 해야 한다.

그렇다면 처음부터 직교하지 않는 기저를 갖고 있다면 어떻게 해야 할까?

여기서 등장하는 것이 <strong>Gram–Schmidt process(그람–슈미트 직교화)</strong>다. 아이디어는 의외로 단순하다.

<strong>새 벡터에서 이미 확보한 방향으로의 정사영을 빼면, 그 방향에 수직인 나머지만 남는다.</strong>

다음 두 벡터는 선형독립이지만 직교하지 않는다.

$$
v_1=\begin{bmatrix}1\\1\end{bmatrix},\qquad
v_2=\begin{bmatrix}1\\0\end{bmatrix}
$$

#### Step 1. 첫 번째 방향을 유지한다

$$
u_1=v_1=\begin{bmatrix}1\\1\end{bmatrix}
$$

#### Step 2. 두 번째 벡터에서 첫 번째 방향의 성분을 뺀다

$$
\operatorname{proj}_{u_1}(v_2)
=\frac{u_1^Tv_2}{u_1^Tu_1}u_1
=\frac12\begin{bmatrix}1\\1\end{bmatrix}
$$

$$
\begin{aligned}
u_2
&=v_2-\operatorname{proj}_{u_1}(v_2)\\
&=\begin{bmatrix}1\\0\end{bmatrix}
-\begin{bmatrix}1/2\\1/2\end{bmatrix}\\
&=\begin{bmatrix}1/2\\-1/2\end{bmatrix}
\end{aligned}
$$

검산하면

$$
u_1^Tu_2
=1\cdot\frac12+1\cdot\left(-\frac12\right)
=0
$$

이다. 즉 두 벡터가 직교하게 됐다.

#### Step 3. 각 벡터 길이를 1로 만든다

$$
q_1=\frac{u_1}{\|u_1\|_2}
=\frac1{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}
$$

$$
q_2=\frac{u_2}{\|u_2\|_2}
=\frac1{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}
$$

이제 서로 직교하고 각 길이도 1이다.

$$
q_1^Tq_2=0,\qquad
\|q_1\|_2=\|q_2\|_2=1
$$

따라서 원래 두 벡터가 만들던 <strong>같은 공간</strong>에 대해 orthonormal basis를 얻었다.

세 개 이상의 선형독립 벡터에 대해서도 원리는 같다. 새로운 벡터에서 앞서 구한 직교 방향들의 정사영을 모두 제거한다.

$$
u_k
=v_k-\sum_{j=1}^{k-1}
\frac{u_j^Tv_k}{u_j^Tu_j}u_j
$$

그리고 정규화한다.

$$
q_k=\frac{u_k}{\|u_k\|_2}
$$

입력 벡터들이 선형독립이라는 조건이 필요하다. 종속된 벡터를 넣으면 어느 단계에서 나머지가 영벡터가 되어 정규화할 수 없다.

Gram–Schmidt가 의미 있는 이유는 <strong>일반 기저를 더 계산하기 쉬운 정규직교기저로 바꾸면서도, 그 기저가 만드는 공간 자체는 유지하기 때문</strong>이다.

---

#### 기저를 바꾸면 관측값은 어떻게 읽힐까?

방금 만든 $q_1=(1,1)^T/\sqrt2$, $q_2=(1,-1)^T/\sqrt2$로 $v=(3,1)^T$를 읽으면 계수는 $q_1^Tv=2\sqrt2$, $q_2^Tv=\sqrt2$다. 따라서

$$
v=(2\sqrt2)q_1+(\sqrt2)q_2
=\begin{bmatrix}2\\2\end{bmatrix}+\begin{bmatrix}1\\-1\end{bmatrix}.
$$

첫 방향만 남기면 처음의 예측 $p=(2,2)^T$이고, 버린 두 번째 방향의 성분이 잔차 $r=(1,-1)^T$다. 기저를 바꾸면서 관측값을 바꾼 것이 아니라, <strong>같은 관측값을 서로 겹치지 않는 두 방향의 좌표로 다시 읽은 것</strong>이다.

## Part D. 가장 가까운 예측을 증명하고 확장하기

### 12. Residual: 왜 정사영은 가장 가까운 점인가?

정사영의 또 다른 중요한 해석은 <strong>부분공간 안의 최근접 벡터(closest vector in a subspace)</strong>다. 이 부분은 최적화와 직접 연결된다.

어떤 부분공간이 있고 그 밖에 원래 벡터가 있다고 하자. 정사영을 $p$라고 쓰면,

$$
p=\operatorname{proj}_W(v)
$$

원래 벡터와 정사영 사이의 차이를 <strong>residual(잔차)</strong>이라고 한다.

$$
r=v-p
$$

정사영의 핵심 성질은 residual이 부분공간의 모든 방향과 수직이라는 것이다.

$$
r\perp W
$$

왜 이 점이 최단거리인지 확인해 보자. 부분공간 안에서 정사영이 아닌 임의의 다른 벡터를 $y$라고 하자.

$$
y\in W
$$

차이를 두 부분으로 나눌 수 있다.

$$
v-y=(v-p)+(p-y)
$$

첫 번째는 부분공간에 수직이고, 두 번째는 부분공간 안에 있다. 그러므로 두 부분은 직교하고 피타고라스 정리를 사용할 수 있다.

$$
\|v-y\|_2^2
=\|v-p\|_2^2+\|p-y\|_2^2
$$

마지막 항은 항상 0 이상이므로

$$
\boxed{
\|v-y\|_2^2\ge\|v-p\|_2^2
}
$$

가 된다. equality가 되려면 다른 점 $y$가 바로 정사영 $p$여야 한다.

따라서 정사영은 <strong>부분공간 안에서 원래 벡터와의 거리를 최소화하는 유일한 벡터</strong>다.

#### 작은 숫자 예시

다음 직선에 정사영한다고 하자.

$$
W=\operatorname{span}\left\{\begin{bmatrix}1\\1\end{bmatrix}\right\},\qquad
v=\begin{bmatrix}3\\1\end{bmatrix}
$$

정사영을 구하면

$$
p=\frac{4}{2}\begin{bmatrix}1\\1\end{bmatrix}
=\begin{bmatrix}2\\2\end{bmatrix}
$$

이고 잔차는

$$
r=v-p=\begin{bmatrix}1\\-1\end{bmatrix}
$$

이다. 이 잔차는 직선의 방향과 내적이 0이다.

$$
\begin{bmatrix}1&1\end{bmatrix}
\begin{bmatrix}1\\-1\end{bmatrix}=0
$$

이제 정사영과 최적화 사이의 연결이 보인다. 많은 문제에서는 <strong>정답과 완전히 일치하는 표현을 찾는 대신, 가능한 공간 안에서 오차를 가장 작게 만드는 표현</strong>을 찾는다. Least squares도 이 아이디어와 이어진다.

---


#### 숫자 몇 개의 비교를 모든 예측에 대한 증명으로 바꾸기

처음 문제의 모든 예측은 $p(a)=(a,a)^T$다. 제곱 오차를 전개하고 완전제곱으로 정리하면

$$
\begin{aligned}
E(a)&=(3-a)^2+(1-a)^2\\
&=2a^2-8a+10\\
&=2(a-2)^2+2.
\end{aligned}
$$

어떤 실수 $a$에서도 제곱항은 0 이상이므로 $E(a)\ge2$다. 등호는 $a=2$일 때만 성립한다. 따라서 단지 비교한 후보 중에서 좋은 정도가 아니라, <strong>모든 가능한 예측 중 유일하게 가장 좋은 예측</strong>이 $(2,2)^T$다. 예측 벡터의 길이는 $\sqrt8$, 잔차의 길이는 $\sqrt2$이고 $\|v\|_2^2=10=8+2$도 확인된다.

이것이 회귀에서 쓰는 <strong>Least Squares(최소제곱)</strong>의 가장 작은 예다. 지금은 모든 관측을 같은 값으로 예측했지만, 이후에는 여러 방향의 선형결합으로 예측 벡터를 만들고 같은 방식으로 오차 제곱합을 줄인다. 정사영은 그 계산의 기하학적 의미를 먼저 보여 준다.

### 13. 행렬과 최적화로 이어지는 질문

#### 열벡터를 모으면 행렬의 곱셈이 된다

앞에서 쓴 두 방향을 나란히 모아 $A$라고 쓰고 계수를 $c$에 모아 보자.

$$
A=\begin{bmatrix}1&1\\1&0\end{bmatrix},\quad
c=\begin{bmatrix}c_1\\c_2\end{bmatrix},\quad
Ac=c_1\begin{bmatrix}1\\1\end{bmatrix}+c_2\begin{bmatrix}1\\0\end{bmatrix}.
$$

행렬과 벡터의 곱은 열벡터들의 선형결합이다. 관측값 $(3,1)^T$를 정확히 만들려면 $c_1+c_2=3$, $c_1=1$을 풀면 된다. 여기서는 $c=(1,2)^T$가 답이다. 다음 행렬 단원에서는 어떤 방향들이 주어졌을 때 이런 방정식이 풀리는지, 계수가 유일한지를 rank·null space로 설명한다.

#### 내적은 제약의 경계와 이동 방향도 연결한다

$3x_1+2x_2=12$라는 직선을 생각하자. 이 선 위에서 $d=(2,-3)^T$만큼 이동하면 왼쪽 값의 변화는 $3(2)+2(-3)=0$이다. 이를 $c=(3,2)^T$와의 내적 $c^Td=0$으로 쓴다. 따라서 $c$는 그 직선에 수직인 방향이다. 이 한 가지 내적 계산이 뒤에서 제약의 경계선과 비용의 변화 방향을 해석하는 데 쓰인다.

| 이번에 이해한 계산 | 다음에 풀 수 있는 질문 |
|---|---|
| $v-p$와 $\|v-p\|^2$ | 예측값이 관측값을 얼마나 틀리는가? |
| 선형결합과 span | 모델이 어떤 예측을 만들 수 있는가? |
| 독립인 기저와 차원 | 표현에 몇 개의 자유로운 계수가 필요한가? |
| 내적이 0인 잔차 | 가능한 공간에서 오차를 더 줄일 수 없는 이유는? |
| $c^Td$ | 경계를 따라 움직이는가, 비용을 바꾸는가? |

한 번에 뒤의 이론까지 외울 필요는 없다. <strong>표현 가능한 방향을 정하고, 그 안에서 가장 가까운 값을 찾는다</strong>는 문제를 기억하면 된다. [다음 행렬 글](/enai601-matrices-and-psd/)은 그 방향들을 행렬 하나에 모아 다룬다.

### 14. 혼자 풀어 보는 확인 문제

#### 문제 1. 같은 값으로 예측하기

관측값이 $(5,1)^T$일 때 $(a,a)^T$ 중 제곱 오차가 가장 작은 예측과 잔차를 구하라.

<details class="review-answer"><summary>정답과 해설 펼치기</summary>
<div class="review-answer-body">

방향 $u=(1,1)^T$에 대해 $a=u^Tv/(u^Tu)=6/2=3$이다. 예측은 $(3,3)^T$, 잔차는 $(2,-2)^T$이며 내적 $u^Tr=0$이다. 제곱 오차는 8이고, 모든 $a$에서 $(5-a)^2+(1-a)^2=2(a-3)^2+8\ge8$이라 최적성이 증명된다.

</div></details>

#### 문제 2. 같은 직선의 방향벡터를 두 배로 바꾸기

관측값 $(3,1)^T$를 $u=(2,2)^T$ 방향에 정사영하라. 계수도 두 배가 되는가?

<details class="review-answer"><summary>정답과 해설 펼치기</summary>
<div class="review-answer-body">

계수는 $u^Tv/(u^Tu)=8/8=1$이고 정사영은 여전히 $1(2,2)^T=(2,2)^T$다. 방향벡터를 두 배로 바꾸면 그 벡터에 곱하는 계수는 절반이 되어 같은 점을 표현한다. 방향벡터의 길이, 곱하는 계수, 정사영 벡터를 구별하자.

</div></details>

#### 문제 3. 독립인 두 벡터에 각각 정사영해서 더하면?

$v=(3,1)^T$와 $w_1=(1,0)^T$, $w_2=(1,1)^T$에 대해 $\operatorname{proj}_{w_1}v+\operatorname{proj}_{w_2}v$를 구하라. 두 벡터의 span으로 정사영한 결과와 같은가?

<details class="review-answer"><summary>정답과 해설 펼치기</summary>
<div class="review-answer-body">

각 정사영은 $(3,0)^T$, $(2,2)^T$여서 합은 $(5,2)^T$다. 하지만 두 독립 벡터는 평면 전체를 span하므로 그 부분공간으로 정사영하면 $v$ 자체인 $(3,1)^T$여야 한다. 두 방향이 직교하지 않아 개별 정사영의 합에서 성분을 중복해서 센 것이다. Gram–Schmidt로 직교기저를 만든 뒤 합치는 방법을 사용할 수 있다.

</div></details>

#### 문제 4. 정사영한 길이와 원래 길이 구별하기

$v=(3,1)^T$를 $q_1=(1,1)^T/\sqrt2$ 방향에 정사영했다. 내적 계수의 제곱 $(q_1^Tv)^2$는 원래 $\|v\|^2$와 같은가?

<details class="review-answer"><summary>정답과 해설 펼치기</summary>
<div class="review-answer-body">

계수는 $2\sqrt2$이므로 제곱은 8이다. 이는 정사영 $(2,2)^T$의 제곱 노름이며, 원래 제곱 노름 $3^2+1^2=10$과는 다르다. 빠진 2는 잔차 $(1,-1)^T$의 제곱 노름이다. 부분공간의 기저가 벡터 전체를 표현하지 못하면, 계수 제곱의 합은 그 부분공간 성분만의 크기를 나타낸다.

</div></details>

<span id="참고한-수업-자료와-정리-범위"></span>

## 참고 자료

- ENAI601, <strong>Module 1 — Linear Algebra</strong>: Vector Space, Projection, Gram–Schmidt.
- <strong>2026년 9월 2일·9월 9일 수업</strong>.
- 개인 필기 <strong>「1 Vector」 1–6페이지</strong>.
