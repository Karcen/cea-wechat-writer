<!-- source: /Users/karcenzheng/Downloads/CEA_Skill/train_by_category_html/学术前沿/07_【学术前沿】PSM匹配效果不太好？试试随机相似森林.html -->
<!-- category: 学术前沿 -->
<!-- historical-example-only: true -->

# 【学术前沿】PSM匹配效果不太好？试试随机相似森林

技术分享：基于人工智能随机相似森林（Random Similarity Forests）的匹配方法，在经济学和管理学领域的应用

Podcast (English)

![历史文章图片](https://mmbiz.qpic.cn/mmbiz_png/KwzjmZic8l4XVUztickKM9V4Rvia5jEgaicdwQffyvXCVhiayBsaK6APHg8LdEFvRMaOvMFKNDnP1HZkF0SZ3okxV1w/640?wx_fmt=png&from=appmsg)
作者信息：
Shijie Jin：英国卡迪夫大学商学院博士研究生，研究领域为绿色金融。

【研究问题】
各位经管领域的学术伙伴们，今天要为大家介绍一位人工智能领域和数据科学界的"超级红娘"——Random Similarity Forests（随机相似森林，简称RSF）。这个让因果推断更精准的利器，正在悄然革新我们的研究方法！
🔍传统PSM的"相亲困局"
做过政策评估或企业效果研究的同仁们，一定对倾向评分匹配（PSM）又爱又恨。这个经典方法就像"传统媒婆"，只按学历、收入等硬性指标牵线搭桥。但面对数字经济时代的高维、非线性数据（想想动辄上百个企业特征变量），PSM常常陷入"条件越多越难匹配"的窘境。
🌳RSF的智能匹配革命
波兰学者Piernik团队2022年提出的RSF算法，就像搭载了AI算法的"智能红娘系统"。它将随机森林的"集体智慧"与相似性森林的"多维相面术"完美融合：
1️⃣ 特征维度大爆炸：不仅能处理常规数值/离散数据，连时间序列、图数据等复杂类型都能轻松驾驭（非常适合处理企业面板数据！）
2️⃣ 相似性立体扫描：每个决策树节点都在构建"多维相似空间"，通过Gini系数等指标进行智能相似度评估（就像同时考察学历匹配度、消费习惯相似度、社交网络重合度）
3️⃣ 动态匹配引擎：通过构建随机投影矩阵，自动发现数据中隐藏的关联模式（堪比红娘识别"隐性般配"的直觉）
💡经管研究的三大应用场景
政策评估：精准匹配受政策影响/未受影响的企业样本

并购研究：为发生并购的企业找到"双胞胎"对照组

消费者实验：在复杂用户特征中锁定可比群体

🎯方法优势速览
✅ 高维数据不降维：直接处理上百个协变量
✅ 非线性关系捕捉：自动识别变量间的交互作用
✅ 混合数据通吃：问卷数据+企业财报+社交网络数据一站式处理🛠️操作指南TIP
当研究遇到以下情况时，建议尝试RSF：
协变量超过30个

存在大量分类变量

需要处理时空面板数据

传统PSM匹配失败率过高

文末彩蛋：我们团队已将RSF方法封装成Python工具包，方便大家学习和使用，关注公众号，不错过最新技术的介绍！

【干货部分】
RSF方法的核心思想
Piernik et al. (2022) 提出的RSF结合了随机森林（Random Forests）和相似性森林（Similarity Forests）的优点。在构建决策树时，每个分裂节点不仅仅使用传统的数值特征，还结合特征的距离度量进行投影。之后每个节点根据特定的相似性度量进行数据划分（如 Gini 指标），而不仅仅依赖数值特征的直接分割。RSF可用于分类任务，并能适应混合类型的数据(数值、离散、时间序列、图数据等)。

代码简介
为了将上述RSF方法用于匹配任务，作者在构建决策树后计算了随机森林叶子节点的相似性（即两个样本若在多数树的叶子节点相同，则它们的相似性较高），并结合欧几里得距离形成最终的匹配度量。本文将详细解析代码的每个步骤，帮助大家更好理解这个匹配方法的工作原理。

代码详解

1. 环境设置

设置代码环境前要先安装numpy, pandas matplotlib, scipy, scikit-learn, 和 openpyxl包：

pip install numpy pandas matplotlib scipy scikit-learn openpyxlimport numpy as npimport pandas as pdimport matplotlib.pyplot as pltfrom scipy import statsfrom sklearn.utils import resamplefrom sklearn.metrics import pairwise_distancesfrom sklearn.preprocessing import StandardScalerfrom sklearn.ensemble import RandomForestClassifier

2. 读取数据集并设置分类变量及需要匹配的变量

其中GreenBond变量为处理变量（GreenBond=1 为处理组，GreenBond=0 为对照组），需要基于"IssueYear", "IssueMonth", "Amount", "Yrs2Maturity", "Asset", "Liability", "CashFlow", "ROA", 以及 "DomesticIssuer" 变量进行匹配：

# 读取数据集(已处理过缺失值和极端值)df = pd.read_csv(r'F:\_PyCharm_\training.csv')
# 选择和目标变量和需要用于匹配的特征变量dummy='GreenBond'features = ["IssueYear","IssueMonth","Amount","Yrs2Maturity","Asset","Liability","CashFlow","ROA","DomesticIssuer"]

3. 当对照组观测值过多时对对照组执行抽样

如果GreenBond=0的样本数量远超GreenBond=1（大于 10 倍），则进行随机抽样，将倍数控制在 10 倍。这一过程为的是以减少计电脑算量。构建RSF的样本过多会对电脑内存有一定需求，可根据实际情况调高target_ratio:

# Âü∫‰∫é dummy variable=1 Âíå dummy variable=0 ÂàÜÁªÑy = df[dummy]df_classification_1 = df[y == 1].copy()df_classification_0 = df[y == 0].copy()
# 当dummy variable=0的观测值是dummy variable=1的观测值的很多倍时，对前者进行抽ʆ∑‰ª•ÊéßÂà∂Âú®10ÂÄçÔºå‰ªéËÄåÂáèÂ∞ëÂØπÁîµËÑëÂÜÖÂ≠òÁöÑË¶ÅÊ±Çtarget_ratio = 10current_ratio = len(df_classification_0) / len(df_classification_1)if current_ratio > target_ratio: n_samples_to_sample = len(df_classification_1) * target_ratio df_classification_0 = resample(df_classification_0, replace=False, n_samples=n_samples_to_sample, random_state=42)df = pd.concat([df_classification_1, df_classification_0]).reset_index(drop=True)y = df[dummy]X = df[features]df_classification_1 = df[y == 1].copy()df_classification_0 = df[y == 0].copy()

4. 构建RSF以用于计算样本之间的分类相似性距离：

# ÊûÑÂª∫ÈöèÊú∫Ê£ÆÊûóÊ®°Âûã‰ª•ÂÆûÁé∞ RSFrf = RandomForestClassifier(n_estimators=100, random_state=42)rf.fit(X, y)# ÊèêÂèñÂè∂ËäÇÁÇπË°®Á§∫ÔºåËÆ°ÁÆóÁõ∏‰ººÊÄßÁü©Èòµleaf_nodes = rf.apply(X)n_samples = X.shape[0]similarity_matrix = np.zeros((n_samples, n_samples))for tree_leaf in leaf_nodes.T: for i in range(n_samples): for j in range(i + 1, n_samples): if tree_leaf[i] == tree_leaf[j]: similarity_matrix[i, j] += 1 similarity_matrix[j, i] += 1# ÂΩí‰∏ÄÂåñÁõ∏‰ººÊÄßÂæóÂàÜsimilarity_matrix /= rf.n_estimators# ÊèêÂèñÁâπÂæÅÂπ∂Ê†áÂáÜÂåñscaler = StandardScaler()X_scaled = scaler.fit_transform(X)# ÂàõÂª∫ÂéüÂßãÁ¥¢ÂºïÂà∞Áü©ÈòµË°åÂè∑ÁöÑÊò†Â∞Ñindex_mapping = {idx: i for i, idx in enumerate(df.index)}# Â∞ÜÁ¥¢ÂºïÊò†Â∞ÑÂà∞ similarity_matrix ÁöÑË°åÂè∑mapped_indices_1 = [index_mapping[idx] for idx in df_classification_1.index]mapped_indices_0 = [index_mapping[idx] for idx in df_classification_0.index]

5. 基于RSF结果计算分类相似性距离，并基于欧几里得距离计算特征距离：

# 计算分类相似性距离：两个样本在随机森林模型中的行为相似性。如果两个样本在许多树中都落在相同的节点上，这表明它们在模型使用的决策规则下表现出类似的特征。similarity_distances = 1 - similarity_matrix[np.ix_(mapped_indices_1, mapped_indices_0)]# 计算特征距离：基于选择的特征变量计算的两个样本之间的欧几里得距离(类似于PSM)。这种距离测量的是在多维特征空间中，两个样本之间在量化特征上的直接距离。X_test_scaled = scaler.transform(df_classification_1[features])feature_distances = pairwise_distances(X_test_scaled, X_scaled[y == 0], metric='euclidean')

6. 将上述两个距离按1:1赋予权重，计算出综合距离以用于最终匹配：

# 计算综合距离alpha =�0.5� # 分类相似性距离的权重beta = (1-alpha) � # 设置特征相似距离的权重combined_distances = alpha*similarity_distances + beta*feature_distances
# 找到最近邻索引并提取匹配的 dummy variable=0�的数据nearest_indices = np.argmin(combined_distances, axis=1)nearest_indices = nearest_indices[nearest_indices <�len(df_classification_0)] �# 确保索引有效matched_0 = df_classification_0.iloc[nearest_indices].copy()

7. 检验匹配结果并将匹配后的数据保存在csv文件中：

# TÊ£ÄÈ™åÂíåÂèØËßÜÂåñÂåπÈÖçÁªìÊûúfeatures_for_ttest = featurest_test_results = []for feature in features_for_ttest: group_1_before = df_classification_1[feature] group_0_before = df_classification_0[feature] group_0_after = matched_0[feature] if group_0_after.empty or group_1_before.empty: print(f"Feature {feature}: Matched data is empty. Skipping t-test.") continue # ËÆ°ÁÆóÂåπÈÖçÂâçÂêéÁöÑtÊ£ÄÈ™å t_stat_before, p_value_before = stats.ttest_ind(group_1_before, group_0_before, equal_var=False) t_stat_after, p_value_after = stats.ttest_ind(group_1_before, group_0_after, equal_var=False) # ËÆ∞ÂΩïÁªìÊûú t_test_results.append({ 'Feature': feature, 'T-Stat Before Matching': t_stat_before, 'P-Value Before Matching': p_value_before, 'T-Stat After Matching': t_stat_after, 'P-Value After Matching': p_value_after}) # ÂèØËßÜÂåñÂåπÈÖçÂâçÂêéÁöÑÂàÜÂ∏ÉÔºàÁÆ±ÂûãÂõæÔºâ plt.figure(figsize=(10, 6)) plt.boxplot([group_0_before, group_0_after, group_1_before], labels=['Green=0 (pre-matching)', 'Green=0 (post-matching)', 'Green=1']) plt.axvline(x=1.5, color='gray', linestyle='--', linewidth=1) title_font = {'fontsize': 16, 'fontname': 'Times New Roman'} label_font = {'fontsize': 14, 'fontname': 'Times New Roman'} plt.xticks(fontsize=12, fontname='Times New Roman') plt.yticks(fontsize=12, fontname='Times New Roman') plt.title(f'Distribution Comparison for {feature}', fontdict=title_font) plt.ylabel(feature, fontdict=label_font) plt.savefig(f'result_matching_T_test_{feature}_boxplot_comparison.png') # ‰øùÂ≠òÂõæË°® plt.close()# ËæìÂá∫tÊ£ÄÈ™åÁªìÊûú‰∏∫Ë°®Ê†ºÂΩ¢Âºèt_test_df = pd.DataFrame(t_test_results)t_test_df = t_test_df.round(5)print(t_test_df)with pd.ExcelWriter('result_matching_T_test.xlsx') as writer: t_test_df.to_excel(writer, index=False, sheet_name='T-Test Results')
# 输出匹配后的数据集到CSV文件matched_data = pd.concat([df_classification_1, matched_0], axis=0)matched_data.to_csv('result__matched_data.csv', index=False)print("T-test results have been saved to 'result_T_test.xlsx'.")print("Matched data has been saved to 'result__matched_data.csv'.")

总结：与常用的PSM相比，这一基于RSF的匹配方法在需要匹配的体征变量较多时存在优势，但是当样本量过大时需要较长事件完成匹配。此外，在实际应用过程中，如果某一特征变量十分重要（e.g., X），可生两个与其完全一样的变量一同带入匹配过程（e.g., X_copy1, X_copy2），从而实现增加其权重的效果。

代码及数据文件

![历史文章图片](https://mmbiz.qpic.cn/mmbiz_png/KwzjmZic8l4XVUztickKM9V4Rvia5jEgaicdzHcPYKlicVW5icjicC90aRGfqNvnksnUOicaGrxOibcOMvGVYicnTdsq36Qg/640?wx_fmt=png&from=appmsg)

点击此处获取代码及数据文件
附录：参考文献

Piernik, M., Brzezinski, D., & Zawadzki, P. (2022). Random similarity forests. In Joint European Conference on Machine Learning and Knowledge Discovery in Databases (pp. 53-69). Cham: Springer Nature Switzerland.
