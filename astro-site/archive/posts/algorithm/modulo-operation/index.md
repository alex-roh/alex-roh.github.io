---
title:  "나머지(Modular) 연산 및 유용한 정리"
description:
date: 2020-11-29
update: 2020-11-29
tags:
  - algorithm
  - mathematics
series: "수학을 활용한 문제"
---

## 나머지(Moular) 연산

문제에서 종종 ‘**정답을 특정 수로 나눈 나머지는 무엇인가**’라는 표현을 찾아볼 수 있다. 이는 자료형(e.g., int, long long etc)이 저장할 수 있는 범위가 한정되어 있기 때문이다. 즉, 너무 긴 자리의 연산을 시키지 않도록 하기 위해 나머지 값만 물어보는 것이다.


핵심은 **정답을 다 구하고 나머지 연산을 수행하는 게 아니라, 정답이 갱신될 때마다 연산을 수행하는 것**이다. 나머지 연산은 다음과 같은 성질을 지니고 있기 때문이다.

$$A\ mod\ M = (A\ mod\ M)\ mod\ M$$

또한, 나머지 연산은 덧셈과 곱셈에서 다음 정리를 만족한다.

$$(A+B)\ mod\ M=((A\ mod\ M)+(B\ mod\ M))\ mod\ M$$
    
$$(A×B)\ mod\ M=((A\ mod\ M)×(B\ mod\ M))\ mod\ M$$
    
단, 나누기의 경우에는 위와 같은 공식이 성립하지 않는다. ([Modular Inverse](https://ko.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/modular-inverses)를 구해야 한다.) 그러나 **뺄셈의 경우에는 성립**하며, 이 경우에는 각각의 수에 나머지 연산을 먼저 수행한 결과가 음수가 나올 수 있으므로 **M을 더하고 나머지 연산을 수행한다.**
        
$$(A-B)\ mod\ M=((A\ mod\ M)-(B\ mod\ M)+M)\ mod\ M$$
        
뺄셈에 대한 나머지 연산의 예를 들어보면 아래와 같다.
    
$$(6-5)\ mod\ 3=\ 1\ mod\ 3=1$$이라고 할 때,

$$((6\ mod\ 3)-(5\ mod\ 3))\ mod\ 3=(0-2 + 3)\ mod\ 3=1\ mod\ 3=1$$이다.

다만 이때 마지막에 M을 더하지 않고, 음수에 모듈로 연산을 수행하면 어떻게 될까? 정답은 **-2일 수도 있고 1일 수도 있다**는 것이다. 프로그래밍 언어에 따라 결과가 다르다. (e.g., C11, C++14에서는 -2가 출력되고, Java와 Python3에서는 1이 출력된다.)

마지막으로, 뺄셈에도 위 정리가 성립하는 이유는 아래와 같다.

1. $0≤a\ mod\ c <c$이고, $0≤b\ mod\ c<c$이다.
2. 따라서 $$-c<(a\ mod\ c-b\ mod\ c)<c$$이다.
3. 결국 $$(a\ mod\ c-b\ mod\ c+c)$$는 언제나 0보다 크므로, 이 상태에서 다시 $$c$$로 나누면 원하는 결과를 얻을 수 있다.

나머지 연산의 위와 같은 성질을 이용하여 풀어볼 수 있는 문제로는 다음이 있다.

1. [BOJ 4375번 문제 - 1](https://www.acmicpc.net/problem/4375) [(해설)](https://alex-roh.github.io/boj/4375)