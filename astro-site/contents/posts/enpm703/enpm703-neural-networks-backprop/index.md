---
title: "[ENPM703] 01 — 신경망을 처음부터: Affine, ReLU, Loss와 역전파"
description: "이미지와 feature의 구분부터 순전파·손실·역전파까지. dW, db, dX에서 무엇을 곱하고 어느 경로를 합하는지 작은 예제와 NumPy 코드로 이해한다."
date: 2026-10-22
publishedAt: "2026-10-22T21:03:37-04:00"
tags:
  - ENPM703
  - deep-learning
  - neural-networks
  - backpropagation
series: "ENPM703 Deep Learning"
seriesOrder: 1
updatedAt: "2026-10-22T21:07:17-04:00"
---

신경망은 입력 숫자에서 특징을 만들고, 그 특징으로 예측하는 함수를 학습한다. 이미지를 숫자로 펴서 class score를 계산하는 것까지는 행렬곱으로 설명할 수 있다. 학습을 이해하려면 그다음 질문까지 이어져야 한다. **예측이 틀렸을 때, 어떤 weight를 어느 방향으로 바꿔야 할까?**

ENPM703 시리즈의 첫 글은 **입력 → Affine → ReLU → Score → Loss → Backpropagation → Update**를 한 흐름으로 연결한다. 숫자 하나의 계산에서 출발해 mini-batch의 배열 계산으로 확장한다. 읽고 나면 `dW`, `db`, `dX`의 공식을 외우는 대신, 무엇을 곱하고 어떤 경로를 더하는지 설명하는 것이 목표다.

처음 읽을 때는 **1–7절의 순전파**, **8–14절의 역전파 원리**, **15–18절의 구현 연결** 순서로 읽으면 된다. 행렬곱은 한 행과 한 열의 같은 위치 숫자들을 곱해 더하는 계산이고, 편미분은 다른 변수들을 고정한 채 한 변수만 조금 바꿀 때 결과가 얼마나 변하는지 나타내는 값이다. 이 두 계산을 작은 예제로 연결한다.

> **표기 약속:** `N`은 한 번에 처리하는 sample 수, `D`는 sample당 입력 feature 수, `M`은 한 affine layer의 출력 수다. `dX`는 작은 변화량 자체가 아니라 **최종 loss를 X로 미분한 gradient**를 뜻한다. `@`는 행렬곱, `*`와 $\odot$는 같은 위치의 성분끼리 곱하는 연산이다.

## 1. 신경망은 왜 필요한가?

### 출발점: linear classifier

CIFAR-10에는 비행기, 자동차, 고양이 같은 이미지들이 있다. 이미지가 주어지면 모델은 각 class에 대한 **score**를 계산하고, 가장 높은 score를 가진 class를 예측한다.

Linear classifier는 입력 feature들에 weight를 곱해 더한 다음 bias를 더한다.

$$
s = w^T x+b
$$

여기서 입력 feature는 이미지의 pixel values일 수도 있고, 사람이 미리 계산해 놓은 특징(HOG 등)일 수도 있다. **Weight는 어떤 feature가 score에 얼마만큼 기여하는지** 결정한다. Bias는 전체 score를 이동시키는 항이다.

하지만 하나의 linear transformation만으로는 복잡한 class 경계를 자유롭게 표현하기 어렵다. 예를 들어 XOR처럼 단일 직선으로 두 class를 나눌 수 없는 경우가 있다.

입력 특징을 사람이 설계하는 **feature engineering**에서 한 걸음 더 나아가, neural network는 분류에 쓸 중간 특징도 학습한다. 이전처럼 입력을 곧바로 class score로 보내는 대신, 중간에 **derived features(학습된 중간 특징)**를 만드는 것이다.

### 신경망의 아이디어

한 neuron도 기본적으로는 weighted sum과 bias를 계산한다. 새로운 것은 그 다음에 **nonlinear activation function**을 적용한다는 점이다. 여러 neuron을 사용하면 입력을 여러 방향에서 변환한 뒤, 그 결과를 다음 layer에서 다시 조합할 수 있다.

따라서 신경망을 신비한 블랙박스보다는 **익숙한 linear operations와 작은 nonlinear operations를 여러 번 연결한 모델**로 이해하는 편이 쉽다.

---

## 2. 이미지, sample, feature, neuron을 먼저 구분하기

먼저 **training sample 수**, **feature 수**, **neuron 수**를 구분해야 한다. 셋은 배열에서 서로 다른 역할을 한다.

- **Sample:** 학습에 쓰는 이미지 한 장. Mini-batch가 100이면 sample이 100장이다.
- **Feature:** 이미지 한 장을 설명하는 숫자 하나. CIFAR-10 RGB 원본 이미지는 한 장당 3 × 32 × 32 = **3,072 features**다.
- **Neuron / hidden unit:** 해당 layer가 만들어 내는 새로운 출력값 하나. Hidden unit을 100개로 설정하면 이미지 한 장에서 100개의 hidden values가 나온다.
- **Class:** 최종 예측 대상. CIFAR-10의 class 수는 10개다.

Mini-batch 100장을 하나의 배열에 담으면 다음 shape이다.

$$
X:\;(100,3,32,32)
$$

이미지별 픽셀을 한 줄로 펴면:

$$
X_{\mathrm{flat}}:\;(100,3072)
$$

100개 hidden units에 연결하는 weight matrix는:

$$
W_1:\;(3072,100)
$$

첫 affine layer를 통과하면:

$$
Z_1:\;(100,100)
$$

**첫 번째 100은 이미지 수, 두 번째 100은 이미지 한 장에서 만들어진 hidden feature 수**다. 둘이 우연히 같을 뿐 전혀 다른 축이다.

여기서 정말 중요한 사실이 있다.

> 각 sample의 입력값은 서로 다르지만, **같은 layer의 weight와 bias는 mini-batch 모든 sample이 공유한다.**

이 한 문장이 나중에 `dW`와 `db`에서 여러 sample의 gradient contribution을 더하는 이유다.

---

## 3. Affine forward: 입력을 score로 바꾸는 계산

