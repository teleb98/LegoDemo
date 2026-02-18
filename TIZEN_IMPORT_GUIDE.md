# LegoWorld V3 - Tizen Studio Import 해결 방법

## 문제 상황
Tizen Studio에서 "Existing Tizen Project" Import 시 프로젝트가 리스트에 나타나지 않음

## 해결 방법: 수동 복사 (가장 확실함)

### 1단계: Tizen Studio Workspace 경로 찾기

Tizen Studio를 열고:
- **Window** → **Preferences** → **General** → **Workspace**
- 현재 workspace 경로 확인 (예: `/Users/chiwon/tizen-studio-data/workspace`)

또는 터미널에서:
```bash
# 일반적인 경로들
ls ~/tizen-studio-data/workspace
ls ~/workspace
ls ~/Documents/tizen-workspace
```

### 2단계: 프로젝트 복사

Workspace 경로를 확인했다면, 터미널에서 실행:

```bash
# workspace 경로를 본인 경로로 변경
WORKSPACE=~/tizen-studio-data/workspace

# LegoWorld V3 프로젝트 복사
cp -r /Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3/tizen "$WORKSPACE/LegoWorldV3"

# 복사 확인
ls -la "$WORKSPACE/LegoWorldV3"
```

### 3단계: Tizen Studio에서 프로젝트 인식

1. **Tizen Studio를 완전히 종료** (Command+Q)
2. Tizen Studio 재시작
3. Project Explorer에서 **LegoWorldV3** 프로젝트가 자동으로 보임
4. 프로젝트가 안 보이면: **File** → **Refresh** (F5) 또는 **File** → **Restart**

---

## 대안: 새 프로젝트 생성 후 파일 복사

만약 위 방법도 안 되면:

### 1. Tizen Studio에서 새 프로젝트 생성

1. **File** → **New** → **Tizen Project**
2. **Template** 선택
3. **Profile**: TV, **Version**: 9.0, **Template**: Web Application → **Basic**
4. **Project name**: `LegoWorldV3`
5. **Finish** 클릭

### 2. 생성된 프로젝트에 파일 복사

터미널에서:
```bash
WORKSPACE=~/tizen-studio-data/workspace  # 본인 workspace 경로로 수정

# 기존 템플릿 파일 삭제 (필요한 것만 남김)
rm "$WORKSPACE/LegoWorldV3/index.html"
rm -rf "$WORKSPACE/LegoWorldV3/css"
rm -rf "$WORKSPACE/LegoWorldV3/js"

# 우리 파일 복사
cp /Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3/tizen/index.html "$WORKSPACE/LegoWorldV3/"
cp /Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3/tizen/config.xml "$WORKSPACE/LegoWorldV3/"
cp /Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3/tizen/icon.png "$WORKSPACE/LegoWorldV3/"
cp -r /Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3/tizen/css "$WORKSPACE/LegoWorldV3/"
cp -r /Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3/tizen/js "$WORKSPACE/LegoWorldV3/"
cp -r /Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3/tizen/assets "$WORKSPACE/LegoWorldV3/"
```

### 3. Tizen Studio에서 Refresh

- Project Explorer에서 **LegoWorldV3** 우클릭 → **Refresh**
- 모든 파일이 업데이트되어 보임

---

## 확인 사항

복사 후 다음을 확인:

### ✅ 파일 구조
```
LegoWorldV3/
├── .project
├── .tproject
├── config.xml
├── index.html
├── icon.png
├── css/
│   └── main.css
├── js/
│   └── main.js
└── assets/
    ├── smartbrick1.jpg
    ├── city1.jpg
    ├── space.png
    └── ...
```

### ✅ config.xml 확인
프로젝트 우클릭 → **Properties** → **Tizen** → **Package**:
- Application ID: `LegoWrldV3.LegoWorldV3`
- Package: `LegoWrldV3`
- Version: `3.0.0`

### ✅ 빌드 테스트
- **Project** → **Build Project**
- Console에서 에러 없이 빌드 완료 확인

### ✅ 패키징 테스트
- **Project** → **Build Package**
- 프로젝트 폴더에 `LegoWorldV3.wgt` 파일 생성 확인

---

## 실행 방법

### 에뮬레이터에서 실행
1. **Tools** → **Emulator Manager**
2. TV 에뮬레이터 선택 (9.0)
3. **Launch**
4. 프로젝트 우클릭 → **Run As** → **Tizen Web Application**

### 실제 TV에서 실행
1. **Tools** → **Device Manager**
2. **Remote Device Manager** → TV 추가
3. TV와 연결
4. 프로젝트 우클릭 → **Run As** → **Tizen Web Application**

---

## 자주 묻는 질문

**Q: workspace 경로를 모르겠어요**
- Tizen Studio → Window → Preferences → General → Workspace에서 확인
- 또는 Tizen Studio를 처음 실행할 때 나타나는 경로

**Q: 복사했는데 프로젝트가 회색으로 표시돼요**
- Tizen SDK 9.0이 설치되지 않았을 수 있습니다
- Tools → Package Manager → Tizen SDK → TV 9.0 설치

**Q: 빌드 에러가 나요**
- config.xml의 application ID가 고유한지 확인
- 프로젝트 우클릭 → Clean → OK → Build

---

## 현재 프로젝트 위치

소스 파일:
```
/Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3/tizen/
```

이 디렉토리를 Tizen Studio workspace로 복사하면 됩니다!

---

## 도움이 필요하면

1. **Workspace 경로를 알려주세요** - 정확한 복사 명령어를 제공하겠습니다
2. **에러 메시지를 공유해주세요** - 구체적인 해결 방법을 안내하겠습니다
3. **스크린샷을 공유해주세요** - 시각적으로 확인하여 도와드리겠습니다
