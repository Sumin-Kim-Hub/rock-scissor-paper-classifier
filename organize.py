import os
import subprocess
import datetime
import re

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    except:
        return ""

# 1. 정리에서 제외할 파일들
exclude_list = ['README.md', 'organize.py', '.gitignore', '.git']
files = [f for f in os.listdir('.') if os.path.isfile(f) and f not in exclude_list]

print(f"🧹 중복을 제거하고 '{datetime.datetime.now().strftime('%y%m%d')}' 형식으로 정리를 시작합니다...")

for old_name in files:
    try:
        # 깃허브 업로드 날짜 가져오기 (YYMMDD 형식: %y%m%d)
        date_str = run_cmd(f'git log -1 --format=%cd --date=format:%y%m%d -- "{old_name}"')
        if not date_str:
            date_str = datetime.datetime.now().strftime('%y%m%d')

        # 파일명과 확장자 분리
        name, ext = os.path.splitext(old_name)

        # [중복 제거 로직] 기존에 붙었던 '김수민'이나 '날짜(8자리 또는 6자리)'를 싹 지웁니다.
        # 1. '_김수민' 제거
        name = name.replace('_김수민', '')
        # 2. 숫자_숫자 패턴이나 끝에 붙은 날짜 패턴 제거 (정규표현식 사용)
        name = re.sub(r'_\d{6,8}', '', name) # _20250109 또는 _250109 형태 제거
        name = re.sub(r'\d{6,8}_', '', name) # 앞부분에 붙은 날짜 제거

        # 3. 최종 이름 결정: 파일명_김수민_날짜.확장자
        new_name = f"{name}_김수민_{date_str}{ext}"
        
        # 이름이 실제로 바뀔 때만 실행
        if old_name != new_name:
            os.rename(old_name, new_name)
            print(f"✅ 정리 완료: {old_name} -> {new_name}")
    except Exception as e:
        print(f"❌ {old_name} 에러: {e}")

# 2. 깃허브 업로드
print("\n🚀 깨끗해진 파일들을 깃허브에 반영합니다...")
os.system('git add .')
os.system('git commit -m "파일명 형식 통일 (파일명_이름_YYMMDD)"')
os.system('git push origin main')

print("\n✨ 이제 깃허브가 아주 깔끔해졌을 거예요! 수고하셨습니다!")
#python organize.py