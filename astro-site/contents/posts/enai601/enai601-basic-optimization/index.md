---
title: "[ENAI601] 05 — Basic Optimization, 무엇을 어디에서 최소화할까?"
description: "목적함수와 제약조건에서 출발해 Domain·Feasible Set·Infimum·Optimal Point와 Active·Redundant Constraint를 구별한다"
tags:
  - ENAI601
  - optimization
  - mathematical-optimization
series: ENAI601 Numerical Methods
seriesOrder: 5
date: 2026-10-21
publishedAt: "2026-10-21T23:04:15-04:00"
updatedAt: "2026-10-22T05:14:51+00:00"
---

[앞 글의 Convex Function](/enai601-convex-functions/)까지 함수의 모양과 미분 조건을 공부했다. 이제는 그 함수를 목적함수와 제약조건으로 사용해, 가장 좋은 선택을 찾는 문제를 구성한다.

모델의 파라미터를 고르기 전에 무엇을 최소화할지, 어떤 값까지 허용할지 정해야 한다. 이때 <strong>Domain, Feasible Set, Optimal Value, Optimal Point를 구별</strong>해야 문제의 조건과 답의 의미를 정확히 읽을 수 있다. 다음 글에서는 이 언어 위에 Convexity를 더한다.

## 1. 왜 최적화 문제를 수학으로 표현할까?

머신러닝에서는 모델을 구성하는 파라미터를 무작정 고르는 것이 아니라, 예측 오차를 최소화하는 방향으로 선택한다. 예를 들어 집값 예측 모델을 만든다면 방의 개수나 주거 면적을 입력으로 사용하고, 실제 거래 가격과 예측 가격의 차이를 <strong>Loss Function</strong>으로 측정한다. 그 Loss를 작게 만드는 파라미터를 찾는 과정이 바로 <strong>Mathematical Optimization</strong>이다.

하지만 어떤 값이든 선택할 수 있는 것은 아니다. 모델이나 시스템이 반드시 지켜야 하는 조건이 있을 수 있다. 따라서 최적화 문제에는 두 요소가 등장한다.

- <strong>Objective Function / Cost Function:</strong> 최소화하거나 최대화하려는 값.
- <strong>Constraints:</strong> 선택한 변수가 만족해야 하는 조건.

강의의 일반적인 최소화 문제(Standard Form)는 다음과 같다.

$$
\begin{aligned}
\operatorname{minimize}\quad & f_0(x)\\
\text{subject to}\quad & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_j(x)=0,\quad j=1,\ldots,p
\end{aligned}
$$

여기서 미지수인 벡터는 <strong>Optimization Variable</strong>, 목적함수는 <strong>Objective Function</strong>, 부등식과 등식은 각각 <strong>Inequality Constraint</strong>, <strong>Equality Constraint</strong>다. 제약조건이 없는 경우를 <strong>Unconstrained Optimization</strong>이라고 한다.

> <strong>중요한 표기 구분:</strong> 이 글에서는 허용 가능한 점들의 집합을 `D`(Feasible Set), 최적점을 `x^*`, 최적값을 `p^*`로 구분한다. 교안에서는 `D`가 공통 Domain, `D*`가 Feasible Set이다. 이 글에서는 Domain을 `𝒟`, Feasible Set을 `D`로 구별하므로 교안의 `D*`가 본문의 `D`에 해당한다. 기호보다 역할을 먼저 파악한다.


### 교안의 ML 예제: 입력 데이터와 최적화 변수를 구별하기

집값 예측에서는 집의 특성인 <strong>Features</strong>와 이미 관측한 가격인 <strong>Labels</strong>가 주어진 데이터다. 최적화 과정에서 바꾸는 것은 그 데이터를 설명할 모델의 <strong>Parameters</strong>다. 데이터 한 건의 입력과 최적화 변수를 모두 `x`라고 쓰면 혼동하기 쉬우므로, 여기서는 데이터 행렬을 `X`, 관측값을 `y`, 학습할 파라미터를 `w`로 구별한다.

$$
X=\begin{bmatrix}1&u_1^T\\\vdots&\vdots\\1&u_N^T\end{bmatrix},
\qquad
w=\begin{bmatrix}w_0\\\bar w\end{bmatrix},
\qquad \hat y=Xw
$$

