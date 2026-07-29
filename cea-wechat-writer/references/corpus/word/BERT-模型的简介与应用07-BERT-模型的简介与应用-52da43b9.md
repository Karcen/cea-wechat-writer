<!-- source: /Users/karcenzheng/Downloads/CEA_Skill/train_by_Shijie_Word/07.【学术前沿】BERT 模型的简介与应用/BERT.docx -->
<!-- category: 学术前沿 -->
<!-- historical-example-only: true -->

# 07.【学术前沿】BERT 模型的简介与应用

BERT 模型的简介与应用

一、引言

最近在Management Science上的一篇来自德克萨斯大学的Federico Siano撰写的独作论文“The news in earnings announcement disclosures: Capturing word context using LLM methods”受到了广泛关注。文章论证了BERT模型在捕捉财报文本中语境信息方面的优势。

文章提到的BERT 是当前被广泛使用的一类大型语言模型（Large Language Model， LLM）架构，属于基于 Transformer 的 LLM 家族。具体来说，在自然语言处理（Natural Language Processing, NLP）领域，理解和处理人类语言的复杂性一直是核心挑战。传统的语言模型往往依赖于手工设计的特征或单向的上下文信息，难以全面捕捉语言的语义和结构。为此，Google AI研究院的Devlin、Chang、Lee 和 Kristina Toutanova 等人提出了 BERT（Bidirectional Encoder Representations from Transformers）模型，该模型通过深度双向的语言表示，提升了计算机对语言的理解能力。在上述文章中，Siano 就是对 BERT 模型进行了微调，使其能根据企业盈利公告文本内容预测市场对公告发布后2日内股价的异常反应。这种做法不仅捕捉了词语本身的语义，也反映了词语在具体语境中的信息含量。

为了帮大家快速了解该模型，本期我们将跳过详细的原理及发展史，带大家简单了解该模型并给出简单的应用示例（情感分析+问答）。

二、BERT 模型概述

BERT 是一种基于 Transformer 架构的预训练语言模型，其核心特点在于：

双向编码：BERT 同时考虑词语左右两侧的上下文信息，从而更准确地理解词语的含义。

预训练与微调机制：BERT 首先在大规模无标注文本上进行预训练，然后通过微调适应特定的下游任务，如问答系统、情感分析等。

三、预训练阶段

BERT 的预训练阶段包括两个主要任务：

遮蔽语言模型（Masked Language Model, MLM）：在输入文本中随机遮蔽部分词语，模型需要根据上下文预测被遮蔽的词语。例如，给定句子“我喜欢吃[MASK]”，模型应预测出被遮蔽的词可能是“苹果”或“香蕉”。

下一句预测（Next Sentence Prediction, NSP）：模型学习判断两个句子之间是否存在连续关系。例如，句子 A：“我今天去了公园。”和句子 B：“我在那里遇到了一个老朋友。”，模型需要判断句子 B 是否是句子 A 的下一句。

通过这两个任务，BERT 能够学习到丰富的语言表示，捕捉词语之间的深层次关系。

四、微调阶段

在预训练完成后，BERT 可以通过微调适应各种具体的 NLP 任务。微调过程中，模型的参数会根据特定任务的数据进行调整，从而提升在该任务上的表现。例如，在情感分析任务中，BERT 可以根据标注的情感数据学习区分正面和负面情绪。

五、应用场景

BERT 在多个 NLP 任务中取得了显著成果，包括：

文本分类：将文本自动分类到不同的主题或类别中。

命名实体识别（Named Entity Recognition, NER）：识别文本中的特定实体，如人名、地名、组织机构等。

情感分析：判断用户评论或社交媒体帖子是正面、负面还是中性。

问答系统：如智能客服，BERT 能够根据用户的问题，从大量文本中找到最相关的答案。

例如，谷歌搜索引擎采用了 BERT 来更好地理解用户的查询意图，从而提供更准确的搜索结果。

六、代码示例

本案例旨在帮大家快速了解应用流程，代码中给出了从配置虚拟环境到保存结的全部流程，即使是刚刚安装完jubyter notebook后0编程基础也不用担心。案例整体比较简单，训练和分析涉及的材料也比较少，在实际应用中会涉及更大量的训练和分析。

在此案例中，我们通过BP、 Eni、 TotalEnergies三家公司2019-2024年的年报分析了：

公司财报情绪打分分析：使用的是现成的FinBERT情绪分类模型，它已经在SEC年报、Earnings Calls、金融新闻等真实金融文本上微调完成，

不需要再做围绕财报的专项训练。

公司对俄乌战争的反应以及经营上是否有所调整：涉及模型训练，我们收集了另外10家能源公司2022年年报，基于公司对俄乌战争的态度以及运营上的变化构建围绕这一案例的专项QA list并对谷歌的通用型BERT QA模型进行了围绕本案例的专项训练。

代码链接：https://pan.baidu.com/s/1qMXBQ3Gwya2sBCcjQiSqnQ?pwd=1234

部分结果可视化：

图1：公司年报净情绪

图2：俄乌战争对公司影的响相关内容长度热力图

图1可以看出TotalEnergies的财报情绪在2021年有小幅下降，而Eni则在2022年出现大幅下降。这一情况与图2结果相似。图2为公司在年报中涉及的“俄乌战争对公司运营的影响？”的内容长度热力图。

七、总结

BERT 通过引入双向编码和预训练机制，显著提升了计算机对自然语言的理解能力。其在多个 NLP 任务中的成功应用，展示了预训练语言模型在实际场景中的巨大潜力。对于非计算机专业的研究者，理解 BERT 的基本原理和应用方式，有助于在各自领域中有效利用这一先进的语言处理工具。

附录：参考文献及摘要：

Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019, June). Bert: Pre-training of deep bidirectional transformers for language understanding. In Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers) (pp. 4171-4186).

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models (Peters et al., 2018a; Radford et al., 2018), BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5 (7.7 point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

Siano, F. (2025). The news in earnings announcement disclosures: Capturing word context using LLM methods. Management Science.

This study examines the information content of textual disclosures in firms’ earnings announcements. Using a large language model (LLM) to capture information in both words and word context, I show that the news in earnings press releases (i) explains three times more variation in short-window stock returns than a host of textual measures based on dictionary and non-LLM machine learning methods; (ii) doubles the R2 of an array of financial statement surprises, modeled with conventional regression or machine learning approaches; and (iii) accounts for a large fraction of immediate price revisions within just five minutes of release. LLM-modeled conference calls further enhance R2 by one fourth compared with press releases and financial surprises. Textual disclosures are more informative when earnings are less persistent and during periods of aggregate uncertainty. Most news arises from text describing numbers, at the beginning of the disclosure, and including novel contents. These findings highlight the role of firms’ textual disclosures in moving stock prices and advance our understanding of how investors utilize corporate disclosures.

## 表格抽取


