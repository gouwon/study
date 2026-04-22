import math

"""
레벨 (SBD 비율),가중치(W) / 목적,체중 대비 본 운동 비율,68kg 기준 무게,목표 반복 횟수
Elite,1.2 (스트렝스),약 162%,110.0 kg,10회
(8.00배),1.0 (근비대),약 148%,100.0 kg,12회
,0.6 (근지구력),약 119%,80.0 kg,20회
---,---,---,---,---
Advanced,1.2 (스트렝스),약 131%,90.0 kg,10회
(6.50배),1.0 (근비대),약 120%,82.5 kg,12회
,0.6 (근지구력),약 96%,65.0 kg,20회
---,---,---,---,---
Intermediate,1.2 (스트렝스),약 91%,62.5 kg,10회
(4.50배),1.0 (근비대),약 83%,57.5 kg,12회
,0.6 (근지구력),약 67%,45.0 kg,20회
---,---,---,---,---
Novice,1.2 (스트렝스),약 57%,37.5 kg,10회
(2.80배),1.0 (근비대),약 52%,35.0 kg,12회
,0.6 (근지구력),약 42%,27.5 kg,20회
---,---,---,---,---
Beginner,1.2 (스트렝스),0% ~ 56%,37.5 kg 미만,10회
(0.00배~),1.0 (근비대),0% ~ 51%,35.0 kg 미만,12회
,0.6 (근지구력),0% ~ 41%,27.5 kg 미만,20회
"""

LEVELS = [
    {"name": "Elite", "ratio": 0.95, "color": "red", "emoji": "🔥", "threshold": 8.00, "guide": "최고 수준의 근력", "eq": "자유로운 머신 운동과 프리웨이트"},
    {"name": "Advanced", "ratio": 0.90, "color": "orange", "emoji": "💪", "threshold": 6.50, "guide": "강한 저항 통제 및 근육 밀도 극대화", "eq": "해머 스트렝스 ISO-LATERAL, 프리웨이트 심화"},
    {"name": "Intermediate", "ratio": 0.80, "color": "yellow", "emoji": "🏋️", "threshold": 4.50, "guide": "좌우 불균형 해소 및 V-Taper 완성", "eq": "해머 스트렝스 MTS, 프리웨이트 활용"},
    {"name": "Novice", "ratio": 0.70, "color": "blue", "emoji": "🚴", "threshold": 2.80, "guide": "기초 근력 확보 및 프레임 확장", "eq": "해머 스트렝스 셀렉트, 프리웨이트 도입"},
    {"name": "Beginner", "ratio": 0.00, "color": "gray", "emoji": "🚶", "threshold": 0.00, "guide": "자극 인지 및 기초 근신경계 발달", "eq": "라이프니스 피트니스 인시그니아, 테크노짐 셀렉트"},
]

# --- [유틸리티 함수] ---
def round_to_plate(weight, step=2.5):
    """주어진 무게를 가장 가까운 플레이트 단위로 반올림합니다."""
    return round(weight / step) * step

def calculate_1rm(weight, reps):
    """공식에 기반하여 1RM을 계산합니다."""
    if reps <= 0: 
        print("⚠️ 반복 횟수는 0보다 커야 합니다.")
        return 0
    if reps == 1:
        print("⚠️ 1회는 실제 1RM과 동일하므로 공식 적용 없이 입력된 무게를 반환합니다.")
        return weight

    # 1. 고중량 저반복 (2~6회): Brzycki 공식
    if reps <= 6:
        return weight * (36 / (37 - reps))
    # 2. 중중량 중반복 (7~12회): Epley 공식의 평균
    elif reps <= 12:
        return weight * (1 + 0.0333 * reps)
    else:
    # 3. 저중량 고반복 (13회 이상): Wathan 공식
        return (100 * weight) / (48.8 + 53.8 * math.exp(-0.075 * reps))
    