앞의 1은 <strong>Intercept / Bias(절편)</strong>를 포함하기 위한 열이다. 제곱 오차를 합한 <strong>Squared-error Loss</strong>를 최소화하면 앞서 행렬에서 공부한 최소제곱 문제가 된다.

$$
\operatorname{minimize}_{w}\quad
\sum_{i=1}^{N}(w_0+\bar w^Tu_i-y_i)^2
=\|Xw-y\|_2^2
$$

노름 자체를 최소화해도 제곱한 노름과 최적점은 같다. 0 이상에서 제곱은 순서를 보존하기 때문이다. 다만 미분과 Hessian 계산에는 제곱한 형태가 편하다. [행렬 글의 최소제곱·의사역행렬](/enai601-matrices-and-psd/)은 이렇게 <strong>학습 문제의 파라미터를 고르는 도구</strong>로 이어진다.

교안에는 특성별 가중치를 음수가 아니게 제한하는 예제도 있다.

$$
-w_j\leq0\quad(j=1,\ldots,n),
\qquad D=\mathbb R\times\mathbb R_+^n
$$

이 경우 절편은 자유롭고 나머지 가중치가 비음수다. <strong>모든 집값 회귀가 반드시 이 조건을 요구하는 것은 아니다.</strong> 특정 모델에 부여한 제약이라는 점을 구별한다.

추천 시스템 예제도 관측된 평점으로 다른 사람의 평점을 예측한다는 구조는 비슷하다. 예를 들어 Tom과 Mary의 평점으로 Ben의 평점을 예측할 때, 바꾸는 것은 이미 주어진 평점이 아니라 다음 모델의 파라미터다.

$$
\hat r_B=\theta_0+\theta_1r_T+\theta_2r_M
$$

교안의 일반적인 학습 목적함수에는 <strong>Regularization(정규화 / 규제)</strong>도 등장한다.

$$
\operatorname{minimize}_{\theta}\quad
\sum_{i=1}^{N}\ell(\theta;z_i)+\gamma R(\theta),
\qquad\gamma\geq0
$$

Loss는 데이터에 얼마나 잘 맞는지를 측정하고, Regularization은 큰 파라미터나 복잡한 모델 등에 별도의 비용을 부여한다. 구체적인 의미는 선택한 규제 함수에 달려 있다. 여기서 파라미터 벡터의 길이를 1로 맞추는 <strong>Normalization</strong>과는 역할이 다르다.

### 분류 문제에서는 무엇을 가장 좋다고 볼까?

교안의 <strong>Support Vector Machine(SVM)</strong>은 라벨이 -1 또는 +1인 데이터를 분류한다. 두 종류가 선형으로 분리 가능하다고 가정하면, 다음 Hyperplane의 양쪽에 데이터를 놓을 수 있다.

$$
H(w,b)=\{u:w^Tu+b=0\},\qquad w\ne0
$$

그런데 데이터를 올바르게 나누는 선은 여럿일 수 있다. SVM에서는 가장 가까운 학습 데이터와 분리면 사이의 거리인 <strong>Margin</strong>을 크게 만드는 기준을 사용한다. 올바르게 분류된 점과 Hyperplane 사이의 거리는 다음과 같다.

$$
d_i=\frac{|w^Tu_i+b|}{\|w\|_2}
=\frac{v_i(w^Tu_i+b)}{\|w\|_2},
\qquad v_i\in\{-1,+1\}
$$

마지막 등식은 올바르게 분류되어 라벨을 곱한 점수가 양수일 때 성립한다. 이 글에서 Margin은 <strong>분리면에서 가장 가까운 점까지의 거리</strong>를 뜻한다. 양쪽 경계면 사이의 전체 폭은 그 두 배다.

$$
\begin{aligned}
\operatorname{maximize}_{w,b}\quad
&\min_i\frac{v_i(w^Tu_i+b)}{\|w\|_2}\\
\text{subject to}\quad &v_i(w^Tu_i+b)>0\quad(i=1,\ldots,N)
\end{aligned}
$$

