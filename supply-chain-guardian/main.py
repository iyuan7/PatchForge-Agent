import json
from agents.monitor import MonitorAgent
from agents.dependency_analyzer import DependencyAnalyzerAgent
from agents.fixer import FixerAgent
from agents.verifier import VerifierAgent
from agents.backtrack import BacktrackAgent
from config import MAX_RETRY_ATTEMPTS

def main():
    monitor = MonitorAgent()
    analyzer = DependencyAnalyzerAgent()
    fixer = FixerAgent()
    verifier = VerifierAgent()
    backtrack = BacktrackAgent()

    print("=== 供應鏈守護者啟動 ===")
    
    alerts = monitor.check_new_vulnerabilities()
    if not alerts:
        print("無新漏洞，流程結束。")
        return

    for alert in alerts:
        print(f"\n===== 處理漏洞：{alert['cve_id']} =====")
        print(f"套件: {alert['package']}")
        print(f"影響版本: {alert['affected_versions']}")
        print(f"嚴重性: {alert['severity']}")
        print(f"描述: {alert['description']}")

        reachable_services = analyzer.analyze_reachability(alert)
        
        if not reachable_services:
            print("[Dependency Analyzer] 未發現可達漏洞的服務，跳過此漏洞")
            continue

        for svc in reachable_services:
            service_name = svc["service"]
            installed_version = svc["installed_version"]
            print(f"\n[修復迴圈開始] 服務：{service_name}")
            print(f"安裝版本：{installed_version}")

            fix_proposal = fixer.generate_fix(service_name, alert, installed_version)
            print(f"[Fixer] 初始修復方案：")
            print(json.dumps(fix_proposal, indent=2, ensure_ascii=False))

            test_result = verifier.run_tests(service_name, fix_proposal)
            attempt = 1

            while not test_result.get("passed", False) and attempt < MAX_RETRY_ATTEMPTS:
                print(f"\n[Verifier] 測試失敗 (嘗試 {attempt}/{MAX_RETRY_ATTEMPTS})")
                print(f"失敗原因：{test_result.get('failure_reason', '未知')}")
                
                fix_proposal = backtrack.re_evaluate(
                    service_name, fix_proposal,
                    test_result.get("failure_reason", ""),
                    alert
                )
                print(f"[Backtrack] 新修復方案：")
                print(json.dumps(fix_proposal, indent=2, ensure_ascii=False))
                
                test_result = verifier.run_tests(service_name, fix_proposal)
                attempt += 1

            if test_result.get("passed", False):
                print(f"\n[成功] 服務 {service_name} 修復完成")
                print(f"最終方案：{json.dumps(fix_proposal, indent=2, ensure_ascii=False)}")
                print(f"測試結果：{test_result.get('test_results', {})}")
                print(f"漏洞已堵塞：{test_result.get('vulnerability_blocked', True)}")
            else:
                print(f"\n[警告] 服務 {service_name} 修復嘗試失敗 ({attempt}/{MAX_RETRY_ATTEMPTS})")
                print("需人手處理")

    print("\n===== 全流程結束 =====")

if __name__ == "__main__":
    main()