<!-- source: /Users/karcenzheng/Downloads/CEA_Skill/train_by_Shijie_Word/05.【学术前沿】不是所有DiD都需要动态效应 + 两种能看见“动态效应”的DiD方法/【学术前沿】不是所有DiD都需要动态效应 + 两种能看见“动态效应”的DiD方法.docx -->
<!-- category: 学术前沿 -->
<!-- historical-example-only: true -->

# 05.【学术前沿】不是所有DiD都需要动态效应 + 两种能看见“动态效应”的DiD方法

【DiD系列 上篇】不是所有DiD都需要动态效应：Stacked DiD 与 Synthetic DiD的Stata示例

## DiD的基础理念 ##

Difference-in-Differences(DiD) 是一种常用于评估政策或干预措施因果效应的准实验方法，其直观思想其实非常简单：不只看一个群体在政策前后的变化，而是比较“受影响组”和“未受影响组”的变化差异。

我们可以通过一个简化的例子来理解这一思想。假设城市A在某一年推行了某项新就业政策(处理组)，而城市B没有推行(对照组)。城市A在政策实施前后的失业率分别为是10%和7%，而城市B在同时期的失业率分别为9%和8%。

如果我们只看城市A，会认为政策让失业率下降了3%。但也许整个宏观经济环境本身就变好了，所以大家失业率都在下降。城市B作为对照组的变化给我们提供了“正常趋势”——失业率下降了1%，而城市A下降了3%，所以净效应(DiD估计量)= 3% - 1% = 2%。这就是“双重差分”的基本思想。

与此同时，上述案例也体现出DiD方法的有效性依赖于一个关键前提：如果没有发生政策或干预，处理组和对照组的趋势应是平行的。也就是说，任何非干预因素对两个组的影响应该是一样的。为了检验这一假设的合理性，常见的策略包括：

观察干预前几个时期的趋势是否一致；

做“安慰剂检验”(placebo test)，比如在未受干预的对象或与政策无关的结果上应用DiD；

更换不同的对照组做稳健性分析。

## 使用DiD方法时常见的误区 ##

在使用DiD方法进行政策评估或事件分析时存在的一个常见的误解是：“只要面板数据跨越多个年份，加上年份虚拟变量，就能识别动态效应。”但实际上，这是对“多期”与“动态”之间关系的误解。有多期数据只是前提之一，是否能识别动态效应，还取决于你所用的方法。

真正的“动态效应”指的是能够估计某一事件在每一个相对时间点所产生的边际影响是怎样的。该事件可能立刻起效，也可能滞后半年或一年才显现，甚至可能是先增强后减弱。这类估计方法常用来揭示政策是否是逐步生效的、是否具有持续性，甚至是否在正式生效前就已影响行为。

事实上，“是否支持动态效应”更像是一个方法特征而非优劣标志，不同方法在支持与不支持之间，各自优化了不同的性能目标。动态效应听起来很诱人，但并不是所有研究都需要它，也不是所有方法都适合做它。正如刚刚提到的，支持动态效应的方法适合回答：“政策是何时开始见效的？是否具有持续性？”这类动态因果路径问题；但代价是模型结构复杂、估计方差更高、样本需求更大。而不支持动态效应的方法虽然不能提供完整的时间路径，但却能在估计稳健性、对复杂趋势的控制、有限样本下的表现等方面提供更强保障。它们适合回答：“政策是否有效？”这类更基础但常常更关键的问题。

为了更详细介绍不同类型的DiD模型，我们将本话题拆成上下两篇文章：本篇将介绍两种不支持动态效应识别，但在稳健性、解释力和结构控制上具有突出优势的方法：Stacked DiD 与 Synthetic DiD；下篇将介绍两种支持动态效应估计，适用于分析政策效应时间路径的方法：csdid 与 did_imputation。

方法一：Stacked DiD

Cengiz, D., Dube, A, Lindner, A. and Zipperer, B., 2019. The effect of minimum wages on low-wage jobs. The Quarterly Journal of Economics, 134(3), pp.1405-1454.

Stacked DiD是基于事件研究视角的DiD估计方法，由 Cengiz et al. (2019) 首次提出。该方法适用于多个单位在不同时间受到处理(treatment)的场景，典型应用如政策滚动实施。与传统 DiD 相比，Stacked DiD最大的特点是将不同处理时间的个体视为“局部实验”，分别构造事件时间(event-time)窗口，然后“堆叠”成一个统一的分析样本，估计每一个事件时间的平均效应。