### Scalar부터 시작하기

Feature가 두 개이고 output neuron이 하나라면:

$$
y=x_1w_1+x_2w_2+b
$$

`x1`과 `x2`를 고정했을 때, weight와 bias에 따라 output이 달라진다. 우리가 학습하려는 것은 이 weight와 bias의 적절한 값이다.

여러 입력과 여러 neuron을 한꺼번에 계산할 때는 이 식을 matrix로 바꾼다.

$$
Y=XW+b
$$

**Affine**은 linear transformation에 bias를 더한 형태다. 엄밀하게는 bias가 있으므로 affine이라고 부른다.

### 실제 NumPy 코드 읽기

```python
x_flat = x.reshape(x.shape[0], -1)
out = x_flat @ w + b
cache = (x, w, b)
return out, cache
```

첫 번째 줄의 `x.shape[0]`은 sample 수다. `-1`은 나머지 차원의 크기를 자동 계산하라는 뜻이다. 따라서 CIFAR-10처럼 `(N, 3, 32, 32)`인 배열을 `(N, 3072)`로 바꾼다.

두 번째 줄의 `@`는 matrix multiplication이다. `+ b`는 **broadcasting** 덕분에 같은 bias vector를 모든 sample row에 더한다.

세 번째 줄은 나중에 backward에서 다시 필요한 값을 저장한다. `cache`는 output이 아니라 **forward 당시의 메모**다. 마지막 줄에서 output과 cache를 함께 돌려준다.

일반적인 shape은 다음과 같다.

| 값 | Shape | 의미 |
|---|---|---|
| `x_flat` | `(N, D)` | N개 sample, sample당 D개 features |
| `w` | `(D, M)` | D개 input features를 M개 outputs에 연결 |
| `b` | `(M,)` | output neuron마다 bias 하나 |
| `out` | `(N, M)` | sample마다 M개 outputs |

### 왜 한 neuron이 여러 개 있는 것처럼 보이나?

Output neuron이 M개면 weight matrix의 **각 column**이 하나의 output neuron으로 들어가는 연결 weight들을 담는다(현재 NumPy 코드 기준). 같은 input sample이 여러 column과 dot product하면서 M개의 score를 얻는다.

---

## 4. ReLU: 왜 affine만 반복하면 안 되는가?

두 affine layer를 연속해서 계산하고, 중간에 activation이 없다고 하자.

$$
Z_1=XW_1+b_1
$$

$$
S=Z_1W_2+b_2
$$

첫 식을 대입하면:

$$
S=(XW_1+b_1)W_2+b_2
$$

$$
S=X(W_1W_2)+(b_1W_2+b_2)
$$

결국 **큰 affine transformation 하나로 합쳐진다.** 층을 두 개 쌓은 것만으로는 새로운 비선형 표현력이 생기지 않는다.

그래서 중간에 **activation function**을 넣는다. 여기서는 ReLU를 사용한다.

$$
\operatorname{ReLU}(z)=\max(0,z)
$$

예를 들어:

$$
[-3,2,-1,5]\ \xrightarrow{\operatorname{ReLU}}\ [0,2,0,5]
$$

즉 음수는 0으로, 양수는 그대로 보낸다.

```python
out = np.maximum(0, x)
cache = x
return out, cache
```

왜 입력 `x`를 cache할까? Backward에서는 **forward 당시 입력이 양수였는지** 알아야 하기 때문이다. ReLU는 단순하지만 신경망에 꼭 필요한 nonlinearity를 제공한다.

---

## 5. Two-layer neural network의 전체 forward

이 글에서 말하는 **two-layer network**는 weight를 가진 affine layer가 두 개라는 뜻이다. **Hidden layer는 하나**다. Input layer를 별도의 trainable layer로 세지 않는다.

첫 번째 affine layer:

$$
Z_1=XW_1+b_1
$$

ReLU로 hidden features 생성:

$$
H=\operatorname{ReLU}(Z_1)
$$

두 번째 affine layer로 class scores 생성:

$$
S=HW_2+b_2
$$

최종 score는 아직 확률이 아니다. Softmax를 이용해 loss를 계산할 수 있고, 예측 시 가장 큰 score의 class를 선택할 수 있다.

예를 들어 CIFAR-10에서 hidden unit이 100개라면:

| 값 | Shape |
|---|---|
| `X` | `(N, 3072)` |
| `W1` | `(3072, 100)` |
| `b1` | `(100,)` |
| `H` | `(N, 100)` |
| `W2` | `(100, 10)` |
| `b2` | `(10,)` |
| `scores` | `(N, 10)` |

`fc_net.py`의 forward는 보통 다음 두 단계로 표현된다.

```python
h, cache1 = affine_relu_forward(X, W1, b1)
scores, cache2 = affine_forward(h, W2, b2)
```

`affine_relu_forward`는 새로운 수학을 추가한 함수가 아니라 **affine forward + ReLU forward를 묶어 부르는 편의 함수**다.

---

## 6. Scores에서 Loss까지: SVM과 Softmax

모델이 class scores를 만들었다고 해서 학습이 끝난 것은 아니다. 현재 weight가 얼마나 나쁜지 숫자로 평가해야 한다. 그 숫자가 **loss**다.

### SVM loss

Multiclass SVM은 올바른 class의 score가 다른 class보다 **margin만큼 더 높기를 요구**한다.

$$
L_{\mathrm{SVM}}=\sum_{j\ne y}\max(0,s_j-s_y+1)
$$

Margin 조건을 만족하면 해당 class에 대한 penalty는 0, 위반하면 penalty가 생긴다. 여기서 `svm_loss` 함수에 들어가는 `x`라는 이름은 원본 이미지가 아니라 **이미 계산된 score matrix**라는 점을 주의하자.

### Softmax loss

여기서는 **softmax + cross-entropy**를 사용한다.

먼저 score들을 class probability로 바꾼다.

$$
p_c=\frac{e^{s_c}}{\sum_k e^{s_k}}
$$

Correct class의 probability가 높을수록 loss가 작아지게 만든다.

