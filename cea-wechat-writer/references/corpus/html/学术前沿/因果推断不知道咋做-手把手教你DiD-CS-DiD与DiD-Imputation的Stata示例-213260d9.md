<!-- source: /Users/karcenzheng/Downloads/CEA_Skill/train_by_category_html/学术前沿/02_【学术前沿】因果推断不知道咋做？手把手教你DiD：CS DiD与DiD Imputation的Stata示例.html -->
<!-- category: 学术前沿 -->
<!-- historical-example-only: true -->

# 【学术前沿】因果推断不知道咋做？手把手教你DiD：CS DiD与DiD Imputation的Stata示例

往期精彩文章：
【文章解读】生成式AI重塑信贷风险评估�|�针对华人经济学家的引用歧视�|�中国两千年经济不平等史�|�明清晋商公司治理�|�绿债贴标选择与影响�|�AI在商业与金融领域的应用
【学术前沿】手把手DID系列�|�系统性文献综述�|�随机相似森林

技术分享：两种支持动态效应识别的DiD与Stata示例

Podcast (English)

![历史文章图片](https://mmbiz.qpic.cn/mmbiz_png/KwzjmZic8l4V83DxrVkrUz4pCmBiarOduAXibohibM3XaA1btTUkqVLiaibaVkrZEXpTaPEwtrbsHrEKEKHo0ZGZAQbA/640?wx_fmt=png&from=appmsg)

作者信息：
Shijie Jin：英国卡迪夫大学商学院博士研究生，研究领域为绿色金融。

【支持动态效应的DiD】
在上一篇文章中，我们区分了“多期数据”与“动态效应”的概念，并介绍了两种不支持动态效应识别的 Difference-in-Differences (DiD) 分析方法 (Stacked DiD 和 Synthetic DiD)，它们在“识别平均效应”、“应对非平行趋势”、“稳健性控制”等方面表现优异。但如果你的研究目的不仅是判断政策有没有效，而是想进一步了解：
政策什么时候开始生效？

效果是否会增强或减弱？

有没有提前反应或持续性？

那你就需要支持动态效应的DiD工具，也就是本篇要介绍的主角：CS DiD 与 DiD Imputation。这两种支持动态效应的 DiD 方法，能够识别在政策实施前后各个时点上的处理效应。这种时间路径视角尤其适合：
多期面板 + 异质处理时间

政策渐进生效(如渐进式最低工资)

可能存在滞后效应或前瞻反应

【方法一：Callaway and Sant’Anna (CS) DiD】
CS DiD是 Callaway and Sant’Anna (2021) 提出的支持多期、异步处理的DiD估计方法，主要用于分析多个单位在不同时间点接受处理后的动态效应。该方法的核心是估计每一个首次接受处理的组(group)在每一个时间点 t 的平均处理效应 (ATT(g,t)), 为检验平行趋势假设和理解政策影响机制提供了重要工具。
💡适用场景
需要估计事件时间效应(event-time ATT)

关心“处理效果是否随时间递增/递减”

需要更透明的控制组设定(never-treated 或 not-yet-treated)

🎯方法优势速览
✅ 支持 event-time 分解，识别效应变化路径
✅�可选择控制组：never-treated、not-yet-treated 等🛠️限制
每个 event-time 的估计依赖样本支撑，晚期处理组置信区间往往较大

估计方差普遍较高，不适合样本有限或研究只聚焦一个时间点时使用

【Stata 示例代码(使用 csdid 包)】

**ÂÆâË£ÖÂëΩ‰ª§**ssc install csdid, replacessc install drdid, replace // ÈÉ®ÂàÜcsdidÊñπÊ≥ïÈúÄË¶ÅË∞ÉÁî®drdid()ÂáΩÊï∞ssc install event_plot, replace //Áî®‰∫éÁîªÂõæ**ÂàõÂª∫Á§∫‰æãÊï∞ÊçÆ**clear allset seed 12345// ÁîüÊàê200‰∏™‰∏™‰ΩìÔºåÊØè‰∏™ÂåÖÂê´10Âπ¥ÁöÑËßÇÊµãÂÄºset obs 200gen id = _nexpand 10bysort id: gen year = 2000 + _n - 1// ÈÉ®ÂàÜ‰∏™‰ΩìÂú®2004, 2006, 20008Âπ¥Ë¢´Â§ÑÁêÜgen treat_year = .replace treat_year = 2004 if id <= 50replace treat_year = 2006 if id > 50 & id <= 100replace treat_year = 2008 if id > 100 & id <= 150// ÂàõÂª∫treat‰ª•Âå∫ÂàÜ‰∏™‰ΩìÊòØÂê¶Ë¢´Â§ÑÁêÜgen D = (year >= treat_year + 1) & treat_year != .// ÊûÑÈÄ†ÁªìÊûúÂèòÈáè Ygen effect = 0replace effect = 10*(year - treat_year) if D == 1 & inrange(year - treat_year, 1, 5)gen x = rnormal(0, 3)gen alpha = rnormal(0, 3)gen gamma = 0.1*(year - 2000)gen epsilon = rnormal(0, 3)gen Y = 1 + alpha + gamma + effect + 0.5*x + epsilon**ÊâßË°åCS DiDÂπ∂ÁîªÂõæ**csdid Y x, ivar(id) time(year) gvar(treat_year) method(dripw)estat event, window(-5 5) estore(cs)event_plot cs, stub_lead(Tm#) stub_lag(Tp#) default_look ///together graph_opt(title("CS DiD") ytitle("") ///xtitle("years since the event") xlabel(-5(1)5))

示例代码结果

![历史文章图片](https://mmbiz.qpic.cn/mmbiz_png/KwzjmZic8l4V83DxrVkrUz4pCmBiarOduAKGCfGl9F0cnhUmYX2tShGaRqib0icCibiazpyBvNTwicsXOlre9DguVphCg/640?wx_fmt=png&from=appmsg)

csdid参数解读参数名称
类型
是否必填
作用说明

depvar
变量名
‚úÖ ÊòØ
因变量

indepvars
变量列表
‚¨ú ÂèØÈÄâ
协变量(控制变量)

ivar(id)
变量名
‚úÖ ÊòØ
‰∏™‰Ωì ID

time(varname)
变量名
‚úÖ ÊòØ
时间变量(如年份)

gvar(varname)
变量名
‚úÖ ÊòØ
每个单位第一次接受处理的时间，未处理为�.�或�0

method(methodname)
字符串
‚¨ú ÂèØÈÄâ
指定估计方法，常见有：dr(默认)、ipw、reg、dripw

vce(cluster varname)
变量名
‚¨ú ÂèØÈÄâ
指定聚类稳健标准误，通常为�id

post
选项
‚¨ú ÂèØÈÄâ
‰øùÂ≠ò‰º∞ËÆ°ÁªìÊûúÔºåÁî®‰∫é estat event Êàñ event_plot

reps(#)
数值
‚¨ú ÂèØÈÄâ
自举次数，配合�vce(bootstrap)�使用

wboot
选项
‚¨ú ÂèØÈÄâ
加速�bootstrap，自举时常用

logit / probit
选项
‚¨ú ÂèØÈÄâ
设置倾向得分模型类型(默认是�probit)

noisily
选项
‚¨ú ÂèØÈÄâ
显示底层估计细节(如�propensity score�模型)

„ÄêÊñπÊ≥ï‰∫åÔºöDiD Imputation„Äë
DiD�Imputation 是 Borusyak et al.(2023)提出的一种适用于估计在不同时间接受处理的单位的因果效应。该方法的核心在于利用未处理(或尚未处理)观察值拟合一个预测模型，并将该模型外推至处理期，从而构造处理单位的潜在结果。通过比较真实结果与预测值，得到单位时间层面的处理效应。该方法有效避免了传统双向固定效应估计中的“负权重”问题。
💡适用场景
协变量结构不复杂，或满足线性回归假设

研结果变量适用于线性建模

🎯方法优势速览
✅�不依赖固定效应或线性回归残差平行趋势假设
✅ 尤结构清晰，便于解释、复现和连接政策机制分析
✅ 可结合机器学习方法模型 (见下文的方法二进阶版)🛠️限制
依赖预测 Y(0)，若建模偏误则识别失效

默认使用线性回归，拟合复杂结构时可能失准

【Stata 示例代码(使用�did_imputation �包)】

**安装命令***ssc install did_imputation, replace
**ÂàõÂª∫Á§∫‰æãÊï∞ÊçÆ**clear allset seed 12345// ÁîüÊàê200‰∏™‰∏™‰ΩìÔºåÊØè‰∏™ÂåÖÂê´10Âπ¥ÁöÑËßÇÊµãÂÄºset obs 200gen id = _nexpand 10bysort id: gen year = 2000 + _n - 1// ÈÉ®ÂàÜ‰∏™‰ΩìÂú®2004, 2006, 20008Âπ¥Ë¢´Â§ÑÁêÜgen treat_year = .replace treat_year = 2004 if id <= 50replace treat_year = 2006 if id > 50 & id <= 100replace treat_year = 2008 if id > 100 & id <= 150// ÊûÑÈÄ†ÁªìÊûúÂèòÈáè Ygen Y = 5 + 0.5*(year - 2000) + rnormal(0,1)gen treat_effect = 0replace treat_effect = 2 if year >= treat_year + 1replace treat_effect = 4 if year >= treat_year + 2replace treat_effect = 6 if year >= treat_year + 3replace Y = Y + treat_effect if !missing(treat_year)
**ÊâßË°åDiD ImputationÂπ∂ÁîªÂõæ**did_imputation Y id year treat_year, horizons(0/3) pretrends(3) autosampleevent_plot, default_look ///together graph_opt(title("DiD Imputation") ytitle("") ///xtitle("years since the event") xlabel(-3(1)3))

示例代码结果

![历史文章图片](https://mmbiz.qpic.cn/mmbiz_png/KwzjmZic8l4V83DxrVkrUz4pCmBiarOduAd9XArw9XLTwOZqZREuAKgmoVlA16eRiaJfP2QR4X5SzWqqpDGgo1gsw/640?wx_fmt=png&from=appmsg)

did_imputation参数解读
参数名称
类型
是否必填
作用说明

Y
变量名
‚úÖ ÊòØ
结果变量(因变量)

i
变量名
‚úÖ ÊòØ
‰∏™‰Ωì ID

t
变量名
‚úÖ ÊòØ
时间变量(如年份)

Ei
变量名
‚úÖ ÊòØ
处理起始时间(未处理设为缺失)

fe(i t)
变量列表
‚¨ú ÂèØÈÄâ
默认：双向固定效应模型

controls(x1 x2)
变量列表
‚¨ú ÂèØÈÄâ
时间变化的连续控制变量

horizons(0/6)
数值列表
‚¨ú ÂèØÈÄâ
指定处理后的各期效应

allhorizons
选项
‚¨ú ÂèØÈÄâ
自动识别所有�horizon

pretrends(5)
整数
‚¨ú ÂèØÈÄâ
进行前置趋势检验

autosample
选项
‚¨ú ÂèØÈÄâ
自动剔除不可估计样本

cluster(i)
变量名
‚¨ú ÂèØÈÄâ
指定聚类单元(默认是�i)

hetby(group)
变量名
‚¨ú ÂèØÈÄâ
按子组估计异质性效应

saveestimates(tau)
变量名
‚¨ú ÂèØÈÄâ
保存个体估计效应结果

saveweights
选项
‚¨ú ÂèØÈÄâ
保存权重变量，便于复用

【方法二进阶版：基于机器学习的�DiD�Imputation】
ML+DiD Imputation 是一种结合机器学习预测与 DiD 框架的估计方法，适用于高维控制变量或复杂非线性关系的场景。该方法的核心是在第一步中利用机器学习 (如随机森林、Lasso、XGBoost 等) 对未处理样本拟合潜在结果模型Y(0)，并将其用于预测处理观测的 counterfactual，再通过 imputation 得到处理效应。该方法在保持 DiD 识别假设的前提下，提升了对Y(0)的拟合精度，并适用于数据维度高、结构复杂或传统回归难以建模的情况。
💡适用场景
协变量结构复杂、数量多，存在非线性关系或交互项

Y 是非线性变量(如 0/1、跳跃值、长尾分布)

追求预测准确性，而不是解释性

有足够样本支撑机器学习建模 + bootstrap 估计标准误

🎯方法优势速览
✅�可使用任何外部 ML 模型 (如随机森林、XGBoost) 预测潜在 Y(0)
✅ 不受线性建模限制，适合复杂趋势、非线性响应
✅�在预测质量高时，ATT 更稳定、误差更小🛠️限制
模型涉及“黑箱”，机制解释困难 (如重要变量解释)

依赖预测模型质量，若过拟合则识别严重偏误

„ÄêStata Á§∫‰æã‰ª£Á†Å(‰ΩøÁî® rforest ÂåÖ + did_imputation ÂåÖ)„Äë

**安装命令***ssc install did_imputation, replace*ssc install rforest, replace
**ÂàõÂª∫Á§∫‰æãÊï∞ÊçÆ**clear allset seed 123set obs 1000gen id = _nexpand 10bysort id: gen time = _ngen Ei = cond(mod(id, 5)==0, ., 5 + mod(id, 3))gen D = (time >= Ei) if Ei < .gen x1 = runiform()gen x2 = runiform()gen u = rnormal()gen y0 = 1 + 2*x1 - 1.5*x2 + sin(2*_pi*x1) + 0.5*x1*x2 + ugen tau = cond(D==1, 3 + 0.5*x1, 0)gen y = y0 + tau
**ML+DiD Imputation 第一步：用 rforest 拟合 Y(0) 并 构造残差变量**gen�use_sample�=�D !=�1rforest y x1 x2�if�use_sample, type(reg) iterations(200)predict yhat_mlgen�y_resid�=�y - yhat_ml**ML+DiD Imputation 第二步：用 did_imputation 拟合残差**did_imputation y_resid id time Ei, fe(.) horizons(0/4) pretrends(4) autosample�cluster(id)//note: FE需要设为 fe(.)，即不再使用固定效应，因为已经用 rforest 拟合过了 Y(0)，并计算了 y - yhat_ml 得到残差 y_resid，这本质上就是固定效应的估计目标。
rforest参数解读
参数名称
类型
是否必填
作用说明

Y
变量名
✅是
结果变量(因变量)

i
变量名
✅是
‰∏™‰Ωì ID

t
变量名
✅是
时间变量(如年份)

Ei
变量名
✅是
处理起始时间(未处理设为缺失)

fe(i t)
变量列表
⬜可选
默认：双向固定效应模型

controls(x1 x2)
变量列表
⬜可选
时间变化的连续控制变量

horizons(0/6)
数值列表
⬜可选
指定处理后的各期效应

allhorizons
选项
⬜可选
自动识别所有�horizon

pretrends(5)
整数
⬜可选
进行前置趋势检验

autosample
选项
⬜可选
自动剔除不可估计样本

cluster(i)
变量名
⬜可选
指定聚类单元(默认是�i)

hetby(group)
变量名
⬜可选
按子组估计异质性效应

saveestimates(tau)
变量名
⬜可选
保存个体估计效应结果

saveweights
选项
⬜可选
保存权重变量，便于复用

【总结】
支持动态效应的 DiD 分析结果看起来信息丰富、解释直观，但如果你：
‚Ä¢ Ê†∑Êú¨ÈáèÊúâÈôêÔºåÈÉ®ÂàÜ event-time ÁÇπÂè™ÊúâÂ∞ëÊï∞‰∏™‰Ωì
‚Ä¢ Áõ∏ËæÉ‰∫é‚Äú‰ªÄ‰πàÊó∂ÂÄôËµ∑Êïà‚ÄùÔºåÊõ¥ÂÖ≥ÂøÉ‚ÄúÊòØÂê¶ÊúâÊïà‚Äù
� � � •�面临政策跳跃、突变式干预，动态路径意义不强那使用这些方法反而可能：
‚Ä¢ Â¢ûÂä†ËØØÂ∑ÆÔºö‰º∞ËÆ°ÊñπÂ∑ÆÈ´òÔºåÊòæËëóÊÄß‰∏çË∂≥
� � � • 误导解读：波动大的 event-study 曲线易被过度解读
总的来说，分析方法选择的核心是“匹配你的研究问题”。模型支持动态效应不是形式主义加分项，而是当你的研究目标本身是关注效应的时间结构时，才值得采用的识别设计。
✅如果你想知道：“政策有没有效?” —— 你不一定需要动态DiD

✅如果你想知道：“什么时候开始有效? 什么时候最强?” —— 这才是动态DiD的用武之地
编辑：周鹏附录：参考文献
Borusyak, K., Jaravel, X. and Spiess, J., 2024. Revisiting event-study designs: robust and efficient estimation. Review of Economic Studies, 91(6), pp.3253-3285.
Callaway, B. and Sant‚ÄôAnna, P.H., 2021. Difference-in-differences with multiple time periods. Journal of econometrics, 225(2), pp.200-230.
