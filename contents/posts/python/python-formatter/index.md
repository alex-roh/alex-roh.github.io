---
title: "파이썬 포매터 : Black"
description:
date: 2022-06-10
update: 2022-06-11
tags:
  - python
series: "파이썬 문법"
---

## 포매터 사용법 (formatter)

포매터 [black](https://black.readthedocs.io/en/stable/index.html)을 사용하면 띄어쓰기와 같은 사소한 규칙들은 무시하고 코드의 내용에 집중할 수 있다. 또한, 코드 스타일을 통일시키므로 가독성과 생산성이 증진된다.

## 포매터 설치 방법

터미널에서 `pip install black`으로 간단하게 설치할 수 있다. 그 후에 VSCode의 설정 화면에서 python formatting provider를 Black으로 설정하고 format on save에 체크하면, VSCode에서 파이썬 코드를 저장할 때마다 자동으로 포매팅된다.

## 포매터 사용법

`black {파일 또는 폴더 이름}`으로 포매팅할 수 있다.

```bash
black practice.py
```

## 코드 포매팅 예제

[해당 링크](https://black.vercel.app/?version=stable&state=_Td6WFoAAATm1rRGAgAhARYAAAB0L-Wj4ARUAmtdAD2IimZxl1N_WlkPinBFoXIfdFTaTVkGVeHShArYj9yPlDvwBA7LhGo8BvRQqDilPtgsfdKl-ha7EFp0Ma6lY_06IceKiVsJ3BpoICJM9wU1VJLD7l3qd5xTmo78LqThf9uibGWcWCD16LBOn0JK8rhhx_Gf2ClySDJtvm7zQJ1Z-Ipmv9D7I_zhjztfi2UTVsJp7917XToHBm2EoNZqyE8homtGskFIiif5EZthHQvvOj8S2gJx8_t_UpWp1ScpIsD_Xq83LX-B956I_EBIeNoGwZZPFC5zAIoMeiaC1jU-sdOHVucLJM_x-jkzMvK8Utdfvp9MMvKyTfb_BZoe0-FAc2ZVlXEpwYgJVAGdCXv3lQT4bpTXyBwDrDVrUeJDivSSwOvT8tlnuMrXoD1Sk2NZB5SHyNmZsfyAEqLALbUnhkX8hbt5U2yNQRDf1LQhuUIOii6k6H9wnDNRnBiQHUfzKfW1CLiThnuVFjlCxQhJ60u67n3EK38XxHkQdOocJXpBNO51E4-f9z2hj0EDTu_ScuqOiC9cI8qJ4grSZIOnnQLv9WPvmCzx5zib3JacesIxMVvZNQiljq_gL7udm1yeXQjENOrBWbfBEkv1P4izWeAysoJgZUhtZFwKFdoCGt2TXe3xQ-wVZFS5KoMPhGFDZGPKzpK15caQOnWobOHLKaL8eFA-qI44qZrMQ7sSLn04bYeenNR2Vxz7hvK0lJhkgKrpVfUnZrtF-e-ubeeUCThWus4jZbKlFBe2Kroz90Elij_UZBMFCcFo0CfIx5mGlrINrTRFyNsHRkoRBLruYzynsdQIZlZ2M2AAAE3z3tcACOrHAAGHBdUIAADeZ5kXscRn-wIAAAAABFla)에서 확인해볼 수 있다.