$$
L_{\mathrm{sample}}=-\log p_{\mathrm{correct}}
$$

Mini-batch에서는 각 sample loss를 평균낸다.

$$
L_{\mathrm{data}}=\frac{L_1+L_2+\cdots+L_N}{N}
$$

실제 `softmax_loss` 구현은 먼저 각 row의 최대 score를 빼서 exponential overflow를 방지한다. 모든 score에서 같은 값을 빼도 softmax probability는 변하지 않는다.

```python
shifted = x - np.max(x, axis=1, keepdims=True)
```

중요한 건 `softmax_loss`가 **loss 값만 주는 것이 아니라 score에 대한 gradient도 반환한다**는 사실이다. 그 gradient가 신경망 전체 backward의 출발점이 된다.

SVM과 softmax는 **모델의 weight 구조 자체가 아니라 scores를 평가하는 서로 다른 loss 설계**라고 이해하면 된다.

---

## 7. Loss를 계산한 뒤에는 왜 gradient가 필요한가?

우리의 목표는 단순히 loss를 측정하는 데 있지 않다. **Loss가 작아지도록 weight와 bias를 바꿔야 한다.**

Gradient는 현재 parameter를 조금 움직였을 때 loss가 어떻게 변하는지를 알려준다. **Gradient descent**는 그 gradient의 반대 방향으로 parameter를 업데이트한다.

$$
W_{\mathrm{new}}=W_{\mathrm{old}}-\eta\frac{\partial L}{\partial W}
$$

여기서 learning rate는 한 번에 얼마나 움직일지를 조절한다.

Weight가 수십만 개라면 모든 weight의 gradient가 필요하다. 그 수많은 미분을 일일이 처음부터 계산하지 않고, **작은 계산 단위로 쪼개서 거꾸로 전달하는 방법**이 backpropagation이다.

---

## 8. Backpropagation: upstream × local, 그리고 여러 경로의 합

처음에는 거대한 신경망 대신 아주 작은 연산 하나만 보자.

$$
q=x+y
$$

$$
f=qz
$$

Loss 역할을 하는 최종 결과가 `f`이고, 우리가 `x`의 영향을 알고 싶다고 하자. `x`는 직접 `f`에 들어가지 않지만 `q`를 거쳐 영향을 준다. 그래서 chain rule을 쓴다.

$$
\frac{\partial f}{\partial x}
=
\frac{\partial f}{\partial q}
\frac{\partial q}{\partial x}
$$

앞에 있는 값은 뒤쪽에서 돌아온 **upstream gradient**, 뒤에 있는 값은 지금 연산의 **local gradient**다.

$$
\text{gradient passed backward}
=
\text{upstream gradient}\times\text{local derivative}
$$

그런데 하나의 변수가 **여러 계산 경로로** 최종 loss에 영향을 줬다면 어떻게 될까?

각 경로에서 chain rule로 contribution을 계산한 다음, **같은 변수에 대한 contribution을 전부 더한다.**

$$
\frac{\partial L}{\partial x}
=g_1+g_2+g_3+\cdots
$$

여기서 `g1`은 upstream 자체가 아니라 **해당 경로의 upstream × local derivative까지 완료한 contribution**이라고 정의한다. 이 구분을 지켜야 한다. 이미 `g1` 안에 local derivative를 곱해 놓고 마지막에 weight를 또 곱하면 잘못된 계산이 된다.

> **역전파의 핵심:** 여러 경로마다 **upstream × local**을 구한 후, 그것들이 **같은 변수로 돌아오면 합한다.** Matrix multiplication은 이 곱과 합을 한꺼번에 계산할 뿐이다.

---

## 9. 왜 forward에서 cache를 저장하나?

Affine forward를 다시 보자.

$$
Y=XW+b
$$

뒤에서 loss에 대한 gradient가 돌아왔을 때 weight, input, bias 각각에 대한 gradient를 계산해야 한다.

아주 작은 scalar 식으로 보면:

$$
y=xw+b
$$

Weight에 대한 local derivative:

$$
\frac{\partial y}{\partial w}=x
$$

Input에 대한 local derivative:

$$
\frac{\partial y}{\partial x}=w
$$

Bias에 대한 local derivative:

$$
\frac{\partial y}{\partial b}=1
$$

따라서 **weight gradient를 계산하려면 forward 당시의 input이 필요하고**, **input gradient를 계산하려면 forward 당시의 weight가 필요하다.**

그래서 다음처럼 저장한다.

```python
cache = (x, w, b)
```

실제로 이 구현의 `affine_backward`에서는 `b`의 값을 계산에 직접 사용하지 않는다. Bias의 local derivative는 항상 1이기 때문이다. 그럼에도 forward 인자 전체를 저장하면 일관된 인터페이스를 유지할 수 있다.

원래 `x`의 shape도 기억해야 한다. Forward에서 flatten했지만, backward에서 돌려주는 `dx`는 **원래 입력과 같은 shape**이어야 하기 때문이다.

정리하면:

- `out`은 **다음 layer로 보내는 결과**다.
- `cache`는 **현재 layer가 나중에 backward할 때 쓸 정보**다.
- `dout`은 **뒤쪽 layer에서 나중에 도착한 upstream gradient**다.

---

## 10. `dW`: 왜 여러 sample의 기여를 더하나?

Weight가 여러 sample에 함께 쓰인다는 사실을 미분과 연결해 보자.

> “Weight는 샘플마다 같은 거니까, 여러 sample이 만드는 loss에 동시에 영향을 주겠네?”

정확하다. Mini-batch 안에서 sample A와 sample B는 서로 다른 입력을 갖지만 **같은 weight**를 쓴다.

일단 neuron 하나, weight 하나만 보자.

$$
y_A=x_Aw+b
$$

$$
y_B=x_Bw+b
$$

Batch 전체 loss는 평균이다.

$$
L=\frac{L_A+L_B}{2}
$$

우리가 구하려는 것은 **전체 loss를 현재 weight에 대해 미분한 것**이다.

