import os

def check_progress(progress_dir: str, total_slides: int):
    """추출 실패한 슬라이드 확인"""
    
    failed_slides = []
    empty_slides = []
    success_count = 0

    for i in range(1, total_slides + 1):
        progress_file = os.path.join(progress_dir, f"slide_{i:03d}.md")
        
        # 파일 자체가 없는 경우
        if not os.path.exists(progress_file):
            failed_slides.append(i)
            continue
        
        # 파일은 있지만 내용이 비어있거나 추출 실패인 경우
        with open(progress_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        if not content or "슬라이드 추출 실패" in content:
            empty_slides.append(i)
        else:
            success_count += 1

    # 결과 출력
    print(f"\n===== 매뉴얼 추출 결과 확인 =====")
    print(f"전체 슬라이드: {total_slides}장")
    print(f"성공: {success_count}장 ✅")
    print(f"파일 없음: {len(failed_slides)}장 ❌")
    print(f"추출 실패: {len(empty_slides)}장 ⚠️")

    if failed_slides:
        print(f"\n❌ 파일 없는 슬라이드: {failed_slides}")
    
    if empty_slides:
        print(f"\n⚠️ 추출 실패 슬라이드: {empty_slides}")

    if not failed_slides and not empty_slides:
        print("\n모든 슬라이드가 정상적으로 추출됐어요! 🎉")
    else:
        print("\n위 슬라이드들을 재처리하려면 아래 명령어를 실행해주세요.")
        print("python retry_failed.py")

if __name__ == "__main__":
    # 전체 슬라이드 수를 입력해주세요
    TOTAL_SLIDES = 250
    check_progress("temp_progress", TOTAL_SLIDES)