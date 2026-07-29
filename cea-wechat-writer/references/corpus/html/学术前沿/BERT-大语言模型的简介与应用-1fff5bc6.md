<!-- source: /Users/karcenzheng/Downloads/CEA_Skill/train_by_category_html/学术前沿/01_【学术前沿】BERT 大语言模型的简介与应用.html -->
<!-- category: 学术前沿 -->
<!-- historical-example-only: true -->

# 【学术前沿】BERT 大语言模型的简介与应用

往期精彩文章：
【文章解读】生成式AI重塑信贷风险评估�|�针对华人经济学家的引用歧视�|�中国两千年经济不平等史�|�明清晋商公司治理�|�绿债贴标选择与影响�|�AI在商业与金融领域的应用
„ÄêÂ≠¶ÊúØÂâçÊ≤ø„ÄëCS DID | Stack/Synthetic DID | Á≥ªÁªüÊÄßÊñáÁåÆÁªºËø∞ | ÈöèÊú∫Áõ∏‰ººÊ£ÆÊûó

技术分享：从0开始的BERT模型入门

![历史文章图片](https://mmbiz.qpic.cn/mmbiz_png/KwzjmZic8l4WAJg7JIyEaH1fws9D5IT38Z0h5XcqxP6jw6hKib17jlInpGH5oGLpsXibXBH6fB9gBiaqoJxRq9lCOw/640?wx_fmt=png&from=appmsg)

作者信息：
Shijie Jin：英国卡迪夫大学商学院博士研究生，研究领域为绿色金融。

【引言】
最近在Management Science上的一篇来自德克萨斯大学的Federico Siano撰写的独作论文“The news in earnings announcement disclosures: Capturing word context using LLM methods”受到了广泛关注。文章论证了BERT�(Bidirectional Encoder Representations from Transformers)�模型在捕捉财报文本中语境信息方面的优势。
文章提到的BERT 是当前被广泛使用的一类大型语言模型（Large Language Model， LLM）架构，属于基于 Transformer 的 LLM 家族。具体来说，在自然语言处理（Natural Language Processing, NLP）领域，理解和处理人类语言的复杂性一直是核心挑战。传统的语言模型往往依赖于手工设计的特征或单向的上下文信息，难以全面捕捉语言的语义和结构。为此，Google 模型，该模型通过深度双向的语言表示，提升了计算机对语言的理解能力。在上述文章中，Siano 就是对 BERT 模型进行了微调，使其能根据企业盈利公告文本内容预测市场对公告发布后2日内股价的异常反应。这种做法不仅捕捉了词语本身的语义，也反映了词语在具体语境中的信息含量。
为了帮大家快速了解该模型，本期我们将跳过详细的原理及发展史，带大家简单了解该模型并给出简单的应用示例（情感分析+问答）。
彩蛋：我们团队已将BERT案例代码封装成Python工具包，方便大家学习和使用，关注公众号，不错过最新技术的介绍！
【模型概述】
BERT 是一种基于Transformer架构的预训练语言模型，其核心特点在于：
双向编码：BERT 同时考虑词语左右两侧的上下文信息，从而更准确地理解词语的含义。

预训练与微调机制：BERT 首先在大规模无标注文本上进行预训练，然后通过微调适应特定的下游任务，如问答系统、情感分析等。

预训练阶段
BERT 的预训练阶段包括两个主要任务：
遮蔽语言模型（Masked Language Model, MLM）：在输入文本中随机遮蔽部分词语，模型需要根据上下文预测被遮蔽的词语。例如，给定句子“我喜欢吃[MASK]”，模型应预测出被遮蔽的词可能是“苹果”或“香蕉”。

下一句预测（Next Sentence Prediction, NSP）：模型学习判断两个句子之间是否存在连续关系。例如，句子 A：“我今天去了公园。”和句子 B：“我在那里遇到了一个老朋友。”，模型需要判断句子 B 是否是句子 A 的下一句。

通过这两个任务，BERT 能够学习到丰富的语言表示，捕捉词语之间的深层次关系。
微调阶段
在预训练完成后，BERT 可以通过微调适应各种具体的 NLP 任务。微调过程中，模型的参数会根据特定任务的数据进行调整，从而提升在该任务上的表现。例如，在情感分析任务中，BERT 可以根据标注的情感数据学习区分正面和负面情绪。
应用场景
BERT 在多个 NLP 任务中取得了显著成果，包括：
文本分类：将文本自动分类到不同的主题或类别中。

命名实体识别（Named Entity Recognition, NER）：识别文本中的特定实体，如人名、地名、组织机构等。

情感分析：判断用户评论或社交媒体帖子是正面、负面还是中性。

问答系统：如智能客服，BERT 能够根据用户的问题，从大量文本中找到最相关的答案。

例如，谷歌搜索引擎采用了 BERT 来更好地理解用户的查询意图，从而提供更准确的搜索结果。

【案例简介】
本案例旨在帮大家快速了解应用流程，代码中给出了从配置虚拟环境到保存结的全部流程，即使是刚刚安装完jubyter notebook后0编程基础也不用担心。案例整体比较简单，训练和分析涉及的材料也比较少，在实际应用中会涉及更大量的训练和分析。
在此案例中，我们通过BP、 Eni、 TotalEnergies三家公司2019-2024年的年报分析了：
公司财报情绪变化：使用的是deepset团队训练好的的模型，该模型泛化能力强，能在泛商业/政策类语句中回答合理问题，故再做围绕财报的专项训练。

围绕俄乌战争对公司影响的问答：涉及模型训练，我们收集了另外10家能源公司2022年年报，基于公司对俄乌战争的态度以及运营上的变化构建围绕这一案例的专项QA list并对上述模型进行了围绕本案例的专项训练。

【部分结果可视化】

图1：公司年报净情绪

![历史文章图片](https://mmbiz.qpic.cn/mmbiz_png/KwzjmZic8l4WAJg7JIyEaH1fws9D5IT38bxsMwf81RYC5eJqZ5sNdu3LN8S4j5iaOBDNGbqru4pmPuop0WGPopcQ/640?wx_fmt=png&from=appmsg)

图2：俄乌战争对公司影的响相关内容长度热力图

![历史文章图片](https://mmbiz.qpic.cn/mmbiz_png/KwzjmZic8l4WAJg7JIyEaH1fws9D5IT38H4L9qz6usDInCCSzZS86pyDY8lZQ16ZsnrsgyrWscia8x2Cic1Spvu4w/640?wx_fmt=png&from=appmsg)

从图1可以看出TotalEnergies的财报情绪在2021年有小幅下降，而Eni则在2022年出现大幅下降。这一情况与图2结果相似，Eni在2022年用了较长篇幅提价俄乌战争对公司运营的影响。

代码及数据文件

![历史文章图片](https://mmbiz.qpic.cn/mmbiz_jpg/KwzjmZic8l4WAJg7JIyEaH1fws9D5IT38VklM1hQBZlffHA4FGibVyFfJZaonPVkgl4QsGJbn9kr19ftFdSsxEsg/640?wx_fmt=jpeg&from=appmsg)

附录：参考文献

Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019, June). Bert: Pre-training of deep bidirectional transformers for language understanding. In Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers) (pp. 4171-4186).

Siano, F. (2025). The news in earnings announcement disclosures: Capturing word context using LLM methods. Management Science.
