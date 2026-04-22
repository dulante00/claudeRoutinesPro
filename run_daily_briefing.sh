#!/bin/bash
# 每日科技简报执行脚本

set -e

echo "🚀 开始执行每日科技简报任务..."
echo ""

# 检查环境变量
if [ -z "$SERVERCHAN_SENDKEY" ]; then
    echo "⚠️  警告: SERVERCHAN_SENDKEY 未设置"
else
    echo "✅ SERVERCHAN_SENDKEY 已配置"
fi

# 运行Python脚本
echo "运行简报生成脚本..."
python3 daily_briefing.py

# 如果推送失败，检查是否有手动重试选项
if [ -f last_failed.md ]; then
    echo ""
    echo "💡 提示: 上次推送失败，内容已保存到 last_failed.md"
fi

echo ""
echo "✅ 任务完成！"
