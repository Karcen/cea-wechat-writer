# DUYI WeChat Skill Suite

本包是公众号生产 skill 套件的本地运行版。

维护者：DUYI

完整安装和使用说明见：

```text
README.md
```

本包只保留可执行的 Skill、脚本、模板和发布流程说明；运行无关资料、截图资产、缓存和私密配置不放入本包。

## 包含的 Skills

```text
skills/
  duyi-wechat/
  duyi-wechat-css-layer/
  duyi-wechat-paipan/
  duyi-wechat-peitu/
  duyi-wechat-fabu/
```

## 不包含的内容

- `duyi-wechat-decrypt`
- `node_modules`
- `.env`
- `__pycache__`
- `.DS_Store`
- `*.pyc`
- 非运行必需的过程文档
- 实验预览资产
- 本地浏览器登录配置
- `~/.wechat-article-suite/` 私密配置

## 运行依赖

公众号发布后端：

```bash
cd skills/duyi-wechat-fabu/scripts/wechat-posting-backend
bun install
```

排版渲染依赖：

```bash
cd skills/duyi-wechat-paipan/scripts/vendor
npm install
```

私密密钥和账号配置应放在包外：

```text
~/.wechat-article-suite/.env
~/.wechat-article-suite/wechat-fabu/EXTEND.md
```

## 安装边界

建议统一安装到：

```text
~/.agents/skills/<skill-name>
```

再按实际使用的运行客户端创建或刷新软链：

```text
~/.claude/skills/<skill-name> -> ../../.agents/skills/<skill-name>
~/.codex/skills/<skill-name>  -> ../../.agents/skills/<skill-name>
~/.hermes/skills/<skill-name> -> ../../.agents/skills/<skill-name>
```
