#!/bin/bash
# LegoWorld V3 - Tizen Studio Workspace Copy Script
# 이 스크립트를 실행하면 프로젝트가 Tizen Studio workspace에 복사됩니다

echo "=================================="
echo "LegoWorld V3 Tizen Studio Import"
echo "=================================="
echo ""

# Tizen Studio workspace 경로 찾기
POSSIBLE_WORKSPACES=(
    "$HOME/tizen-studio-data/workspace"
    "$HOME/workspace"
    "$HOME/Documents/tizen-workspace"
    "$HOME/tizen-workspace"
)

WORKSPACE=""
for ws in "${POSSIBLE_WORKSPACES[@]}"; do
    if [ -d "$ws" ]; then
        WORKSPACE="$ws"
        echo "✅ Tizen Studio workspace 발견: $WORKSPACE"
        break
    fi
done

if [ -z "$WORKSPACE" ]; then
    echo "❌ Tizen Studio workspace를 찾을 수 없습니다."
    echo ""
    echo "수동으로 workspace 경로를 입력하세요:"
    echo "예: /Users/yourname/tizen-studio-data/workspace"
    read -p "Workspace 경로: " WORKSPACE
    
    if [ ! -d "$WORKSPACE" ]; then
        echo "❌ 입력한 경로가 존재하지 않습니다: $WORKSPACE"
        exit 1
    fi
fi

echo ""

# 소스 프로젝트 경로
SOURCE="/Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3/tizen"

if [ ! -d "$SOURCE" ]; then
    echo "❌ 소스 프로젝트를 찾을 수 없습니다: $SOURCE"
    exit 1
fi

# 프로젝트 복사
DEST="$WORKSPACE/LegoWorldV3"

echo "📂 소스: $SOURCE"
echo "📂 대상: $DEST"
echo ""

if [ -d "$DEST" ]; then
    echo "⚠️  대상 위치에 이미 LegoWorldV3 프로젝트가 존재합니다."
    read -p "기존 프로젝트를 삭제하고 새로 복사하시겠습니까? (y/n): " answer
    if [ "$answer" != "y" ] && [ "$answer" != "Y" ]; then
        echo "취소되었습니다."
        exit 0
    fi
    echo "🗑️  기존 프로젝트 삭제 중..."
    rm -rf "$DEST"
fi

echo "📋 프로젝트 복사 중..."
cp -r "$SOURCE" "$DEST"

if [ $? -eq 0 ]; then
    echo "✅ 복사 완료!"
    echo ""
    echo "=================================="
    echo "다음 단계:"
    echo "=================================="
    echo "1. Tizen Studio를 완전히 종료 (Command+Q)"
    echo "2. Tizen Studio 재시작"
    echo "3. Project Explorer에서 LegoWorldV3 프로젝트 확인"
    echo "4. 프로젝트가 안 보이면: File → Refresh (F5)"
    echo ""
    echo "프로젝트 위치: $DEST"
    echo ""
    ls -la "$DEST"
else
    echo "❌ 복사 실패"
    exit 1
fi
