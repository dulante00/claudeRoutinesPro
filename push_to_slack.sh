#!/bin/bash
# 直接推送到 Slack Webhook 的脚本

WEBHOOK_URL="$SLACK_WEBHOOK_URL"
CONTENT="$1"

if [ -z "$WEBHOOK_URL" ]; then
    echo "错误：SLACK_WEBHOOK_URL 未设置"
    exit 1
fi

# 使用 curl 推送
RESPONSE=$(curl -s -X POST \
    -H 'Content-Type: application/json' \
    -d "$CONTENT" \
    "$WEBHOOK_URL")

echo "推送响应: $RESPONSE"

if [ "$RESPONSE" = "ok" ]; then
    echo "✅ 推送成功"
    exit 0
else
    echo "❌ 推送失败: $RESPONSE"
    exit 1
fi
