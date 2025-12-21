#!/usr/bin/env python3
"""
동영상 파일의 음성을 텍스트로 변환하는 스크립트
Whisper AI 모델을 사용하여 한국어 음성 인식
"""

import whisper
from moviepy import VideoFileClip
import os
import sys

def extract_audio(video_path, audio_path):
    """동영상에서 오디오 추출"""
    print(f"동영상에서 오디오 추출 중: {video_path}")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()
    print(f"오디오 추출 완료: {audio_path}")

def transcribe_audio(audio_path, model_size="base"):
    """Whisper를 사용하여 오디오를 텍스트로 변환"""
    print(f"\nWhisper 모델 로딩 중 (크기: {model_size})...")
    model = whisper.load_model(model_size)

    print(f"음성 인식 중... (시간이 걸릴 수 있습니다)")
    result = model.transcribe(audio_path, language="ko", verbose=True)

    return result["text"]

def main():
    # 파일 경로 설정
    video_path = "/Users/foodie/Downloads/아파트값 5차파동_5교시.webm"
    audio_path = "/Users/foodie/Downloads/아파트값_5차파동_5교시_audio.mp3"
    output_text_path = "/Users/foodie/Downloads/아파트값_5차파동_5교시_transcript.txt"

    try:
        # 1. 동영상에서 오디오 추출
        extract_audio(video_path, audio_path)

        # 2. 오디오를 텍스트로 변환
        transcript = transcribe_audio(audio_path, model_size="base")

        # 3. 텍스트 파일로 저장
        print(f"\n텍스트 파일 저장 중: {output_text_path}")
        with open(output_text_path, 'w', encoding='utf-8') as f:
            f.write(transcript)

        print(f"\n✅ 변환 완료!")
        print(f"🎵 오디오 파일: {audio_path}")
        print(f"📝 텍스트 파일: {output_text_path}")

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
