#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国际物流信息自动监控脚本
每周五自动收集国际物流信息并生成报告
"""

import json
import datetime
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
import time

class LogisticsMonitor:
    """国际物流监控器"""

    def __init__(self):
        self.data = {
            "report_period": {},
            "us_logistics": {},
            "global_logistics": {},
            "customs_monitor": {},
            "usps_fedex_amazon": {},
            "data_sources": []
        }
        self.start_date = None
        self.end_date = None

    def set_report_period(self, days_back: int = 7):
        """设置报告周期（默认过去7天）"""
        today = datetime.datetime.now()
        self.end_date = today
        self.start_date = today - datetime.timedelta(days=days_back)

        self.data["report_period"] = {
            "start_date": self.start_date.strftime("%Y年%m月%d日"),
            "end_date": self.end_date.strftime("%Y年%m月%d日"),
            "report_date": today.strftime("%Y年%m月%d日")
        }

        print(f"✅ 报告周期已设置：{self.data['report_period']['start_date']} 至 {self.data['report_period']['end_date']}")

    def collect_from_websources(self) -> Dict:
        """
        从网络数据源收集信息
        注意：此功能需要配合我（AI助手）使用，或者使用专门的爬虫工具
        """
        print("⚠️  注意：网络数据收集需要配合AI助手完成")
        print("💡 建议：每周五执行时，先将此部分信息提供给AI助手")

        return {
            "note": "网络数据收集建议使用AI助手完成",
            "manual_trigger": True
        }

    def collect_manual_input(self) -> Dict:
        """
        手动输入收集到的信息
        返回一个结构化的数据字典
        """
        print("\n" + "="*50)
        print("请根据信息收集模板手动填写以下信息：")
        print("="*50 + "\n")

        collected_data = {
            "us_logistics": {
                "labor_strikes": self._collect_labor_strikes(),
                "hub_incidents": self._collect_hub_incidents(),
                "policy_updates": self._collect_policy_updates(),
                "extreme_weather": self._collect_extreme_weather(),
                "port_data": self._collect_port_data()
            },
            "global_logistics": {
                "geopolitical": self._collect_geopolitical(),
                "freight_rates": self._collect_freight_rates(),
                "port_congestion": self._collect_port_congestion(),
                "major_events": self._collect_major_events()
            },
            "customs_monitor": {
                "policy_enforcement": self._collect_customs_policy(),
                "risk_categories": self._collect_risk_categories()
            },
            "usps_fedex_amazon": self._collect_service_monitoring()
        }

        return collected_data

    def _collect_labor_strikes(self) -> List[Dict]:
        """收集劳资罢工事件"""
        print("\n【劳工与罢工事件】")
        strikes = []

        while True:
            print(f"\n事件 #{len(strikes)+1}")
            has_event = input("是否有罢工事件？(y/n): ").strip().lower()
            if has_event != 'y':
                break

            event = {
                "company": input("罢工公司/组织: ").strip(),
                "affected_states": input("涉及州/地区: ").strip(),
                "personnel_count": input("涉及人员数量: ").strip(),
                "start_time": input("起始时间: ").strip(),
                "end_time_estimated": input("预计结束时间: ").strip(),
                "impact_level": input("影响程度（轻微/中度/严重）: ").strip(),
                "ecommerce_impact": input("对跨境电商影响: ").strip(),
                "notes": input("备注: ").strip()
            }
            strikes.append(event)

        return strikes

    def _collect_hub_incidents(self) -> List[Dict]:
        """收集枢纽事故"""
        print("\n【枢纽事故与突发事件】")
        incidents = []

        while True:
            has_event = input(f"\n是否有枢纽事故？(y/n): ").strip().lower()
            if has_event != 'y':
                break

            incident = {
                "incident_type": input("事故类型（化学品泄漏/火灾/系统故障/其他）: ").strip(),
                "hub_name": input("影响枢纽名称: ").strip(),
                "location": input("地点: ").strip(),
                "start_time": input("起始时间: ").strip(),
                "recovery_time": input("预计恢复时间: ").strip(),
                "impact_level": input("影响程度（轻微/中度/严重）: ").strip(),
                "services_suspended": input("暂停的服务: ").strip(),
                "services_resumed": input("恢复的服务: ").strip(),
                "notes": input("备注: ").strip()
            }
            incidents.append(incident)

        return incidents

    def _collect_policy_updates(self) -> List[Dict]:
        """收集政策更新"""
        print("\n【政策与合规更新】")
        updates = []

        while True:
            has_update = input(f"\n是否有新政策发布？(y/n): ").strip().lower()
            if has_update != 'y':
                break

            update = {
                "policy_type": input("政策类型（海关查验/关税调整/认证要求/其他）: ").strip(),
                "agency": input("发布机构: ").strip(),
                "policy_name": input("政策名称: ").strip(),
                "effective_date": input("生效日期: ").strip(),
                "scope": input("适用范围: ").strip(),
                "impact_level": input("对行业影响（轻微/中度/严重）: ").strip(),
                "seller_guidance": input("卖家应对要点: ").strip(),
                "notes": input("备注: ").strip()
            }
            updates.append(update)

        return updates

    def _collect_extreme_weather(self) -> List[Dict]:
        """收集极端天气"""
        print("\n【极端天气与自然灾害】")
        events = []

        while True:
            has_event = input(f"\n是否有极端天气？(y/n): ").strip().lower()
            if has_event != 'y':
                break

            event = {
                "weather_type": input("天气类型（暴风雪/洪水/飓风/火灾/其他）: ").strip(),
                "affected_area": input("影响地区: ").strip(),
                "start_time": input("起始时间: ").strip(),
                "end_time_estimated": input("预计结束时间: ").strip(),
                "impact_level": input("影响程度（轻微/中度/严重）: ").strip(),
                "ports_closed": input("关闭的港口: ").strip(),
                "flights_cancelled": input("取消航班数量: ").strip(),
                "cost_increase": input("物流成本预估涨幅: ").strip(),
                "notes": input("备注: ").strip()
            }
            events.append(event)

        return events

    def _collect_port_data(self) -> Dict:
        """收集港口运营数据"""
        print("\n【港口运营数据】")
        ports = {}

        port_names = [
            "纽约/新泽西港",
            "洛杉矶/长滩港",
            "西雅图/塔科马港",
            "休斯顿港",
            "迈阿密港"
        ]

        for port_name in port_names:
            print(f"\n{port_name}")
            current = input(f"当前数据（TEU或等待时间等）: ").strip()
            yoy_change = input("同比变化: ").strip()
            mom_change = input("环比变化: ").strip()

            if current or yoy_change or mom_change:
                ports[port_name] = {
                    "current": current,
                    "yoy_change": yoy_change,
                    "mom_change": mom_change
                }

        return ports

    def _collect_geopolitical(self) -> Dict:
        """收集地缘政治与航运通道"""
        print("\n【地缘政治与航运通道】")
        return {
            "channel_status": input("关键通道状态（正常/受限/中断）: ").strip(),
            "affected_channels": input("影响通道（霍尔木兹海峡/苏伊士运河/巴拿马运河/其他）: ").strip(),
            "affected_routes": input("受影响航线: ").strip(),
            "carrier_actions": input("航司/船司行动: ").strip(),
            "additional_charges": input("新增附加费: ").strip(),
            "estimated_duration": input("预计持续时长: ").strip(),
            "supply_chain_impact": input("对全球供应链影响（轻微/中度/严重）: ").strip(),
            "alternative_routes": input("替代路线情况: ").strip(),
            "notes": input("备注: ").strip()
        }

    def _collect_freight_rates(self) -> Dict:
        """收集运价数据"""
        print("\n【运价与成本指数】")
        return {
            "wti_crude": input("WTI原油价格（美元/桶）: ").strip(),
            "brent_crude": input("布伦特原油价格（美元/桶）: ").strip(),
            "scfi_index": input("SCFI综合运价指数: ").strip(),
            "persian_gulf_rate": input("波斯湾航线运价: ").strip(),
            "war_risk_insurance": input("战争风险保险费率: ").strip(),
            "notes": input("备注: ").strip()
        }

    def _collect_port_congestion(self) -> Dict:
        """收集全球港口拥堵"""
        print("\n【全球港口拥堵情况】")
        ports = {}

        port_names = [
            "鹿特丹港",
            "汉堡港",
            "安特卫普港",
            "迪拜杰贝阿里港"
        ]

        for port_name in port_names:
            print(f"\n{port_name}")
            utilization = input("堆场利用率: ").strip()
            wait_time = input("平均等待时间: ").strip()
            status = input("状态（正常/拥堵/严重拥堵）: ").strip()

            if utilization or wait_time or status:
                ports[port_name] = {
                    "utilization": utilization,
                    "wait_time": wait_time,
                    "status": status
                }

        return ports

    def _collect_major_events(self) -> List[Dict]:
        """收集其他重大事件"""
        print("\n【其他重大事件】")
        events = []

        while True:
            has_event = input(f"\n是否有重大事件？(y/n): ").strip().lower()
            if has_event != 'y':
                break

            event = {
                "event_name": input("事件名称: ").strip(),
                "occurrence_time": input("发生时间: ").strip(),
                "affected_scope": input("影响范围: ").strip(),
                "severity": input("严重程度（轻微/中度/严重）: ").strip(),
                "notes": input("备注: ").strip()
            }
            events.append(event)

        return events

    def _collect_customs_policy(self) -> Dict:
        """收集海关政策执行情况"""
        print("\n【美国海关5H查验专项】")
        return {
            "enforcement_strength": input("5H查验力度（维持/加强/趋于宽松）: ").strip(),
            "inspection_rate_change": input("查验率变化: ").strip(),
            "new_focus_categories": input("新增重点关注品类: ").strip(),
            "compliance_requirement_changes": input("合规要求变化: ").strip(),
            "detention_case_count": input("扣货案例数量: ").strip(),
            "notes": input("备注: ").strip()
        }

    def _collect_risk_categories(self) -> List[Dict]:
        """收集高风险品类"""
        print("\n【高风险品类监控】")
        categories = []

        category_names = [
            "电子产品",
            "儿童用品",
            "食品接触材料",
            "带电产品",
            "服装纺织"
        ]

        for category_name in category_names:
            print(f"\n{category_name}")
            inspection_rate = input("查验率: ").strip()
            main_issues = input("主要问题: ").strip()
            guidance = input("应对建议: ").strip()

            if inspection_rate or main_issues or guidance:
                categories.append({
                    "category": category_name,
                    "inspection_rate": inspection_rate,
                    "main_issues": main_issues,
                    "guidance": guidance
                })

        return categories

    def _collect_service_monitoring(self) -> Dict:
        """收集USPS/FedEx/亚马逊服务监控"""
        print("\n【USPS/FedEx/亚马逊物流专项】")
        return {
            "usps": self._collect_single_service("USPS"),
            "fedex": self._collect_single_service("FedEx"),
            "amazon_fba": self._collect_single_service("亚马逊FBA")
        }

    def _collect_single_service(self, service_name: str) -> Dict:
        """收集单个服务商的信息"""
        print(f"\n{service_name}")
        has_incident = input("是否有服务中断事件？(y/n): ").strip().lower()

        if has_incident != 'y':
            return {"incidents": []}

        incidents = []

        while True:
            has_more = input(f"\n{service_name} - 事件 #{len(incidents)+1}，是否有更多事件？(y/n): ").strip().lower()
            if has_more != 'y':
                break

            incident = {
                "service_name": input("中断服务名称: ").strip(),
                "start_time": input("起始时间: ").strip(),
                "recovery_time": input("恢复时间: ").strip(),
                "affected_scope": input("影响范围: ").strip(),
                "timing_impact": input("时效影响评估: ").strip(),
                "alternatives": input("替代方案: ").strip(),
                "notes": input("备注: ").strip()
            }
            incidents.append(incident)

        return {"incidents": incidents}

    def save_data(self, filename: str = None):
        """保存收集的数据为JSON文件"""
        if filename is None:
            filename = f"logistics_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 数据已保存至: {filename}")
        return filename

    def generate_ai_prompt(self) -> str:
        """生成AI助手提示词"""
        prompt = f"""
