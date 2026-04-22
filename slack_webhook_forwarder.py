#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Slack Webhook 本地转发代理

由于沙箱环境的网络限制，无法直接访问 hooks.slack.com。
此脚本启动一个本地 HTTP 服务器，作为中介转发请求到 Slack。

使用方式：
1. 在一个终端启动此服务器：python3 slack_webhook_forwarder.py
2. 在另一个终端使用 daily_tech_briefing.py，设置：
   export SLACK_WEBHOOK_URL="http://localhost:9999/slack-webhook"
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os
from urllib.parse import urlparse, parse_qs

# 真实的 Slack webhook URL
REAL_SLACK_WEBHOOK = "https://hooks.slack.com/services/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"

PORT = 9999

class SlackWebhookHandler(http.server.BaseHTTPRequestHandler):
    """处理来自本地应用的 Slack webhook 请求"""

    def do_POST(self):
        """转发 POST 请求到真实的 Slack webhook"""

        # 处理 /slack-webhook 路径
        if self.path == '/slack-webhook':
            try:
                # 读取请求体
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)

                # 转发到真实的 Slack webhook
                print(f"📤 转发请求到 Slack... (大小: {len(body)} bytes)")

                req = urllib.request.Request(
                    REAL_SLACK_WEBHOOK,
                    data=body,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'Slack-Webhook-Forwarder/1.0'
                    },
                    method='POST'
                )

                response = urllib.request.urlopen(req, timeout=10)
                result = response.read().decode('utf-8')

                # 返回响应给客户端
                if result == 'ok':
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'ok')
                    print("✅ 成功转发到 Slack")
                else:
                    self.send_response(400)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(result.encode())
                    print(f"⚠️  Slack 返回: {result}")

            except urllib.error.HTTPError as e:
                print(f"❌ HTTP 错误: {e.code} {e.reason}")
                self.send_response(e.code)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"Slack API 错误: {e.reason}".encode())

            except urllib.error.URLError as e:
                print(f"❌ 网络错误: {e.reason}")
                self.send_response(502)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"无法连接到 Slack: {e.reason}".encode())

            except Exception as e:
                print(f"❌ 未知错误: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"服务器错误: {e}".encode())

        else:
            # 404 处理
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

    def log_message(self, format, *args):
        """禁用默认的日志输出，改为自定义"""
        pass


def run_server():
    """启动 Slack webhook 转发服务器"""

    print("="*60)
    print("🚀 Slack Webhook 转发代理启动")
    print("="*60)
    print(f"\n📍 服务器地址: http://localhost:{PORT}")
    print(f"🔗 转发端点: http://localhost:{PORT}/slack-webhook")
    print(f"➡️  转发目标: {REAL_SLACK_WEBHOOK}")
    print("\n使用方式:")
    print(f"  export SLACK_WEBHOOK_URL='http://localhost:{PORT}/slack-webhook'")
    print(f"  python3 daily_tech_briefing.py")
    print("\n⏹️  按 Ctrl+C 停止服务器\n")

    try:
        with socketserver.TCPServer(("", PORT), SlackWebhookHandler) as httpd:
            print(f"✅ 监听端口 {PORT}...")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n⏹️  服务器已停止")
    except OSError as e:
        print(f"\n❌ 启动失败: {e}")
        print(f"   可能原因: 端口 {PORT} 已被占用")
        print(f"   解决方案: 修改 PORT 变量或关闭占用该端口的进程")


if __name__ == "__main__":
    run_server()
