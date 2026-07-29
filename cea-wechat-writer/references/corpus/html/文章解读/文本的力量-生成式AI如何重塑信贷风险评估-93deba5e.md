<!-- source: /Users/karcenzheng/Downloads/CEA_Skill/train_by_category_html/文章解读/17_【文章解读】文本的力量：生成式AI如何重塑信贷风险评估？.html -->
<!-- category: 文章解读 -->
<!-- historical-example-only: true -->

# 【文章解读】文本的力量：生成式AI如何重塑信贷风险评估？

文章题目：挖掘文本在信用违约预测中的潜能：人工撰写与生成式人工智能优化文本的比较研究（Unleashing the power of text for credit default prediction: Comparing human-written and generative AI-refined texts）
发表期刊：European Journal of Operational Research
联合国可持续发展目标：SDG9 产业创新和基础设施
Podcast (English)

![历史文章图片](https://mmbiz.qpic.cn/mmbiz_png/KwzjmZic8l4Uu7Wu95smOZ2JcIo8xuuknC4GRria58lVpnqV7HhNkQScC62PoJgJfnXcnHKqbUQt6LwlAJz3LBzw/640?wx_fmt=png&from=appmsg)

作者信息：
Zongxiao Wu：爱丁堡大学商学院博士，研究方向为自然语言处理/大模型/多模态学习在金融风险管理中的应用。
Yizhe Dong：爱丁堡大学商学院教授、博士生导师，主要研究领域包括公司金融、银行经营与风险管理、人工智能在风险预测与金融投资中的应用等。
Yaoyiran Li：剑桥大学语言技术实验室博士，研究方向为自然语言处理、大模型推理、机器翻译、推荐系统等。
Baofeng Shi：西北农林科技大学经济管理学院院长、教授、博士生导师，主要研究领域包括金融风险管理、金融工程、普惠金融、涉农信用风险管理等。
【研究问题】
在当下信息技术浪潮席卷全球的背景下，生成式人工智能（Generative AI）正快速渗透各行各业。而在金融行业，尤其是银行信贷决策环节，其广泛的应用潜力仍待深入挖掘。
这篇最新发表于 European Journal of Operational Research 的研究，聚焦于一个具体且关键的问题：在贷款审批中，如何有效利用生成式AI处理信贷员撰写的文本，以更精准地预测借款人是否可能违约？
【研究背景】
从结构化信用评分到“文本赋能”

传统的信用评分模型主要基于结构化数据，如借款人的年龄、资产、收入和还款历史。
然而，在面向小微企业（micro and small enterprises, mSEs）时，结构化数据往往不全、不准甚至缺失，极大限制了模型的预测效能。
在这种背景下，贷款文本——即由信贷员实地走访企业后撰写的贷款评估——成为一种重要的“替代性数据”。
这些文本通常包含借款人经营状况、资产负债、还款意愿、个性特征等非量化的信息，具有重要的潜在价值。
然而，人类撰写的文本具有显著的个体差异，包括语言风格、篇幅长短、逻辑结构等方面的不一致性。
这不仅增加了自然语言处理（NLP）模型建模的难度，也限制了文本信息在风控中的应用效率。
因此，本文提出使用ChatGPT对原始文本进行“提炼”和“结构化分析”，以探索这种生成式AI文本在信贷预测中的可行性与优势。
【数据构建】

用ChatGPT重塑文本，再送入模型“测验”

本研究使用了来自中国一家商业银行的真实mSE贷款数据。每条贷款样本均包含：
借款人的31个结构化变量（如行业、营业额、资产情况等）；

一段由信贷员撰写的贷款文本评估；

借款结果标签（违约或未违约）。

在此基础上，本文构造了两种文本形式：原始人工撰写文本和通过ChatGPT提炼后的AI文本。
ChatGPT提炼流程采用明确的提示模板，要求其从原文中提炼出两部分内容：一是支持借款人还款能力的因素，二是可能导致借款人违约的风险因素。这种结构化的内容生成，为后续模型建模提供了统一的文本表达基础。
为了验证不同文本的预测效果，本文构建了基于四种主流NLP技术的模型，包括LDA（topic model）、fastText（word-embedding model）、Ada-002（OpenAI sentence-embedding model）与BERT（pre-trained language model），并结合多层感知器（MLP）作为分类器进行违约预测。
每种模型均在以下三类输入下进行训练与评估：仅结构化数据，仅文本数据，结构化与文本联合输入。
【主要结论】
关键发现一：ChatGPT文本显著提升预测性能
结果显示，相较于传统模型仅依赖结构化数据的做法，加入文本数据可以显著提升模型的预测表现，而ChatGPT提炼后的文本效果明显优于原始人工文本。
以最先进的BERT模型为例，当结构化数据与原始人工文本结合时，模型AUC为0.667；而结合ChatGPT提炼文本后，AUC上升至0.710。
KS、H-measure等指标也均有显著提升，表明模型在区分违约与非违约样本上的能力更强。
这一发现揭示了生成式AI文本不仅保留了原始信息，还进一步清晰化了风险信号，具有实际的预测增益价值。
同时，值得注意的是在部分情形下，PRAUC值（衡量模型在识别极少数违约者中的精确度）在使用AI文本时略有下降，提示生成式AI重塑文本时可能削弱了一些高风险借款人在表达层面的“微弱异质性”。
关键发现二：ChatGPT能“强化”风险信息，并提供更具一致性的文本表达
从语言层面分析，ChatGPT生成的文本在篇幅、语义相似度、词汇分布等维度上，与人工文本存在系统性差异。
ChatGPT更倾向于生成较长、逻辑更清晰的评估文本，尤其在风险信息的提取方面表现更为突出。
通过用LIME模型解释两类文本的预测结果，本文发现，在人工文本中，像“客户”、“诚实”、“业务良好”等正面词汇与低违约概率相关。
而在ChatGPT文本中，模型更关注风险因素的表述，如“逾期”、“信用评级降低”、“回款压力”等，这些信息被清晰地结构化呈现了出来，增强了风险识别的精准性。
此外，模型对于相同词语的判断也体现出语境依赖性：如“偿还”出现在人工文本中会降低违约概率，但在ChatGPT文本中却可能提升风险预测。这反映了上下文结构对模型感知的影响，也提示并非词本身携带风险，而是其在语境中的逻辑位置。
关键发现三：分离风险因子，ChatGPT文本中“负面信息”最具预测价值
一个颇具启发性的设计是：本文将ChatGPT生成的“支持还款”和“潜在违约”两个部分信息分开输入模型，分别评估其预测能力。
结果显示，仅使用负面因素的信息，其预测效果优于仅使用正面信息的模型，甚至超过了原始人工文本的效果。
值得注意的是，当本文将“负面+正面”组合使用时，预测表现最为优异。这表明，ChatGPT的逻辑结构化表达方式，能够清晰地将风险信号提取并呈现，有效帮助模型识别“违约倾向性”。
【商业价值】
AI文本能带来更高的利润回报
最后，本文还进一步评估了在实际放贷决策中不同模型可能带来的利润表现。结果显示，基于ChatGPT文本的模型，除了某些极端情况，在大多数拒贷阈值下均表现出更高的净利润。
这说明，生成式AI在辅助信贷风控决策中的潜力，不仅仅体现在技术性能上，更在于其直接创造的商业价值。
【文章贡献】
综合来看，本文的研究具有三方面的关键贡献：
理论创新：首次系统性地评估了生成式AI在信贷风险评估中的表现，并揭示语言表达方式与违约信号之间的深层互动机制，拓展了文本信息在信用建模中的理论边界。

方法贡献：构建了“原始文本—AI精炼—建模预测”的全流程分析框架，适用于银行信贷以外的其他金融预测任务，并可复制推广至金融欺诈、财务审计、财报分析等领域。

实践价值：验证了将ChatGPT等LLM作为前置文本处理工具的可行性，为商业银行提升中小企业客户风险识别能力、提高资产质量、优化贷款决策流程提供了现实可行的解决方案。

本研究亦提醒监管者与从业者注意：生成式AI尽管在处理与表达层面具备显著能力，但其在风险预测中的应用仍需严格的伦理审查、偏差控制与可解释性设计，避免“黑箱模型”在高风险领域带来的潜在误导。
未来的研究可以进一步拓展至以下方向：一是探索不同类型大模型（如Claude、Gemini等）在金融任务中的表现差异；二是将结构化prompt工程作为控制变量，研究提示设计对模型输出稳定性的影响；三是从人机协同的角度，构建“AI辅助+人工校验”的贷款审批流程，推动生成式AI在人类决策链中的合理嵌入与赋能。
附录：文章摘要
Wu, Z., Dong, Y., Li, Y., & Shi, B. (2025). Unleashing the power of text for credit default prediction: Comparing human-written and generative AI-refined texts. European Journal of Operational Research. DOI: 10.1016/j.ejor.2025.04.032.
This study explores the integration of a representative large language model, ChatGPT, into lending decision-making with a focus on credit default prediction. Specifically, we use ChatGPT to analyse and interpret loan assessments written by loan officers and generate refined versions of these texts. Our comparative analysis reveals significant differences between generative artificial intelligence (AI)-refined and human-written texts in terms of text length, semantic similarity, and linguistic representations. Using deep learning techniques, we show that incorporating unstructured text data, particularly ChatGPT-refined texts, alongside conventional structured data significantly enhances credit default predictions. Furthermore, we demonstrate how the contents of both human-written and ChatGPT-refined assessments contribute to the models‚Äô prediction and show that the effect of essential words is highly context-dependent. Moreover, we find that ChatGPT‚Äôs analysis of borrower delinquency contributes the most to improving predictive accuracy. We also evaluate the business impact of the models based on human-written and ChatGPT-refined texts, and find that, in most cases, the latter yields higher profitability than the former. This study provides valuable insights into the transformative potential of generative AI in financial services.
