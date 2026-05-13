# Codex Red Team Opt-In Mode

[English](./README.md) | 中文

> **默认普通模式。只有在你明确开启时，才进入红队模式。**

这是一个面向 Codex 的**轻量级、分层路由型红队配置层**。

项目默认保持 **normal mode**，只有你显式开启时，才会进入 **red-team routing**。当前提供：

- opt-in 红队模式
- 轻量 hooks
- 结构化 JSON 模式状态
- 规则优先 + 语义兜底的 phase 检测
- 会话隔离状态
- 结构化红队任务编排
- **phase → method → router → leaf** 四层路由
- 对 `qiushi-skill`、`hack-skills`、`Anthropic-Cybersecurity-Skills` 的结构化集成参考
- 根目录 `config.toml` + `instruction.ctf.md` 提示词布局

---

## 为什么做这个项目

很多“常驻红队提示词”最后都会变成两种坏结果：

1. **污染普通工作**
2. **注入过重，导致上下文膨胀**

这个项目反过来做：

- **普通模式保持普通**
- **红队模式必须显式开启**
- **hooks 保持轻量**
- **路由保持分层与克制**

---

## 功能特性

- **仅显式开启**
  - 默认是 normal mode
  - 必须显式开启才进入 red-team mode

- **分层路由**
  - phase
  - method
  - router
  - leaf

- **skill 集成**
  - `qiushi-skill` → 方法层
  - `hack-skills` → 技术路由层
  - `Anthropic-Cybersecurity-Skills` → skill pack 结构与 progressive disclosure 参考

- **扩展后的红队域**
  - web
  - ad
  - postex
  - reverse
  - code-audit
  - payload
  - evasion

- **规则优先 + 语义兜底**
  - 显式命令与强特征优先命中
  - 对自然语言表达使用轻量语义兜底

- **会话隔离**
  - 一个会话不会覆盖另一个会话的模式状态

- **结构化任务编排层**
  - recon → strategy → exploit-dev → review → reporting
  - 结构化 artifact
  - review-before-delivery

- **跨平台安装**
  - Windows / macOS / Linux

- **可验证**
  - 安装验证
  - hook 验证
  - router 验证
  - orchestration gate 验证
  - 普通模式洁净性验证

---

## 安装

安装器现在默认执行**托管式增量安装**：

- 保留用户原有的 `AGENTS.md` 与 `hooks.json`
- 在 `AGENTS.md` 中增量注入本项目的托管区块
- 在 `hooks.json` 中增量注入本项目的托管 hooks
- 直接删除旧版本遗留的托管运行时代码路径
- 再写入当前版本运行时代码
- 写入本地 install manifest 供后续升级使用
- 安装后自动运行 validate

### Python

```bash
python scripts/install.py
```

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

### macOS / Linux

```bash
python3 scripts/install.py
```

---

## 快速开始

### 开启红队模式

```text
进入红队模式
开启红队模式
/redteam on
/redteam light
/redteam full
enable red team mode
```

### 关闭红队模式

```text
退出红队模式
关闭红队模式
/redteam off
disable red team mode
```

### 验证安装

```bash
python scripts/validate.py
```

---

## 工作方式

### 1. 模式门控

项目默认处于 **normal** 模式。

除非你明确开启红队模式，否则：

- 不会注入 offensive doctrine
- 不会把普通任务强行解释成红队任务

### 2. 轻量 hooks

运行时 hook 刻意保持很小：

- SessionStart 注入短上下文
- 不做巨型 prompt 注入
- 不做 always-on offensive 偏置

### 3. 分层路由

运行时现在会发出紧凑的 route envelope：

```text
[security:redteam]
[mode:redteam-light]
[phase:web]
[method:investigation-first]
[router:auth-sec]
[leaf:jwt-oauth-token-attacks]
```

### 4. 结构化任务编排

对于更大的任务，项目提供轻量编排层：

```text
recon -> strategy -> exploit-dev -> review -> reporting
```

注意：

- 这不是 always-on 自动攻击链
- 它是一个**结构化规划与 gate 框架**

---

## 仓库结构

```text
.github/
config.toml
instruction.ctf.md
agents/
  skills/
    red-team-command-doctrine/
codex/
  AGENTS.md
  hooks/
  router/
  orchestrator/
docs/
scripts/
templates/
tests/
```

当前仓库的**主提示词文件**改为：

- `./instruction.ctf.md`

根目录 `config.toml` 现在指向：

```toml
# Codex red-team profile
model_instructions_file = './instruction.ctf.md'
```

---

## 验证内容

当前项目会验证：

- 模式开启/关闭
- phase 路由
- method / router / leaf 路由
- 语义 fallback
- 普通模式洁净性
- 会话隔离
- orchestration gates

---

## 当前限制

- 它是一个**控制层 / 配置层**，不是完整攻击平台
- 不包含 RAG 或私有知识库检索
- 实际执行深度仍依赖你的 MCP / 工具面

---

## ⚠️ 免责声明

**本项目仅供授权渗透测试（Authorized Penetration Testing）、红队研究与防御性安全实验使用。**

- 仅限在你拥有明确授权的系统或环境中使用。
- 未经授权用于第三方或生产系统属于禁止行为。
- 作者及贡献者对误用、法律后果、服务中断或数据损失 **不承担任何责任**。
- 使用本项目即表示你同意自行承担全部风险，并确保行为符合适用法律和规则。

---

## 贡献与致谢

感谢米斯特安全团队的洺熙大佬提出的修改意见：加入语义判定。  
洺熙X：@xishan12509850

感谢 `qiushi-skill`、`hack-skills` 与 `Anthropic-Cybersecurity-Skills` 提供的方法层、技术路由层与 skill pack 结构参考。  
参考项目：`qiushi-skill` / `yaklang/hack-skills` / `mukul975/Anthropic-Cybersecurity-Skills`

见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## 许可证

MIT + authorized-use-only notice。  
见 [LICENSE](./LICENSE)。