请根据以下收集到的国际物流数据，生成一份完整的分析报告。

**报告周期：** {self.data['report_period']['start_date']} 至 {self.data['report_period']['end_date']}
**报告日期：** {self.data['report_period']['report_date']}

**一、美国物流市场核心动态**

## 劳工与罢工事件
{self._format_list(self.data['us_logistics'].get('labor_strikes', []))}

## 枢纽事故与突发事件
{self._format_list(self.data['us_logistics'].get('hub_incidents', []))}

## 政策与合规更新
{self._format_list(self.data['us_logistics'].get('policy_updates', []))}

## 极端天气与自然灾害
{self._format_list(self.data['us_logistics'].get('extreme_weather', []))}

## 港口运营数据
{self._format_dict(self.data['us_logistics'].get('port_data', {}))}

**二、全球物流市场连锁反应**

## 地缘政治与航运通道
{self._format_dict(self.data['global_logistics'].get('geopolitical', {}))}

## 运价与成本指数
{self._format_dict(self.data['global_logistics'].get('freight_rates', {}))}

## 全球港口拥堵情况
{self._format_dict(self.data['global_logistics'].get('port_congestion', {}))}

## 其他重大事件
{self._format_list(self.data['global_logistics'].get('major_events', []))}

**三、美国海关5H查验专项监控**

