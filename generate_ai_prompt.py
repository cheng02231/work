#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI提示词生成脚本
读取监控数据并生成结构化提示词供AI使用
"""

import json
import os
import glob
import datetime


def generate_prompt(data_file: str) -> str:
    """
    根据监控数据生成AI提示词

    Args:
        data_file: JSON数据文件路径

    Returns:
        生成的AI提示词文本
    """
    # 读取数据
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取关键信息
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

    # 生成提示词
    prompt = f"""# 国际物流监控报告生成请求

## 📊 基本信息

**报告类型**: 国际物流形势深度分析报告
**监控周期**: {start_date} 至 {end_date}
**生成时间**: {timestamp}
**事件统计**:
- 美国事件: {us_incidents}起
- 全球事件: {global_events}起
- 海关风险: {customs_issues}项
- 承运商问题: {carrier_issues}起

## 🎯 任务要求

请基于以下监控数据，生成一份专业的国际物流形势分析报告，要求：

### 报告结构
1. **执行摘要** (Executive Summary)
   - 核心观点总结
   - 关键风险提醒
   - 影响评估（高/中/低）

2. **美国物流市场分析**
   - 劳工罢工事件（如有）
   - 枢纽事故影响（如有）
   - 政策更新解读
   - 极端天气影响
   - 港口运营数据

3. **全球物流趋势**
   - 地缘政治影响
   - 运价走势分析
   - 港口拥堵状况
   - 重大事件回顾

4. **海关与合规**
   - 查验政策变化
   - 风险类别说明
   - 合规建议

5. **承运商服务状态**
   - USPS服务状态
   - FedEx服务状态
   - 亚马逊FBA状态

6. **风险警示与建议**
   - 高风险事件清单
   - 应对策略建议
   - 预警指标监测

### 写作要求
- ✅ 专业术语准确
- ✅ 数据支撑充分
- ✅ 分析逻辑清晰
- ✅ 建议具体可操作
- ✅ 语言简洁专业
- ✅ 使用Markdown格式
- ✅ 字数：5000-8000字

---

## 📋 监控数据

```json
{json.dumps(data, ensure_ascii=False, indent=2)}
```

---

## 📌 注意事项

1. 对于数据为空或"待更新"的项，请标注"数据更新中"
2. 重要风险事件请用⚠️符号标注
3. 关键数据请用加粗突出显示
4. 每个章节前请提供简要的内容预告
5. 报告结尾请提供后续关注重点
"""

    return prompt


def main():
    """主函数"""
    # 查找输出目录中的JSON文件
    output_dir = "output"
    if not os.path.exists(output_dir):
        print(f"❌ 输出目录不存在: {output_dir}")
        return False

    # 查找最新的JSON文件
    json_files = glob.glob(os.path.join(output_dir, "logistics_data_*.json"))
    if not json_files:
        print("❌ 未找到监控数据文件")
        return False

    # 获取最新的文件
    data_file = max(json_files, key=os.path.getmtime)
    print(f"📄 使用数据文件: {data_file}")

    # 生成提示词
    prompt = generate_prompt(data_file)

    # 保存提示词
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    prompt_file = os.path.join(output_dir, f"ai_prompt_{timestamp}.txt")

    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)

    print(f"✅ AI提示词已生成: {prompt_file}")
    print(f"📝 提示词长度: {len(prompt)} 字符")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