$$
\frac{\partial L}{\partial w}
=
\frac{1}{2}
\left(
\frac{\partial L_A}{\partial w}
+
\frac{\partial L_B}{\partial w}
\right)
$$

왜 합할까? **전체 loss 자체가 각 sample loss의 평균**이기 때문이다. 같은 weight를 움직이면 A의 loss도 B의 loss도 바뀐다.

그다음 각 sample의 contribution을 따로 구한다.

**Sample A — upstream × local**

$$
g_A
=
\frac{\partial L_A}{\partial y_A}
\frac{\partial y_A}{\partial w}
=
\frac{\partial L_A}{\partial y_A}x_A
$$

**Sample B — upstream × local**

$$
g_B
=
\frac{\partial L_B}{\partial y_B}
\frac{\partial y_B}{\partial w}
=
\frac{\partial L_B}{\partial y_B}x_B
$$

따라서:

$$
\boxed{
\frac{\partial L}{\partial w}
=
\frac{g_A+g_B}{2}
}
$$

Sample이 더 많으면:

$$
\frac{\partial L}{\partial w}
=
\frac{g_1+g_2+\cdots+g_N}{N}
$$

이것이 **하나의 weight가 여러 sample에서 공유되는 경우**, gradient contribution을 sample 방향으로 합하는 이유다.

### 그런데 코드에는 왜 `+`가 안 보일까?

NumPy에서는 matrix multiplication의 `@` 연산 자체가 **multiply-and-add**를 수행한다.

샘플 두 개와 입력 feature 두 개로 축소해 보자. Output neuron은 하나다.

$$
X=
\begin{bmatrix}
2 & 3\\
4 & 5
\end{bmatrix}
$$

그리고 `dout`에 각 sample의 **평균 loss 기준 upstream gradient**가 들어 있다고 하자.

$$
dY=
\begin{bmatrix}
10\\
20
\end{bmatrix}
$$

첫 번째 weight gradient는 **첫 번째 feature의 sample별 기여분을 합한 것**이다.

$$
dw_1=2(10)+4(20)=100
$$

두 번째 weight는:

$$
dw_2=3(10)+5(20)=130
$$

이걸 행렬곱으로 동시에 하면:

$$
X^TdY
=
\begin{bmatrix}
2 & 4\\
3 & 5
\end{bmatrix}
\begin{bmatrix}
10\\
20
\end{bmatrix}
=
\begin{bmatrix}
100\\
130
\end{bmatrix}
$$

즉 `@` **안에 이미 곱셈과 덧셈이 들어 있다.** 그래서 Python에 `+`나 `sum()`이 따로 보이지 않는다.

일반적으로 다음과 같이 쓴다.

$$
\boxed{dW=X^TdY}
$$

```python
dw = x_flat.T @ dout
```

**주의:** 위 숫자 예제의 `dY`를 **이미 평균 loss의 미분값**으로 놓았다. 일반적인 `softmax_loss`도 gradient를 마지막에 batch size로 나눈다. 따라서 그 뒤의 `affine_backward`에서 다시 나누지 않는다. 평균을 두 번 적용하면 틀린다.

---

## 11. `db`: 왜 bias gradient는 `sum(axis=0)`인가?

이제 같은 방식으로 bias 하나를 보자.

$$
y_A=x_Aw+b
$$

$$
y_B=x_Bw+b
$$

전체 loss에 대한 bias gradient는:

$$
\frac{\partial L}{\partial b}
=
\frac{1}{2}
\left(
\frac{\partial L_A}{\partial b}
+
\frac{\partial L_B}{\partial b}
\right)
$$

Sample A의 경로를 chain rule로 계산한다.

$$
g_A
=
\frac{\partial L_A}{\partial y_A}
\frac{\partial y_A}{\partial b}
$$

그런데 bias는 단순히 더해졌으므로:

$$
\frac{\partial y_A}{\partial b}=1
$$

따라서:

$$
g_A=\frac{\partial L_A}{\partial y_A}
$$

Sample B도 동일하다.

$$
g_B=\frac{\partial L_B}{\partial y_B}
$$

같은 bias 하나가 두 sample에 쓰이므로 contribution을 더한다.

$$
\boxed{
\frac{\partial L}{\partial b}
=
\frac{g_A+g_B}{2}
}
$$

즉 `dW`와 원리가 똑같다. 다만 **bias의 local derivative는 1**이라 input을 곱하는 과정이 없다.

```python
db = dout.sum(axis=0)
```

여기서 `axis=0`은 **sample 방향**이다. `(N, M)` 크기의 upstream을 sample 방향으로 더하면 output neuron마다 bias gradient 하나씩 남아서 `(M,)`이 된다.

**`db`만 더하는 것이 아니다.** `dW`도 sample에 대해 합한다. 다만 `dW`의 합은 `@`에 숨어 있고, `db`는 `sum()`으로 눈에 보일 뿐이다.

---

## 12. `dX`: 왜 입력 gradient는 다른 방향으로 합할까?

이번에는 입력 feature 하나로 돌아오는 경로를 살펴보자.

> “입력 하나는 여러 output에 영향을 줬잖아? 그러면 각 output에서 오는 gradient를 전부 합해야 하는 거 아닌가?”

**맞다. 이것이 `dX`의 핵심이다.**

이번에는 **sample 하나만** 보자. 그 sample의 입력 feature 하나를 `x`라고 하고, output neuron 세 개에 모두 연결되어 있다고 하자. 다른 feature들의 기여는 생략한다.

$$
y_1=xw_1+\cdots+b_1
$$

$$
y_2=xw_2+\cdots+b_2
$$

$$
y_3=xw_3+\cdots+b_3
$$

입력 `x` 하나가 **세 output 모두에 영향을 준다.**

우리는 전체 loss를 `x`에 대해 미분하고 싶다.

먼저 각 output path에서 `x`로 돌아오는 gradient contribution을 정의한다.

**첫 번째 output 경로:**

$$
g_1
=
\frac{\partial L}{\partial y_1}
\frac{\partial y_1}{\partial x}
=
\frac{\partial L}{\partial y_1}w_1
$$

**두 번째 output 경로:**

