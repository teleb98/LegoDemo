# LegoWorld V3 - ngrok 설정 가이드 🚀

이 가이드는 Streamlit Cloud 앱과 로컬 백엔드 서버를 연결하기 위한 ngrok 설정 방법을 안내합니다.

## ✅ 완료된 작업

- [x] `streamlit_app.py` - 환경 변수 지원 추가
- [x] `server/app.py` - 동적 포트 설정 지원
- [x] 백엔드 서버 실행 확인 (포트 5000)

## 📋 다음 단계

### 1️⃣ ngrok 설치

ngrok 공식 웹사이트에서 다운로드:

**방법 A: 웹사이트에서 직접 다운로드**
```bash
# 1. https://ngrok.com/download 방문
# 2. macOS용 파일 다운로드
# 3. 압축 해제 후 실행
```

**방법 B: curl로 다운로드**
```bash
# Downloads 폴더로 이동
cd ~/Downloads

# ngrok 다운로드 (macOS Intel)
curl -O https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip

# 압축 해제
unzip ngrok-v3-stable-darwin-amd64.zip

# 실행 권한 부여
chmod +x ngrok

# /usr/local/bin으로 이동 (선택사항 - 어디서든 실행 가능)
sudo mv ngrok /usr/local/bin/
```

**방법 C: Apple Silicon (M1/M2) Mac**
```bash
cd ~/Downloads
curl -O https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-arm64.zip
unzip ngrok-v3-stable-darwin-arm64.zip
chmod +x ngrok
sudo mv ngrok /usr/local/bin/
```

### 2️⃣ ngrok 실행

백엔드 서버가 실행 중인 상태에서:

```bash
# 새 터미널을 열고 실행
ngrok http 5000
```

다음과 같은 화면이 표시됩니다:

```
Session Status                online
Account                       ...
Version                       3.x.x
Region                        ...
Forwarding                    https://abc123def456.ngrok.io -> http://localhost:5000
```

> [!IMPORTANT]
> **`https://abc123def456.ngrok.io`** 형식의 URL을 복사하세요!

### 3️⃣ Streamlit Cloud 설정

1. **Streamlit Cloud 대시보드 접속**
   - https://share.streamlit.io/ 로그인
   - LegoWorld 앱 선택

2. **Secrets 설정**
   - App settings (⚙️) → Secrets 메뉴
   - 다음 내용 추가:

```toml
BACKEND_URL = "https://your-ngrok-url.ngrok.io"
```

   - `your-ngrok-url`을 실제 ngrok URL로 변경
   - Save 클릭

3. **앱 재시작**
   - Streamlit Cloud가 자동으로 재배포됩니다
   - 약 1-2분 소요

### 4️⃣ TV 앱 설정 (선택사항)

TV 앱도 동일한 백엔드를 사용하려면:

```bash
# tizen/js/main.js 파일 열기
# BACKEND_URL 변수를 ngrok URL로 변경
const BACKEND_URL = 'https://your-ngrok-url.ngrok.io';
```

## ✅ 테스트

### 백엔드 헬스 체크
```bash
curl https://your-ngrok-url.ngrok.io/health
```

예상 결과:
```json
{"status": "ok", "service": "LegoWorld V3 Backend"}
```

### 모바일 앱 테스트
1. https://legodemo-bzfvc6bgmxmhrmxyfxhcsk.streamlit.app/ 접속
2. "📸 Add Photo" 탭에서 사진 촬영
3. "📤 Add to Collection" 클릭
4. "🖼️ My Gallery" 탭에서 사진 확인

### TV 앱 테스트
1. Tizen TV 앱 또는 브라우저에서 `tizen/index.html` 열기
2. Down 화살표로 "My Photos" 씬 이동
3. 업로드한 사진이 표시되는지 확인

## 📝 중요 사항

> [!WARNING]
> **ngrok 무료 플랜 제한사항:**
> - 세션이 종료되면 URL이 변경됩니다
> - 새 URL을 받을 때마다 Streamlit Secrets를 업데이트해야 합니다
> - 동시 연결 제한 (무료: 1개 터널)

> [!TIP]
> **ngrok을 계속 실행하려면:**
> - ngrok 터미널을 열어둔 채로 유지
> - 또는 `tmux`/`screen`을 사용하여 백그라운드 실행

## 🔄 대안: 영구 솔루션

테스트 후 프로덕션 환경으로 전환하려면:

**Railway 무료 배포 (추천)**
```bash
# 1. railway.app 회원가입
# 2. GitHub 리포지토리 연결
# 3. server/ 디렉토리 배포
# 4. 제공된 URL을 Streamlit Secrets에 설정
```

자세한 내용은 [implementation_plan.md](file:///Users/chiwon/.gemini/antigravity/brain/bb5ac186-e961-4515-819d-6cfcc9970de0/implementation_plan.md) 참조.

## 🐛 문제 해결

### ngrok이 실행되지 않음
```bash
# ngrok 버전 확인
ngrok version

# 버전이 표시되지 않으면 재설치
```

### Streamlit에서 여전히 연결 오류
- Streamlit Secrets의 URL이 정확한지 확인
- `https://` 포함 확인
- 앱 재시작 확인

### ngrok URL이 작동하지 않음
```bash
# ngrok 웹 인터페이스 확인
# 브라우저에서 http://localhost:4040 접속
# 요청 로그 확인
```

---

**준비 완료!** 이제 모바일에서 사진을 찍으면 TV에 나타납니다! 🎉
