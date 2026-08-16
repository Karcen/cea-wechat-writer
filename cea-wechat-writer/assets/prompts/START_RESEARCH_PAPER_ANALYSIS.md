# 论文解读启动 Prompt

## 中文版

复制以下内容开始一个新任务：

```text
使用 $cea-wechat-writer 启动“两阶段论文解读”工作流。

现在只进行输入收集和阶段 1 需求对齐。不得开始完整论文解读，不得生成最终 Markdown。

请先一次性向我询问并等待我提供以下四个绝对路径：
1. Skill 目录
2. 论文 PDF 路径
3. 论文 Markdown 路径
4. 论文 figures 目录路径

询问论文 Markdown 时，请同时提示：如果尚未生成，请先在 https://markitdown.online/ 将 PDF 转换为 Markdown，下载到本地后提供 .md 文件的绝对路径；论文如未公开或存在版权、保密限制，上传第三方网站前应先确认授权。

同时询问结果保存位置。用户可以提供自定义绝对路径，也可以回复“默认”。默认保存目录必须与实际解析到的 SKILL.md 所在目录一致，默认生成“<论文PDF文件名去除扩展名>_论文解读.md”和“<论文PDF文件名去除扩展名>_编辑核查记录.md”。阶段 1 不得创建或覆盖结果文件。

收齐输入后，完整读取指定 SKILL.md 及其要求的资源，检查 PDF、Markdown、figures 和输出路径，然后只按 A 任务理解、B 预定结构、C 需要确认的事项、D 文件检查结果四部分汇报。完成后停止。

只有在我确认阶段 1 的必要选择并明确回复“开始阶段 2”“可以开始”或同等授权后，才能正式解读论文和保存结果。仅提供路径、回复“收到”或补充材料不算授权。

阶段 2 的读者正文必须按论文论证顺序自然展开，只选理解问题、方法、主要发现和证据边界所需的重点，通常使用 4—6 个二级标题，不逐节复述，也不为显得全面而拉长篇幅。正文不得显示“研究级解读”“已确认”“作者陈述”“证据直接支持”“分析者评价”“核验状态”或机器审核状态；使用自然主语说明判断归属。所有来源映射、判断主体、冲突、未决问题和编辑决定写入单独的编辑核查记录。

如果本 Prompt 与 Skill 冲突，优先执行本 Prompt 中明确的用户要求，同时列明冲突位置与处理方式，不得静默忽略。
```

收到上述 Prompt 后，Skill 应首先发出以下输入表，不添加论文分析内容：

```text
请按下面格式一次回复。前四项请粘贴绝对路径；保存位置可直接写“默认”。

1. Skill 目录：
2. 论文 PDF：
3. 论文 Markdown：
4. 论文 figures 目录：
5. 结果保存位置：默认

如果还没有论文 Markdown，请先使用 https://markitdown.online/ 将 PDF 转换为 .md 并下载到本地。论文如未公开或受版权、保密限制，请先确认是否允许上传第三方网站。
```

## English version

```text
Use $cea-wechat-writer to start the two-stage paper analysis workflow.

For now, collect inputs and perform Stage 1 alignment only. Do not begin the full paper analysis and do not create the final Markdown file.

First ask me for these four absolute paths in one message, then wait:
1. Skill directory
2. Paper PDF
3. Paper Markdown
4. Paper figures directory

When asking for the Markdown path, also explain that, if it does not yet exist, I should convert the PDF at https://markitdown.online/, download the .md file locally, and then provide its absolute path. Before uploading an unpublished, copyrighted, or confidential paper to a third-party website, I must confirm that I am authorised to do so.

Also ask where to save the results. I may provide a custom absolute path or reply "default". The default directory must be the directory containing the resolved SKILL.md. Create "<PDF stem>_论文解读.md" and "<PDF stem>_编辑核查记录.md" by default. Stage 1 must not create or overwrite either file.

After collecting the inputs, read the specified SKILL.md and every required resource, check the PDF, Markdown, figures, and output path, and report only: A task understanding, B proposed structure, C decisions requiring confirmation, and D file-check results. Then stop.

Begin Stage 2 only after I confirm all required Stage 1 choices and explicitly say "start Stage 2", "you may begin", or an equivalent authorisation. Providing paths, replying "received", or adding materials is not authorisation.

In Stage 2, make the reader-facing analysis flow naturally in the paper's argumentative order. Select only the material needed to understand the question, method, main findings, and evidence boundaries; normally use four to six level-two headings, do not reproduce every paper section, and do not inflate the length for apparent completeness. Do not display workflow labels such as “research-grade analysis,” “confirmed,” “author statement,” “directly supported by evidence,” “analyst assessment,” verification status, or machine-review states. Use natural subjects to attribute claims. Put source mapping, judgement ownership, conflicts, unresolved items, and editorial decisions in the separate editor-review record.

If this prompt conflicts with the Skill, follow the user's explicit requirements in this prompt, identify the conflict and explain how it was handled, and never ignore it silently.
```