$$
g_2
=
\frac{\partial L}{\partial y_2}
\frac{\partial y_2}{\partial x}
=
\frac{\partial L}{\partial y_2}w_2
$$

**세 번째 output 경로:**

$$
g_3
=
\frac{\partial L}{\partial y_3}
\frac{\partial y_3}{\partial x}
=
\frac{\partial L}{\partial y_3}w_3
$$

여기서 `g1`, `g2`, `g3`는 각각 **upstream과 local derivative를 이미 곱해 놓은 값**이다. 같은 `x`에 대한 기여분이므로 마지막에 더한다.

$$
\boxed{
\frac{\partial L}{\partial x}=g_1+g_2+g_3
}
$$

바로 이 방식으로 계산하면 무작정 matrix 공식을 외우지 않아도 된다.

값을 풀어서 쓰면:

$$
\frac{\partial L}{\partial x}
=
\frac{\partial L}{\partial y_1}w_1
+
\frac{\partial L}{\partial y_2}w_2
+
\frac{\partial L}{\partial y_3}w_3
$$

즉 **하나의 input이 영향을 준 모든 output 경로의 `upstream × weight`를 더한다.**

이 계산을 모든 sample, 모든 input feature에 대해 matrix로 한 번에 하면:

$$
\boxed{dX=dYW^T}
$$

```python
dx = (dout @ w.T).reshape(x.shape)
```

### 왜 `dX`는 sample끼리 더하지 않나?

각 sample의 **입력은 별개의 값**이다. Sample A의 input gradient와 sample B의 input gradient를 섞어 하나로 만들면 안 된다.

$$
dX=
\begin{bmatrix}
dX_A\\
dX_B\\
\vdots
\end{bmatrix}
$$

**`dX`에서는 한 sample 안의 여러 output 경로를 합한다.** 반면 **`dW`와 `db`에서는 같은 parameter가 여러 sample에서 공유되므로 sample 방향으로 합한다.**

그리고 첫 layer의 raw image input `dX`가 계산되더라도, 기본적인 supervised training에서는 그 image pixels를 optimizer가 학습 parameter처럼 업데이트하는 것이 아니다. `dX`는 이전 layer가 있다면 그쪽으로 전달할 gradient이고, 학습되는 주된 parameter는 weight와 bias다.

---

## 13. 왜 transpose가 붙을까? 공식보다 shape 먼저 보기

여기까지 오면 matrix 공식은 **새로운 수학 규칙이 아니라 앞에서 계산한 합을 묶어 쓴 표기**라는 걸 알 수 있다.

이 글의 NumPy 표기는 **각 sample을 row로 저장**한다.

$$
X:(N,D),\quad W:(D,M),\quad Y:(N,M)
$$

Upstream은 output과 같은 shape다.

$$
dY:(N,M)
$$

### Weight gradient

Weight와 같은 shape의 결과가 필요하다.

$$
X^T:(D,N)
$$

$$
\underbrace{X^T}_{(D,N)}
\underbrace{dY}_{(N,M)}
\;\longrightarrow\;
\underbrace{dW}_{(D,M)}
$$

그래서:

$$
\boxed{dW=X^TdY}
$$

반대로 upstream을 먼저 transpose해서 곱할 수도 있다.

$$
dY^TX=(dW)^T
$$

즉 그 계산도 정보를 담고 있지만 **원래 `W`와 반대 shape**으로 나온다. 최종 `dW`를 얻으려면 한 번 더 transpose해야 한다.

### Input gradient

원래 input과 같은 shape이 필요하다.

$$
\underbrace{dY}_{(N,M)}
\underbrace{W^T}_{(M,D)}
\;\longrightarrow\;
\underbrace{dX}_{(N,D)}
$$

따라서:

$$
\boxed{dX=dYW^T}
$$

### Bias gradient

각 output neuron에 하나의 bias만 있다.

$$
dY:(N,M)
$$

Sample 차원을 합치면:

$$
\boxed{db:\;(M,)}
$$

### 한눈에 비교

| Gradient | 행렬/배열 계산 | 합쳐지는 경로 | 최종 shape |
|---|---|---|---|
| `dW` | `x_flat.T @ dout` | 여러 sample의 같은 weight | `(D, M)` |
| `db` | `dout.sum(axis=0)` | 여러 sample의 같은 bias | `(M,)` |
| `dX` | `dout @ w.T` | 한 sample의 여러 output paths | `(N, D)` |

**중요한 notation 차이:** 자료에 따라 sample 하나를 column vector로 놓고 `Wx` 형태로 설명하기도 한다. 이 글에서는 sample이 row이고 `X @ W`로 계산한다. 따라서 다른 자료와 이 글 사이에서 weight matrix 방향이 바뀔 수 있다. **의미는 같은 affine transformation이지만, transpose 위치를 외울 때는 어떤 convention을 사용하는지 먼저 확인해야 한다.**

또 하나의 엄밀한 주의점: 위의 **local derivative = X 또는 W**라는 표현은 scalar 예제로 설명할 때 직관적으로 유용하다. Matrix-to-matrix derivative를 엄밀하게 쓰면 Jacobian이라는 더 큰 구조가 등장한다. 그러나 실제 구현은 그 거대한 Jacobian을 만들지 않고 위의 matrix products로 계산한다.

---

### 과제 코드에서 세 gradient를 함께 읽기

`layers.py`의 `affine_backward`에서 초기 placeholder와 안내 주석을 덜어내면 아래 계산이 남는다. `import numpy as np`가 되어 있다고 가정한다.

```python
def affine_backward(dout, cache):
    x, w, b = cache
    x_flat = x.reshape(x.shape[0], -1)
    dw = x_flat.T @ dout
    dx = (dout @ w.T).reshape(x.shape)
    db = dout.sum(axis=0)
    return dx, dw, db
```

`dw`는 입력값을 곱해 sample 방향으로 합하고, `db`는 local derivative가 1이라 upstream만 sample 방향으로 합한다. `dx`는 output 방향으로 합한 뒤 forward 이전 입력 shape로 복구한다. **세 계산 모두 같은 최종 loss를 미분한다. 합하는 축이 다른 이유는 미분 대상이 다르기 때문이다.**

