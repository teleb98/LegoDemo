# Streamlit Cloud Secrets 설정

ngrok 터널이 성공적으로 시작되었습니다! 🎉

## ngrok Public URL

```
https://marlena-glossological-hyperconfidently.ngrok-free.dev
```

## Streamlit Cloud 설정 방법

### 1. Streamlit Cloud 대시보드 접속

브라우저에서:
```
https://share.streamlit.io/
```

### 2. 앱 찾기

- 왼쪽 메뉴에서 앱 목록 확인
- LegoWorld 또는 해당 앱 선택

### 3. Settings 열기

- 앱 우측의 Settings (⚙️) 버튼 클릭
- 또는 오른쪽 상단 메뉴에서 Settings 선택

### 4. Secrets 추가

- 왼쪽 메뉴에서 **Secrets** 클릭
- 다음 내용을 입력:

```toml
BACKEND_URL = "https://marlena-glossological-hyperconfidently.ngrok-free.dev"
```

### 5. 저장 및 재배포

- **Save** 버튼 클릭
- 앱이 자동으로 재시작됩니다 (1-2분 소요)
- "Your app is being redeployed" 메시지 확인

## 테스트

재배포 완료 후:

1. **모바일 앱 접속**
   ```
   https://legodemo-bzfvc6bgmxmhrmxyfxhcsk.streamlit.app/
   ```

2. **사진 업로드**
   - "📸 Add Photo" 탭
   - 카메라로 사진 촬영 또는 파일 업로드
   - "📤 Add to Collection" 클릭

3. **성공 확인**
   - "✅ Photo added successfully!" 메시지
   - 🎈 풍선 애니메이션
   - "🖼️ My Gallery" 탭에서 사진 확인

## 중요 사항

> [!WARNING]
> - ngrok 터미널을 닫으면 연결이 끊어집니다
> - 터미널을 열어둔 채로 유지하세요
> - URL 변경 시 Streamlit Secrets도 업데이트 필요

## 백엔드 상태 확인

ngrok Web Interface에서 실시간 모니터링:
```
http://localhost:4040
```

모든 HTTP 요청/응답을 확인할 수 있습니다.

---

**설정 완료 후 테스트해보세요!** 🚀
