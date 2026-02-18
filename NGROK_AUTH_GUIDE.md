# ngrok 인증 설정 가이드 🔐

ngrok을 사용하려면 무료 계정 생성과 인증 토큰 설정이 필요합니다.

## 현재 상태 ✅

- [x] ngrok v3.36.1 설치 완료
- [x] 백엔드 서버 실행 중 (포트 5000)
- [ ] ngrok 인증 필요

## 1️⃣ ngrok 계정 생성 (무료)

1. **회원가입 페이지 방문**
   - https://dashboard.ngrok.com/signup
   
2. **가입 방법 선택**
   - Google 계정으로 로그인 (가장 빠름)
   - 또는 이메일로 가입

3. **계정 인증**
   - 이메일 확인 (이메일 가입 시)

## 2️⃣ Authtoken 받기

1. **대시보드 접속**
   - 가입 후 자동으로 https://dashboard.ngrok.com/get-started/your-authtoken 페이지로 이동
   - 또는 직접 접속

2. **Authtoken 복사**
   - 페이지에 표시된 authtoken 복사
   - 예: `2abcdefGHIJKLMnopQRSTuvWXYz_123456789aBcDeFgHiJkLmNo`

## 3️⃣ Authtoken 설정

터미널에서 다음 명령어 실행:

```bash
~/Downloads/ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

**예시:**
```bash
~/Downloads/ngrok config add-authtoken 2abcdefGHIJKLMnopQRSTuvWXYz_123456789aBcDeFgHiJkLmNo
```

성공 시 메시지:
```
Authtoken saved to configuration file: /Users/chiwon/.config/ngrok/ngrok.yml
```

## 4️⃣ ngrok 터널 시작

인증 설정 후 다시 실행:

```bash
~/Downloads/ngrok http 5000
```

성공하면 다음과 같은 화면 표시:

```
Session Status                online
Account                       your-email@example.com
Version                       3.36.1
Region                        Asia Pacific (ap)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123def456.ngrok.io -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

> [!IMPORTANT]
> **`https://abc123def456.ngrok.io`** 형태의 URL을 복사하세요!
> 이 URL을 Streamlit Cloud secrets에 설정합니다.

## 5️⃣ ngrok URL 테스트

새 터미널에서 백엔드 헬스 체크:

```bash
curl https://your-ngrok-url.ngrok.io/health
```

예상 응답:
```json
{"status": "ok", "service": "LegoWorld V3 Backend"}
```

## 6️⃣ Streamlit Cloud 설정

1. **Streamlit 대시보드**
   - https://share.streamlit.io/ 접속
   - LegoWorld 앱 선택

2. **Secrets 추가**
   - Settings (⚙️) → Secrets
   - 다음 내용 입력:

```toml
BACKEND_URL = "https://your-ngrok-url.ngrok.io"
```

3. **저장 및 재배포**
   - Save 클릭
   - 앱 자동 재시작 (1-2분 소요)

## ✅ 최종 테스트

1. **모바일 앱 접속**
   - https://legodemo-bzfvc6bgmxmhrmxyfxhcsk.streamlit.app/

2. **사진 업로드 테스트**
   - "📸 Add Photo" 탭
   - 사진 촬영 또는 업로드
   - "📤 Add to Collection" 클릭

3. **확인**
   - "🖼️ My Gallery" 탭에서 사진 확인
   - "✅ Photo added successfully!" 메시지 표시

## 🔍 ngrok Web Interface

ngrok 실행 중 브라우저에서 확인 가능:
- http://localhost:4040
- 모든 HTTP 요청/응답 실시간 모니터링
- 디버깅에 유용

## 📝 중요 사항

> [!WARNING]
> **ngrok 무료 플랜 제한:**
> - ngrok 터미널을 닫으면 URL이 무효화됨
> - 새로 시작하면 URL이 변경됨
> - URL 변경 시 Streamlit Secrets도 업데이트 필요

> [!TIP]
> **ngrok을 백그라운드로 실행:**
> ```bash
> # tmux 사용
> tmux new -s ngrok
> ~/Downloads/ngrok http 5000
> # Ctrl+B, D로 detach
> 
> # 다시 연결
> tmux attach -t ngrok
> ```

## 🚀 다음 단계

인증 완료 후:
1. ngrok 터널 시작
2. HTTPS URL 복사
3. Streamlit Cloud secrets 설정
4. 모바일에서 사진 촬영 테스트
5. TV 앱에서 확인!

---

**질문이 있으시면 언제든지 물어보세요!** 🎉
