<!-- source: /Users/karcenzheng/Downloads/CEA_Skill/train_by_Shijie_Word/03.【学术前沿】PSM匹配效果不太好？试试随机相似森林(Random Similarity Forests)/基于Random Similarity Forests和Python的匹配方法.docx -->
<!-- category: 学术前沿 -->
<!-- historical-example-only: true -->

# 03.【学术前沿】PSM匹配效果不太好？试试随机相似森林(Random Similarity Forests)

原创：

技术分享：基于Random Similarity Forests和Python的匹配方法

Podcast (English)

RSF for Matching,CEA Europe UK,10分钟

作者信息：

Peng Zhou：卡迪夫大学商学院教授，博士生导师。研究领域为经济增长、经济不平等、创新经济学、金融经济学等。参与多项英国政府科研项目。

Shijie Jin：卡迪夫大学商学院博士研究生，研究领域为绿色金融。

研究问题

在数据分析中，匹配出合适的对照组十分重要。目的是在控制组和处理组之间找到高度相似的个体，以减少潜在混杂因素的影响，确保因果效应估计的准确性。传统的倾向评分匹配(Propensity Score Matching) 是一种经典且广泛应用的匹配方法，但在处理高维、非线性数据时常常表现不佳。为了解决这个问题，本文在Piernik et al. (2022) 推出的Random Similarity Forests(RSF)的基础上构建了这一匹配方法，使其更适用于观测值的匹配任务。

RSF方法的核心思想

Piernik et al. (2022) 提出的RSF结合了随机森林(Random Forests) 和相似性森林(Similarity Forests) 的优点。在构建决策树时，每个分裂节点不仅仅使用传统的数值特征，还结合特征的距离度量进行投影。之后每个节点根据特定的相似性度量进行数据划分(如 Gini 指标)，而不仅仅依赖数值特征的直接分割。RSF可用于分类任务，并能适应混合类型的数据(数值、离散、时间序列、图数据等)。

代码简介

为了将上述RSF方法用于匹配任务，作者在构建决策树后计算了随机森林叶子节点的相似性(即两个样本若在多数树的叶子节点相同，则它们的相似性较高)，并结合欧几里得距离形成最终的匹配度量。本文将详细解析代码的每个步骤，帮助大家更好理解这个匹配方法的工作原理。

代码详解

1. 环境设置

设置代码环境前要先安装numpy, pandas matplotlib, scipy, scikit-learn, 和 openpyxl包：

pip install numpy pandas matplotlib scipy scikit-learn openpyxlimport numpy as npimport pandas as pdimport matplotlib.pyplot as pltfrom scipy import statsfrom sklearn.utils import resamplefrom sklearn.metrics import pairwise_distancesfrom sklearn.preprocessing import StandardScalerfrom sklearn.ensemble import RandomForestClassifier

2. 读取数据集并设置分类变量及需要匹配的变量

其中GreenBond变量为处理变量 (GreenBond=1 为处理组，GreenBond=0 为对照组)，需要基于"IssueYear", "IssueMonth", "Amount", "Yrs2Maturity", "Asset", "Liability", "CashFlow", "ROA", 以及 "DomesticIssuer" 变量进行匹配：

# 读取数据集(已处理过缺失值和极端值)df = pd.read_csv(r'F:\_PyCharm_\training.csv')
# 选择和目标变量和需要用于匹配的特征变量dummy='GreenBond'features = ["IssueYear","IssueMonth","Amount","Yrs2Maturity","Asset","Liability","CashFlow","ROA","DomesticIssuer"]

3. 当对照组观测值过多时对对照组执行抽样

如果GreenBond=0的样本数量远超GreenBond=1(大于 10 倍)，则进行随机抽样，将倍数控制在 10 倍。这一过程为的是以减少计电脑算量。构建RSF的样本过多会对电脑内存有一定需求，可根据实际情况调高target_ratio:

