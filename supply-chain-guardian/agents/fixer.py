import json
from typing import Dict
from utils.llm_client import ask_llm

class FixerAgent:
    """對可達漏洞生成修復 PR（升級版本或打補丁），檢查兼容性"""
    
    def generate_fix(self, service_name: str, alert: Dict, installed_version: str) -> Dict:
        system_prompt = """你係一位資深 DevOps 工程師。請根據漏洞信息提出具體修復方案。
回傳格式必須為有效的 JSON：
{
  "strategy": "upgrade" | "patch",
  "target_version": "建議的安全版本號",
  "compatibility_notes": "潛在兼容性問題描述",
  "pr_description": "PR 描述文字",
  "estimated_risk": "low" | "medium" | "high"
}"""
        
        user_prompt = f"""
服務：{service_name}
漏洞套件：{alert['package']}
目前版本：{installed_version}
影響版本範圍：{alert['affected_versions']}
漏洞描述：{alert['description']}
漏洞嚴重性：{alert['severity']}
請提供最適合的修復方案。"""
        
        response = ask_llm(system_prompt, user_prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "strategy": "upgrade",
                "target_version": "unknown",
                "compatibility_notes": "解析失敗",
                "pr_description": f"修復 {alert['cve_id']} 漏洞",
                "estimated_risk": "high"
            }