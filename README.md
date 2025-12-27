# Speech-To-Text

동영상과 음성 파일을 텍스트로 변환하는 범용 도구입니다.

## 기능

- 동영상에서 음성 추출 (MP3) 및 텍스트 변환 (TXT)
- 음성 파일을 텍스트로 변환 (TXT)
- Whisper AI를 사용한 한국어 음성 인식
- 폴더 내 파일 일괄 자동 변환
- 이미 변환된 파일 자동 건너뛰기

## 설치

### 1. 가상환경 활성화

프로젝트의 가상환경을 활성화합니다:

```bash
# macOS/Linux
source /Users/foodie/myproject/venv/bin/activate

# 또는 프로젝트 로컬 가상환경 사용
source .venv/bin/activate
```

### 2. 필요한 패키지 설치

```bash
pip install openai-whisper moviepy
```

## 사용법

### 📁 프로젝트 구조

```
Speech-To-Text/
├── Source/
│   ├── 동영상/        # 변환할 동영상 파일을 여기에 넣으세요
│   ├── 음성/          # 변환할 음성 파일 또는 추출된 음성이 저장됩니다
│   └── Text/          # 변환된 텍스트 파일이 저장됩니다
├── convert_to_text.py # 변환 스크립트
└── README.md
```

### 🚀 빠른 시작

#### 1단계: 파일 준비

변환하려는 파일을 해당 폴더에 넣으세요:
- **동영상 파일** → `Source/동영상/` 폴더
- **음성 파일** → `Source/음성/` 폴더

#### 2단계: 변환 실행

```bash
python convert_to_text.py
```

### 📝 상세 사용 예시

#### 예시 1: 동영상 파일 변환

```bash
# 1. 동영상 파일을 Source/동영상/ 폴더에 복사
cp ~/Downloads/강의영상.mp4 Source/동영상/

# 2. 변환 실행
python convert_to_text.py

# 결과:
# - Source/음성/강의영상.mp3 (추출된 음성)
# - Source/Text/강의영상.txt (변환된 텍스트)
```

#### 예시 2: 음성 파일만 변환

```bash
# 1. 음성 파일을 Source/음성/ 폴더에 복사
cp ~/Downloads/녹음파일.mp3 Source/음성/

# 2. 변환 실행
python convert_to_text.py

# 결과:
# - Source/Text/녹음파일.txt (변환된 텍스트)
```

#### 예시 3: 여러 파일 일괄 변환

```bash
# 여러 파일을 한 번에 복사
cp ~/Downloads/*.mp4 Source/동영상/
cp ~/Downloads/*.mp3 Source/음성/

# 변환 실행 (자동으로 모든 파일 처리)
python convert_to_text.py
```

## 지원 형식

| 입력 타입 | 지원 확장자 |
|----------|-----------|
| 동영상 | `.mp4`, `.webm`, `.avi`, `.mov`, `.mkv` |
| 음성 | `.mp3`, `.wav`, `.m4a`, `.flac`, `.aac` |

| 출력 타입 | 확장자 |
|----------|--------|
| 음성 | `.mp3` |
| 텍스트 | `.txt` |

## 주요 특징

### ✨ 자동 중복 방지
- 이미 변환된 파일은 자동으로 건너뜁니다
- 변환 중 중단되어도 다시 실행하면 이어서 진행됩니다

### 🎯 스마트 처리
- 동영상 파일: 음성 추출 → 텍스트 변환 (2단계)
- 음성 파일: 텍스트 변환 (1단계)
- 동영상에서 추출된 음성 파일은 중복 변환하지 않습니다

### 📊 실시간 진행 상황
```
총 5개의 파일을 찾았습니다:
  - 동영상: 3개
  - 음성: 2개

[동영상 → 음성 + 텍스트 변환]
[1/5] 처리 중: 강의_1.mp4
  ✓ 오디오 추출 완료: 강의_1.mp3
  음성 인식 중...
  ✓ 변환 완료: 강의_1

변환 완료!
  ✓ 새로 변환: 5개
  ⊘ 건너뜀: 0개
  전체: 5개
```

## 추가 도구

### video_to_text.py (레거시)

특정 동영상 파일 하나를 변환할 때 사용합니다.
코드 내 경로를 수정하여 사용하세요.

```bash
python video_to_text.py
```

## 참고 사항

- **Whisper 모델**: `base` 모델 사용 (한국어 최적화)
- **변환 시간**: 파일 길이에 비례 (10분 영상 ≈ 5-10분 소요)
- **디스크 공간**: 동영상 파일의 약 10-20% 크기의 MP3 파일 생성
- **GPU 가속**: CUDA 지원 시 자동으로 GPU 사용 (변환 속도 향상)

## 문제 해결

### 오류 발생 시

1. **가상환경이 활성화되어 있는지 확인**
   ```bash
   which python
   # 결과: /Users/foodie/myproject/venv/bin/python
   ```

2. **패키지가 설치되어 있는지 확인**
   ```bash
   pip list | grep -E "whisper|moviepy"
   ```

3. **ffmpeg 설치 확인** (moviepy 의존성)
   ```bash
   # macOS
   brew install ffmpeg

   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   ```

## 최근 작업 이력

### 2024-12-27

- **나미브 대출 강의 (251127)** 텍스트 변환 완료
  - 동영상 2개 → 음성 추출 및 텍스트 변환
  - 맞춤법 교정 및 마크다운 형식으로 통합 (200개 이상 오타 수정)
  - Obsidian 노트로 이동: `/Volumes/T9/Obsidian-Foodie/02. 부동산/11. 대출/`
  - 최종 파일: `나미브_대출 강의_251127.md` (61KB, 585줄)

## 라이선스

MIT License