이 식은 우리가 원하는 기준을 표현하지만, 아직 앞의 최소화 Standard Form과는 다르다. <strong>좋은 해의 의미를 정하는 일과, 계산하기 좋은 문제로 표현하는 일은 별개의 단계</strong>다. 다음 글에서 같은 분리면을 유지하며 Convex Optimization 형태로 바꾸는 과정을 이어 본다.

## 2. Domain과 Feasible Set은 왜 구별할까?

<strong>Domain</strong>은 함수가 정의되는 입력의 범위이고, <strong>Feasible Set</strong>은 그중 모든 제약조건까지 만족하는 점들의 집합이다.

수학적으로는 공통 Domain과 제약조건의 교집합을 생각해야 한다.

$$
D=\left\{x\in\mathcal D:\ f_i(x)\leq0,\ h_j(x)=0\right\}
$$

$$
\mathcal D=\operatorname{dom}f_0\cap\bigcap_i\operatorname{dom}f_i\cap\bigcap_j\operatorname{dom}h_j
$$

- <strong>Feasible Point:</strong> 모든 제약조건과 Domain 요건을 만족하는 점.
- <strong>Infeasible Problem:</strong> Feasible Point가 하나도 없는 문제.
- <strong>Optimal Point:</strong> Feasible Point 가운데 목적함수값이 최적인 점.
- <strong>Optimal Value:</strong> 최적화 문제에서 얻을 수 있는 목적함수의 가장 작은 값(최솟값이 달성되지 않으면 하한의 의미를 주의해서 써야 한다).

$$
p^*=\inf_{x\in D} f_0(x)
$$

`Feasible`하다는 것과 `Optimal`하다는 것은 다르다. 조건을 지켰다고 해서 그 점이 가장 좋은 답인 것은 아니다. 또한 Feasible Set이 비어 있지 않아도 최솟값을 실제로 달성하는 점이 없을 수 있다.


### Domain도 Convex인지 확인해야 하는 이유

처음에는 이렇게 생각하기 쉽다.

> "목적함수와 제약조건의 Convexity를 확인했다면 Feasible Set은 이미 Convex한 것 아닌가?"

아니다. 제약조건이 만들어 내는 영역이 Convex해도, <strong>공통 Domain이 비볼록이면 교집합의 볼록성을 보장할 수 없다.</strong> 반대로 Domain이 비볼록하다는 이유만으로 Feasible Set이 반드시 비볼록한 것도 아니다. 우리가 사용하는 표준 판별법에서 보장이 사라진다는 의미다.

예를 들어 다음과 같은 Domain이 지정돼 있다고 하자.

$$
\mathcal D=[-2,-1]\cup[1,2]
$$

부등식은 매우 단순해도 두 구간 사이의 빈 부분은 Domain에서 제외되므로, Feasible Set은 여전히 분리된 두 구간일 수 있다.

$$
x\leq2
$$

Convex Function의 정의 자체가 Convex Domain을 포함한다는 점도 함께 기억한다. 비볼록 Domain에 제한한 함수를 그대로 Convex Function이라고 부를 수는 없다.

따라서 <strong>Domain은 별도의 암묵적 제약조건(Implicit Constraint)</strong> 이다. 다만 LP나 전형적인 QP처럼 Domain이 전체 실수 공간이면 볼록성이 자동으로 성립해 별도 확인이 간단하다.


## 3. Infimum은 있는데 Optimal Point는 없을 수 있다

앞의 최적값 정의에서 <strong>Minimum(최솟값)</strong> 대신 <strong>Infimum(최대하한)</strong>을 쓴 이유를 직접 비교해 보자. Infimum은 가능한 목적함수값 전체의 아래쪽 경계이며, 그 경계에 실제로 도달하는 점이 있어야 Minimum도 존재한다.

| 문제 | Feasible Set | Optimal Value | Optimal Point |
| --- | --- | --- | --- |
| `min x²`, `x ∈ ℝ` | 비어 있지 않음 | 0 | 0 |
| `min x`, `x > 0` | 비어 있지 않음 | 0 | 없음: 0은 허용되지 않음 |
| `min x`, `x ∈ ℝ` | 비어 있지 않음 | −∞ | 없음: 아래로 유계가 아님 |
| `min x²`, `x ≥ 1`과 `x ≤ 0` | 공집합 | +∞로 약속 | 없음: Infeasible |