Notebook의 affine backward 확인 셀은 numerical gradient와 이 세 값을 비교한다. 저장된 출력은 `dx` 약 $5.40\times10^{-11}$, `dw` 약 $9.90\times10^{-11}$, `db` 약 $2.41\times10^{-11}$의 상대 오차다. 이는 Notebook에 남아 있는 실행 기록이며, 아래에서 설명하는 numerical gradient는 입력을 아주 조금씩 바꿔 출력 변화를 측정해 analytic gradient와 비교하는 방법이다.

---

## 14. ReLU backward와 softmax gradient가 어떻게 붙는가?

### ReLU backward

ReLU의 local derivative는 입력값이 양수일 때 1, 음수일 때 0이다. 정확히 0인 점에서는 수학적으로 미분 가능하지 않지만, 아래 구현에서는 그 지점의 backward 값을 0으로 정한다.

$$
\frac{d}{dz}\operatorname{ReLU}(z)
=
\begin{cases}
1,&z>0\\
0,&z<0
\end{cases}
$$

따라서 뒤에서 들어온 upstream gradient를 그대로 통과시키거나 0으로 막는다.

```python
dx = dout * (x > 0)
```

`(x > 0)`은 Boolean mask다. Forward 입력을 cache했던 이유가 여기서 바로 드러난다.

### Softmax loss가 주는 첫 upstream gradient

Softmax + cross-entropy의 score gradient는 간단한 형태로 정리된다.

$$
\frac{\partial L_{\mathrm{sample}}}{\partial s_c}
=
p_c-\mathbf{1}[c=y]
$$

즉 incorrect class 위치에는 확률이 남고, correct class 위치에서는 확률에서 1을 뺀다. Mini-batch 평균 loss라면 전체를 sample 수로 나눈다.

실제 구현 핵심은 다음과 같다.

```python
dx = np.exp(log_probs)
dx[rows, y] -= 1
dx /= N
```

이렇게 나온 score gradient를 마지막 affine backward에 **upstream**으로 전달한다.

---

### 과제의 softmax 함수: 생략했던 중간값까지 연결하기

```python
def softmax_loss(x, y):
    N = x.shape[0]
    rows = np.arange(N)
    shifted = x - np.max(x, axis=1, keepdims=True)
    log_probs = shifted - np.log(
        np.sum(np.exp(shifted), axis=1, keepdims=True)
    )
    loss = -np.mean(log_probs[rows, y])
    dx = np.exp(log_probs)
    dx[rows, y] -= 1
    dx /= N
    return loss, dx
```

여기의 `x`는 이미지가 아니라 `(N,C)` 크기의 **score matrix**다. `y`는 `(N,)` 크기의 정수 정답 label이며, class 번호는 0부터 시작한다. `rows`와 `y`를 함께 사용하면 각 sample에서 정답 class의 값 하나씩을 고른다.

`log_probs`는 softmax 확률의 로그다. 먼저 확률을 만든 뒤 아주 작은 확률에 로그를 취하는 대신, 로그 형태를 직접 계산한다. `np.exp(log_probs)`로 확률을 얻고, 정답 위치에서 1을 뺀 뒤 **이 함수에서만** `N`으로 나눈다. 반환된 `dx`가 다음 절의 `dS`, 즉 `dscores`다.

---

## 15. 두 개의 affine layer를 끝까지 역전파하기

이제 `fc_net.py`의 forward를 알고 있다는 전제에서 전체 backward를 읽어 보자.

### Forward에서 한 일

첫 번째 layer:

$$
Z_1=XW_1+b_1
$$

Hidden activation:

$$
H=\operatorname{ReLU}(Z_1)
$$

최종 score:

$$
S=HW_2+b_2
$$

마지막에 softmax loss를 계산한다.

### Backward에서는 반대 순서

**첫째.** Softmax loss가 score gradient를 돌려준다.

$$
dS=\frac{\partial L}{\partial S}
$$

**둘째.** 두 번째 affine backward가 세 gradient를 계산한다.

$$
dW_2=H^TdS
$$

$$
db_2=\sum_{\mathrm{samples}}dS
$$

$$
dH=dSW_2^T
$$

여기서 `dH`는 끝이 아니다. **첫 번째 layer 쪽으로 전달할 upstream gradient**다.

**셋째.** ReLU backward가 gradient를 통과시키거나 0으로 막는다.

$$
dZ_1=dH\odot\mathbf{1}[Z_1>0]
$$

**넷째.** 첫 번째 affine backward로 내려간다.

$$
dW_1=X^TdZ_1
$$

$$
db_1=\sum_{\mathrm{samples}}dZ_1
$$

$$
dX=dZ_1W_1^T
$$

이것이 two-layer network의 backpropagation이다. 여러 계층처럼 보여도 각 함수가 하는 일은 변하지 않는다.

코드에서 `cache2`를 먼저 꺼내고 `cache1`을 나중에 쓰는 이유도 **forward의 역순**이기 때문이다.

---

### `TwoLayerNet.loss`의 핵심 구간

다음은 과제 소스의 `loss` 메서드에서 순전파·역전파 부분만 뽑은 것이다. `self.params`에 `W1`, `b1`, `W2`, `b2`가 준비되어 있고, affine·ReLU helper 함수가 import된 문맥에서 읽는다.

```python
W1, b1 = self.params["W1"], self.params["b1"]
W2, b2 = self.params["W2"], self.params["b2"]

h, cache1 = affine_relu_forward(X, W1, b1)
scores, cache2 = affine_forward(h, W2, b2)
if y is None:
    return scores

loss, dscores = softmax_loss(scores, y)
loss += 0.5 * self.reg * (np.sum(W1 * W1) + np.sum(W2 * W2))

dh, dW2, db2 = affine_backward(dscores, cache2)
dX, dW1, db1 = affine_relu_backward(dh, cache1)

grads = {}
grads["W1"] = dW1 + self.reg * W1
grads["b1"] = db1
grads["W2"] = dW2 + self.reg * W2
grads["b2"] = db2
return loss, grads
```

