# 客服 Agent 数据库回归测试

在本实验目录中运行：

```bash
python -m pip install tinydb
python -m unittest discover -s tests -v
```

测试使用临时 JSON 文件和真实 TinyDB，覆盖指定数据库的初始化、重置后的查询缓存、默认辅助函数兼容性，以及 `reseed=False` 时保留数据。测试从 Notebook 读取并执行实际的提示词、生成与执行函数和 `customer_service_agent`；仅替换模型响应和 HTML 展示，不需要 API Key，也不调用远程模型。临时目录会在测试结束后清理，不会修改实验的 `store_db.json`。
