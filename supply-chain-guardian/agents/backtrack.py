import json
from typing import Dict
from utils.llm_client import ask_llm

class BacktrackAgent:
    """驗證失敗時，分析根因並重新規劃修復策略（反思長鏈推理）"""
    
    def re_evaluate(self, service_name: str, original_fix: Dict, failure_reason: str, alert: Dict) -> Dict:
        system_prompt = """你係一位資深 SRE 工程師。上次修復失敗，請分析原因並提供一個新的修復方案。
回傳格式必須為有效的 JSON，與之前相同：
{
  "strategy": "upgrade" | "patch" | "workaround",
  "target_version": "建議的安全版本號或修補方法",
  "compatibility_notes": "潛在兼容性問題描述",
  "pr_description": "PR 描述文字",
  "estimated_risk": "low" | "medium" | "high"
}"""
        
        user_prompt = f"""
服務：{service_name}
原始修復提案：{original_fix}
失敗原因：{failure_reason}
漏洞詳情：
  - CVE ID: {alert['cve_id']}
  - 套件: {alert['package']}
  - 影響版本: {alert['affected_versions']}
  - 嚴重性: {alert['severity']}
  - 描述: {alert['description']}

請分析失敗根因，並重新生成修復方案，避免相同問題。"""
        
        response = ask_llm(system_prompt, user_prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "strategy": "workaround",
                "target_version": "manual-review",
                "compatibility_notes": f"自動修復失敗，原因：{failure_reason}",
                "pr_description": f"修復 {alert['cve_id']} - 需要手動審查",
                "estimated_risk": "high"
            }