`y is None`이면 정답과 비교하지 않고 score만 반환한다. 정답이 주어지면 loss와 gradient를 계산한다. **Forward에는 `cache1 → cache2`, backward에는 `cache2 → cache1`이 쓰인다.** `dh`가 첫 번째 layer로 들어가는 upstream이고, `dX`는 원본 입력까지 되돌아온 gradient다.

`affine_relu_backward` 안에서는 아래처럼 ReLU를 먼저, affine을 나중에 되돌린다.

```python
fc_cache, relu_cache = cache
da = relu_backward(dout, relu_cache)
dx, dw, db = affine_backward(da, fc_cache)
```

Loss와 weight gradient에 함께 들어간 `self.reg` 항은 다음 절에서 연결한다.

---

## 16. Regularization과 실제 weight update

위에서 계산한 gradient는 기본적으로 **data loss의 영향**이다. L2 regularization을 사용한다면 loss에 추가 항이 들어간다.

$$
L_{\mathrm{total}}
=
L_{\mathrm{data}}
+
\frac{\lambda}{2}
\left(\lVert W_1\rVert_F^2+\lVert W_2\rVert_F^2\right)
$$

이때 weight gradient에도 regularization term이 추가된다.

$$
dW_1^{\mathrm{total}}=dW_1^{\mathrm{data}}+\lambda W_1
$$

$$
dW_2^{\mathrm{total}}=dW_2^{\mathrm{data}}+\lambda W_2
$$

여기서는 bias에 L2 penalty를 적용하지 않는다. 따라서 bias gradient에는 위 regularization term이 추가되지 않는다.

구현에서는 **loss·gradient 계산**과 **parameter update**를 구분한다. Network와 Solver로 역할을 나누는 구조라면 network가 loss와 gradients를 반환하고, Solver가 optimizer를 호출해 parameter를 업데이트한다.

Vanilla SGD에서는:

$$
W_{\mathrm{new}}=W_{\mathrm{old}}-\eta dW
$$

```python
w = w - learning_rate * dw
```

그다음 새로운 mini-batch로 forward → loss → backward → update 과정을 반복한다.

Dataset이 천만 장이어도 **매 update마다 천만 장 전부를 사용해야 하는 것은 아니다.** 예를 들어 mini-batch 100장에 대해서만 loss/gradient를 계산하고 update한 다음 다음 batch로 넘어갈 수 있다. 이것이 mini-batch SGD의 핵심이다.

---

### Notebook에서 실제 학습을 시작하는 부분

`two_layer_net.ipynb`에서 사용한 SGD 학습 호출이다. CIFAR-10 전처리를 마친 `data`와 `TwoLayerNet`, `Solver` import가 필요한 코드다.

```python
model = TwoLayerNet(32 * 32 * 3, 50, 10)
solver = Solver(
    model,
    data,
    update_rule="sgd",
    optim_config={"learning_rate": 1e-3},
    lr_decay=0.95,
    num_epochs=10,
    batch_size=100,
    print_every=100,
)
solver.train()
```

입력 3,072개에서 hidden feature 50개를 만들고 class score 10개를 출력한다. `batch_size=100`은 한 update에 사용할 sample 수, `learning_rate`는 parameter를 움직이는 크기다. Epoch는 훈련 데이터 한 번 분량을 처리하는 단위이며, 이 Solver는 epoch 경계에서 learning rate에 `lr_decay`를 곱한다.

`solver.train()`이 호출되면 mini-batch 선택 → `model.loss(X_batch, y_batch)` → gradient로 parameter update를 반복한다. **`model.loss`를 한 번 호출하는 것과 모델 학습을 끝내는 것은 다르다.** 이 설정은 당시 실험을 읽기 위한 예이며, 항상 가장 좋은 설정이라는 뜻은 아니다.

---

## 17. `FullyConnectedNet`: 같은 계산을 여러 층으로 확장하기

`TwoLayerNet`은 첫 번째 affine + ReLU, 마지막 affine + softmax loss라는 고정된 구조였다.

`FullyConnectedNet`은 원리를 바꾸는 것이 아니라 **같은 building blocks를 원하는 수만큼 반복하는 과제**다.

예를 들어 hidden dimensions를 `[100, 100]`으로 지정하면 hidden layer 둘과 마지막 output affine 하나가 생긴다. 그래서 course convention으로는 **three-layer network**라고 부른다.

핵심은 네 가지다.

1. 각 layer에 맞는 `W`, `b`를 초기화한다.
2. Forward에서 affine/ReLU를 반복하고 **layer별 cache를 순서대로 저장**한다.
3. 최종 score로 softmax loss를 계산한다.
4. Backward에서는 **cache를 역순으로** 꺼내면서 `dW`, `db`를 저장하고, `dX`를 다음 이전 layer의 upstream으로 전달한다.

`fc_net.py`에서 `for` loop로 여러 층을 처리하는 것은 복잡한 수학이 추가돼서가 아니다. **고정된 두 계층을 일반적인 개수의 계층으로 확장했기 때문**이다.

Momentum, RMSProp, Adam은 **gradient를 계산하는 규칙이 아니라, 계산된 gradient로 parameter를 업데이트하는 방식의 차이**다. 이 글에서 backpropagation의 원리를 먼저 마친 이유가 바로 여기에 있다.

---

## 18. 구현 순서와 이해 확인

### 코드를 작성할 때의 순서

1. **배열의 shape를 먼저 적는다.** 입력 `(N,D)`, hidden `(N,H)`, score `(N,C)`를 구분하고 weight·bias shape를 정한다.
2. **작은 연산부터 연결한다.** Affine forward와 ReLU forward를 연결하고 각 연산의 cache를 남긴다.
3. **Loss와 score gradient를 계산한다.** 평균 loss의 `1/N`을 어디에 적용하는지 한 곳으로 정한다.
4. **Forward의 역순으로 backward한다.** 마지막 affine → ReLU → 첫 affine 순서로 upstream을 넘긴다. 각 gradient의 shape는 미분 대상과 같아야 한다.
5. **L2 항을 loss와 gradient 양쪽에 넣는다.** $\lambda\lVert W\rVert_F^2/2$를 더했다면 weight gradient에는 $\lambda W$를 더한다.
6. **Optimizer가 parameter를 갱신한다.** Cache를 사용하는 backward가 끝나기 전에 weight를 바꾸지 않는다.

