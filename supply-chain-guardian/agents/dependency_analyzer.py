import json
from typing import List, Dict
from utils.llm_client import ask_llm

class DependencyAnalyzerAgent:
    """建構全域依賴圖譜，利用長鏈推理判斷漏洞可達性"""
    
    def __init__(self, sbom_path: str = "data/sbom_registry.json"):
        with open(sbom_path, "r") as f:
            self.sbom = json.load(f)
    
    def analyze_reachability(self, alert: Dict) -> List[Dict]:
        affected_package = alert["package"]
        results = []
        
        for service_name, info in self.sbom.items():
            if affected_package in info["direct_dependencies"]:
                version = info["direct_dependencies"][affected_package]
                reachable = self._trace_reachability(service_name, info, alert)
                results.append({
                    "service": service_name,
                    "installed_version": version,
                    "reachable": reachable,
                    "api_entry": info["api_endpoints"],
                    "call_graph": info.get("call_graph", {})
                })
        
        reachable_services = [r for r in results if r["reachable"]]
        print(f"[Dependency Analyzer] 可達漏洞的服務：{[r['service'] for r in reachable_services]}")
        return reachable_services
    
    def _trace_reachability(self, service_name: str, info: Dict, alert: Dict) -> bool:
        system_prompt = """你係一位軟件安全專家。請根據提供的資訊判斷漏洞是否可從外部API被利用。
回答只能係「TRUE」或「FALSE」，然後加上簡短解釋。"""
        
        user_prompt = f"""
服務：{service_name}
API端點：{info['api_endpoints']}
調用圖譜：{info.get('call_graph', {})}
存在漏洞的套件：{alert['package']}，版本：{info['direct_dependencies'].get(alert['package'])}，漏洞描述：{alert['description']}
請推理：從這些API入口是否可以呼叫到該漏洞函數？若無明確呼叫路徑則為FALSE。
"""
        
        response = ask_llm(system_prompt, user_prompt)
        return "TRUE" in response.upper()