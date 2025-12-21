#!/usr/bin/env python3
"""
동영상 폴더의 모든 파일을 음성(MP3)과 텍스트(TXT)로 변환하는 스크립트
Whisper AI 모델을 사용하여 한국어 음성 인식
"""

import whisper
from moviepy import VideoFileClip
import os
import sys
from pathlib import Path


def extract_audio(video_path, audio_path):
    """동영상에서 오디오 추출하여 MP3로 저장"""
    print(f"  오디오 추출 중: {video_path}")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()
    print(f"  오디오 추출 완료: {audio_path}")


def transcribe_audio(audio_path, model):
    """Whisper를 사용하여 오디오를 텍스트로 변환"""
    print(f"  음성 인식 중... (시간이 걸릴 수 있습니다)")
    result = model.transcribe(audio_path, language="ko", verbose=True)
    return result["text"]


def process_video(video_path, audio_dir, text_dir, model):
    """단일 동영상 파일 처리"""
    # 파일명 추출 (확장자 제외)
    video_name = Path(video_path).stem

    # 출력 경로 설정
    audio_path = os.path.join(audio_dir, f"{video_name}.mp3")
    text_path = os.path.join(text_dir, f"{video_name}.txt")

    # 이미 변환된 파일이 있으면 건너뛰기
    if os.path.exists(audio_path) and os.path.exists(text_path):
        print(f"  이미 변환됨 - 건너뜀")
        return None  # 건너뛴 경우

    try:
        # 1. 동영상에서 오디오 추출
        extract_audio(video_path, audio_path)

        # 2. 오디오를 텍스트로 변환
        transcript = transcribe_audio(audio_path, model)

        # 3. 텍스트 파일로 저장
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(transcript)

        print(f"  변환 완료: {video_name}")
        return True

    except Exception as e:
        print(f"  오류 발생: {str(e)}")
        return False


def main():
    # 경로 설정
    base_dir = "/Users/foodie/myproject/Speech-To-Text/사이클투자반_부지런_2025"
    video_dir = os.path.join(base_dir, "동영상")
    audio_dir = os.path.join(base_dir, "음성")
    text_dir = os.path.join(base_dir, "Text")

    # 지원하는 동영상 확장자
    video_extensions = {'.mp4', '.webm', '.avi', '.mov', '.mkv'}

    # 동영상 파일 목록 가져오기
    video_files = [
        f for f in os.listdir(video_dir)
        if Path(f).suffix.lower() in video_extensions
    ]

    if not video_files:
        print("변환할 동영상 파일이 없습니다.")
        return

    print(f"\n총 {len(video_files)}개의 동영상 파일을 찾았습니다.")
    print("=" * 50)

    # Whisper 모델 로딩 (한 번만 로드)
    print("\nWhisper 모델 로딩 중 (base 모델)...")
    model = whisper.load_model("base")
    print("모델 로딩 완료!\n")

    # 각 동영상 파일 처리
    success_count = 0
    skipped_count = 0
    for i, video_file in enumerate(video_files, 1):
        print(f"\n[{i}/{len(video_files)}] 처리 중: {video_file}")
        print("-" * 40)

        video_path = os.path.join(video_dir, video_file)
        result = process_video(video_path, audio_dir, text_dir, model)
        if result is True:
            success_count += 1
        elif result is None:
            skipped_count += 1

    # 결과 요약
    print("\n" + "=" * 50)
    print(f"새로 변환: {success_count}개 / 건너뜀: {skipped_count}개 / 전체: {len(video_files)}개")
    print(f"MP3 파일 위치: {audio_dir}")
    print(f"텍스트 파일 위치: {text_dir}")


if __name__ == "__main__":
    main()
