# 链上存证说明（Blockchain Attestation）

本插件的**创建记录**与**全部版本（git tag）**均已通过蚂蚁链开放联盟链（myevm）的
**AstrBot 插件存证合约（`AstrBotPluginDeposit`）** 完成链上存证，可公开核验、不可篡改。

- **合约地址**：`0x377e1ffe880072164581de8258864c2df95820e187fbfc84eeb476e966c28e03`
- **链 ID**：`a00e36c5`（蚂蚁链开放联盟链）
- **存证组织路径**：`XMZZUZHI/Astrbot`
- **合约版本**：`1.0.0`

> 说明：本仓库（CNB 侧）未打 git tag；**git tag 仅存在于 GitHub 镜像仓库**
> （`https://github.com/xiaomizhoubaobei/astrbot_plugin_emojis`）。
> 因此版本存证以 **GitHub 镜像的 tag 为真源**读取 tag → commit → 产物指纹。

## 插件创建存证

| 项目 | 值 |
|------|-----|
| 存证编号 | `#1` |
| 类别 | 插件创建 `PluginCreation` |
| 仓库 | `XMZZUZHI/Astrbot/astrbot_plugin_emojis` |
| 插件名 | `astrbot_plugin_emojis` |
| 创建 commit | `accc64e0d85120d6d2f1955ac17d2f7d37ab5276`（Initial commit） |
| 产物摘要 (SHA256) | `b14e1455185517c396c1de3af51a648e0fdcb1d9af3756eb4eebd30018e8468d` |
| **交易 hash** | `00368abd86967e1c2cc4f99f73518b99969329b2d4410e448f215ae090883920` |
| 区块高度 | `182739065` |
| gasUsed | `509,948` |
| 上链结果 | `result=0`（成功） |

## 版本（tag）存证

### tag `v0.0.1`

| 项目 | 值 |
|------|-----|
| 存证编号 | `#3` |
| 类别 | 版本发布 `ReleasePublish` |
| 版本号 | `v0.0.1` |
| 来源 | **GitHub 镜像 tag**（真源） |
| commit | `724ca595cc2fa8a8dc8d9b051664bfbde823749a` |
| 产物摘要 (SHA256) | `7c874334ca49f3b3bd833472ca3a06efde33c88b21c49f64e1783ee50f2ff4f1` |
| **交易 hash** | `c1c825afc3110558bc4a836de7338e0960d13494e00230fa6cfebf09b99ce383` |
| 区块高度 | `182739549` |
| gasUsed | `511,901` |
| 上链结果 | `result=0`（成功） |

> 另有存证 `#2`：初次存证以 CNB 侧 HEAD（`1b6c6ae6…`）记录 `metadata.yaml.version = v0.0.1`，
> 交易 hash `a6c58fb8b4a74890e923873cc71d4558c071fe022a238d719051841239f305e0`（区块 `182739072`）。
> 存证 `#3` 为补录 GitHub 镜像 tag 真源 commit。

## 产物摘要（digest）如何计算

摘要取自 **确定性 tar 归档**，任何环境均可复现同一指纹：

```bash
git archive --format=tar <tag-or-commit> | sha256sum
```

> `zip` / `tar.gz` 含时间戳等非确定性字段，同一源码在不同环境会产生不同指纹，故不采用。

## 如何核验

在「蚂蚁链开放联盟链浏览器」按合约地址搜索，或用配套脚本 `chain-contracts` 查询：

```bash
# 按插件名查询全部存证编号
python3 scripts/contract_astrbot_plugin.py query-by-plugin \
  --plugin astrbot_plugin_emojis --name AstrBotPluginDeposit

# 按 commit 查询（创建）
python3 scripts/contract_astrbot_plugin.py query-by-commit \
  --commit accc64e0d85120d6d2f1955ac17d2f7d37ab5276 --name AstrBotPluginDeposit

# 按 commit 查询（tag v0.0.1 真源）
python3 scripts/contract_astrbot_plugin.py query-by-commit \
  --commit 724ca595cc2fa8a8dc8d9b051664bfbde823749a --name AstrBotPluginDeposit

# 查看完整存证记录
python3 scripts/contract_astrbot_plugin.py get-evidence-detail \
  --id 3 --name AstrBotPluginDeposit
```

## 存证字段说明

| 字段 | 含义 |
|------|------|
| `repo` | 插件仓库路径 |
| `pluginName` | 插件名（`metadata.yaml` 的 `name`） |
| `releaseTag` | 版本号 / git tag（插件创建存证时为空） |
| `commitRef` | 存证时对应的 commit SHA（核心证据） |
| `artifactDigest` | 发布产物摘要（tar 归档 SHA256，核心证据） |
| `depositor` / `timestamp` / `blockNumber` | 存证人、时间戳、区块高度 |

---

*存证由 [XMZZUZHI/chain-contracts](https://cnb.cool/XMZZUZHI/chain-contracts) 的
`AstrBotPluginDeposit` 合约与 `scripts/contract_astrbot_plugin.py` 脚本完成。*
