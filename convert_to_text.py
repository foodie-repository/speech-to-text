#!/usr/bin/env python3
"""
동영상과 음성 파일을 텍스트로 변환하는 범용 스크립트
Whisper AI 모델을 사용하여 한국어 음성 인식

사용법:
    1. 동영상 파일을 Source/동영상/ 폴더에 넣으면 자동으로 음성(MP3)과 텍스트(TXT)로 변환
    2. 음성 파일을 Source/음성/ 폴더에 넣으면 자동으로 텍스트(TXT)로 변환

출력:
    - MP3 파일: Source/음성/
    - TXT 파일: Source/Text/
"""

import whisper
from moviepy import VideoFileClip
import os
from pathlib import Path


def extract_audio(video_path, audio_path):
    """동영상에서 오디오 추출하여 MP3로 저장"""
    print(f"  오디오 추출 중: {Path(video_path).name}")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    video.close()
    print(f"  ✓ 오디오 추출 완료: {Path(audio_path).name}")


def transcribe_audio(audio_path, model):
    """Whisper를 사용하여 오디오를 텍스트로 변환"""
    print(f"  음성 인식 중... (시간이 걸릴 수 있습니다)")
    result = model.transcribe(audio_path, language="ko", verbose=True)
    return result["text"]


def process_video(video_path, audio_dir, text_dir, model):
    """동영상 파일을 음성과 텍스트로 변환"""
    # 파일명 추출 (확장자 제외)
    video_name = Path(video_path).stem

    # 출력 경로 설정
    audio_path = os.path.join(audio_dir, f"{video_name}.mp3")
    text_path = os.path.join(text_dir, f"{video_name}.txt")

    # 이미 변환된 파일이 있으면 건너뛰기
    if os.path.exists(audio_path) and os.path.exists(text_path):
        print(f"  ⊘ 이미 변환됨 - 건너뜀")
        return None  # 건너뛴 경우

    try:
        # 1. 동영상에서 오디오 추출
        if not os.path.exists(audio_path):
            extract_audio(video_path, audio_path)

        # 2. 오디오를 텍스트로 변환
        if not os.path.exists(text_path):
            transcript = transcribe_audio(audio_path, model)

            # 3. 텍스트 파일로 저장
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(transcript)

        print(f"  ✓ 변환 완료: {video_name}")
        return True

    except Exception as e:
        print(f"  ✗ 오류 발생: {str(e)}")
        return False


def process_audio(audio_path, text_dir, model):
    """음성 파일을 텍스트로 변환"""
    # 파일명 추출 (확장자 제외)
    audio_name = Path(audio_path).stem

    # 출력 경로 설정
    text_path = os.path.join(text_dir, f"{audio_name}.txt")

    # 이미 변환된 파일이 있으면 건너뛰기
    if os.path.exists(text_path):
        print(f"  ⊘ 이미 변환됨 - 건너뜀")
        return None  # 건너뛴 경우

    try:
        # 오디오를 텍스트로 변환
        transcript = transcribe_audio(audio_path, model)

        # 텍스트 파일로 저장
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(transcript)

        print(f"  ✓ 변환 완료: {audio_name}")
        return True

    except Exception as e:
        print(f"  ✗ 오류 발생: {str(e)}")
        return False


def main():
    # 프로젝트 루트 디렉토리 자동 탐지
    script_dir = Path(__file__).parent
    source_dir = script_dir / "Source"

    # 경로 설정
    video_dir = source_dir / "동영상"
    audio_dir = source_dir / "음성"
    text_dir = source_dir / "Text"

    # 디렉토리 존재 확인
    for dir_path in [video_dir, audio_dir, text_dir]:
        if not dir_path.exists():
            print(f"경고: {dir_path} 폴더가 없습니다.")
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  → {dir_path} 폴더를 생성했습니다.")

    # 지원하는 파일 확장자
    video_extensions = {'.mp4', '.webm', '.avi', '.mov', '.mkv'}
    audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac'}

    # 동영상 파일 목록 가져오기
    video_files = [
        f for f in os.listdir(video_dir)
        if Path(f).suffix.lower() in video_extensions
    ]

    # 음성 폴더에 있는 음성 파일 중 동영상에서 변환된 것이 아닌 파일만 가져오기
    # (동영상 파일명과 같은 이름의 MP3는 제외)
    video_stems = {Path(vf).stem for vf in video_files}
    audio_files = [
        f for f in os.listdir(audio_dir)
        if Path(f).suffix.lower() in audio_extensions and Path(f).stem not in video_stems
    ]

    total_files = len(video_files) + len(audio_files)

    if total_files == 0:
        print("\n변환할 파일이 없습니다.")
        print(f"\n사용법:")
        print(f"  1. 동영상 파일을 {video_dir} 폴더에 넣으세요")
        print(f"  2. 또는 음성 파일을 {audio_dir} 폴더에 넣으세요")
        print(f"\n그런 다음 이 스크립트를 다시 실행하세요: python convert_to_text.py")
        return

    print(f"\n{'='*60}")
    print(f"총 {total_files}개의 파일을 찾았습니다:")
    print(f"  - 동영상: {len(video_files)}개")
    print(f"  - 음성: {len(audio_files)}개")
    print(f"{'='*60}")

    # Whisper 모델 로딩 (한 번만 로드)
    print("\nWhisper 모델 로딩 중 (base 모델)...")
    model = whisper.load_model("base")
    print("✓ 모델 로딩 완료!\n")

    # 통계 변수
    success_count = 0
    skipped_count = 0
    error_count = 0
    current = 0

    # 동영상 파일 처리
    if video_files:
        print(f"\n[동영상 → 음성 + 텍스트 변환]")
        print("-" * 60)
        for video_file in video_files:
            current += 1
            print(f"\n[{current}/{total_files}] 처리 중: {video_file}")

            video_path = os.path.join(video_dir, video_file)
            result = process_video(video_path, audio_dir, text_dir, model)

            if result is True:
                success_count += 1
            elif result is None:
                skipped_count += 1
            else:
                error_count += 1

    # 음성 파일 처리
    if audio_files:
        print(f"\n\n[음성 → 텍스트 변환]")
        print("-" * 60)
        for audio_file in audio_files:
            current += 1
            print(f"\n[{current}/{total_files}] 처리 중: {audio_file}")

            audio_path = os.path.join(audio_dir, audio_file)
            result = process_audio(audio_path, text_dir, model)

            if result is True:
                success_count += 1
            elif result is None:
                skipped_count += 1
            else:
                error_count += 1

    # 결과 요약
    print("\n" + "=" * 60)
    print("변환 완료!")
    print(f"  ✓ 새로 변환: {success_count}개")
    print(f"  ⊘ 건너뜀: {skipped_count}개")
    if error_count > 0:
        print(f"  ✗ 오류: {error_count}개")
    print(f"  전체: {total_files}개")
    print(f"\n출력 위치:")
    print(f"  - 음성 파일: {audio_dir}")
    print(f"  - 텍스트 파일: {text_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
