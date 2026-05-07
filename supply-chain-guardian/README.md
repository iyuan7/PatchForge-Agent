# 供應鏈守護者 (Supply Chain Guardian)

基於多 Agent 協作的智能軟件供應鏈漏洞檢測與自動修復系統。

透過「監測 → 分析 → 修復 → 驗證 → 回溯」閉環，將高危漏洞修復時間由數週縮短至數小時。

## 核心亮點

- **多 Agent 協作**：5 個專職 Agent 互相配合完成漏洞修復閉環
- **長鏈推理**：從 API 入口逐層追蹤至脆弱函數，精準判斷漏洞真實可達性
- **反思回溯**：修復失敗時自動分析根因並重新規劃策略
- **沙箱驗證**：自動執行整合測試與模糊測試確保修復安全

## 架構圖

```
[監測 Agent] → [依賴分析 Agent] → [修復 Agent] → [驗證 Agent]
                     ↑                                   ↓
                     └──── [回溯 Agent] ←─── 驗證失敗 ────┘
```

## 快速開始

1. Clone 專案
```bash
git clone https://github.com/yourname/supply-chain-guardian.git
cd supply-chain-guardian
```

2. 安裝依賴
```bash
pip install -r requirements.txt
```

3. 設定環境變數
```bash
cp .env.example .env
# 編輯 .env，填入你的 OpenAI API Key
```

4. 運行主流程
```bash
python main.py
```

## 自訂數據

- `data/cve_feed.json`：漏洞情報（CVE/NVD 公告）
- `data/sbom_registry.json`：服務的軟件物料清單（SBOM）

按照現有格式添加你的微服務即可。

## 系統要求

- Python 3.10+
- OpenAI API Key（或其他兼容介面）

## License

MIT