실제 함수의 인자·반환값·정규화 계수는 사용하는 코드의 인터페이스에 맞춰야 한다.

### 한 줄씩 기억할 핵심

- **Affine forward:** feature에 weight를 곱하고 bias를 더해서 output을 만든다.
- **ReLU:** 중간에 nonlinearity를 넣는다.
- **Loss:** 현재 score가 정답과 얼마나 맞지 않는지 계산한다.
- **Gradient:** parameter가 바뀔 때 최종 loss가 얼마나 변하는지를 나타낸다.
- **Chain rule:** 한 경로에서는 upstream gradient × local derivative.
- **Branch sum:** 같은 변수로 돌아오는 여러 경로의 gradient contributions는 더한다.
- **`dW`:** 같은 weight를 여러 sample이 공유하므로 sample별 contribution을 더한다.
- **`db`:** 같은 bias를 여러 sample이 공유하고 local derivative가 1이므로 upstream을 sample 방향으로 더한다.
- **`dX`:** 하나의 input이 여러 outputs에 영향을 줬으므로 그 output 경로들의 contribution을 더한다. **서로 다른 sample의 inputs는 합치지 않는다.**
- **Transpose:** 현재 코드에서 sample을 row로 저장하므로 matrix multiplication의 shape가 맞게 배치하는 것이다.
- **Cache:** backward에 필요한 forward 당시의 input/weight/activation 정보를 저장한다.
- **SGD:** 구한 parameter gradient를 이용해 loss가 줄어드는 방향으로 weight를 업데이트한다.

### 필기용 세 공식

$$
\boxed{dW=X^TdY}
$$

$$
\boxed{db=\sum_{\mathrm{samples}}dY}
$$

$$
\boxed{dX=dYW^T}
$$

이 공식 자체보다 **합산이 왜 생기는지**가 더 중요하다.

### 스스로 확인할 질문

**Q1.** 이미지가 두 장일 때 왜 첫 번째 이미지와 두 번째 이미지가 **하나의 weight**에 대한 gradient를 각각 만들까?  
**답:** 두 이미지가 그 weight를 공유하고, 전체 loss가 두 이미지 loss의 합 또는 평균이기 때문이다.

**Q2.** `dW = X.T @ dout`에는 `sum`이 없는데 왜 sample contribution이 더해질까?  
**답:** Matrix multiplication 자체가 row와 column의 corresponding elements를 곱한 뒤 더하는 연산이기 때문이다.

**Q3.** 왜 `db = dout.sum(axis=0)`에는 input 값이나 bias 값이 곱해지지 않을까?  
**답:** Bias의 local derivative는 1이므로 각 sample의 upstream contribution만 남는다.

**Q4.** 왜 `dX`는 sample마다 나뉜 row를 그대로 유지할까?  
**답:** 각 sample의 input은 서로 다른 변수이기 때문이다. 대신 하나의 input이 연결된 **여러 output neuron 방향**으로 gradient를 더한다.

**Q5.** 왜 `affine_backward`는 `dx`, `dw`, `db` 세 개를 반환할까?  
**답:** Affine forward의 입력인 `x`, `w`, `b` 각각에 대한 최종 loss gradient가 필요하기 때문이다. 이 중 `dw`와 `db`는 학습 parameter를 업데이트하는 데 쓰이고, `dx`는 앞선 layer로 gradient를 전달한다.

**Q6.** 왜 softmax loss 뒤의 `affine_backward`에서는 또 batch size로 나누지 않을까?  
**답:** Softmax loss에서 이미 평균 loss를 미분하며 `1/N`이 gradient에 반영되었기 때문이다.

### 이 글에서 의도적으로 다루지 않은 내용

- 깊은 network의 학습 안정성, initialization, vanishing/exploding gradients
- Momentum, RMSProp, Adam의 세부 update equations
- Batch normalization, dropout, convolution
- 모든 경우에 적용되는 일반 Jacobian 계산

이 항목들은 **`dW`, `db`, `dX`가 왜 이렇게 계산되는지 설명할 수 있는 다음**에 공부하는 편이 훨씬 수월하다.

---

## 출처와 설명 범위

제공된 개인 학습 노트 **「신경망을 처음부터 다시 이해하기: Affine, ReLU, Loss, Backpropagation」**을 바탕으로 독립적인 설명문으로 재구성했다. 원본의 sample·feature 구분, affine gradient의 경로별 유도, ReLU, softmax, L2 regularization, 다층 확장의 범위를 유지했다.

코드 연결에는 추가로 제공된 `Python Notebooks/two_layer_net.ipynb`, `FullyConnectedNets.ipynb`와, 구현이 들어 있는 `assignment1-part2/assignment1/cs231n/`의 `layers.py`, `layer_utils.py`, `classifiers/fc_net.py`를 참고했다. 코드 발췌에서는 과제 안내 주석과 placeholder를 생략했다. Notebook의 저장된 출력은 실행 기록으로 구분했으며, 전체 CIFAR-10 학습을 이번 글 작성 과정에서 다시 실행하지 않았다.

원본 노트는 ENPM703의 *Module 05a — Neural Networks*, *Module 05b — Back Propagation*, 2026년 10월 1일·8일 강의 캡션과 `layers.py`, `fc_net.py`, `optim.py`를 참고 자료로 적고 있다. 슬라이드·강의 캡션과 현재 과제 전체 요구사항은 이번 글에서 별도로 대조하지 않았다. 특정 과제의 최신 요구사항이나 채점 기준보다는 그 코드를 이해하기 위한 기초를 설명한다.

Batch normalization, dropout, convolution과 Momentum·Adam의 세부 계산은 이 글의 범위에 포함하지 않는다.