두 번째 문제에서는 양의 값을 얼마든지 작게 만들 수 있지만 0을 선택할 수 없다. 세 번째 문제의 <strong>Unbounded Below</strong>는 목적함수값을 음의 무한대로 보낼 수 있다는 뜻이다. Feasible Set이 무한히 넓다는 뜻과는 다르다. 첫 번째 문제의 Feasible Set도 전체 실수 공간이지만 최적점은 존재한다.

최적점을 모두 모은 집합은 <strong>Optimal Set</strong>이다.

$$
X_{\mathrm{opt}}=\{x\in D:f_0(x)=p^*\}
$$

이 집합은 비어 있을 수도, 한 점일 수도, 여러 점일 수도 있다. 예를 들어 상수함수를 최소화하면 모든 Feasible Point가 Optimal Point다. 최적점이 실제로 존재해 최적값을 달성하면 <strong>Solvable</strong>하다고 한다. <strong>Feasible과 Solvable은 같은 말이 아니다.</strong>

## 4. Active·Inactive·Redundant Constraint는 무엇이 다를까?

교안과 수업에서 소개한 세 용어는 제약조건을 읽는 서로 다른 질문이다.

$$
\begin{aligned}
f_i(x)=0&\quad\Rightarrow\quad\text{Active at }x\\
f_i(x)<0&\quad\Rightarrow\quad\text{Inactive at }x
\end{aligned}
$$

<strong>Active / Inactive는 특정 Feasible Point에서 판단한다.</strong> 부등식이 경계에 딱 맞으면 Active, 여유를 두고 만족하면 Inactive다. 예를 들어 0 이상 2 이하인 구간에서 상한 제약은 2에서 Active지만 1에서는 Inactive다. Inactive라고 해서 다른 모든 제약까지 무시하고 움직일 수 있다는 뜻은 아니다.

<strong>Redundant(중복된) Constraint는 그 제약을 삭제해도 Feasible Set 전체가 변하지 않는지</strong>를 묻는다.

$$
x\geq0,\qquad x\leq2,\qquad x\leq3
$$

앞의 두 조건만으로 구간이 정해지므로 마지막 조건은 Redundant다. 반면 상한 2는 점 1에서 Inactive여도 삭제하면 구간이 넓어지므로 Redundant가 아니다.

중복된 제약이 항상 Inactive인 것도 아니다. 상한 2를 같은 식으로 두 번 적으면 둘 중 하나는 삭제할 수 있지만, 두 식 모두 점 2에서는 Active다. <strong>Active는 점별 상태, Redundant는 문제 전체의 중복 여부</strong>라고 기억하면 된다. 두 분류를 섞지 않는 것이 중요하다.

## 5. 다음 글로 이어지는 질문

Basic Optimization에서 먼저 확인할 것은 다음과 같다.

1. <strong>무엇을 바꾸는가?</strong> 데이터와 Optimization Variables를 구분한다.
2. <strong>무엇을 좋다고 보는가?</strong> Objective와 Loss를 정한다.
3. <strong>어디에서 선택하는가?</strong> Domain과 Constraints로 Feasible Set을 정한다.
4. <strong>최적값에 도달하는가?</strong> Feasibility, Optimal Value, Optimal Point를 구분한다.
5. <strong>어떤 제약이 경계에 닿거나 중복되는가?</strong> Active와 Redundant를 구분한다.

여기까지는 일반적인 최적화 문제의 언어다. [다음 글의 Convex Optimization](/enai601-convex-optimization/)에서는 이 문제에 볼록성이라는 구조를 더해, Local Minimum이 Global Minimum이 되는 이유와 Gradient로 후보점을 검증하는 방법을 살펴본다.

### 참고 자료

- ENAI601, Richard J. La, *Module 4 — Basic Optimization*, Fall 2026 교안.
- ENAI601 2026년 9월 30일 수업 및 10월 7일의 Basic Optimization 복습 설명.
- 별도로 공부하며 정리한 스터디 노트의 Basic Optimization·Domain·Feasible Set 설명을 중심으로 구성했다. ML 예제와 제약조건의 용어는 교안·수업에서 보충했으며, Infimum 비교표와 제약조건의 수치 예제는 개념 확인을 위해 구성했다.
