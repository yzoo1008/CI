# 창의적 통합설계
=> ./de

## Cennor.py
 - Main 문
### Step 1.
 - Model 읽기  
### Step 2.
 - 읽은 Model로부터 PPF(Point Pair Feature) 계산 및 Hash table에 저장  
### Step 3.
 - Scene을 읽어 PPF를 계산하고 Hash table 속 Model의 PPF와 같은 값인 있는지 체크  
 - 같은 PPF를 가지는 Scene의 점 Pair(Sr, Si)와 Model의 점 (Mr, Mi)를 G(1, 0, 0)으로 회전 변환시키는  
 회전 변환 Tstog와 Tmtog 그리고 사이각 알파 계산
 - 알파 값을 key로 Tstog와 Tmtog 그리고 (Mr, Mi), (Sr, Si) 저장 및 voting 숫자 계산
### Step 4.
 - Voting된 결과로부터 투표를 가장 많이 받은 알파 값 선정
 - 선정된 알파 key에 저장된 Tstog와 Tmtog 그리고 (Mr, Mi), (Sr, Si)로부터 최종 변환 행렬 계산
### Step 5.
 - 최종 변환 행렬을 적용하여 답 비교
### Step 6.
 - 변환 값 저장
 
## module.py
 - Step 6를 위한 Stl파일 I/O
 
## transform.py
 - 변환 관련 함수들 모아놓은 Script
