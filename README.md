# Speech-To-Text

동영상 파일에서 음성을 추출하고 텍스트로 변환하는 도구입니다.

## 기능

- 동영상에서 음성 추출 (MP3)
- Whisper AI를 사용한 한국어 음성 인식 (TXT)
- 폴더 내 동영상 일괄 변환
- 이미 변환된 파일 자동 건너뛰기

## 설치

```bash
# 가상환경 활성화
source /Users/foodie/myproject/venv/bin/activate

# 필요한 패키지 설치
pip install openai-whisper moviepy
```

## 사용법

### 일괄 변환 (batch_convert.py)

`사이클투자반_부지런_2025/동영상` 폴더의 모든 동영상을 변환합니다.

```bash
python batch_convert.py
```

**출력 위치:**
- MP3: `사이클투자반_부지런_2025/음성/`
- TXT: `사이클투자반_부지런_2025/Text/`

### 단일 파일 변환 (video_to_text.py)

특정 동영상 파일 하나를 변환할 때 사용합니다.
코드 내 경로를 수정하여 사용하세요.

```bash
python video_to_text.py
```

## 지원 형식

- 입력: mp4, webm, avi, mov, mkv
- 출력: mp3 (음성), txt (텍스트)

## 참고

- Whisper `base` 모델 사용 (한국어 인식)
- 동영상 길이에 따라 변환 시간이 달라집니다
