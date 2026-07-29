# DUYI WeChat Skill Suite

DUYI WeChat Skill Suite 是一套公众号生产 Skill 套件。

它面向已经写好的公众号文章，帮助使用者把稿件继续推进到可发布状态：配图、选择 CSS 风格、生成 WeChat-ready HTML、做截图质检、执行 API dry-run，并在确认链路通过后创建微信公众号草稿箱。

维护者：DUYI

## 快速开始

### 1. 获取套件

如果你下载的是 Release 压缩包：

```bash
mkdir -p duyi-wechat-skill-suite
unzip duyi-wechat-local-skill-suite-20260630.zip -d duyi-wechat-skill-suite
cd duyi-wechat-skill-suite
```

如果你使用 GitHub 仓库：

```bash
git clone https://github.com/duyi2076/duyi-wechat-skill-suite.git
cd duyi-wechat-skill-suite
```

### 2. 安装 Skills

```bash
mkdir -p "$HOME/.agents/skills"

for skill in duyi-wechat duyi-wechat-css-layer duyi-wechat-paipan duyi-wechat-peitu duyi-wechat-fabu; do
  mkdir -p "$HOME/.agents/skills/$skill"
  rsync -a "skills/$skill/" "$HOME/.agents/skills/$skill/"
done
```

### 3. 连接到你的 Agent 运行环境

只需要创建你实际使用的运行环境软链。下面一次性给出 Claude、Codex、Hermes 三种入口：

```bash
mkdir -p "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.hermes/skills"

for skill in duyi-wechat duyi-wechat-css-layer duyi-wechat-paipan duyi-wechat-peitu duyi-wechat-fabu; do
  ln -sfn "../../.agents/skills/$skill" "$HOME/.claude/skills/$skill"
  ln -sfn "../../.agents/skills/$skill" "$HOME/.codex/skills/$skill"
  ln -sfn "../../.agents/skills/$skill" "$HOME/.hermes/skills/$skill"
done
```

### 4. 安装运行依赖

公众号发布后端：

```bash
cd "$HOME/.agents/skills/duyi-wechat-fabu/scripts/wechat-posting-backend"
bun install
```

排版渲染依赖：

```bash
cd "$HOME/.agents/skills/duyi-wechat-paipan/scripts/vendor"
npm install
```

### 5. 配置微信公众号密钥

只有在创建微信公众号草稿箱时才需要配置密钥。密钥不要放进仓库。

```bash
mkdir -p "$HOME/.wechat-article-suite"

cat > "$HOME/.wechat-article-suite/.env" <<'EOF'
WECHAT_APP_ID=replace_with_your_app_id
WECHAT_APP_SECRET=replace_with_your_app_secret
EOF
```

可选的账号偏好配置放在：

```text
~/.wechat-article-suite/wechat-fabu/EXTEND.md
```

### 6. 在 Agent 里调用

把写好的文章交给 Agent，然后说：

```text
使用 duyi-wechat 处理这篇公众号稿，完成排版、配图、HTML QA，并创建微信公众号草稿箱。
```

如果只想生成中间产物，需要明确说明：

```text
只排版看看，不进草稿箱。
```

## 包含的 Skills

```text
skills/
  duyi-wechat/
  duyi-wechat-css-layer/
  duyi-wechat-paipan/
  duyi-wechat-peitu/
  duyi-wechat-fabu/
```

## 交付边界

- 默认交付目标是微信公众号草稿箱。
- 不保存、不随包分发任何公众号密钥。
- 不包含 `node_modules`。
- 不包含本地浏览器登录配置。
- 除非使用者明确要求改稿，否则不改正文句子、用词、语气和论证顺序。
- 正式群发发布不在本套件内自动执行。

## 每个 Skill 负责什么

| Skill | 作用 |
|---|---|
| `duyi-wechat` | 公众号生产总控 |
| `duyi-wechat-css-layer` | CSS 风格选择和主题体系 |
| `duyi-wechat-paipan` | Markdown / WeChat-ready HTML 排版 |
| `duyi-wechat-peitu` | 封面图和正文配图 |
| `duyi-wechat-fabu` | 草稿箱创建和手机预览流程 |

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

## 私密配置位置

```text
~/.wechat-article-suite/.env
~/.wechat-article-suite/wechat-fabu/EXTEND.md
```

不要把这些文件提交到 GitHub。
