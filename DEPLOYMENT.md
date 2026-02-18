# LegoWorld V3 - GitHub & Streamlit Cloud 배포 가이드

## 현재 상황
- ✅ Git repository 초기화 완료
- ✅ 코드 수정 완료 (ngrok 헤더 추가)
- ⏳ GitHub repository 생성 필요
- ⏳ Streamlit Cloud 연결 필요

## 1단계: GitHub Repository 생성

### 웹에서 생성 (추천)

1. **GitHub 접속**
   - https://github.com/new 접속

2. **Repository 설정**
   - Repository name: `LegoWorldV3` (또는 원하는 이름)
   - Description: "LegoWorld V3 - Mobile photo capture and TV display demo"
   - Public 또는 Private 선택
   - **DO NOT** initialize with README (이미 로컬에 있음)
   - Create repository 클릭

3. **Remote URL 복사**
   ```
   https://github.com/YOUR_USERNAME/LegoWorldV3.git
   ```

## 2단계: 로컬 Repository 연결 및 푸시

### 터미널에서 실행:

```bash
cd /Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3

# GitHub remote 추가 (YOUR_USERNAME을 본인 것으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/LegoWorldV3.git

# main 브랜치로 이름 변경 (필요시)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

## 3단계: Streamlit Cloud 연결

### 기존 앱 재배포 방법

만약 기존 Streamlit Cloud 앱(`legodemo`)이 다른 repository에 연결되어 있다면:

**Option A: 새 앱으로 배포**
1. https://share.streamlit.io/ 접속
2. "New app" 클릭
3. Repository: 방금 만든 `YOUR_USERNAME/LegoWorldV3` 선택
4. Branch: `main`
5. Main file path: `streamlit_app.py`
6. Advanced settings → Secrets 추가:
   ```toml
   BACKEND_URL = "https://marlena-glossological-hyperconfidently.ngrok-free.dev"
   ```
7. Deploy! 클릭

**Option B: 기존 앱 repository 변경**
1. https://share.streamlit.io/ 접속
2. `legodemo` 앱 선택
3. Settings → General
4. Repository 변경: `YOUR_USERNAME/LegoWorldV3`
5. Branch: `main`
6. Main file path: `streamlit_app.py`
7. Save 클릭
8. Reboot app

### Secrets 확인/추가

Streamlit Cloud Settings → Secrets:
```toml
BACKEND_URL = "https://marlena-glossological-hyperconfidently.ngrok-free.dev"
```

## 4단계: 테스트

### 모바일에서 테스트

1. Streamlit 앱 URL 접속 (예: https://legodemo-....streamlit.app/)
2. "📸 Add Photo" 탭
3. 레고 사진 촬영/업로드
4. "📤 Add to Collection" 클릭
5. ✅ "Photo added successfully!" 확인

### TV 앱에서 확인

1. 브라우저에서 `tizen/index.html` 열기
2. Down 화살표로 "My Photos" 이동
3. 업로드한 사진 확인
4. Enter로 리프레시

## 트러블슈팅

### GitHub 인증 문제

Personal Access Token 사용:
1. https://github.com/settings/tokens → Generate new token (classic)
2. repo 권한 선택
3. 생성된 토큰 복사
4. Push 시 비밀번호 대신 토큰 입력

### Streamlit Cloud 앱이 기존 repo에 연결되어 있는 경우

기존 repository를 찾아서 거기에 코드를 업데이트하는 것이 더 간단할 수 있습니다.

## 빠른 명령어 요약

```bash
# 1. GitHub에서 repository 생성 후
cd /Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3
git remote add origin https://github.com/YOUR_USERNAME/LegoWorldV3.git
git branch -M main
git push -u origin main

# 2. Streamlit Cloud에서 앱 배포/연결
# 3. Secrets 설정
# 4. 테스트!
```

## 향후 업데이트

코드 수정 후:
```bash
git add .
git commit -m "설명"
git push origin main
```

Streamlit Cloud가 자동으로 재배포합니다 (1-2분 소요).