def calculate_plate_distribution(total_weight, bar_weight=20, plate_weights=[25, 20, 15, 10, 5, 2.5]):
    """총 무게에서 바벨 무게를 제외한 나머지를 플레이트로 분배합니다."""
    # 1. 머신 사용자를 위해 바벨 무게보다 낮으면 계산 생략
    if total_weight <= bar_weight:
        return "머신 또는 빈 바벨 사용"
    
    remaining_weight = total_weight - bar_weight
    plate_weights = [25, 20, 15, 10, 5, 2.5]
    plate_distribution = {}
    for plate in plate_weights:
        count = int(remaining_weight // (2 * plate))
        if count > 0:
            plate_distribution[plate] = count
            remaining_weight -= count * 2 * plate
    return ", ".join([f"{p}kg x {count}개" for p, count in plate_distribution.items()])

def get_level_info(ratio):
    """사용자의 체중 대비 SBD 비율(ratio)을 기준으로 현재 레벨(current_lv)과 다음 목표 레벨(next_lv)을 반환합니다."""
    for i, lv in enumerate(LEVELS):
        if ratio >= lv["threshold"]:
            current_lv = lv
            next_lv = LEVELS[i-1] if i > 0 else None
            return current_lv, next_lv
    return LEVELS[-1], LEVELS[-2] # 기본값

# --- [메인 로직] ---
# 1. 사용자 기본 설정 입력 받기
try:
    user_input_weight = input("⚖️ 현재 체중을 입력하세요 (kg, 기본값 68): ")
    USER_WEIGHT = float(user_input_weight) if user_input_weight.strip() else 68.0
except ValueError:
    print("⚠️ 올바른 숫자가 아닙니다. 기본값 68.0kg으로 설정합니다.")
    USER_WEIGHT = 68.0
print(f"✅ 체중: {USER_WEIGHT}kg")

# 2. 가중치 입력 받기
try:    
    print("\n[목적 선택] 1.스트렝스(1.2)  2.근비대(1.0)  3.근지구력(0.6)")
    w_input = input("👉 목적 번호 선택 (기본 2): ")
    W = 1.2 if w_input == '1' else (0.6 if w_input == '3' else 1.0)
    rest_time = "3~5분" if W == 1.2 else ("60~90초" if W == 1.0 else "30~60초")
except ValueError:
    print("⚠️ 올바른 숫자가 아닙니다. 기본값 1.0으로 설정합니다.")
    W = 1.0
print(f"✅ 선택한 목적에 따른 가중치: {W}")

# 3. 가중치 기반 산출
STANDARD_VOLUME = 12
BASE_REPS = round(STANDARD_VOLUME / W)
TOTAL_SETS = 4
warmup_ratio = 0.45 * W
warmup_reps = round(10 / W)

# 3. 웜업 세트 가이드
try:
    prev_weight = input("🔄 이전 세트에서 사용한 무게를 입력하세요 (kg, 기본값 50): ")
    suggested_warmup_w = round_to_plate(float(prev_weight) * warmup_ratio)
except ValueError:
    print("⚠️ 올바른 숫자가 아닙니다. 기본값 50kg으로 설정합니다.")
    suggested_warmup_w = round_to_plate(50 * warmup_ratio)

print(f"\n🔔 [오늘의 웜업 가이드]")
print(f"   ▶ 추천: {suggested_warmup_w}kg로 {warmup_reps}회 수행하세요.(휴식 시간: {rest_time})")
print(f"   ▶ 가중치({W}) 기반 자동 산출된 가이드입니다.")

# 4. 웜업 세트 입력 받기
try:
    warmup_set_weight = input("🔄 웜업 세트에서 사용한 무게를 입력하세요 (kg, 기본값 50): ")
    warmup_set_reps = input(f"🔄 웜업 세트에서 수행한 반복 횟수를 입력하세요 (기본값 {warmup_reps}): ")
    warmup_set_weight = float(warmup_set_weight) if warmup_set_weight.strip() else 50.0
    warmup_set_reps = int(warmup_set_reps) if warmup_set_reps.strip() else warmup_reps

    # 1. 이전 운동 무게 기준 기대 1RM 역산 (근비대 가중치 1.0 기준 역산)
    intensity_factor = 0.375 * W + 0.4   #  W=0.6(60%), 1.0(76%), 1.2(85%)
    expected_1rm = float(prev_weight) / intensity_factor 

    # 2. 웜업 결과로 얻은 실시간 1RM (컨디션 확인용)
    warmup_estimated_1rm = calculate_1rm(warmup_set_weight, warmup_set_reps)

    # 3. 최종 타겟 1RM 결정 (이전 기록과 웜업 기록 중 높은 쪽 선택하여 역행 방지)
    # 단, 웜업은 전력을 다하지 않으므로 보정치 1.2배를 곱해 기대치 산출
    final_target_1rm = max(expected_1rm, warmup_estimated_1rm * 1.2)

except ValueError:
    print("⚠️ 올바른 숫자가 아닙니다. 기본값 50kg, 10회로 설정합니다.")
    warmup_set_weight = 50.0
    warmup_set_reps = warmup_reps
print(f"✅ 웜업 세트 입력: {warmup_set_weight}kg x {warmup_set_reps}회")

# 5. 본 운동 가이드
BASE_WEIGHT = float(prev_weight)
target_weight = round_to_plate(BASE_WEIGHT)
target_reps = BASE_REPS
min_reps_threshold = math.ceil(target_reps * 0.7)  # 최소 반복 횟수는 목표 반복 횟수의 70%로 설정

print(f"\n🎯 [본 운동 설정 완료]")
print(f"   ▶ 목표: {target_weight}kg / {target_reps}회씩 {TOTAL_SETS}세트 (휴식 시간: {rest_time})")
print(f"   ▶ 최소 유지 기준: {min_reps_threshold}회")
print("-" * 45)

# 6. 본 운동 세트 입력 받기
actual_total_volume, perfect_sets, completed_sets, best_reps = 0, 0, 0, 0
for set_num in range(1, TOTAL_SETS + 1):
    while True:
        try:
            set_weight = input(f"🔄 세트 {set_num} - 사용한 무게를 입력하세요 (kg, 기본값 {target_weight}): ")
            set_reps = input(f"🔄 세트 {set_num} - 수행한 반복 횟수를 입력하세요 (기본값 {target_reps}): ")
            set_weight = float(set_weight) if set_weight.strip() else target_weight
            set_reps = int(set_reps) if set_reps.strip() else target_reps
            break
        except ValueError:
            print("⚠️ 올바른 숫자가 아닙니다. 다시 입력해주세요.")
    
    actual_total_volume += (set_weight * set_reps)

    if set_reps > best_reps: best_reps = set_reps
    if set_weight >= target_weight and set_reps >= target_reps:
        perfect_sets += 1
        completed_sets += 1
        print(f"✅ 세트 {set_num}: 완벽한 세트! ({set_weight}kg x {set_reps}회)")
    elif set_reps >= min_reps_threshold:
        completed_sets += 1
        print(f"✅ 세트 {set_num}: 세트 완료! ({set_weight}kg x {set_reps}회)")
    else:
        print(f"⚠️ 세트 {set_num}: 세트 미완료. 다음 세트에서 더 노력해보세요! ({set_weight}kg x {set_reps}회)")
print("-" * 45)

# 7. 세트 결과 요약
print(f"\n📊 [세트 결과 요약]")
print(f"   ▶ 완벽한 세트: {perfect_sets}개")
print(f"   ▶ 완료된 세트: {completed_sets}개")
print(f"   ▶ 미완료 세트: {TOTAL_SETS - completed_sets}개")
print(f"   ▶ 최고 반복 횟수: {best_reps}회")
print(f"   ▶ 총 볼륨: {actual_total_volume}kg")

current_1rm = calculate_1rm(target_weight, best_reps)
# est_sbd_total = (current_1rm * 0.8) * 3 # SBD 합계는 1RM의 80%를 기준으로 계산 추정치(벤치프레스, 스쿼트, 데드리프트 각각)
est_sbd_total = current_1rm * 4.2 # 단일 종목 1RM 대비 SBD 총합 추정치를 보수적으로 조정
sbd_ratio = est_sbd_total / USER_WEIGHT
current_lv, next_lv = get_level_info(sbd_ratio)

# A. 증량/유지/검토 판정
if perfect_sets == TOTAL_SETS:
    next_w = round_to_plate(target_weight * 1.05)
    result_msg = f"🔥 [증량] 모든 세트 완벽 달성! 다음엔 {next_w}kg으로 올립니다."
elif completed_sets == TOTAL_SETS:
    result_msg = f"👍 [유지] 4세트 완수 성공! {target_weight}kg이 익숙해질 때까지 유지하세요."
else:
    down_w = round_to_plate(target_weight * 0.95)
    result_msg = f"🧊 [검토] 미달 세트 발생. 다음번엔 {down_w}kg으로 낮추거나 컨디션을 체크하세요."

print(f"📊 현재 추정 수준: [{current_lv['name']}] (SBD 예상 합계 대비 {sbd_ratio:.2f}배)")
print(f"🚀 현재 수준: SBD 대비 {sbd_ratio:.2f}배 (체중 기준)")

print(f"📊 분석 결과: \n{result_msg} \n(추정 1RM: {current_1rm:.1f}kg)")
print(f"🛠️ 추천 장비: {current_lv['eq']}")
print(f"📝 가이드: {current_lv['guide']}")
# D. 다음 단계 안내 혹은 최상위 단계 축하
if next_lv:
    needed_ratio = next_lv['threshold'] - sbd_ratio
    print("-" * 45)
    print(f"🚀 [LEVEL UP 목표] 다음 단계인 '{next_lv['name']}'까지")
    print(f"   약 {needed_ratio * USER_WEIGHT:.1f}kg(합계) 더 증량이 필요합니다.")
    print(f"   진입 시 사용 장비: {next_lv['eq']}")
else:
    # 고급자 단계 도달 시 출력되는 메시지
    print("-" * 45)
    print("🏆 [CONGRATULATIONS] 최상위 레벨인 '고급자' 단계입니다!")
    print(f"   - 당신은 이제 {current_lv['eq']} 마스터입니다.")
    print("   - 단순한 증량보다 근밀도와 디테일한 세퍼레이션에 집중하세요.")
    print("   - 부상 없는 완벽한 통제가 당신의 품격을 증명합니다. 득근하세요!")
print("=" * 45)