## 政策执行情况
{self._format_dict(self.data['customs_monitor'].get('policy_enforcement', {}))}

## 高风险品类监控
{self._format_list(self.data['customs_monitor'].get('risk_categories', []))}

**四、USPS/FedEx/亚马逊物流专项监控**

## USPS
{self._format_service_monitoring(self.data['usps_fedex_amazon'].get('usps', {}))}

## FedEx
{self._format_service_monitoring(self.data['usps_fedex_amazon'].get('fedex', {}))}

## 亚马逊FBA
{self._format_service_monitoring(self.data['usps_fedex_amazon'].get('amazon_fba', {}))}

请根据上述数据，生成一份完整的分析报告，包括：
1. 执行摘要
2. 美国物流市场核心动态
3. 全球物流市场连锁反应
4. 美国物流数据与市场趋势
5. 未来走势判断与建议

报告格式参考之前的"2026年3月7-13日国际物流形势深度分析报告.docx"。
"""
        return prompt

    def _format_list(self, items: List[Dict]) -> str:
        """格式化列表数据"""
        if not items:
            return "无数据"

        result = []
        for i, item in enumerate(items, 1):
            result.append(f"### 事件 #{i}")
            for key, value in item.items():
                if value:
                    result.append(f"- **{key}**: {value}")
            result.append("")

        return "\n".join(result)

    def _format_dict(self, data: Dict) -> str:
        """格式化字典数据"""
        if not data:
            return "无数据"

        result = []
        for key, value in data.items():
            if value:
                result.append(f"- **{key}**: {value}")

        return "\n".join(result)

    def _format_service_monitoring(self, data: Dict) -> str:
        """格式化服务监控数据"""
        if not data or not data.get('incidents'):
            return "无中断事件"

        incidents = data.get('incidents', [])
        result = []
        for i, incident in enumerate(incidents, 1):
            result.append(f"### 事件 #{i}")
            for key, value in incident.items():
                if value:
                    result.append(f"- **{key}**: {value}")
            result.append("")

        return "\n".join(result)


def main():
    """主函数"""
    print("="*60)
    print("国际物流信息自动监控系统")
    print("="*60)
    print()

    # 创建监控器实例
    monitor = LogisticsMonitor()

    # 设置报告周期（过去7天）
    monitor.set_report_period(days_back=7)

    # 收集数据
    print("\n开始收集数据...")
    collected_data = monitor.collect_manual_input()
    monitor.data.update(collected_data)

    # 保存数据
    json_file = monitor.save_data()
    print(f"\n✅ 数据收集完成，已保存至: {json_file}")

    # 生成AI提示词
    prompt = monitor.generate_ai_prompt()

    # 保存提示词
    prompt_file = f"ai_prompt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)

    print(f"✅ AI提示词已保存至: {prompt_file}")
    print("\n下一步：")
    print("1. 将AI提示词的内容复制并粘贴给我（AI助手）")
    print("2. 我将根据这些数据生成完整的分析报告")
    print("3. 生成后可选择导出为WORD、PPT或公众号格式")

    return json_file, prompt_file


if __name__ == "__main__":
    main()