# 基于 dummy variable=1 和 dummy variable=0 分组y = df[dummy]df_classification_1 = df[y == 1].copy()df_classification_0 = df[y == 0].copy()
# 当dummy variable=0的观测值是dummy variable=1的观测值的很多倍时，对前者进行抽样以控制在3倍，从而减少对电脑内存的要求target_ratio = 10current_ratio = len(df_classification_0) / len(df_classification_1)if current_ratio > target_ratio:    n_samples_to_sample = len(df_classification_1) * target_ratio    df_classification_0 = resample(df_classification_0, replace=False, n_samples=n_samples_to_sample, random_state=42)df = pd.concat([df_classification_1, df_classification_0]).reset_index(drop=True)y = df[dummy]X = df[features]df_classification_1 = df[y == 1].copy()df_classification_0 = df[y == 0].copy()

4. 构建RSF以用于计算样本之间的分类相似性距离：

# 构建随机森林模型以实现 RSFrf = RandomForestClassifier(n_estimators=100, random_state=42)rf.fit(X, y)# 提取叶节点表示，计算相似性矩阵leaf_nodes = rf.apply(X)n_samples = X.shape[0]similarity_matrix = np.zeros((n_samples, n_samples))for tree_leaf in leaf_nodes.T:    for i in range(n_samples):        for j in range(i + 1, n_samples):            if tree_leaf[i] == tree_leaf[j]:                similarity_matrix[i, j] += 1                similarity_matrix[j, i] += 1# 归一化相似性得分similarity_matrix /= rf.n_estimators# 提取特征并标准化scaler = StandardScaler()X_scaled = scaler.fit_transform(X)# 创建原始索引到矩阵行号的映射index_mapping = {idx: i for i, idx in enumerate(df.index)}# 将索引映射到 similarity_matrix 的行号mapped_indices_1 = [index_mapping[idx] for idx in df_classification_1.index]mapped_indices_0 = [index_mapping[idx] for idx in df_classification_0.index]

5. 基于RSF结果计算分类相似性距离，并基于欧几里得距离计算特征距离：

# 计算分类相似性距离：两个样本在随机森林模型中的行为相似性。如果两个样本在许多树中都落在相同的节点上，这表明它们在模型使用的决策规则下表现出类似的特征。similarity_distances = 1 - similarity_matrix[np.ix_(mapped_indices_1, mapped_indices_0)]# 计算特征距离：基于选择的特征变量计算的两个样本之间的欧几里得距离(类似于PSM)。这种距离测量的是在多维特征空间中，两个样本之间在量化特征上的直接距离。X_test_scaled = scaler.transform(df_classification_1[features])feature_distances = pairwise_distances(X_test_scaled, X_scaled[y == 0], metric='euclidean')

6. 将上述两个距离按1:1赋予权重，计算出综合距离以用于最终匹配：

# 计算综合距离alpha = 0.5  # 分类相似性距离的权重beta = (1-alpha)   # 设置特征相似距离的权重combined_distances = alpha*similarity_distances + beta*feature_distances
# 找到最近邻索引并提取匹配的 dummy variable=0 的数据nearest_indices = np.argmin(combined_distances, axis=1)nearest_indices = nearest_indices[nearest_indices < len(df_classification_0)]  # 确保索引有效matched_0 = df_classification_0.iloc[nearest_indices].copy()

7. 检验匹配结果并将匹配后的数据保存在csv文件中：

