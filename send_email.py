#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件发送脚本
支持GitHub Actions环境变量和附件发送
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import glob
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_email_body(data_file: str) -> str:
    """
    创建邮件正文HTML

    Args:
        data_file: JSON数据文件路径

    Returns:
        HTML格式的邮件正文
    """
    import json

    # 读取数据
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取报告信息
    report_date = data.get('report_period', {}).get('report_date', '未知')
    start_date = data.get('report_period', {}).get('start_date', '未知')
    end_date = data.get('report_period', {}).get('end_date', '未知')
    timestamp = data.get('timestamp', '未知')

    # 统计事件数量
    us_incidents = len(data.get('us_logistics', {}).get('labor_strikes', [])) + \
                   len(data.get('us_logistics', {}).get('hub_incidents', [])) + \
                   len(data.get('us_logistics', {}).get('policy_updates', [])) + \
                   len(data.get('us_logistics', {}).get('extreme_weather', []))

    global_events = len(data.get('global_logistics', {}).get('major_events', []))
    customs_issues = len(data.get('customs_monitor', {}).get('risk_categories', []))
    carrier_issues = len(data.get('usps_fedex_amazon', {}).get('usps', {}).get('incidents', [])) + \
                     len(data.get('usps_fedex_amazon', {}).get('fedex', {}).get('incidents', []))

    # 生成HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px 10px 0 0;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .header p {{
                margin: 10px 0 0;
                opacity: 0.9;
            }}
            .content {{
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .summary {{
                display: flex;
                justify-content: space-around;
                margin: 30px 0;
                text-align: center;
            }}
            .summary-item {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                min-width: 120px;
            }}
            .summary-item .number {{
                font-size: 32px;
                font-weight: bold;
                color: #667eea;
            }}
            .summary-item .label {{
                font-size: 14px;
                color: #666;
                margin-top: 5px;
            }}
            .section {{
                background: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }}
            .section h2 {{
                margin-top: 0;
                color: #667eea;
                font-size: 20px;
            }}
            .alert {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 10px 0;
                border-radius: 4px;
            }}
            .alert-urgent {{
                background: #f8d7da;
                border-left: 4px solid #dc3545;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding: 20px;
                background: #f0f0f0;
                border-radius: 8px;
                color: #666;
                font-size: 14px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f8f9fa;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 国际物流监控报告</h1>
            <p>报告日期：{report_date}</p>
        </div>

        <div class="content">
            <div class="summary">
                <div class="summary-item">
                    <div class="number">{us_incidents}</div>
                    <div class="label">美国事件</div>
                </div>
                <div class="summary-item">
                    <div class="number">{global_events}</div>
                    <div class="label">全球事件</div>
                </div>
                <div class="summary-item">
                    <div class="number">{customs_issues}</div>
                    <div class="label">海关风险</div>
                </div>
                <div class="summary-item">
                    <div class="number">{carrier_issues}</div>
                    <div class="label">承运商问题</div>
                </div>
            </div>

            <div class="section">
                <h2>📅 监控周期</h2>
                <table>
                    <tr>
                        <th>项目</th>
                        <th>时间</th>
                    </tr>
                    <tr>
                        <td>开始日期</td>
                        <td>{start_date}</td>
                    </tr>
                    <tr>
                        <td>结束日期</td>
                        <td>{end_date}</td>
                    </tr>
                    <tr>
                        <td>生成时间</td>
                        <td>{timestamp}</td>
                    </tr>
                </table>
            </div>

            <div class="section">
                <h2>🚨 重要提醒</h2>
                <div class="alert alert-urgent">
                    <strong>⚠️ 请注意：</strong>
                    <ul>
                        <li>本邮件包含附件，请下载查看完整数据</li>
                        <li>如需生成分析报告，请将附件中的AI提示词发送给AI助手</li>
                        <li>重要事件请及时关注并采取应对措施</li>
                    </ul>
                </div>
            </div>

            <div class="section">
                <h2>📦 数据统计</h2>
                <p>本报告包含以下监控数据：</p>
                <ul>
                    <li>✅ 美国物流市场动态</li>
                    <li>✅ 全球物流市场趋势</li>
                    <li>✅ 海关查验政策更新</li>
                    <li>✅ USPS/FedEx/亚马逊服务状态</li>
                </ul>
            </div>
        </div>

        <div class="footer">
            <p>此报告由国际物流监控系统自动生成</p>
            <p>生成时间：{timestamp}</p>
            <p>如有疑问，请联系系统管理员</p>
        </div>
    </body>
    </html>
    """

    return html


def attach_file(msg: MIMEMultipart, file_path: str):
    """
    添加附件到邮件

    Args:
        msg: 邮件对象
        file_path: 文件路径
    """
    try:
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())

        encoders.encode_base64(part)

        # 获取文件名
        filename = os.path.basename(file_path)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="{filename}"'
        )

        msg.attach(part)
        logger.info(f"✅ 附件添加成功: {filename}")
        return True

    except Exception as e:
        logger.error(f"❌ 附件添加失败 [{file_path}]: {str(e)}")
        return False


def send_email():
    """
    发送邮件主函数
    从环境变量读取配置，支持多附件
    """
    try:
        # 从环境变量读取配置
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = os.getenv('SMTP_PORT')
        smtp_user = os.getenv('SMTP_USER')
        smtp_password = os.getenv('SMTP_PASSWORD')
        from_addr = os.getenv('FROM_ADDR', smtp_user)
        to_addrs = os.getenv('TO_ADDRS')

        # 验证必要参数
        if not all([smtp_server, smtp_port, smtp_user, smtp_password, to_addrs]):
            missing = []
            if not smtp_server:
                missing.append('SMTP_SERVER')
            if not smtp_port:
                missing.append('SMTP_PORT')
            if not smtp_user:
                missing.append('SMTP_USER')
            if not smtp_password:
                missing.append('SMTP_PASSWORD')
            if not to_addrs:
                missing.append('TO_ADDRS')

            raise ValueError(f"缺少必要的环境变量: {', '.join(missing)}")

        # 打印配置信息（隐藏敏感信息）
        logger.info("="*60)
        logger.info("邮件发送配置")
        logger.info("="*60)
        logger.info(f"SMTP服务器: {smtp_server}:{smtp_port}")
        logger.info(f"发件人: {from_addr}")
        logger.info(f"收件人: {to_addrs}")
        logger.info(f"SMTP用户: {smtp_user}")
        logger.info("="*60)

        # 查找输出目录中的文件
        output_dir = "output"
        if not os.path.exists(output_dir):
            logger.error(f"❌ 输出目录不存在: {output_dir}")
            return False

        # 查找最新的JSON文件
        json_files = glob.glob(os.path.join(output_dir, "*.json"))
        if not json_files:
            logger.error("❌ 未找到JSON数据文件")
            return False

        # 获取最新的文件
        data_file = max(json_files, key=os.path.getmtime)
        logger.info(f"📄 使用数据文件: {data_file}")

        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addrs

        # 生成邮件主题
        import json
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        report_date = data.get('report_period', {}).get('report_date', '未知')
        msg['Subject'] = f"📊 国际物流监控报告 - {report_date}"

        # 创建邮件正文
        html_body = create_email_body(data_file)
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))

        # 添加附件
        files_to_attach = glob.glob(os.path.join(output_dir, "*.*"))
        logger.info(f"📦 准备添加 {len(files_to_attach)} 个附件...")

        attachment_count = 0
        for file_path in files_to_attach:
            if attach_file(msg, file_path):
                attachment_count += 1

        logger.info(f"✅ 成功添加 {attachment_count}/{len(files_to_attach)} 个附件")

        # 发送邮件
        logger.info("📧 开始发送邮件...")

        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            # 启用TLS
            if int(smtp_port) == 587:
                server.starttls()
                logger.info("🔒 TLS加密已启用")

            # 登录
            server.login(smtp_user, smtp_password)
            logger.info("✅ SMTP登录成功")

            # 发送邮件
            server.send_message(msg)
            logger.info("✅ 邮件发送成功!")

        return True

    except Exception as e:
        logger.error(f"❌ 邮件发送失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = send_email()
    exit(0 if success else 1)
