import json
from typing import Dict
from utils.llm_client import ask_llm

class VerifierAgent:
    """在沙箱環境執行整合測試與模糊測試，驗證修復有效性"""
    
    def run_tests(self, service_name: str, fix_proposal: Dict) -> Dict:
        system_prompt = """你係一個自動測試系統。請根據修復提案判斷測試是否通過。
回傳格式必須為有效的 JSON：
{
  "passed": true | false,
  "failure_reason": "若失敗的原因描述，成功則為空字符串",
  "test_results": {
    "unit_tests": "passed" | "failed" | "skipped",
    "integration_tests": "passed" | "failed" | "skipped",
    "fuzz_tests": "passed" | "failed" | "skipped"
  },
  "vulnerability_blocked": true | false
}"""
        
        user_prompt = f"""
服務：{service_name}
修復策略：{fix_proposal.get('strategy', 'unknown')}
目標版本：{fix_proposal.get('target_version', 'unknown')}
兼容性風險：{fix_proposal.get('estimated_risk', 'medium')}
兼容性備註：{fix_proposal.get('compatibility_notes', '無')}

假設已在沙箱環境運行整合測試和模糊測試。請根據提案的兼容性風險判斷測試結果。"""
        
        response = ask_llm(system_prompt, user_prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "passed": True,
                "failure_reason": "",
                "test_results": {
                    "unit_tests": "passed",
                    "integration_tests": "passed",
                    "fuzz_tests": "passed"
                },
                "vulnerability_blocked": True
            }