# T检验和可视化匹配结果features_for_ttest = featurest_test_results = []for feature in features_for_ttest:    group_1_before = df_classification_1[feature]    group_0_before = df_classification_0[feature]    group_0_after = matched_0[feature]    if group_0_after.empty or group_1_before.empty:        print(f"Feature {feature}: Matched data is empty. Skipping t-test.")        continue    # 计算匹配前后的t检验    t_stat_before, p_value_before = stats.ttest_ind(group_1_before, group_0_before, equal_var=False)    t_stat_after, p_value_after = stats.ttest_ind(group_1_before, group_0_after, equal_var=False)    # 记录结果    t_test_results.append({        'Feature': feature,        'T-Stat Before Matching': t_stat_before,        'P-Value Before Matching': p_value_before,        'T-Stat After Matching': t_stat_after,        'P-Value After Matching': p_value_after})    # 可视化匹配前后的分布（箱型图）    plt.figure(figsize=(10, 6))    plt.boxplot([group_0_before, group_0_after, group_1_before],                labels=['Green=0 (pre-matching)', 'Green=0 (post-matching)', 'Green=1'])    plt.axvline(x=1.5, color='gray', linestyle='--', linewidth=1)    title_font = {'fontsize': 16, 'fontname': 'Times New Roman'}    label_font = {'fontsize': 14, 'fontname': 'Times New Roman'}    plt.xticks(fontsize=12, fontname='Times New Roman')    plt.yticks(fontsize=12, fontname='Times New Roman')    plt.title(f'Distribution Comparison for {feature}', fontdict=title_font)    plt.ylabel(feature, fontdict=label_font)    plt.savefig(f'result_matching_T_test_{feature}_boxplot_comparison.png')  # 保存图表    plt.close()# 输出t检验结果为表格形式t_test_df = pd.DataFrame(t_test_results)t_test_df = t_test_df.round(5)print(t_test_df)with pd.ExcelWriter('result_matching_T_test.xlsx') as writer:    t_test_df.to_excel(writer, index=False, sheet_name='T-Test Results')
# 输出匹配后的数据集到CSV文件matched_data = pd.concat([df_classification_1, matched_0], axis=0)matched_data.to_csv('result__matched_data.csv', index=False)print("T-test results have been saved to 'result_T_test.xlsx'.")print("Matched data has been saved to 'result__matched_data.csv'.")

总结：与常用的PSM相比，这一基于RSF的匹配方法在需要匹配的体征变量较多时存在优势，但是当样本量过大时需要较长事件完成匹配。此外，在实际应用过程中，如果某一特征变量十分重要(e.g., X)，可生两个与其完全一样的变量一同带入匹配过程(e.g., X_copy1, X_copy2)，从而实现增加其权重的效果。

代码及数据文件

链接: https://pan.baidu.com/s/1pfUv6uVjwwwbIO8qwmNAqg?pwd=hkvm  提取码:hkvm

编辑：周鹏

附录：参考文献

Piernik, M., Brzezinski, D., & Zawadzki, P. (2022). Random similarity forests. In Joint European Conference on Machine Learning and Knowledge Discovery in Databases (pp. 53-69). Cham: Springer Nature Switzerland.

全欧/全英中国经济学会（Chinese Economic Association UK/Europe，简称CEA）成立于1988年，是一个独立的非盈利的学术团体，是欧洲最具影响力的关注中国经济发展的学会。学会成员包括对中国经济发展感兴趣的学者、学生和企业高管。学会的宗旨是增进公众对中国经济发展的理解，并推动关于中国经济的高质量研究。学会在欧洲和中国举办年会以及学术研讨会，鼓励中国与欧洲之间的学术交流。

CEA学会出版英文期刊Journal of Chinese Economic and Business Studies（JCEBS），期刊注册于牛津大学TMCD研究院，发表可持续发展主题的经济、金融和管理类的跨学科高质量论文，欢迎基于各国样本的原创性研究。其CiteScore（5.6）位列“经济学、计量经济学和金融学”类别中前10%。影响因子（2.4）位列Q2。主编和核心编委会包括经济学领域世界前100引用学者Douglas Cumming，英国社会科学院院士Xiaolan Fu，欧洲科学院经济学部负责人Klaus Zimmermann，英国科学院与发展中国家科学院林毅夫，爱丁堡皇家学会Wenxuan Hou，哈佛大学Dwight Perkins，哥伦比亚大学Jeffrey Sachs，普林斯顿大学Dani Rodrik等具有国际影响力的学者。

欢迎点击下方二维码关注！

拖拽或选择封面

4/120

原创

文字原创 · 作者: 金世杰 · 已开启快捷转载

赞赏

不开启

留言

留言和回复自动精选公开

合集

#学术前沿icon

原文链接

未添加icon

创作来源

不声明icon

平台推荐

已开启icon