- 适用场景

关注处理“前后一个固定窗口”内的平均效应

研究只聚焦一个或几个处理时点

- 优势

将数据拆解为多个独立的二元比较子样本，结构透明、识别清晰

避免 TWFE 的负权重加权问题

可逐步构造和扩展，便于检验不同处理窗口

- 限制

每次只能估一个时间窗口的平均效应(如 t ∈ [-1, +1])，不支持事件时间路径分解

由于子样本独立处理，估计效率偏低，标准误偏大

- Stata 示例代码(使用 stackedev 包)

**安装命令**

ssc install stackedev, replace

ssc install event_plot, replace //用于画图

**创建示例数据**

clear all

set seed 12345

// 生成100个个体，每个包含10年的观测值

set obs 1000

gen id = ceil(_n / 10)

gen year = 2000 + mod(_n-1, 10)

// 一半个体在2005或2006被处理 (要求存在多时点)

gen treatment_year = .

replace treatment_year = 2005 if inrange(id, 1, 30)

replace treatment_year = 2006 if inrange(id, 31, 50)

// 构造ever treated和never treated以区分个体是否被处理

gen ever = !missing(treatment_year)

gen never_treat = ever

recode never_treat (1=0) (0=1)

// 构造相对时间变量

gen rel_year = year - treatment_year

replace rel_year = . if missing(treatment_year)

// 构造结果变量y (post期增加0.5的处理效应)

gen treat = (rel_year >= 0 & rel_year != .)

gen X1 = rnormal()

gen X2 = runiform()

gen y = 1 + 0.5*treat + 0.3*X1 - 0.2*X2 + rnormal()

// 构造 leads/lags dummies(事件期前后3年)

gen pre3 = rel_year == -3

gen pre2 = rel_year == -2

gen pre1 = rel_year == -1

gen post0 = rel_year == 0

gen post1 = rel_year == 1

gen post2 = rel_year == 2

gen post3 = rel_year == 3

**执行Stacked DiD并画图**

stackedev y pre* post*, cohort(treatment_year) time(year) ///

never_treat(never_treat) unit_fe(id) clust_unit(id) covariates(X1 X2)

event_plot, default_look graph_opt(xtitle("years since the event") ///

ytitle("") xlabel(-3(1)3) title("Stacked DiD")) ///

