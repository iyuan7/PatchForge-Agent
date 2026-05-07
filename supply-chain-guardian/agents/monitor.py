import json
from datetime import datetime
from typing import List, Dict

class MonitorAgent:
    """訂閱 CVE/NVD 安全公告，解析受影響組件與版本，生成初始警示"""
    
    def __init__(self, feed_path: str = "data/cve_feed.json"):
        with open(feed_path, "r") as f:
            self.feed = json.load(f)
        self.processed_cves = set()
    
    def check_new_vulnerabilities(self) -> List[Dict]:
        alerts = []
        for cve in self.feed:
            if cve["cve_id"] not in self.processed_cves:
                alerts.append({
                    "cve_id": cve["cve_id"],
                    "package": cve["package"],
                    "affected_versions": cve["affected_versions"],
                    "severity": cve["severity"],
                    "description": cve["description"],
                    "timestamp": datetime.now().isoformat()
                })
                self.processed_cves.add(cve["cve_id"])
        
        print(f"[Monitor] 發現 {len(alerts)} 個新漏洞警示")
        return alerts