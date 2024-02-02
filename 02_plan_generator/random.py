import random

n = 10  # 예시로 10을 사용; 실제로는 원하는 숫자로 변경해주세요.
for _ in range(n):  # n번 반복
    random_number = random.randrange(0, n)  # 0부터 n-1까지의 랜덤 숫자 생성
    print(random_number)
