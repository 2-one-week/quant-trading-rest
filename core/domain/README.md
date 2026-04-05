# Trade Fee Policy

`core/domain/trade_fee.py`는 주문 가능 수량, RP ETF 환전 수량, 최소 매도 기준가 계산에 쓰이는 공통 수수료 계산 로직을 담고 있습니다.

## 구조

- `BaseTradeFeePolicy`
  - 총매수비용, 순매도수령액, 왕복비용, 최대매수수량, 목표 수령액 기준 최소 매도 수량 계산 제공
- `KoreaTradeFeePolicy`
  - 한국 주식 수수료/매도세 계산
  - `ETF`, `ETN`은 거래세 `0`
- `USTradeFeePolicy`
  - 미국 주식 수수료 계산
  - 매도 시 `SEC fee`, `FINRA TAF` 반영

## 현재 요율 기준

- 한국 주식
  - 매수 수수료: `0.015%`
  - 매도 수수료: `0.015%`
  - 매도세: `0.20%`
  - ETF/ETN 매도세: `0%`
- 미국 주식
  - 매수 수수료: `0.25%`
  - 매도 수수료: `0.25%`
  - SEC fee: `20.60 / 1,000,000`
  - FINRA TAF: `0.000195 / share`
  - FINRA TAF cap: `$9.79 / trade`

미국 매도 제세금은 `2026-04-04` 이후 기준입니다.

## 계산식

```text
buy_total = price * quantity + buy_fee
sell_proceeds = price * quantity - sell_fee - sell_tax
target_sell_proceeds = buy_total * 1.005
```

## 예시

한국 주식 `10,000원`, `10주`

```text
buy_total = 100,015
sell_proceeds = 99,785
```

미국 주식 `$100`, `10주`

```text
buy_total = 1,002.5
sell_tax = 0.02255
sell_proceeds = 997.47745
```

## 책임 분리

- wrapper가 국가별 policy를 선택
- `KiwoomWrapper`는 `marketName`을 조회해 ETF/ETN 여부를 policy에 전달
- `HantooWrapper`는 미국 정책만 사용
