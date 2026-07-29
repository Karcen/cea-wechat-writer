#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: render_style_set.sh input.md output_dir [STYLE ...]" >&2
  echo "example: render_style_set.sh article.md 公众号CSS输出 白瓷 蓝图 青笺" >&2
  exit 2
fi

input="$1"
output_dir="$2"
shift 2

if [[ ! -f "$input" ]]; then
  echo "input file not found: $input" >&2
  exit 2
fi

mkdir -p "$output_dir"

if [[ $# -eq 0 ]]; then
  styles=(白瓷 蓝图 紫线 墨线 陶土 宣纸 朱批 杏纸 素纸 萤石 霓虹 橙陶 朱砂 金箔 竹简 青笺)
else
  styles=("$@")
fi

renderer="${DUYI_WECHAT_RENDERER:-$HOME/.agents/skills/duyi-wechat-paipan/scripts/render_wechat_html.py}"
base="$(basename "$input")"
base="${base%.*}"

index="$output_dir/00_公众号CSS风格总览.html"
catalog="$output_dir/风格目录.md"

{
  echo "# 公众号 CSS 风格目录"
  echo
  echo "输入文件：$input"
  echo
  echo "| 风格 | 预览 HTML | 微信 HTML |"
  echo "|---|---|---|"
} > "$catalog"

{
  cat <<'HTML'
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>公众号 CSS 风格总览</title>
<style>
body{margin:0;background:#f4f4f5;color:#18181b;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","PingFang SC",sans-serif;}
main{max-width:920px;margin:0 auto;padding:32px 20px 56px;}
h1{margin:0 0 8px;font-size:28px;line-height:1.2;}
p{margin:0 0 22px;color:#52525b;font-size:15px;line-height:1.7;}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;}
.card{display:block;padding:18px 18px 16px;background:#fff;border:1px solid #e4e4e7;border-radius:10px;text-decoration:none;color:#18181b;}
.card strong{display:block;margin-bottom:6px;font-size:16px;}
.card span{display:block;color:#71717a;font-size:13px;line-height:1.6;}
</style>
</head>
<body>
<main>
<h1>公众号 CSS 风格总览</h1>
<p>点开预览 HTML 对比手机端效果；每个 WeChat HTML 都已通过默认 HTML QA gate，选定后进入后续发布流程。</p>
<section class="grid">
HTML
} > "$index"

for style in "${styles[@]}"; do
  preview="$output_dir/${base}-${style}-preview.html"
  wechat="$output_dir/${base}-${style}-wechat.html"
  python3 "$renderer" "$input" --style "$style" --standalone --output "$preview"
  python3 "$renderer" "$input" --style "$style" --output "$wechat"
  preview_name="$(basename "$preview")"
  wechat_name="$(basename "$wechat")"
  {
    echo "| $style | [$preview_name]($preview_name) | [$wechat_name]($wechat_name) |"
  } >> "$catalog"
  {
    echo "<a class=\"card\" href=\"$preview_name\"><strong>$style</strong><span>预览：$preview_name<br>微信片段：$wechat_name</span></a>"
  } >> "$index"
done

{
  cat <<'HTML'
</section>
</main>
</body>
</html>
HTML
} >> "$index"

echo "$index"