stub_lag(pre#) stub_lead(post#) trimlag(3) trimlead(3) together

**示例代码结果**

stackedev参数解读

方法二：Synthetic DiD

Arkhangelsky, D., Athey, S., Hirshberg, D.A., Imbens, G.W. and Wager, S., 2021. Synthetic difference-in-differences. American Economic Review, 111(12), pp.4088-4118.

Synthetic DiD是一种结合了合成控制法(Synthetic Control)的DiD估计方法， 由 Arkhangelsky et al. (2021) 提出。生成的合成控制组是通过 (1).对控制组单位赋予单位权重omega，和 (2).对预处理时间点赋予时间权重lambda，共同加权构造而成。当处理组与对照组间的平行趋势假设不完全成立时，可通过该方法提升估计的稳健性和准确性。

- 适用场景

面板时间较长，存在单位间非平行趋势

希望更好地控制“预测误差”和“结构趋势差异”

- 优势

同时进行单位加权(借鉴合成控制法)和时间加权，有效控制趋势异质性

尤其适用于处理组样本非常少(甚至为1)的研究

对非线性趋势更稳健

- 限制

默认只输出平均处理效应(ATT)，不支持分解事件时间效应

处理组多、处理时间异质时，加权结构变复杂且难以解释

目前方法结构主要服务于平均效应识别，不适合动态路径分析

- Stata 示例代码(使用 sdid 包)

**安装命令**

ssc install sdid, replace

**创建示例数据**

clear all

set seed 12345

// 生成100个个体，每个包含10年的观测值

set obs 1000

gen id = ceil(_n / 10)

// 生成年份变量(2000–2009)

gen year = 2000 + mod(_n-1, 10)

// 40%的个体在2005被处理(控制组要大于处理组以满足placebo条件)

gen treatment_year = .

replace treatment_year = 2005 if inrange(id, 1, 40)

// 创建treat以区分个体是否被处理

gen treat = (year >= treatment_year) & !missing(treatment_year)

replace treat = 0 if missing(treatment_year)

// 构造结果变量 Y

gen alpha = rnormal(0, 1)  // 所有单位从同一分布抽取

gen gamma = 0.5 * (year - 2000) // 年份趋势

gen tau =  (year >= treatment_year + 1) * treat * 3  // 假设处理效应(2005之后开始有影响)

gen u = rnormal(0,1)  // 加入随机扰动，避免完全线性趋势

gen Y = alpha + gamma + tau

**执行Synthetic DiD并画图**

sdid Y id year treat, vce(placebo) seed(6789) graph ///

g2_opt(graphregion(color(white)) ylabel(0(2)8) xlabel(2000(2)2010)  ///

xtitle("year") ytitle("") title("Synthetic DiD") ///

note("Note: 绿色部分为时间权重lambda"))

**示例代码结果**

sdid参数解读

## 为什么这些分析方法不考虑动态效应但依然重要? ##

很多研究的核心目标不是“政策何时起效”，而是“是否有效”。当研究者只关心一个窗口期的平均效应，而非效应在不同时间如何演化时，过度分解事件时间反而增加模型不稳定性与解释难度。在这种情况下，Stacked DiD的优势在于“多次单期识别”可以避免时间交互的混淆，适合短期窗口评估。而Synthetic did的优势在于“构造最贴近真实趋势的对照组”，在非线性趋势明显、样本有限时提供比 event-study 更稳健的识别。这些方法不是“功能更少”，而是在刻意优化识别目标与估计稳定性。

【DiD系列 下篇】两种能看见“动态效应”的DiD方法：CS DiD 与 DiD Imputation的Stata示例

在上一篇文章中，我们区分了“多期数据”与“动态效应”的概念，并介绍了两种不支持动态效应识别的 DiD 方法(Stacked DiD 和 Synthetic DiD)，它们在“识别平均效应”、“应对非平行趋势”、“稳健性控制”等方面表现优异。

但如果你的研究目的不仅是判断政策有没有效，而是想进一步了解：

政策什么时候开始生效？

效果是否会增强或减弱？

有没有提前反应或持续性？

那你就需要支持动态效应的DiD工具，也就是本篇要介绍的主角：csdid 和 did_imputation。支持动态效应的 DiD 方法，能够识别在政策实施前后各个时点上的处理效应。这种时间路径视角尤其适合：

多期面板 + 异质处理时间

政策渐进生效(如渐进式最低工资)

可能存在滞后效应或前瞻反应

我们要强调的是：动态视角不是更高级，而是服务于更复杂的问题。下面我们分别介绍两种支持动态效应的 DiD 方法。

方法一：Callaway and Sant’Anna (CS) DiD

Callaway, B. and Sant’Anna, P.H., 2021. Difference-in-differences with multiple time periods. Journal of econometrics, 225(2), pp.200-230.

CS DiD是 Callaway and Sant’Anna (2021) 提出的多期、异步处理的DiD估计方法，主要用于分析多个单位在不同时间点接受处理后的动态效应。该方法的核心是估计每一个首次接受处理的组(group)在每一个时间点 t的平均处理效应(ATT(g,t))，为检验平行趋势假设和理解政策影响机制提供了重要工具。

- 适用场景

需要估计事件时间效应(event-time ATT)

关心“处理效果是否随时间递增/递减”

需要更透明的控制组设定(never-treated 或 not-yet-treated)

- 优势：

支持 event-time 分解，识别效应变化路径

可选择控制组：never-treated、not-yet-treated 等

自带 event-study 输出，支持时间路径图与误差区间

- 限制：

每个 event-time 的估计依赖样本支撑，晚期处理组置信区间往往较大

估计方差普遍较高，不适合样本有限或研究只聚焦一个时间点时使用

- Stata 示例代码(使用 csdid 包)

**安装命令**

ssc install csdid, replace

ssc install drdid, replace // 部分csdid方法需要调用drdid()函数

ssc install event_plot, replace //用于画图

**创建示例数据**

clear all

set seed 12345

// 生成200个个体，每个包含10年的观测值

set obs 200

gen id = _n

expand 10

bysort id: gen year = 2000 + _n - 1

// 部分个体在2004, 2006, 20008年被处理

gen treat_year = .

replace treat_year = 2004 if id <= 50

replace treat_year = 2006 if id > 50 & id <= 100

replace treat_year = 2008 if id > 100 & id <= 150

// 创建treat以区分个体是否被处理

gen D = (year >= treat_year + 1) & treat_year != .

// 构造结果变量 Y

gen effect = 0

replace effect = 10*(year - treat_year) if D == 1 & inrange(year - treat_year, 1, 5)

gen x = rnormal(0, 3)

gen alpha = rnormal(0, 3)

gen gamma = 0.1*(year - 2000)

gen epsilon = rnormal(0, 3)

gen Y = 1 + alpha + gamma + effect + 0.5*x + epsilon

**执行CS DiD并画图**

csdid Y x, ivar(id) time(year) gvar(treat_year) method(dripw)

estat event, window(-5 5) estore(cs)

event_plot cs, stub_lead(Tm#) stub_lag(Tp#) default_look ///

together graph_opt(title("CS DiD") ytitle("") ///

xtitle("years since the event") xlabel(-5(1)5))

**示例代码结果**

csdid参数解读

方法二：did_imputation

Borusyak, K., Jaravel, X. and Spiess, J., 2024. Revisiting event-study designs: robust and efficient estimation. Review of Economic Studies, 91(6), pp.3253-3285.

DID Imputation 是 Borusyak et al.(2023)提出的一种适用于估计在不同时间接受处理的单位的因果效应。该方法的核心在于利用未处理(或尚未处理)观察值拟合一个预测模型，并将该模型外推至处理期，从而构造处理单位的潜在结果。通过比较真实结果与预测值，得到单位时间层面的处理效应。该方法有效避免了传统双向固定效应估计中的“负权重”问题。

- 适用场景

协变量结构不复杂，或满足线性回归假设

结果变量适用于线性建模

- 优势：

不依赖固定效应或线性回归残差平行趋势假设

结构清晰，便于解释、复现和连接政策机制分析

能输出 event-time ATT，生成动态效应图(event-study)

可结合机器学习方法模型 (见下文的方法二进阶版)

- 限制：

本质依赖预测 Y(0)，若建模偏误则识别失效

默认使用线性回归，拟合复杂结构时可能失准

- Stata 案例(使用 did_imputation 包)

**安装命令**

*ssc install did_imputation, replace

**创建示例数据**

clear all

set seed 12345

// 生成200个个体，每个包含10年的观测值

set obs 200

gen id = _n

expand 10

bysort id: gen year = 2000 + _n - 1

// 部分个体在2004, 2006, 20008年被处理

gen treat_year = .

replace treat_year = 2004 if id <= 50

replace treat_year = 2006 if id > 50 & id <= 100

replace treat_year = 2008 if id > 100 & id <= 150

// 构造结果变量 Y

gen Y = 5 + 0.5*(year - 2000) + rnormal(0,1)

gen treat_effect = 0

replace treat_effect = 2 if year >= treat_year + 1

replace treat_effect = 4 if year >= treat_year + 2

replace treat_effect = 6 if year >= treat_year + 3

replace Y = Y + treat_effect if !missing(treat_year)

**执行DiD Imputation并画图**

did_imputation Y id year treat_year, horizons(0/3) pretrends(3) autosample

event_plot, default_look ///

together graph_opt(title("DiD Imputation") ytitle("") ///

xtitle("years since the event") xlabel(-3(1)3))

**示例代码结果**

did_imputation参数解读

方法二进阶版：ML + DID Imputation

ML+DID Imputation 是一种结合机器学习预测与 DiD 框架的估计方法，适用于高维控制变量或复杂非线性关系的场景。该方法的核心是在第一步中利用机器学习(如随机森林、Lasso、XGBoost 等)对未处理样本拟合潜在结果模型Y(0)，并将其用于预测处理观测的 counterfactual，再通过 imputation 得到处理效应。该方法在保持 DiD 识别假设的前提下，提升了对Y(0)的拟合精度，并适用于数据维度高、结构复杂或传统回归难以建模的情况。

- 适用场景

协变量结构复杂、数量多，存在非线性关系或交互项

Y 是非线性变量(如 0/1、跳跃值、长尾分布)

追求预测准确性，而不是解释性

有足够样本支撑机器学习建模 + bootstrap 估计标准误

- 优势：

可使用任何外部 ML 模型(如随机森林、XGBoost)预测潜在 Y(0)

不受线性建模限制，适合复杂趋势、非线性响应

在预测质量高时，ATT 更稳定、误差更小

- 限制：

模型涉及“黑箱”，机制解释困难(如重要变量解释)

完全依赖预测模型质量，若过拟合则识别严重偏误

- Stata 案例(使用 rforest 包 + did_imputation 包)

**安装命令**

*ssc install did_imputation, replace

*ssc install rforest, replace

**创建示例数据**

clear all

set seed 123

set obs 1000

gen id = _n

expand 10

bysort id: gen time = _n

gen Ei = cond(mod(id, 5)==0, ., 5 + mod(id, 3))

gen D = (time >= Ei) if Ei < .

gen x1 = runiform()

gen x2 = runiform()

gen u = rnormal()

gen y0 = 1 + 2*x1 - 1.5*x2 + sin(2*_pi*x1) + 0.5*x1*x2 + u

gen tau = cond(D==1, 3 + 0.5*x1, 0)

gen y = y0 + tau

**ML+DiD Imputation 第一步：用 rforest 拟合 Y(0) 并 构造残差变量**

gen use_sample = D != 1

rforest y x1 x2 if use_sample, type(reg) iterations(200)

predict yhat_ml

gen y_resid = y - yhat_ml

**ML+DiD Imputation 第二步：用 did_imputation 拟合残差**

did_imputation y_resid id time Ei, fe(.) horizons(0/4) pretrends(4) autosample cluster(id)

//note: FE需要设为 fe(.)，即不再使用固定效应，因为已经用 rforest 拟合过了 Y(0)，并计算了 y - yhat_ml 得到残差 y_resid，这本质上就是固定效应的估计目标。

rforest参数解读

虽然支持动态效应的DiD分析结果看起来信息丰富、解释直观，但如果你：

样本量有限，部分 event time 点只有少数个体

不关心“什么时候起效”，只关心“是否有效”

面临政策跳跃、突变式干预，动态路径意义不强

那使用这些方法反而可能：

增加误差：估计方差高，显著性不足

误导解读：波动大的 event-study 曲线易被过度解读

放错重点：为了一张图牺牲估计稳健性

总的来说，分析方法选择的核心是“匹配你的研究问题”。模型支持动态效应不是形式主义加分项，而是当你的研究目标本身是关注效应的时间结构时，才值得采用的识别设计。

如果你想知道：“政策有没有效？”——你不一定需要动态 DiD

如果你想知道：“它什么时候开始有效？什么时候最强？”——这才是动态DiD的用武之地

## 表格抽取

参数名称 | 类型 | 是否必填 | 作用说明
outcome | 变量 | ✅ 是 | 因变量(被解释变量y)
leads_lags_list | 变量列表 | ✅ 是 | 相对时间的 dummy 变量(如 pre1, post1 等)
cohort(varname) | 变量名 | ✅ 是 | 表示单位第一次接受处理的时间，未处理单位设为缺失
time(varname) | 变量名 | ✅ 是 | 表示“时间”变量(通常是年份)
never_treat(varname) | 变量名 | ✅ 是 | 二值变量，1 表示从未被处理，0 表示被处理过
unit_fe(varname) | 变量名 | ✅ 是 | 单位固定效应(用于建 stack)
clust_unit(varname) | 变量名 | ✅ 是 | 聚类标准误的单位变量(通常与 unit_fe() 相同)
covariates(varlist) | 变量列表 | ⬜ 可选 | 协变量控制(如 X1 X2)
other_fe(varlist) | 变量列表 | ⬜ 可选 | 其他固定效应(如行业、地区等)
interact_cov(yes) | 字符 | ⬜ 可选 | 若写yes，将协变量与stack dummy相互作用(允许协变量效应跨 stack异质)

参数名称 | 类型 | 是否必填 | 作用说明
depvar | 变量名 | ✅ 是 | 因变量(被解释变量y)
groupvar | 变量名 | ✅ 是 | 个体变量
timevar | 变量名 | ✅ 是 | 表示“时间”变量(通常是年份)
treatment | 变量名 | ✅ 是 | 二值变量，1 表示从未被处理，0 表示被处理过
vce(vcetype) | 选项 | ✅ 是 | 推断方法，支持 bootstrap、jackknife、placebo、noinference
covariates(varlist [, type]) | 变量名+选项 | ⬜ 可选 | 指定协变量及调整方式(optimized 或 projected)
seed(#) | 数值 | ⬜ 可选 | 设置随机数种子，保证结果可重复
reps(#) | 数值 | ⬜ 可选 | 重复次数，用于 bootstrap 和 placebo 推断(默认 50)
method(type) | 字符串 | ⬜ 可选 | 指定估计方法：sdid(默认)、did、sc
zeta_lambda(#) | 数值 | ⬜ 可选 | 时间权重正则化参数
zeta_omega(#) | 数值 | ⬜ 可选 | 单位权重正则化参数
graph | 选项 | ⬜ 可选 | 显示图表(默认关闭)
g1on | 选项 | ⬜ 可选 | 启动单位权重图(默认关闭)
g1_opt(graph options) | 图形选项 | ⬜ 可选 | 修改单位权重图外观
g2_opt(graph options) | 图形选项 | ⬜ 可选 | 修改结果趋势图外观
graph_export(string, type) | 字符串+格式 | ⬜ 可选 | 将生成的图导出到文件(需指定类型如 .pdf、.gph)
msize(markersizestyle) | 图形大小 | ⬜ 可选 | 修改单位图中标记大小
unstandardized | 选项 | ⬜ 可选 | 不对协变量标准化(仅适用于 optimized 协变量)
mattitles | 选项 | ⬜ 可选 | 让权重矩阵含单位标签
xline_opts(string) | 字符串 | ⬜ 可选 | 设置趋势图中处理时间线的外观
yline_opts(string) | 字符串 | ⬜ 可选 | 设置权重图中平均处理效应线的外观

参数名称 | 类型 | 是否必填 | 作用说明
depvar | 变量名 | ✅ 是 | 因变量
indepvars | 变量列表 | ⬜ 可选 | 协变量(控制变量)
ivar(id) | 变量名 | ✅ 是 | 个体 ID
time(varname) | 变量名 | ✅ 是 | 时间变量(如年份)
gvar(varname) | 变量名 | ✅ 是 | 每个单位第一次接受处理的时间，未处理为 . 或 0
method(methodname) | 字符串 | ⬜ 可选 | 指定估计方法，常见有：dr(默认)、ipw、reg、dripw
vce(cluster varname) | 变量名 | ⬜ 可选 | 指定聚类稳健标准误，通常为 id
post | 选项 | ⬜ 可选 | 保存估计结果，用于 estat event 或 event_plot
reps(#) | 数值 | ⬜ 可选 | 自举次数，配合 vce(bootstrap) 使用
wboot | 选项 | ⬜ 可选 | 加速 bootstrap，自举时常用
logit / probit | 选项 | ⬜ 可选 | 设置倾向得分模型类型(默认是 probit)
noisily | 选项 | ⬜ 可选 | 显示底层估计细节(如 propensity score 模型)

参数名称 | 类型 | 是否必填 | 作用说明
Y | 变量名 | ✅ 是 | 结果变量(因变量)
i | 变量名 | ✅ 是 | 个体 ID
t | 变量名 | ✅ 是 | 时间变量(如年份)
Ei | 变量名 | ✅ 是 | 处理起始时间(未处理设为缺失)
fe(i t) | 变量列表 | ⬜ 可选 | 默认：双向固定效应模型
controls(x1 x2) | 变量列表 | ⬜ 可选 | 时间变化的连续控制变量
horizons(0/6) | 数值列表 | ⬜ 可选 | 指定处理后的各期效应
allhorizons | 选项 | ⬜ 可选 | 自动识别所有 horizon
pretrends(5) | 整数 | ⬜ 可选 | 进行前置趋势检验
autosample | 选项 | ⬜ 可选 | 自动剔除不可估计样本
cluster(i) | 变量名 | ⬜ 可选 | 指定聚类单元(默认是 i)
hetby(group) | 变量名 | ⬜ 可选 | 按子组估计异质性效应
saveestimates(tau) | 变量名 | ⬜ 可选 | 保存个体估计效应结果
saveweights | 选项 | ⬜ 可选 | 保存权重变量，便于复用

参数名称 | 类型 | 是否必填 | 作用说明
depvar | 变量名 | ✅ 是 | 被预测变量(回归或分类目标)
indepvars | 变量列表 | ✅ 是 | 自变量列表(预测特征)
type(reg/class) | 字符串 | ✅ 是 | 模型类型：回归(reg)或分类(class)
iterations(#) | 数值 | ⬜ 可选 | 树的数量(默认100)，即迭代次数
numvars(#) | 数值 | ⬜ 可选 | 每次划分中随机选择的特征数(默认：√p)
depth(#) | 数值 | ⬜ 可选 | 每棵树的最大深度(默认不限制)
lsize(#) | 数值 | ⬜ 可选 | 每个叶节点最小观测数(默认1)
seed(#) | 数值 | ⬜ 可选 | 随机数种子，便于结果可重复
newvar | 变量名 | ✅ 是 | 拟合后预测值的存储变量
pr | 选项 | ⬜ 可选 | 分类模型下输出类别概率(仅用于 type(class))
