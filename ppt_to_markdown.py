import os
import time
from PIL import Image
from google import genai
from dotenv import load_dotenv
import comtypes.client

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ppt_to_images(ppt_path: str, output_dir: str):
    """PowerPoint를 이미지로 변환"""
    os.makedirs(output_dir, exist_ok=True)
    
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1
    
    ppt = powerpoint.Presentations.Open(os.path.abspath(ppt_path))
    
    for i, slide in enumerate(ppt.Slides):
        image_path = os.path.abspath(os.path.join(output_dir, f"slide_{i+1:03d}.png"))
        slide.Export(image_path, "PNG")
        print(f"슬라이드 {i+1} 변환 완료")
    
    ppt.Close()
    powerpoint.Quit()

def extract_text_from_image(image_path: str) -> str:
    """Gemini Vision으로 이미지에서 텍스트 추출"""
    image = Image.open(image_path)
    
    models_to_try = ["gemini-3.1-flash-lite", "gemini-3.5-flash", "gemini-flash-latest"]
    
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    image,
                    """이 슬라이드의 내용을 마크다운 형식으로 정리해주세요.
                    
규칙:
1. 슬라이드 제목은 ## 헤더로
2. 본문 내용은 bullet point로
3. 화면 캡처 이미지가 있다면 그 안의 텍스트와 설명도 포함
4. 각주나 설명 텍스트도 빠짐없이 포함
5. 업무 매뉴얼 내용에 집중해서 정리"""
                ]
            )
            return response.text
        except Exception as e:
            print(f"{model_name} 실패: {e}")
            time.sleep(3)
            continue
    
    return "## 슬라이드 추출 실패\n- 이 슬라이드는 수동으로 입력해주세요."

def convert_ppt_to_markdown(ppt_path: str, output_md: str):
    """PPT 전체를 마크다운으로 변환 (중간 저장 지원)"""
    image_dir = "temp_slides"
    progress_dir = "temp_progress"
    os.makedirs(progress_dir, exist_ok=True)

    # 이미지 변환 (이미 있으면 건너뜀)
    if not os.path.exists(image_dir) or len(os.listdir(image_dir)) == 0:
        print("PPT를 이미지로 변환 중...")
        ppt_to_images(ppt_path, image_dir)
    else:
        print("이미지가 이미 존재해서 변환 건너뜀 ✅")

    image_files = sorted([
        f for f in os.listdir(image_dir)
        if f.endswith(".png")
    ])

    print(f"\n총 {len(image_files)}개 슬라이드 텍스트 추출 중...")

    for i, image_file in enumerate(image_files):
        slide_num = i + 1
        progress_file = os.path.join(progress_dir, f"slide_{slide_num:03d}.md")

        # 이미 처리된 슬라이드는 건너뜀
        if os.path.exists(progress_file):
            print(f"슬라이드 {slide_num}/{len(image_files)} 이미 처리됨 ✅")
            continue

        print(f"슬라이드 {slide_num}/{len(image_files)} 처리 중...")
        image_path = os.path.join(image_dir, image_file)
        content = extract_text_from_image(image_path)

        # 슬라이드별로 저장
        with open(progress_file, "w", encoding="utf-8") as f:
            f.write(content)

        time.sleep(2)

    # 전체 합치기
    print("\n전체 내용 합치는 중...")
    all_content = ["# 업무 매뉴얼\n"]

    for i in range(1, len(image_files) + 1):
        progress_file = os.path.join(progress_dir, f"slide_{i:03d}.md")
        if os.path.exists(progress_file):
            with open(progress_file, "r", encoding="utf-8") as f:
                all_content.append(f"\n---\n{f.read()}")

    with open(output_md, "w", encoding="utf-8") as f:
        f.write("\n".join(all_content))

    print(f"\n완료! {output_md} 파일로 저장됐어요. 🎉")

if __name__ == "__main__":
    convert_ppt_to_markdown(
        ppt_path="docs/manual2.pptx",
        output_md="docs/manual.md"
    )