# 课程字幕翻译

1. ## **Planning workflows** —— 工作流程规划

欢迎来到这 **最后一个单元** ，在这里您将学习到能让您构建**高度自主代理**的 **设计模式** ，您**无需事先硬编码**要采取的步骤序列，

0:06

而是可以 **更加灵活** ，让代理**自行决定**要采取哪些步骤来完成任务。

0:11

我们将讨论 **规划 (planning) 设计模式** ，然后在本单元稍后，讨论 **如何构建多代理系统 (multi-agent systems)** 。

0:16

让我们开始吧。

0:20

假设您经营一家 **太阳镜零售店** ，并将有关库存的太阳镜信息存储在一个**数据库**中。

0:23

您可能希望客户服务代理能够回答这样的问题：“你们有**圆形**的太阳镜吗？而且要 **低于 100 美元** 。”

0:30

这是一个 **相当复杂的查询** ，因为它必须**查看产品描述**以确定哪些太阳镜是圆形的，然后 **查看库存** ，最后查看 **哪些低于 100 美元** ，才能告诉客户：“是的，我们有经典的太阳镜。”

0:36

您如何构建一个代理来回答像这样以及许多其他**广泛的客户查询**呢？

0:45

为了做到这一点，我们将给 LLM  **提供一套工具** ，让它能够获取物品描述（例如 **查找不同的眼镜是否为圆形** ）、 **检查库存** 、 **处理物品退货** （这个查询不需要，但其他查询可能需要）、 **获取物品价格** 、 **检查历史交易** 、**处理物品销售**等等。

0:59

为了让 LLM 弄清楚要使用**正确的工具序列**来响应客户请求，您可以编写一个像这样的提示：

1:05

“您有权访问以下工具”，然后给出 LLM 所拥有的（例如）六个或更多 **工具的描述** ，并告诉它**返回一个逐步的计划**来执行用户的请求。

1:15

在这种情况下，要回答这个特定的查询，LLM 可能会输出一个 **合理的计划** ：

1:22

首先，使用**“获取物品描述”**来检查不同的描述以**找到圆形的太阳镜**，然后使用**“检查库存”**来看它们是否**有库存**，并使用**“获取物品价格”**来看有库存的结果是否**低于 100 美元**。

1:29

在一个 LLM 输出这个包含三个步骤的计划后，我们接下来可以 **取出第一步的文本** （即这里用红色写的文本），并将其 **传递给一个 LLM** ，可能附带关于工具有哪些、您的用户查询是什么、额外的背景信息等，然后让 LLM  **执行第一步** 。

1:38

在这种情况下，希望 LLM 会选择**调用“获取物品描述”**来获取合适的物品描述，

1:48

而**第一步的输出**可以让它 **选择哪些是圆形的太阳镜** ，

1:53

然后**第一步的输出**将与**第二步的** **指令** （即我这里用蓝色标记的指令）一起 **传递给另一个 LLM** ，以 **执行计划的第二步** 。

1:57

希望它随后会**检查**我们在上一个页面上找到的 **两副圆形太阳镜的库存** ，

2:05

然后**第二步的输出**会被用于 **另一次 LLM 调用** ，您将拥有第二步的输出以及**第三步的操作** **指令** 。

2:09

将它传递给 LLM，让它 **获取物品价格** ，最后这个输出会 **最后一次反馈给 LLM** ，以 **生成给用户的最终答案** 。

2:16

在这个页面上，我简化了许多细节。LLM 实际编写的计划通常比这些简单的单行指令 **更详细** ，

2:22

但基本的工作流程是：让 LLM  **写出计划的多个步骤** ，然后**依次**给它分配任务，让它 **执行计划的每一步** ，并附带关于任务是什么、可用工具有哪些等等 **适当的周边上下文** 。

2:30

以这种方式使用 LLM 进行规划的**令人兴奋之处**在于，我们**不必事先决定**调用工具的**顺序**来回答一个相当复杂的客户请求。

2:38

如果客户提出一个 **不同的请求** ，例如：“我希望**退回**我购买的 **金色边框眼镜** ，而不是金属边框的”，

2:44

那么您可以想象 LLM 同样能够 **提出一个不同的计划** ，根据他们之前购买的东西，通过**“获取物品描述”**弄清楚他们购买了哪些眼镜，其中哪些是他们想退回的**金色边框**，然后可能会 **调用“处理物品退货”** 。

2:52

因此，有了像这样 **可以规划的代理** ，它就可以执行 **更广泛的任务范围** ，这些任务可能需要以**许多不同顺序**调用 **许多不同的工具** 。

2:59

另一个规划的例子，我们来看看 **邮件助理** 。

3:02

如果您想告诉您的助理：“请**回复** Bob 在纽约的邮件邀请，告诉他 **我会参加** ，并**归档**他的邮件。”

3:07

那么邮件助理可能会被赋予像这样的工具：**搜索邮件、移动邮件、删除邮件**和 **发送邮件** 。

3:14

您可能会编写一个助理提示：“您有权访问以下工具”，并再次要求它 **返回一个逐步的计划** 。

3:18

在这种情况下，LLM 可能会说，这个任务的步骤是：使用**“搜索邮件”**找到 ****Bob**** 发来的、提到晚餐和纽约的邮件，然后**生成并发送一封邮件**确认出席，最后将该邮件**移动到归档文件夹**。

3:24

鉴于这个看起来合理的计划，您将再次**逐步分配任务给 ****LLM** 来执行这个计划。

3:32

因此， **第一步的文本** （这里以红色显示）将被提供给 LLM，附带额外的背景上下文，并希望它能 **触发“搜索邮件”** 。

3:40

然后，**该输出**可以再次交给 LLM，附带**第二步的** **指令** ，以发送适当的回复。

3:44

最后，假设邮件发送成功，您可以 **获取该输出** ，让 LLM  **执行第三步** ，将 Bob 的邮件 **移动到归档文件夹** 。

3:50

**规划设计模式**已经成功地应用于许多**高度代理化的编码系统**中，如果您要求它编写一段软件来构建一些 **相当复杂的应用程序** ，它可能会想出一个计划：先构建这个组件，再构建那个组件，几乎形成一个 **清单** ，然后 **逐一执行这些步骤** ，以构建一个 **相当复杂的软件** 。

3:56

对于许多其他应用程序，规划的使用可能 **仍处于试验阶段** ，尚未广泛使用。规划的**挑战之一**是它有时会使系统 **有点难以控制** ，因为作为开发人员，您**无法真正知道**在运行时它会想出 **什么样的计划** 。

4:09

因此，我认为在 **高度代理化编码系统** （它确实运行得非常好）之外，规划的 **应用仍在其他领域增长** 。

4:14

但这是一项 **令人兴奋的技术** ，我认为它会 **不断改进** ，我们会在**越来越多的应用**中看到它。

4:25

构建可以**自行规划的代理**的酷之处在于，您**无需事先硬编码** LLM 为执行复杂任务可能采取的 **确切步骤序列** 。

4:30

现在，我知道在这个视频中，我以一个**相当高的层次**介绍了规划过程：列出步骤，然后任务 LLM **一次一步**地执行计划的步骤。

4:40

但 **这到底是如何运作的呢** ？在下一个视频中，我们将进行 **更深入的探究** ，进一步了解这些计划的 **实际内部结构** ，以及它们是如何串联起来，让 LLM 为您**规划和执行计划**的。

4:49

让我们在下一个视频中看看。

2. ## **Creating and executing ****LLM**** plans** —— 创建并执行大语言模型计划

在这个视频中，我们将详细了解**如何提示 ****LLM** ** 生成计划** ，以及 **如何读取、解释和执行该计划** 。让我们深入探讨。

0:04

这是您在**上一个视频**中看到的**客户服务代理**的计划，我使用简单的文本描述以**高层次**的方式呈现了该计划。

0:08

让我们看看如何让 LLM 编写 **非常清晰的计划** ，这些计划要**比**那些简单的高层次文本描述 **更进一步** 。

0:17

事实证明，许多开发人员会要求 LLM 以 **JSON**** 格式**来格式化它想要执行的计划，因为这使得**下游代码**能够以相对**清晰和明确**的方式 **解析计划的具体步骤** ，

0:30

而且所有主流的 LLM 目前都**非常擅长生成 ****JSON** ** 输出** 。

0:36

因此，系统提示可能像这样：“您有权访问以下工具”，然后要求它**“以 JSON 格式创建一步一步的计划”**，您可能会**详细描述 JSON 格式**，目标是让它输出如右侧所示的计划。

0:46

在这个 JSON 输出中，它创建了一个 **列表** ，其中第一个列表项有清晰的**键** **和值** ，说明计划的**第一步**有以下 **描述** ，它应该使用以下 **工具** ，并传入以下**参数**给该工具。

1:02

然后，计划的**第二步**是执行这个任务，接着使用这个工具，等等。

1:15

因此，这种 **JSON** ** 格式** （而不是用英文来编写计划）允许下游代码**更清晰地解析**计划的 **确切步骤** ，从而可以**可靠地**一步一步执行。

1:26

除了 JSON 之外，我也看到一些开发人员使用  **XML** ，您可以使用 XML 分隔符。您使用 **XML 标签**来清晰地指定计划的**步骤**以及它是 **第几步** 。

1:38

一些开发人员（我觉得数量较少）会使用  **Markdown** ，但它的解析方式有时**稍微模糊**一些，我认为**纯文本**可能是这些选项中**最不可靠**的。

1:50

但我认为  **JSON** （我这里展示的）或 **XML** 都是 **很好的选项** ，可用于要求 LLM **明确地**格式化计划。

2:00

就是这样。通过以 JSON 格式输出计划，您可以**解析**它，并让下游工作流程 **更系统地执行计划的不同步骤** 。

2:05

现在，关于让 LLM 进行规划，事实证明还有一个 **非常巧妙的思路** ，可以让 LLM 输出**非常复杂的计划**并 **可靠地执行** ，那就是 **让它们编写代码** ，并 **用代码来表达计划** 。

2:20

让我们在下一个视频中看看这个。

3. ## **Planning with code execution** —— 结合代码执行的规划

**使用代码执行进行规划**的想法是：与其要求 LLM 输出一个**例如 ****JSON**** 格式**的计划并 **一步步执行** ，为什么不让 LLM 直接尝试 **编写代码** ，

0:06

这段代码可以 **捕获计划的多个步骤** ，比如调用这个函数，然后调用那个函数，再调用另一个函数。通过 **执行 LLM 生成的代码** ，我们实际上可以执行 **相当复杂的计划** 。

0:12

让我们看看**何时**您可能想要使用这项技术。

0:22

假设您想要构建一个系统，根据一个包含**先前销售数据**的电子表格（如右图所示），来回答有关**咖啡机销售**的问题。

0:27

您可能会给 LLM 一套像这样的 **工具** ：`获取列最大值`（查看某一列并获取最大值，例如回答“最贵的咖啡是什么”），`获取列平均值`，`过滤行`，`获取列最小值`，`获取列中位数`，`对行求和`等等。

0:33

这些是您可以赋予 LLM 的一系列工具的例子，用于以**不同的方式处理**这个电子表格或这些行和列的数据。

0:50

现在，如果用户问：“ **哪个月份热巧克力的销量最高？** ”

1:00

事实证明，您可以使用这些工具回答这个查询，但它 **非常复杂** 。

1:06

您必须使用**“过滤行”**来提取一月份热巧克力的交易，然后对其进行统计，再重复二月份的，对其进行统计，然后重复三月、四月、五月，一直到十二月，然后再取**最大值**。

1:11

因此，您实际上可以使用这些工具将其串联成一个 **相当复杂的过程** ，但这并不是一个很好的解决方案。

1:24

但更糟的是，如果有人问：“ **上周有多少独特的交易？** ” 那么**这些工具是不足以**得到答案的。

1:28

因此，您可能最终会创建一个 **新的工具** ，例如 `获取唯一条目`；或者您可能会遇到另一个查询：“ **最近五笔交易的金额是多少？** ” 那么您又不得不创建**另一个工具**来获取数据以回答该查询。

1:35

在实践中，我见过一些团队，随着遇到的查询越来越多，最终不得不 **创建越来越多、越来越多的工具** ，试图为 LLM 提供**足够的工具**来涵盖人们可能问及这类数据集的所有范围。

1:49

所以，这种方法 **脆弱、效率低下** ，我见过团队不断地处理**边缘情况**并尝试创建更多工具。但事实证明，有一个 **更好的方法** ，

2:06

那就是您可以提示 LLM 说：“请**编写代码**来解决用户的查询，并以 **Python 代码**返回您的答案，可能用这些开始和结束的 `execute_python` XML 标签来分隔。”

2:13

然后 LLM 就可以 **编写代码** ，将电子表格加载到一个**数据处理库**中（这里它使用的是 **Pandas** ** 库** ），然后它实际上是在 **提出一个计划** 。

2:26

计划是：在加载 CSV 后，首先必须确保 **日期列以某种方式解析** ，然后 **按日期排序** ， **选择最近五笔交易** ，**只显示价格列**等等。

2:38

这些就是计划中的第一、二、三、四、五步。

2:49

因为像 Python 这样的编程语言（在这个例子中，还导入了 **Pandas** ** 数据处理库** ），它拥有许多 **内置函数** ， **数百甚至数千个函数** ，而且 LLM 已经看到了**大量关于何时调用这些数据的** **训练数据** 。

2:55

通过让您的 LLM  **编写代码** ，它可以从这**数百或数千个相关函数**中进行选择，而它已经看到了大量关于何时使用它们的数据。因此，这使得它能够将来自这个**非常大的库**的**不同函数选择**串联起来，从而提出一个 **回答相当复杂查询的计划** 。

3:10

再举一个例子。如果有人问：“ **上周有多少独特的交易？** ”

3:18

您可以想出一个计划：**读取 ****CSV** ** 文件** ， **解析日期列** ， **定义时间窗口** ， **过滤行** ， **删除重复行** ，然后 **计数** 。

3:24

这些细节并不重要，但希望您能看到（如果您阅读这里的注释），LLM 大致提出了一个 **四步计划** ，并以**您可以直接执行的代码**表达了每一步，这将为用户获得答案。

3:32

因此，对于**任务可以合理地通过编写代码来完成**的应用，让 LLM 以**您可以直接执行的软件代码**来表达其计划，可以是一种**非常有力的**方式，让它编写 **丰富的计划** 。

3:43

当然，我曾在工具使用单元中提到的**注意事项**也适用：考虑您是否需要一个**安全** **执行环境** ，比如**沙箱**来运行代码。尽管我知道即使可能不是最佳实践，我仍然知道很多开发人员并 **不使用沙箱** 。

4:01

最后，事实证明 **使用代码进行规划效果很好** 。

4:05

从这张改编自 Xinyao Wang 等人研究论文的图表中，您可以看到，对于他们检查的**许多不同模型**的任务， **代码作为行动 (Code as Action)** （其中 LLM 被邀请编写代码并通过代码采取行动）**优于**让它编写 JSON 然后将 JSON 转换成行动或文本。

4:25

您还会看到一个趋势：**编写代码**的表现**优于**让 LLM 以 JSON 编写计划，而**以 JSON 编写计划**也比**仅用纯文本编写计划**要好一些。

4:32

当然，有些应用您可能希望将您的**定制工具**交给 LLM 使用，所以 **编写代码并非适用于每一个应用** 。但当它适用时，它可以是 LLM 表达计划的 **一种非常强大的方式** 。

4:40

这结束了关于**规划**的部分。如今，**规划式代理 ****AI**** 最强大的用途之一**是**高度代理化的软件** **编码器** 。

4:46

事实证明，如果您要求其中一个**高度代理化的软件编码辅助工具**为您编写一段 **复杂的软件** ，它可能会想出一个 **详细的计划** ：先构建软件的这个组件，然后构建第二个组件，构建第三个，甚至可能计划 **在进行过程中测试组件** 。然后它会形成一个 **清单** ，并 **逐一执行** 。

5:00

因此，它在构建**日益复杂的软件**方面确实运行得非常好。对于 **其他应用** ，我认为规划的使用 **仍在发展和完善中** 。

5:08

规划的**缺点之一**是，因为开发人员 **没有告诉系统具体该做什么** ，所以 **控制起来有点困难** ，而且您**无法事先知道**运行时会发生什么。但 **放弃一些控制权** ，确实 **显著增加了模型可能决定尝试的事物范围** 。

5:14

因此，这项重要的技术 **处于前沿** ，**在代理式编码之外**感觉 **尚未完全成熟** （尽管它运行良好，但肯定还有很大的成长空间）。但我希望您有一天能在您的一些应用中享受到它的乐趣。

5:32

关于规划的部分到此结束。在本单元中，我希望与您分享 **最后一个设计模式** ，即 **如何构建多代理系统 (Multi-Agent Systems)** 。我们不再只有一个代理，而是**许多代理协同工作**来为您完成任务。

5:44

让我们在下一个视频中看看这个。

4. ## **【实验】Ungraded Lab: ****Customer Service**** Agent** —— 非评分实验：客服代理

以下是 M5 实验指南的中文翻译：

### M5 智能体 AI - 客户服务智能体

1. 介绍

正如 Andrew 在讲座中解释的，**通过代码执行进行规划** (planning with code execution) 意味着让 LLM  **编写代码，而这些代码本身就成为了规划** 。与纯文本或基于 JSON 的规划相比，这种方法更具表现力和灵活性：代码不仅记录了步骤，还可以直接执行它们。

在本实验中，你将亲手实现这种设计模式。

我们将不再要求 LLM 以 JSON 格式输出规划，然后手动执行每个步骤，而是允许它**编写 Python 代码**来直接捕获规划的多个步骤。通过执行此代码，我们可以自动执行复杂的查询。

为了使事情具体化，我们模拟了一个 **太阳镜商店** ，它有一个产品**库存**和一组 **交易** （销售、退货、余额更新）。这个例子展示了 LLM 如何生成代码来查询或更新记录，证明了这种模式的灵活性。

### 1.1 实验概述

我们将：

* 创建简单的**库存**和**交易**数据集。
* 构建一个描述数据的**模式块** (schema block)。
* 提示 LLM  **以 Python 代码的形式编写规划** （并附有解释每个步骤的注释）。
* 在沙盒 (sandbox) 中执行代码以获取答案。

### 1.2 学习成果

完成本实验后，你将能够：

* 解释 **为什么让模型编写代码** （而不是 JSON 或纯文本规划）能够实现更丰富、更灵活的规划。
* **提示 (Prompt)** LLM 生成带有分步注释的 Python 代码，这些代码既能记录规划也能执行规划。
* 在沙盒中安全地**运行**生成的代码并解释结果。

这说明了**“代码即行动” (Code as Action)** 如何能胜过脆弱的工具链和基于 JSON 的规划方法。

---

2. 设置

```Plain
# ==== Imports ====from __future__ import annotations
import json
from dotenv import load_dotenv
from openai import OpenAI
import re, io, sys, traceback, json
from typing import Any, Dict, Optional
from tinydb import Query, where
 
# Utility modulesimport utils      # helper functions for prompting/printingimport inv_utils  # functions for inventory, transactions, schema building, and TinyDB seeding
 
load_dotenv()
client = OpenAI()
```

在 `inv_utils` 模块中，我们有如下函数：

* `create_inventory()` – 构建太阳镜库存。
* `create_transactions()` – 构建初始交易日志。
* `seed_db()` – 将库存和交易加载到由 JSON 支持的存储中。
* `build_schema_block()` – 生成用于提示中的模式描述。
* 辅助函数如 `get_current_balance()` 和 `next_transaction_id()` – 让 LLM 处理跨库存和交易的一致更新。

### 2.1 创建示例表

我们现在将使用 **TinyDB** 为太阳镜商店模拟创建两个小表。TinyDB 是一个用纯 Python 编写的轻量级面向文档的数据库。

TinyDB 将数据存储为 JSON 文档，非常适合小型应用或原型，因为它不需要服务器设置，并允许你轻松查询和更新数据。

这两个表是：

* `inventory_tbl`: 包含产品详细信息，如名称、商品 ID、描述、库存数量和价格。
* `transactions_tbl`: 以期初余额开始，稍后将跟踪购买、退货和调整。

你将使用 `inv_utils` 中的辅助函数生成这些表，然后在下面预览前几行。

```Plain
db, inventory_tbl, transactions_tbl = inv_utils.seed_db()
```

现在，你可以通过将记录打印为格式化的 JSON 来检查每个表中的记录：

```Plain
utils.print_html(json.dumps(inventory_tbl.all(), indent=2), title="Inventory Table")
utils.print_html(json.dumps(transactions_tbl.all(), indent=2), title="Transactions Table")
```

如上所示，每个表的模式如下：

**库存表 (inventory_tbl)**

* `item_id` (string): 唯一产品标识符 (例如, SG001)。
* `name` (string): 太阳镜款式 (例如, Aviator, Round)。
* `description` (string): 产品的文本描述。
* `quantity_in_stock` (int): 当前可用库存。
* `price` (float): 美元价格。

**交易表 (transactions_tbl)**

* `transaction_id` (string): 唯一标识符 (例如, TXN001)。
* `customer_name` (string): 客户名称，或 `OPENING_BALANCE` (期初余额) 用于初始条目。
* `transaction_summary` (string): 交易的简短描述。
* `transaction_amount` (float): 此交易的金额。
* `balance_after_transaction` (float): 应用此交易后的运行余额。
* `timestamp` (string): 交易的 ISO-8601 格式日期/时间。

---

## 通过代码执行进行规划

### 2.1. 规划

一旦模式清晰，你将构建 **提示 (prompt)** ，指示模型 **通过编写代码来进行规划** ，然后执行该代码。正如 Andrew 强调的， **代码就是规划** ：模型在注释中解释每个步骤，然后执行它。下面的提示还使模型能够自行决定请求是只读的还是状态更改，并且它强制执行安全执行（无 I/O，无网络，仅限 TinyDB 查询，一致的可变操作）。

```Plain
PROMPT = """You are a senior data assistant. PLAN BY WRITING PYTHON CODE USING TINYDB.
 
Database Schema & Samples (read-only):
{schema_block}
 
Execution Environment (already imported/provided):
- Variables: db, inventory_tbl, transactions_tbl  # TinyDB Table objects
- Helpers: get_current_balance(tbl) -> float, next_transaction_id(tbl, prefix="TXN") -> str
- Natural language: user_request: str  # the original user message
 
PLANNING RULES (critical):
- Derive ALL filters/parameters from user_request (shape/keywords, price ranges "under/over/between", stock mentions,
  quantities, buy/return intent). Do NOT hard-code values.
- Build TinyDB queries dynamically with Query(). If a constraint isn't in user_request, don't apply it.
- Be conservative: if intent is ambiguous, do read-only (DRY RUN).
 
TRANSACTION POLICY (hard):
- Do NOT create aggregated multi-item transactions.
- If the request contains multiple items, create a separate transaction row PER ITEM.
- For each item:
  - compute its own line total (unit_price * qty),
  - insert ONE transaction with that amount,
  - update balance sequentially (balance += line_total),
  - update the item’s stock.
- If any requested item lacks sufficient stock, do NOT mutate anything; reply with STATUS="insufficient_stock".
 
HUMAN RESPONSE REQUIREMENT (hard):
- You MUST set a variable named `answer_text` (type str) with a short, customer-friendly sentence (1–2 lines).
- This sentence is the only user-facing message. No dataframes/JSON, no boilerplate disclaimers.
- If nothing matches, politely say so and offer a nearby alternative (closest style/price) or a next step.
 
ACTION POLICY:
- If the request clearly asks to change state (buy/purchase/return/restock/adjust):
    ACTION="mutate"; SHOULD_MUTATE=True; perform the change and write a matching transaction row.
  Otherwise:
    ACTION="read"; SHOULD_MUTATE=False; simulate and explain briefly as a dry run (in logs only).
 
FAILURE & EDGE-CASE HANDLING (must implement):
- Do not capture outer variables in Query.test. Pass them as explicit args.
- Always set a short `answer_text`. Also set a string `STATUS` to one of:
  "success", "no_match", "insufficient_stock", "invalid_request", "unsupported_intent".
- no_match: No items satisfy the filters → suggest the closest in style/price, or invite a different range.
- insufficient_stock: Item found but stock < requested qty → state available qty and offer the max you can fulfill.
- invalid_request: Unable to parse essential info (e.g., quantity for a purchase/return) → ask for the missing piece succinctly.
- unsupported_intent: The action is outside the store’s capabilities → provide the nearest supported alternative.
- In all cases, keep the tone helpful and concise (1–2 sentences). Put technical details (e.g., ACTION/DRY RUN) only in stdout logs.
 
OUTPUT CONTRACT:
- Return ONLY executable Python between these tags (no extra text):
  <execute_python>
  # your python
  </execute_python>
 
CODE CHECKLIST (follow in code):
1) Parse intent & constraints from user_request (regex ok).
2) Build TinyDB condition incrementally; query inventory_tbl.
3) If mutate: validate stock, update inventory, insert a transaction (new id, amount, balance, timestamp).
4) ALWAYS set:
   - `answer_text` (human sentence, required),
   - `STATUS` (see list above).
   Also print a brief log to stdout, e.g., "LOG: ACTION=read DRY_RUN=True STATUS=no_match".
5) Optional: set `answer_rows` or `answer_json` if useful, but `answer_text` is mandatory.
 
TONE EXAMPLES (for `answer_text`):
- success: "Yes, we have our Classic sunglasses, a round frame, for $60."
- no_match: "We don’t have round frames under $100 in stock right now, but our Moon round frame is available at $120."
- insufficient_stock: "We only have 1 pair of Classic left; I can reserve that for you."
- invalid_request: "I can help with that—how many pairs would you like to purchase?"
- unsupported_intent: "We can’t refurbish frames, but I can suggest similar new models."
 
Constraints:
- Use TinyDB Query for filtering. Standard library imports only if needed.
- Keep code clear and commented with numbered steps.
 
User request:
{question}
"""
```

### 2.2 从提示到代码（在代码中规划）

让我们生成**即为规划**的代码。

与其要求模型以 JSON 格式输出规划并使用许多小型工具逐步运行它，不如让它 **编写 Python 代码来编码整个规划** （例如，“过滤这个，然后计算那个，然后更新这一行”）。函数 `generate_llm_code`：

* 从 `inventory_tbl` 和 `transactions_tbl`  **构建实时模式** ，以便模型看到真实的字段、类型和示例。
* 使用该模式和用户的问题 **格式化提示** 。
* **调用模型**以生成**带代码的规划**响应——通常是一个 `<execute_python>...</execute_python>` 块，其主体包含分步逻辑。
* **返回完整的响应** （包括规划和代码）。

**我们在此步骤中不执行任何操作。**

**为什么选择这种模式？** 让我们利用 Python/TinyDB 作为一个丰富的工具箱，模型已经“了解”它，因此它可以直接在代码中组合多步解决方案，而不是依赖于一组不断增长的定制工具。我们将在稍后的步骤中提取并运行代码。

```Plain
# ---------- 1) Code generation ----------def generate_llm_code(
    prompt: str,
    *,
    inventory_tbl,
    transactions_tbl,
    model: str = "gpt-4.1-mini",
    temperature: float = 0.2,
) -> str:"""
    Ask the LLM to produce a plan-with-code response.
    Returns the FULL assistant content (including surrounding text and tags).
    The actual code extraction happens later in execute_generated_code.
    """
    schema_block = inv_utils.build_schema_block(inventory_tbl, transactions_tbl)
    prompt = PROMPT.format(schema_block=schema_block, question=prompt)
 
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": "You write safe, well-commented TinyDB code to handle data questions and updates."
            },
            {"role": "user", "content": prompt},
        ],
    )
    content = resp.choices[0].message.content or ""return content
```

### 2.3 尝试一个示例提示（在代码中规划）

我们将使用 Andrew 在讲座中使用的相同提示：

**提示：** “你们有 100 美元以下的圆形太阳镜库存吗？”

在生成任何代码之前，让我们手动检查 TinyDB 表，看看是否真的有**圆形 (round)** 镜框（仅限单词匹配）以及它们的价格。运行下一个单元格以预览库存并突出显示与“round”一词匹配的商品。

```Plain
Item = Query()                    # Create a Query object to reference fields (e.g., Item.name, Item.description)# Search the inventory table for documents where either the description OR the name# contains the word "round" (case-insensitive). The check is done inline:# - (v or "") ensures we handle None by converting it to an empty string# - .lower() normalizes case# - " round " enforces a crude word boundary (won't match "wraparound")
round_sunglasses = inventory_tbl.search(
    (Item.description.test(lambda v: " round " in ((v or "").lower()))) |
    (Item.name.test(        lambda v: " round " in ((v or "").lower())))
)
 
# Render the results as formatted JSON in the notebook UI
utils.print_html(json.dumps(round_sunglasses, indent=2), title="Inventory Status: Round Sunglasses")
```

太好了——我们确实有圆形镜框。从我们的手动检查来看，有两种圆形款式有库存，但只有**一种**低于 100 美元。因此，满足要求的商品是：

```Plain
{
  "item_id": "SG005",
  "name": "Classic",
  "description": "Classic round profile with minimalist metal frames, offering a timeless and versatile style that fits both casual and formal wear.",
  "quantity_in_stock": 10,
  "price": 60
}
```

现在，让我们要求模型**生成一个代码规划**来回答 Andrew 的提示（尚未执行）。

```Plain
# Andrew's prompt from the lecture
prompt_round = "Do you have any round sunglasses in stock that are under $100?"# Generate the plan-as-code (FULL content; may include <execute_python> tags)
full_content_round = generate_llm_code(
    prompt_round,
    inventory_tbl=inventory_tbl,
    transactions_tbl=transactions_tbl,
    model="o4-mini",
    temperature=1.0,
)
 
# Inspect the LLM’s plan + code (no execution here)
utils.print_html(full_content_round, title="Plan with Code (Full Response)")
```

### 2.4. 定义执行器函数（运行给定规划）

现在我们将定义一个函数，它 **接收模型生成的规划并安全地运行它** ：

* 它**接受**完整的 LLM 响应（带有 `<execute_python>…</execute_python>`）**或**原始 Python 代码。
* 它在需要时**提取**可执行块。
* 它在**受控的命名空间** (namespace) 中运行代码（仅限 TinyDB 表 + 安全的辅助函数）。
* 它捕获  **stdout** 、**错误**以及模型设置的答案变量（`answer_text`, `answer_rows`, `answer_json`）。
* 它呈现**执行前/后**的表快照，以使副作用明确。

这是将**“代码即规划”** (plan-as-code) 转换为行动和简洁的面向用户答案的“执行器”。

```Plain
# --- Helper: extract code between <execute_python>...</execute_python> ---def _extract_execute_block(text: str) -> str:"""
    Returns the Python code inside <execute_python>...</execute_python>.
    If no tags are found, assumes 'text' is already raw Python code.
    """if not text:
        raise RuntimeError("Empty content passed to code executor.")
    m = re.search(r"<execute_python>(.*?)</execute_python>", text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else text.strip()
 
 
# ---------- 2) Code execution ----------def execute_generated_code(
    code_or_content: str,
    *,
    db,
    inventory_tbl,
    transactions_tbl,
    user_request: Optional[str] = None,
) -> Dict[str, Any]:"""
    Execute code in a controlled namespace.
    Accepts either raw Python code OR full content with <execute_python> tags.
    Returns minimal artifacts: stdout, error, and extracted answer.
    """# Extract code here (now centralized)
    code = _extract_execute_block(code_or_content)
 
    SAFE_GLOBALS = {
        "Query": Query,
        "get_current_balance": inv_utils.get_current_balance,
        "next_transaction_id": inv_utils.next_transaction_id,
        "user_request": user_request or "",
    }
    SAFE_LOCALS = {
        "db": db,
        "inventory_tbl": inventory_tbl,
        "transactions_tbl": transactions_tbl,
    }
 
    # Capture stdout from the executed code
    _stdout_buf, _old_stdout = io.StringIO(), sys.stdout
    sys.stdout = _stdout_buf
    err_text = Nonetry:
        exec(code, SAFE_GLOBALS, SAFE_LOCALS)
    except Exception:
        err_text = traceback.format_exc()
    finally:
        sys.stdout = _old_stdout
    printed = _stdout_buf.getvalue().strip()
 
    # Extract possible answers set by the generated code
    answer = (
        SAFE_LOCALS.get("answer_text")
        or SAFE_LOCALS.get("answer_rows")
        or SAFE_LOCALS.get("answer_json")
    )
 
 
    return {
        "code": code,            # <- 已经没有标签了"stdout": printed,
        "error": err_text,
        "answer": answer,
        "transactions_tbl": transactions_tbl.all(),  # For inspection"inventory_tbl": inventory_tbl.all(),  # For inspection
    }
```

你已经检查了货架，确认只有一款 100 美元以下的圆形太阳镜。现在有趣的部分来了：让我们把模型的“代码即规划”交给我们的执行器，看它如何工作。执行器将剥离出 `<execute_python>...</execute_python>` 块，在一个锁定的沙盒中运行它，然后向你展示所有重要信息——表中的变化（之前/之后）、规划打印的任何日志，以及最终的、面向客户的 `answer_text`。

```Plain
# Execute the generated plan for the round-sunglasses question
result = execute_generated_code(
    full_content_round,          # the full LLM response you generated earlier
    db=db,
    inventory_tbl=inventory_tbl,
    transactions_tbl=transactions_tbl,
    user_request=prompt_round, # e.g., "Do you have any round sunglasses in stock that are under $100?"
)
 
# Peek at exactly what Python the plan executed
utils.print_html(result["answer"], title="Plan Execution · Extracted Answer")
```

如你所见，这与我们之前手动分析的预期结果一致。

### 2.4 退回两副飞行员太阳镜

在上一步中，我们只**查询**了数据，因此库存和交易没有变化。

现在，让我们使用“在代码中规划”的模式处理一个**退货**场景：

**请求：** “退回我上周买的 2 副飞行员太阳镜。”

在生成规划之前，让我们**检查当前库存**中的 **Aviator (飞行员)** 模型。

```Plain
Item = Query()                    # Create a Query object to reference fields (e.g., Item.name, Item.description)# Query: fetch all inventory rows whose 'name' is exactly "Aviator".# Notes:# - This is a case-sensitive equality check. "aviator" won't match.# - If you need case-insensitive matching, consider a .test(...) or .matches(...) with re.I.
aviators = inventory_tbl.search(
    (Item.name == "Aviator")
)
 
# Display the matched documents in a readable JSON panel
utils.print_html(json.dumps(aviators, indent=2), title="Inventory status: Aviator sunglasses before return")
```

库存确认有一款 Aviator SKU 在库—— **SG001 (Aviator)** ：**23** 件，每件  **$80** 。现在让我们生成一个规划来回答这个提示：

```Plain
prompt_aviator = "Return 2 Aviator sunglasses I bought last week."# Generate the plan-as-code (FULL content; may include <execute_python> tags)
full_content_aviator = generate_llm_code(
    prompt_aviator,
    inventory_tbl=inventory_tbl,
    transactions_tbl=transactions_tbl,
    model="o4-mini",
    temperature=1,
)
 
# Inspect the LLM’s plan + code (no execution here)
utils.print_html(full_content_aviator, title="Plan with Code (Full Response)")
```

在我们执行规划之前，让我们检查一下交易的当前状态。

```Plain
utils.print_html(json.dumps(transactions_tbl.all(), indent=2), title="Transactions Table Before Return")
```

交易日志目前显示一个条目——**$500.00** 的期初余额 (TXN001)，记录于 `2025-10-03T09:16:59.628898`。

准备就绪——运行下面的单元格来执行规划。

```Plain
# Execute the generated plan for the round-sunglasses question
result = execute_generated_code(
    full_content_aviator,          # the full LLM response you generated earlier
    db=db,
    inventory_tbl=inventory_tbl,
    transactions_tbl=transactions_tbl,
    user_request=prompt_aviator, # e.g., "Return 2 aviator sunglasses I bought last week."
)
 
# Peek at exactly what Python the plan executed
utils.print_html(result["answer"], title="Plan Execution · Extracted Answer")
```

你可以在下面看到，已经为 Aviator 太阳镜的退货插入了一个新的交易。

```Plain
utils.print_html(json.dumps(transactions_tbl.all(), indent=2), title="Transactions Table After Return")
```

通过运行下面的单元格，你会看到 Aviator 库存增加到 25 (quantity_in_stock)。

```Plain
Item = Query()                
 
aviators = inventory_tbl.search(
    (Item.name == "Aviator")
)
 
utils.print_html(json.dumps(aviators, indent=2), title="Inventory status: Aviator sunglasses after return")
```

---

3. 整合：客户服务智能体

你已经构建了各个部分——模式、提示、代码生成器和执行器。现在让我们将它们连接成一个单一的辅助函数，它接收自然语言请求，生成“代码即规划”，安全地执行它，并显示结果（以及执行前后的表）。

### 这个智能体做什么

* 可选地重新播种 (reseed) 演示数据以进行干净的运行。
* 生成规划（`<execute_python>…</execute_python>` 中的 Python）。
* 在受控的命名空间（TinyDB + 辅助函数）中执行规划。
* 呈现简洁的 `answer_text` 并渲染执行前/后的快照。

```Plain
def customer_service_agent(
    question: str,
    *,
    db,
    inventory_tbl,
    transactions_tbl,
    model: str = "o4-mini",
    temperature: float = 1.0,
    reseed: bool = False,
) -> dict:"""
    End-to-end helper:
      1) (Optional) reseed inventory & transactions
      2) Generate plan-as-code from `question`
      3) Execute in a controlled namespace
      4) Render before/after snapshots and return artifacts
 
    Returns:
      {
        "full_content": <raw LLM response (may include <execute_python> tags)>,
        "exec": {
            "code": <extracted python>,
            "stdout": <plan logs>,
            "error": <traceback or None>,
            "answer": <answer_text/rows/json>,
            "inventory_after": [...],
            "transactions_after": [...]
        }
      }
    """# 0) Optional reseedif reseed:
        # Note: These utils functions likely need to modify the tables in-place# or return new ones. Assuming they modify the passed-in tables.
        inv_utils.seed_db(db=db, inventory_tbl=inventory_tbl, transactions_tbl=transactions_tbl, force_reseed=True)
 
    # 1) Show the question
    utils.print_html(question, title="User Question")
 
    # 2) Generate plan-as-code (FULL content)
    full_content = generate_llm_code(
        question,
        inventory_tbl=inventory_tbl,
        transactions_tbl=transactions_tbl,
        model=model,
        temperature=temperature,
    )
    utils.print_html(full_content, title="Plan with Code (Full Response)")
 
    # 3) Before snapshots
    inv_before = inventory_tbl.all()
    trx_before = transactions_tbl.all()
    utils.print_html(json.dumps(inv_before, indent=2), title="Inventory Table · Before")
    utils.print_html(json.dumps(trx_before, indent=2), title="Transactions Table · Before")
 
    # 4) Execute
    exec_res = execute_generated_code(
        full_content,
        db=db,
        inventory_tbl=inventory_tbl,
        transactions_tbl=transactions_tbl,
        user_request=question,
    )
 
    # 5) After snapshots + final answer
    inv_after = inventory_tbl.all()
    trx_after = transactions_tbl.all()
    utils.print_html(exec_res["answer"], title="Plan Execution · Extracted Answer")
    utils.print_html(json.dumps(inv_after, indent=2), title="Inventory Table · After")
    utils.print_html(json.dumps(trx_after, indent=2), title="Transactions Table · After")
 
    # 6) Return artifactsreturn {
        "full_content": full_content,
        "exec": {
            "code": exec_res["code"],
            "stdout": exec_res["stdout"],
            "error": exec_res["error"],
            "answer": exec_res["answer"],
            "inventory_after": inv_after,
            "transactions_after": trx_after,
        },
    }
```

*(译者注：上述代码块中的 **`customer_service_agent`** 函数实现已根据上下文进行了调整，以正确反映 **`reseed`** 逻辑。原始 **Markdown** 中的 **`inv_utils.create_inventory()`** 和 **`inv_utils.create_transactions()`** 可能无法按预期工作，因为 **`seed_db`** 似乎是返回表实例的函数。为了与 **`execute_generated_code`** 一致，假设表对象是可变的或被正确地重新播种。)*

---

4. 试一试（使用客户服务智能体）

使用 `customer_service_agent(...)` 辅助函数，实现从自然语言请求 → 代码即规划 → 安全执行 → 执行前/后快照的完整流程。

试试这些提示：

1. 只读 (Andrew 的例子):
2. “你们有 100 美元以下的圆形太阳镜库存吗？”
3. 可变操作 — 退货:
4. “退回 2 副飞行员太阳镜。”
5. 可变操作 — 购买:
6. “为客户 Alice 购买 3 副 Wayfarer 太阳镜。”
7. 可变操作 - 购买多件商品:
8. “我想买 3 副 classic 太阳镜和 1 副 aviator。”

**🔎 ****`reseed=True`**** 是做什么的？**

当你调用 `customer_service_agent(..., reseed=True)` 时，智能体在运行你的提示之前会**重新初始化**演示数据：

* 将 `inventory_tbl` **重置**为默认产品集。
* 将 `transactions_tbl` **重置**为单个期初余额条目。
* 确保**干净、可重现的**运行，以便结果不受先前测试的影响。

如果你想**保留**当前状态并从先前的操作继续，请设置 `reseed=False`。

```Plain
prompt = "I want to buy 3 pairs of classic sunglasses and 1 pair of aviator sunglasses."
 
out = customer_service_agent(
    prompt,
    db=db,
    inventory_tbl=inventory_tbl,
    transactions_tbl=transactions_tbl,
    model="o4-mini",
    temperature=1.0,
    reseed=True,   # set False to keep current state of the inventory and the transactions
)
```

---

9. 总结

* **你让代码成为了规划。** 遵循 Andrew 的“代码即行动”理念，你让模型编写了链接各个步骤（过滤 → 计算 → 更新）的 Python 代码，然后你只是运行了它。
* **你跳过了脆弱的工具“大杂烩”。** 你没有堆积小型工具或 JSON 规划，而是使用了 Python/TinyDB——给了模型一个它熟悉的、庞大的工具箱，用一个提示就能处理多种查询形态。
* **你保持了运行的安全和可见。** 你在受控的命名空间中执行，捕获了日志/错误，并审查了执行前/后的表——因此你始终知道改变了什么以及为什么改变。

🎉 **恭喜！**

你刚刚完成了实验并构建了一个**智能体**** (agentic)** 客户服务工作流。你让模型编写代码作为规划，安全地运行它，并使用简单的验证来保持更新的可靠性。当出现故障时，你呈现了清晰易懂的原因；当一切正常时，你通过执行前/后的快照准确地看到了发生了什么变化。

有了这种模式——**在代码中**规划，加上透明的执行——你就准备好设计自己的、感觉自动化、安全且易于扩展的工作流了。 🚀

5. ## **Multi-agentic workflows** —— 多代理工作流程

我们已经讨论了**如何构建单个代理**来为您完成任务。

0:04

而在**多代理或多主体工作流程 (multi-agent or multi-agentic ** **workflow** **)** 中，我们拥有**多个代理**组成的集合，它们**协作**为您完成工作。

0:09

当一些人第一次听说**多代理系统**时，他们会想：“为什么我需要多个代理？

0:12

它不就是我一遍又一遍地提示的**同一个 LLM** 吗？或者只是一台电脑。为什么我需要多个代理？”

0:18

我发现一个有用的类比是：即使我是在**一台电脑**上做事情，我们也会把一台电脑上的工作 **分解成多个进程或多个线程** 。

0:25

对于开发人员来说，即使电脑上只有一个 CPU，思考**如何将工作分解**成多个进程和多个计算机程序来运行， **这使得我作为开发人员更容易编写代码** 。

0:37

以类似的方式，如果您有一个**复杂的任务**要执行，有时，与其考虑**雇佣一个人**来为您完成，不如考虑**雇佣一个由几个人组成的团队**来为您完成任务的 **不同部分** 。

0:52

因此，在实践中，我发现对于许多代理系统开发人员来说，拥有这种**思维框架**很有帮助： **不问** “我可以雇佣哪一个人来做这件事？”，而是问“**雇佣三到四个拥有不同角色的人**来完成这个整体任务是否合理？”这为分解复杂的任务提供了另一种方式，将其分解成 **子任务** ，并**逐一**构建这些独立的子任务。

1:08

让我们看一些这种工作方式的例子。

1:33

以**创建营销资产**的任务为例，假设您想营销太阳镜。您能为此制作一本营销手册吗？

1:36

您可能需要团队中有一名**研究员**来研究太阳镜的趋势和竞争对手的产品。

1:43

您可能还需要一名**平面设计师**来渲染图表或美观的太阳镜图形。

1:49

然后，还需要一名**撰稿人**将研究结果和图形资产整合在一起，制作成一本精美的宣传册。

1:56

或者，要撰写一篇 **研究文章** ，您可能需要一名**研究员**进行在线研究，一名**统计学家**计算统计数据，一名 **首席撰稿人** ，以及一名**编辑**来完成一份精美的报告。

2:02

或者，要准备一起 **法律案件** ，真正的律师事务所通常会有 **助理律师** 、 **律师助理** ，可能还有一名 **调查员** 。

2:11

我们很自然地会因为**人类团队的工作方式**而想到，复杂的任务可以被分解成由**不同角色**的个体来完成的不同部分。

2:18

所以，这些都是复杂的任务已经自然地被 **分解成子任务** ，由**具有不同技能**的人来执行的例子。

2:31

以**创建营销资产**为例，深入看看研究员、平面设计师和撰稿人分别会做什么。

2:41

**研究员**的任务可能是**分析市场趋势**和 **研究竞争对手** 。

2:44

在设计研究代理时，要记住的一个问题是：研究员可能需要**哪些工具**才能完成这份关于市场趋势和竞争对手动态的研究报告。

2:55

因此，一个代理式研究员可能需要使用的自然工具是 **网页搜索** 。

3:07

因为作为一名被要求执行这些任务的人类研究员，可能需要**在线搜索**才能完成他们的报告。

3:14

或者对于 **平面设计师代理** ，他们可能被指派 **创建可视化图表和艺术作品** 。

3:20

那么，一个代理式软件平面设计师可能需要**哪些工具**呢？

3:26

他们可能需要**图像生成和操作 ** **API** 。

3:31

或者，类似于您在咖啡机示例中看到的，它可能需要**代码执行**来 **生成图表** 。

3:36

最后，**撰稿人**的任务是 **将研究成果转化为报告文本和营销文案** 。

3:44

在这种情况下，除了 LLM 已经能够做的**文本生成**之外，他们 **不需要任何其他工具** 。

3:49

在这个视频和下一个视频中，我将使用这些**紫色方框**来表示一个 **代理** 。

3:55

构建**单个代理**的方式是**提示 LLM 扮演**研究员、平面设计师或撰稿人的 **角色** ，具体取决于它是哪个代理的一部分。

4:00

例如，对于 **研究代理** ，您可以提示它：“您是一名 **研究代理** ，擅长分析市场趋势和竞争对手，进行在线研究来分析太阳镜产品的市场趋势，并总结竞争对手正在做什么。”

4:11

这就能让您构建一个 **研究员代理** 。

4:27

同样，通过提示 LLM 扮演**平面设计师**并配备适当的工具，以及扮演 **撰稿人** ，您就可以构建平面设计师和撰稿人代理。

4:30

构建了这三个代理后，让它们**协同工作**以生成最终报告的一种方式是使用**一个简单的线性工作流程**或这里的 **线性计划** 。

4:43

因此，如果您想为太阳镜创建 **夏季营销活动** ，您可以将该提示交给 **研究员代理** 。

4:47

研究员代理随后会撰写一份报告，说明当前的太阳镜趋势和竞争产品。

5:00

这份研究报告随后可以 **反馈给平面设计师** ，平面设计师查看研究发现的数据，并创建一些 **数据可视化图表和艺术作品选项** 。

5:08

所有这些资产随后可以 **传递给撰稿人** ，撰稿人将研究结果和图形输出整合起来，撰写 **最终的营销手册** 。

5:17

在这种情况下，构建**多代理工作流程的优势**在于，在设计研究员、平面设计师或撰稿人时，您可以 **一次专注于一件事情** 。

5:27

因此，我可以花时间构建我能做到的 **最好的平面设计师代理** ，而我的协作者可能正在构建**研究员代理**和 **撰稿人代理** 。

5:36

最后，我们将它们 **串联起来** ，形成这个多代理系统。

5:45

在某些情况下，我看到开发人员也开始 **复用一些代理** 。

5:50

因此，在为营销手册构建了一个平面设计师之后，我可能会考虑是否可以构建一个 **更通用的平面设计师** ，它可以帮助我撰写营销手册、社交媒体帖子，以及帮助我设计在线网页插图。

5:56

所以，通过思考 **你会雇佣哪些代理来完成任务** （这有时会对应于你会雇佣哪些**类型的人类员工**来完成任务），

6:10

您可以设计出像这样的工作流程，甚至可能构建出您可以选择**在其他应用中复用**的代理。

6:22

现在，您在这里看到的是一个 **线性计划** ：研究员代理完成工作，然后是平面设计师，然后是撰稿人。

6:30

对于代理，作为 **线性计划的替代方案** ，您还可以让 **代理以更复杂的方式相互交互** 。

6:38

让我用一个**使用多个代理进行规划**的例子来说明。

6:47

之前，您看到了我们如何给 LLM 一套可以**调用**来执行不同任务的 **工具** 。

6:51

在我接下来想展示的内容中，我们将 **转而给 LLM 选项去调用不同的代理** ，要求这些不同的代理帮助完成不同的任务。

6:57

具体来说，您可以编写一个提示，比如：“您是一名 **营销经理** ，拥有以下**代理团队**可供合作”，然后 **描述这些代理** 。

7:07

这与我们使用工具进行规划的方式非常相似，只是 **工具** （绿色方框）被替换成了 LLM 可以调用的 **代理** （紫色方框）。

7:14

您也可以要求它**返回一个逐步的计划**来执行用户的请求。

7:25

在这种情况下，LLM 可能会 **要求研究员研究当前的太阳镜趋势** ，然后 **汇报** 。

7:28

然后，它会 **要求平面设计师创建图像** ，然后 **汇报** ；再要求 **撰稿人创建报告** ；然后 LLM 可能会选择 **最后一次审查或反思并改进报告** 。

7:34

在执行这个计划时，您会取出 **第一步研究员的文本** ，执行研究，然后将其 **传递给平面设计师** ， **传递给撰稿人** ，然后可能进行 **最后一次反思步骤** ，然后就完成了。

7:45

看待这个工作流程的一个有趣视角是：您拥有顶部的这三个代理，但**左侧的这个 LLM** 实际上就像 **第四个代理** ，它是一个 **营销经理** ，**负责协调**营销团队， **设定方向** ，然后将任务 **委托给研究员、平面设计师和撰稿人代理** 。

7:59

因此，这实际上成为了一个 **四个代理的集合** ，由一个营销经理代理**协调**研究员、平面设计师和撰稿人的工作。

8:18

在这个视频中，您看到了 **两种通信模式** 。

8:26

一种是 **线性模式** ，您的代理**依次采取行动**直到结束。

8:30

第二种是**营销经理协调**其他几个代理的活动。

8:36

事实证明，构建多代理系统时，您最终可能需要做出的**关键设计决策之一**是：**您的不同代理之间的通信模式是什么？**

8:41

这是一个艰难的研究领域，并且正在出现多种模式，但在下一个视频中，我想向您展示一些 **让您的代理相互协作的最常见通信模式** 。

8:51

让我们在下一个视频中看看。

6. ## **【实验】Ungraded Lab: ****Market Research**** Team** —— 非评分实验：市场调研团队

### M5 智能体 AI - 市场研究团队

1. ### 介绍

#### 1.1. 实验概述

在本实验中，你将扮演一家时尚品牌 **AI**** 技术主管**的角色，为夏季太阳镜营销活动做准备。你的任务是设计一个 **全自动的创意流程** ，以模拟真实的业务场景。你将不再手动处理每个环节，而是引导一个系统扫描在线资源以获取新兴时尚趋势，将这些趋势与内部目录中的太阳镜相匹配，设计一个营销活动视觉，生成一句简短的营销引语，最后将所有内容打包成一份 **可供高管审阅的报告** 。

目标是体验如何将多个智能体、工具和模型**编排 (orchestrated)** 成一个单一、连贯的工作流。完成本实验后，你将构建一个流程，它感觉不再像一个由孤立步骤组成的脚本，而更像一个小团队协同工作来解决一个创意挑战。

#### 1.2. 🎯 学习成果

通过完成本实验，你将了解如何超越与模型的单轮交互，转而设计**多****智能体** **流程 (multi-agent pipelines)** ，以协调规划、研究和创意生成。你将学会如何将智能体的推理**锚定在 (ground)** 外部工具上，使输出不仅富有想象力，而且有真实数据支持。你还将实验“反思”(reflection) 和“封装”(packaging) 步骤，以实施质量控制，并为高管受众准备结果。

简而言之，本实验旨在学习如何将**大型语言模型的想象力**与**结构化****工作流****的规范性**结合起来，为你提供一个构建兼具创造力和可靠性的自主系统的实用模式。

---

2. ### 设置：导入库和加载环境

与之前的实验一样，你现在导入所需的库，加载环境变量，并设置辅助工具。

```Plain
# =========================# Imports# =========================# --- Standard library ---import base64
import json
import os
import re
from datetime import datetime
from io import BytesIO
 
# --- Third-party ---import requests
import openai
from PIL import Image
from dotenv import load_dotenv
from IPython.display import Markdown, display
import aisuite
 
# --- Local / project ---import tools
import utils
 
 
# =========================# Environment & Client# =========================
load_dotenv()
client = aisuite.Client()
```

---

3. ### 可用工具

只有当模型被赋予其基础推理之外的**明确能力**时，智能体流程才会变得有效。预先声明这些工具可以使智能体的**动作空间 (action space)** 清晰明确，确保提示能够自然地引导工具选择，并通过定义良好的接口保持编排和测试的透明度。

你将组建一个**市场研究** **团队** ，这是一组协同工作的专业智能体，旨在设计一个夏季太阳镜营销活动。为了赋予他们能力，我们首先定义将他们的推理锚定于真实数据的工具。

第一个工具是 `tools.tavily_search_tool`，它执行实时网络搜索，以发现当前时尚趋势的证据。现在通过运行一个关于**“太阳镜时尚趋势”**的简单查询来试试它：

```Plain
tools.tavily_search_tool('trends in sunglasses fashion')
```

第二个工具是 `tools.product_catalog_tool`，它返回内部太阳镜目录。每个条目都包含产品名称、ID、描述、库存数量和价格等详细信息。这些结构化数据将使智能体能够将在线时尚趋势与实际的库存商品联系起来：

```Plain
tools.product_catalog_tool()
```

有了这些工具，你就定义了一个清晰的动作空间和可靠的数据源。在下一节中，你将构建使用这些工具的智能体，将原始的时尚信号转化为结构化的洞察和营销活动素材。

---

4. ### 智能体定义 — 组建你的团队

现在你已经定义了工具，是时候让它们工作了。在此阶段，你将组建一个**市场研究** **团队** ，这是一组你用自然指令指导的专业智能体。

每个智能体都依赖于你之前介绍的工具，它们共同将原始趋势数据转化为精美的营销活动报告。我们将逐一定义它们，介绍它们各自的角色，并展示实现每个智能体的代码。

#### 市场研究智能体

通过**市场研究****智能体** ** (** **Market Research** ** Agent)** ，你迈出了构建营销活动的第一步。你要求它使用 `tavily_search_tool` 扫描网络，发现当下太阳镜的流行趋势。然后，你指示它使用 `product_catalog_tool` 将这些信号与你的内部目录进行交叉核对，这样你就知道你的哪些产品符合当下的潮流。

该智能体返回一份简洁的简报：它发现的顶级时尚洞察、与之匹配的产品，以及关于为什么这些选择适合你的夏季推广的简短解释。这为你提供了一个清晰的、数据驱动的基础，以塑造营销活动的其余部分。

你现在可以运行以下单元格，在代码中定义**市场研究** **智能体** 。

```Plain
def market_research_agent(return_messages: bool = False):
 
    utils.log_agent_title_html("Market Research Agent", "🕵️♂️")
 
    prompt_ = f"""
你是一名时尚市场研究智能体，任务是为夏季太阳镜营销活动准备一份趋势分析报告。
 
你的目标：
1. 使用网络搜索探索与太阳镜相关的当前时尚趋势。
2. 审查内部产品目录，找出与这些趋势相符的商品。
3. 从目录中推荐一个或多个最符合新兴趋势的产品。
4. 如果需要，今天是 {datetime.now().strftime("%Y-%m-%d")}。
 
你可以调用以下工具：
- tavily_search_tool: 发现外部网络趋势。
- product_catalog_tool: 检查内部太阳镜目录。
 
分析完成后，请总结：
- 你发现的 2-3 个主要趋势。
- 目录中符合这些趋势的产品。
- 它们适合夏季营销活动的理由。
"""
    messages = [{"role": "user", "content": prompt_}]
    tools_ = tools.get_available_tools()
 
    while True:
        response = client.chat.completions.create(
            model="openai:o4-mini",
            messages=messages,
            tools=tools_,
            tool_choice="auto"
        )
 
        msg = response.choices[0].message
 
        if msg.content:
            utils.log_final_summary_html(msg.content)
            return (msg.content, messages) if return_messages else msg.content
 
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                utils.log_tool_call_html(tool_call.function.name, tool_call.function.arguments)
                result = tools.handle_tool_call(tool_call)
                utils.log_tool_result_html(result)
 
                messages.append(msg)
                messages.append(tools.create_tool_response_message(tool_call, result))
        else:
            utils.log_unexpected_html()
            return ("[⚠️ Unexpected: No tool_calls or content returned]", messages) if return_messages else "[⚠️ Unexpected: No tool_calls or content returned]"
```

让我们尝试从**市场研究****智能体**那里获取一些关于我们夏季太阳镜营销活动的建议。

```Plain
market_research_result = market_research_agent()
```

接下来，你将使用平面设计师智能体将这份简报转化为视觉概念。

#### 平面设计师智能体

通过**平面设计师****智能体** ** (Graphic Designer Agent)** ，你从分析转向创意。

你获取市场研究智能体的简报，并要求这个智能体将其转化为一个 **视觉概念** 。

由于 `aisuite` **尚不支持**直接生成图像（如 DALL·E），你将分两个阶段指导该过程：

1. 首先，智能体使用 `aisuite` 和 OpenAI 文本模型 (o4-mini) 来打造一个生动的**提示词 (prompt)** 和一个简短、吸引人的 **图注 (caption)** 。
2. 然后，该提示词被发送到 OpenAI 的 `dall-e-3` API，以生成**营销活动图像**本身。

结果为你提供了推进所需的一切：生成的图像（保存在本地以供重用）、生成它的确切提示词（有助于迭代）以及用于营销活动故事讲述的精美图注。

**注意：** 目前，`aisuite` **不支持**直接生成图像。这就是为什么你将其基于文本的输出（提示词 + 图注）与 OpenAI 的 `dall-e-3` 结合起来，以生成最终的营销活动视觉。

你现在可以运行以下单元格，在代码中定义**平面设计师** **智能体** 。

```Plain
def graphic_designer_agent(trend_insights: str, caption_style: str = "short punchy", size: str = "1024x1024") -> dict:"""
    使用 aisuite 生成营销提示词/图注，并（直接）使用 OpenAI 生成图像。
 
    Args:
        trend_insights (str): 来自研究智能体的趋势摘要。
        caption_style (str): 可选的图注风格提示。
        size (str): 图像分辨率 (例如, '1024x1024')。
 
    Returns:
        dict: 包含 image_url、prompt 和 caption 的字典。
    """
 
    utils.log_agent_title_html("Graphic Designer Agent", "🎨")
 
    # 步骤 1: 使用 aisuite 生成提示词和图注
    system_message = (
        "你是一名视觉营销助手。根据输入的趋势洞察，""为 AI 图像生成模型编写一个富有创意和视觉冲击力的提示词，并附上一句简短的图注。"
    )
 
    user_prompt = f"""
趋势洞察：
{trend_insights}
 
请输出：
1. 一个生动的、描述性的提示词，用于指导图像生成。
2. 一句风格为 {caption_style} 的营销图注。
 
请按此格式回应：
{{"prompt": "...", "caption": "..."}}
"""
 
    chat_response = client.chat.completions.create(
        model="openai:o4-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]
    )
 
    content = chat_response.choices[0].message.content.strip()
    match = re.search(r'\{.*\}', content, re.DOTALL)
    parsed = json.loads(match.group(0)) if match else {"error": "No JSON returned", "raw": content}
 
    prompt = parsed["prompt"]
    caption = parsed["caption"]
 
    # 步骤 2: 直接使用 openai-python 生成图像
    openai_client = openai.OpenAI()
 
    image_response = openai_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
        response_format="url"
    )
 
    image_url = image_response.data[0].url
 
    # 将图像保存到本地
    img_bytes = requests.get(image_url).content
    img = Image.open(BytesIO(img_bytes))
 
    filename = os.path.basename(image_url.split("?")[0])
    image_path = filename
    img.save(image_path)
 
 
    # 使用本地图像记录摘要
    utils.log_final_summary_html(f"""
        <h3>生成的图像和图注</h3>
 
        <p><strong>图像路径：</strong> <code>{image_path}</code></p>
 
        <p><strong>生成的图像：</strong></p>
        <img src="{image_path}" alt="Generated Image" style="max-width: 100%; height: auto; border: 1px solid #ccc; border-radius: 8px; margin-top: 10px; margin-bottom: 10px;">
 
        <p><strong>提示词：</strong> {prompt}</p>
    """)
 
 
    return {
        "image_url": image_url,
        "prompt": prompt,
        "caption": caption,
        "image_path": image_path  
    }
 
 
现在，让我们运行 `graphic_designer_agent`，使用**市场研究智能体**提供的趋势洞察来生成营销活动图像。
```

```Plain
graphic_designer_agent_result = graphic_designer_agent(
    trend_insights=market_research_result,
)
```

有了视觉素材，你将使用文案撰写智能体来打造营销活动的声音。

#### 文案撰写智能体

一旦**市场研究****智能体**和**平面设计师智能体**完成了他们的工作，你现在转向 **文案撰写智能体 (Copywriter Agent)** 。同时掌握了营销活动图像和趋势摘要，你要求这个智能体来打造你的营销活动“代言之声”。

它将视觉和分析一起作为 **多模态输入 (multimodal input)** ，精心制作一句简短、优雅的营销引语 (quote)，以捕捉信息的精髓。除了引语，它还为你提供了一个清晰的 **理由阐释 (justification)** ——为什么这个短语适合这张图片，以及它如何与趋势相联系。

这样，你不仅得到了一句吸引人的标语，还得到了它背后的推理过程，使其在利益相关者面前更容易得到辩护和完善。

```Plain
def copywriter_agent(image_path: str, trend_summary: str, model: str = "openai:o4-mini") -> dict:"""
    使用 aisuite (仅限 OpenAI) 发送图像和趋势摘要，并返回一句营销活动引语。
 
    Args:
        image_path (str): 待分析图像的 URL。
        trend_summary (str): 来自研究智能体的文本。
        model (str): OpenAI 模型 (例如, openai:o4-mini, openai:gpt-4o)
 
    Returns:
        dict: {
            "quote": "...",
            "justification": "...",
            "image_path": "..."
        }
    """
 
    utils.log_agent_title_html("Copywriter Agent", "✍️")
 
    # 步骤 1: 加载本地图像并编码为 base64with open(image_path, "rb") as f:
        img_bytes = f.read()
 
    b64_img = base64.b64encode(img_bytes).decode("utf-8")
 
    # 步骤 2: 构建兼容 OpenAI 的多模态消息
    messages = [
        {
            "role": "system",
            "content": "你是一名文案撰写人，根据图像和营销趋势摘要创作优雅的营销活动引语。"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{b64_img}",
                        "detail": "auto"
                    }
                },
                {
                    "type": "text",
                    "text": f"""
这是一张视觉营销图像和一份趋势分析：
 
趋势摘要：
\"\"\"{trend_summary}\"\"\"
 
请返回一个 JSON 对象，如下所示：
{{
  "quote": "一句简短、优雅的营销短语（最多 12 个词）",
  "justification": "为什么这句引语与图像和趋势相匹配"
}}"""
                }
            ]
        }
    ]
 
    # 步骤 3: 通过 aisuite 发送请求
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
 
    # 步骤 4: 解析 JSON 响应
    content = response.choices[0].message.content.strip()
 
    utils.log_final_summary_html(content)
 
    try:
        match = re.search(r'\{.*\}', content, re.DOTALL)
        parsed = json.loads(match.group(0)) if match else {"error": "No valid JSON returned"}
    except Exception as e:
        parsed = {"error": f"Failed to parse: {e}", "raw": content}
 
 
    parsed["image_path"] = image_path
    return parsed
```

接下来，让我们调用**文案撰写** **智能体** ，根据早先生成的营销图像和趋势洞察来生成一句简短的营销活动引语。

```Plain
copywriter_agent_result = copywriter_agent(
    image_path=graphic_designer_agent_result["image_path"],
    trend_summary=market_research_result,
)
```

有了引语和理由阐释，你将使用封装智能体将所有内容打包成一份可供高管审阅的产出物。

#### 封装智能体

最后，你引入**封装****智能体**** (Packaging Agent)** 来将所有内容整合在一起。在**市场研究** **智能体** 、**平面设计师智能体**和**文案撰写智能体**各自贡献了他们的部分之后，这个智能体将整个故事汇编成一个精美的产出物。

你要求它获取趋势摘要、营销活动视觉、精心制作的引语和理由阐释，并将它们组装成一份**可供高管审阅的 ****Markdown** ** 报告** 。在此过程中，它会为了清晰度和语气**重写**趋势洞察，确保引语与图像恰当搭配，并组织所有内容，使最终文档看起来专业且有说服力。

通过这一步，你最终得到了一个完整的营销活动包——易于分享、视觉上吸引人，并准备好供 CEO 级别的审阅。

```Plain
def packaging_agent(trend_summary: str, image_url: str, quote: str, justification: str, output_path: str = "campaign_summary.md") -> str:"""
    将营销活动素材打包成一份格式精美的 Markdown 报告，以供高管审阅。
 
    Args:
        trend_summary (str): 市场趋势摘要。
        image_url (str): 营销活动图像的 URL。
        quote (str): 要叠加的营销引语。
        justification (str): 对引语的解释。
        output_path (str): 保存 Markdown 报告的路径。
 
    Returns:
        str: 保存的 Markdown 文件的路径。
    """
 
    utils.log_agent_title_html("Packaging Agent", "📦")
 
    # 我们在 <img> 的 src 中使用此路径
    styled_image_html = f"""
![打开生成的文件以查看]({image_url})
    """
 
    beautified_summary = client.chat.completions.create(
        model="openai:o4-mini",
        messages=[
            {"role": "system", "content": "你是一名营销传播专家，为高管撰写优雅的营销活动摘要。"},
            {"role": "user", "content": f"""
请重写以下趋势摘要，使其对 CEO 受众而言清晰、专业且具吸引力：
 
\"\"\"{trend_summary.strip()}\"\"\"
"""}
        ]
    ).choices[0].message.content.strip()
 
    utils.log_tool_result_html(beautified_summary)
 
    # 将所有部分组合成 Markdown
    markdown_content = f"""# 🕶️ 夏季太阳镜营销活动 – 高管摘要
 
## 📊 优化后的趋势洞察
{beautified_summary}
 
## 🎯 营销活动视觉
{styled_image_html}
 
## ✍️ 营销活动引语
{quote.strip()}
 
## ✅ 为什么这很有效
{justification.strip()}
 
---
 
*报告生成于 {datetime.now().strftime('%Y-%m-%d')}*
"""with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
 
    return output_path
 
 
准备好你的趋势摘要、营销活动图像和引语后，你现在将所有内容交给**封装智能体**。它的工作是将这些部分组合成一份精美的、可供高管审阅的报告。运行下一个单元格来生成它。
```

```Plain
packaging_agent_result = packaging_agent(
    trend_summary=market_research_result,
    image_url=graphic_designer_agent_result["image_path"],
    quote=copywriter_agent_result["quote"],
    justification=copywriter_agent_result["justification"],
    output_path=f"campaign_summary_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
)
```

最终结果将是一份格式精美的营销活动报告，你可以直接在 notebook 中查看。它将包括：

* 一份 **优化后的趋势摘要** ，你将看到它被重写以使高管更清晰地理解
* 一个 **视觉风格化的图像** ，用 HTML 叠加你的营销活动引语
* 一个 **清晰的理由阐释** ，让你明白为什么视觉和信息与当前趋势一致
* 一个 **时间戳** ，显示报告的确切生成时间

你可以用以下方式查看它：

```Plain
# 加载并渲染 Markdown 内容with open(packaging_agent_result, "r", encoding="utf-8") as f:
    md_content = f.read()
 
display(Markdown(md_content))
```

最后，你将把整个工作流包装成一个单一的可调用函数，以便一步运行完整的流程。

---

#### 完整的营销活动流程 – `run_sunglasses_campaign_pipeline`

在此步骤中，你将定义一个单一函数 `run_sunglasses_campaign_pipeline`，它将所有部分整合成一个为你的夏季太阳镜营销活动设计的无缝工作流。

该函数将：

1. 运行市场研究，扫描时尚趋势并将其与你的目录匹配。
2. 生成视觉风格化的图像和图注。
3. 创建一句简短、优雅的营销活动引语，并附上理由阐释。
4. 将所有内容打包成一份为高管审阅量身定制的精美 Markdown 报告。

通过定义此函数，你可以轻松地 **通过一次调用运行整个流程** ，同时仍能跟踪中间结果并查看最终报告。

```Plain
def run_sunglasses_campaign_pipeline(output_path: str = "campaign_summary.md") -> dict:"""
    运行完整的夏季太阳镜营销活动流程：
    1. 市场研究（搜索趋势 + 匹配产品）
    2. 生成视觉 + 图注
    3. 根据图像 + 趋势生成引语
    4. 创建高管 Markdown 报告
 
    Returns:
        dict: 包含所有中间结果 + 最终报告路径的字典
    """# 1. 运行市场研究智能体
    trend_summary = market_research_agent()
    print("✅ 市场研究完成")
 
    # 2. 生成图像 + 图注
    visual_result = graphic_designer_agent(trend_insights=trend_summary)
    image_path = visual_result["image_path"]
    print("🖼️ 图像已生成")
 
    # 3. 根据图像 + 趋势生成引语
    quote_result = copywriter_agent(image_path=image_path, trend_summary=trend_summary)
    quote = quote_result.get("quote", "")
    justification = quote_result.get("justification", "")
    print("💬 引语已创建")
 
    # 4. 生成 Markdown 报告
    md_path = packaging_agent(
        trend_summary=trend_summary,
        image_url=image_path,  
        quote=quote,
        justification=justification,
        output_path=f"campaign_summary_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
    )
 
    print(f"📦 报告已生成: {md_path}")
 
    return {
        "trend_summary": trend_summary,
        "visual": visual_result,
        "quote": quote_result,
        "markdown_path": md_path
    }
 
 
你现在可以通过一次调用运行该流程来创建一份完整的营销活动报告。只需执行下一个单元格：
```

```Plain
results = run_sunglasses_campaign_pipeline()
```

#### 结果

运行以下单元格以查看完整营销活动流程生成的输出。

```Plain
with open(results["markdown_path"], "r", encoding="utf-8") as f:
    md_content = f.read()
display(Markdown(md_content))
```

---

5. ### 关键总结

通过完成本实验，你已经了解了如何：

* 使用**多****智能体****LLM**** 流程**来端到端地自动化创意工作流。
* 结合 **推理、工具调用和外部数据** ，将你的输出锚定于现实。
* 应用 **多模态模型** （如 `gpt-4o`）处理 **文本和图像** ，以完成诸如生成营销活动引语之类的任务。
* 使用工具（`tavily_search_tool`, `product_catalog_tool`）扩展模型的能力，使你的输出不仅富有想象力，而且实用。
* 通过结构化日志和 HTML 风格的块，保持执行过程 **透明且可调试** 。
* 以 Markdown 格式交付一份精美的、 **可供高管审阅的报告** ，将洞察、视觉和理由阐释融合成一个单一的产出物。

🎉 **恭喜！** 🎉

现在你已经成功构建并运行了一个**多****智能体** **流程** ：你研究了趋势，生成了视觉素材，精心制作了营销活动引语，并将所有内容打包成一份 **可供高管审阅的报告** 。

这个工作流向你展示了如何将 **LLM 的创造力**与**结构化编排的规范性**结合起来，为你提供一个可重复的模式，你可以将其应用于许多现实世界的场景。 🌟

7. ## **Communication patterns for multi-agent systems** —— 多代理系统的通信模式

当您有一个**团队**协同工作时，他们之间的**通信模式**可能会 **非常复杂** 。事实上，设计**组织****结构图**本身就是一件相当复杂的事情，需要弄清楚人们**沟通协作的最佳方式**是什么。

0:06

事实证明，设计**多代理系统的通信模式**也 **相当复杂** 。但让我向您展示一些我今天看到的被不同团队使用的 **最常见的设计模式** 。

0:16

在采用**线性计划**的营销团队中，先是研究员工作，然后是平面设计师，接着是撰稿人，其 **通信模式是线性的** 。

0:26

研究员会与平面设计师沟通，研究员和平面设计师都可能会将 **输出传递给撰稿人** 。因此，这是一种 **非常线性的通信模式** 。这是我今天看到被使用的 **两种最常见的通信计划之一** 。

0:40

第二种最常见的通信计划类似于您在这个使用多代理进行规划的例子中看到的，其中有一个**经理**与许多**团队成员**进行沟通并 **协调他们的工作** 。

0:46

在这个例子中，营销经理决定**调用研究员**进行一些工作。如果您将营销经理视为 **接收报告** ，然后将其 **发送给平面设计师** ，接收报告，然后 **发送给撰稿人** ，那么这将是一种 **层级式通信模式 (hierarchical communication pattern)** 。

1:05

如果您实际实现层级式通信模式，让 **研究员将报告传回给营销经理** ，而不是让研究员直接将结果传递给平面设计师和撰稿人，可能会更简单。

1:20

但这种**层级结构**也是一种规划通信模式的**相当常见**方式，即您有一个**经理**来 **协调许多其他代理的工作** 。

1:34

为了与您分享一些**更高级**且 **使用频率较低** ，但在实践中有时也会使用的通信模式：

1:45

一种是 **更深的层级结构 (deeper hierarchy)** 。与之前一样，营销经理向研究员、平面设计师、撰稿人发送任务，但**研究员本身**可能又调用 **另外两个代理** ，例如**网络研究员**和 **事实核查员** 。

1:50

平面设计师可能只是独自工作，而撰稿人可能有**初步文风撰稿人**和 **引用核查员** 。因此，这将是一种 **层级式的代理组织** ，其中一些代理 **本身可能会调用其他子代理** 。

2:07

我在一些应用中也看到了这种用法，但这比单层层级结构 **复杂得多** ，所以今天使用频率较低。

2:19

最后一种模式 **执行起来相当具有挑战性** ，但我看到一些实验性项目在使用，那就是 **全互联通信模式 (all-to-all communication pattern)** 。

2:25

在这种模式下，**任何人**都 **被允许随时与其他人交谈** 。

2:31

您实现此模式的方式是：您 **提示所有四个代理** （在这个例子中），告诉它们 **还有其他三个代理可以决定调用** 。当您的一个代理决定向另一个代理发送消息时，该消息会被**添加到接收代理的联系人**中。

2:44

然后，接收代理可以思考一会儿，并决定**何时回复**第一个代理。因此，它们可以在一个群体中**协作和相互交谈**一段时间，直到（例如）它们中的**每一个**都声明**已完成**任务，然后开始停止交谈。也许当所有人都认为任务完成时，或者当撰稿人得出结论说报告足够好时，就生成最终输出。

3:07

在实践中，我发现 **全互联通信模式的结果有点难以预测** 。

3:13

因此，有些应用不需要高度控制。您可以运行它，看看您得到了什么。如果营销手册不够好，那可能没关系。您只需再运行一次，看看是否得到了不同的结果。

3:22

但我认为对于那些**愿意容忍一些混乱和不可预测性**的应用，我确实看到一些开发人员在使用这种通信模式。

3:37

我希望这能传达多代理系统的 **一些丰富性** 。今天，也有**相当多的软件框架**支持轻松构建多代理系统。它们也使得实现其中一些通信模式 **相对容易** 。因此，如果您使用自己的多代理系统，您可能会发现其中一些框架对于探索这些不同的通信模式很有帮助。

3:44

现在，这也将我们带到了 **本单元和本课程的最后一个视频** 。让我们继续观看最后一个视频进行总结。

1. ## Module 5 quiz** —— 模块5测验
2. ## M5 Graded Assignment - Agentic Workflows** —— 模块5评分作业：智能代理工作流程
3.  ## **Conclusion** —— 总结

欢迎来到本课程的 **最后一个视频** 。感觉我们一起经历了许多，只有你和我，我们共同学习了**代理式 ****AI** 中的许多主题。让我们回顾一下。

0:04

在**第一个单元**中，我们讨论了**代理式 ****AI** 可以构建的、**以前不可能实现**的应用。

0:10

然后我们开始研究 **关键设计模式** ，包括 **反思 (reflection) 设计模式** （这是一种简单的、有时能给您的应用带来良好性能提升的方法），以及 **工具使用 (tool use) 或函数调用 (function calling)** （它扩展了您的 LLM 应用的能力，**代码执行**是其中一个重要的例子）。

0:22

接着，我们花费大量时间讨论了**评估 (evaluations)** 和 **错误分析 (error analysis)** ，以及如何推动一个 **严谨的流程** ，将**构建**与**分析**结合起来，从而高效地不断提高您的代理式 AI 系统的性能。

0:38

这**第四个单元**中的一些材料，我希望您在**长期构建代理式 ****AI**** 系统**的过程中会觉得 **非常有用** 。

0:50

在本单元中，我们讨论了**规划 (planning)** 和 **多代理系统 (multi-agent systems)** ，它们可以帮助您构建 **更强大** ，尽管有时 **更难控制** 、**更难事先预测**的系统。

1:01

因此，凭借您从本课程学到的技能，我认为您现在知道如何构建许多**酷炫、令人兴奋的代理式 ****AI** ** 应用** 。

1:13

当我的团队，或者我看到其他团队在进行**面试招聘**时，我发现面试通常试图评估候选人是否具备 **您正在本课程中学习的这些技能** 。因此，我希望本课程也能为您开启 **新的职业机会** ，并让您能做更多事情。

1:19

无论您是为了乐趣还是在专业的实践环境中做这些事情，我认为您都会喜欢这 **套新的构建能力** 。

1:36

最后，我想再次**感谢**您与我共度的所有时间，我希望您能**负责任地**运用这些技能，然后去 **构建酷炫的东西** 。

# 课程内容总结

1. ## **Planning workflows** —— 工作流程规划

### 规划 (Planning) 设计模式与高度自主代理

这段演讲介绍了 **规划 (Planning) 设计模式** ，这是一种构建**高度自主代理 (Highly Autonomous Agents)** 的方法，使其能够**自行决定**执行复杂任务所需的工具调用序列，而无需事先硬编码。

1. 核心概念：规划模式 (The Planning Design Pattern)

* **目标：** 构建能够回答广泛、复杂查询的代理，在运行时**灵活地**决定采取哪些行动。
* **方法：**
  * **提供工具集：** 给 LLM 提供一套功能工具（例如：检查库存、获取价格、处理退货等）。
  * **LLM 编写计划：** 向 LLM 提示，要求它根据用户请求 **返回一个逐步的执行计划** ，说明应按什么顺序调用哪些工具。
  * **逐步执行：** 按照计划，将**每一步的****指令**和**上一步的输出/上下文**依次喂给 LLM，让它调用相应的工具并执行。
  * **最终输出：** 将所有步骤的结果反馈给 LLM，生成最终的用户答案。

2. 案例分析

| 案例       | 复杂请求                                          | LLM 生成的计划（简化）                                                                  | 关键优势                                               |
| ---------- | ------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| 太阳镜客服 | “有没有低于 100 美元的圆形太阳镜？”             | 1.获取物品描述（找圆形）。2. 检查库存（看是否有货）。3. 获取物品价格（筛选低于 $100）。 | 代理无需硬编码就能处理涉及多重约束和多步骤逻辑的查询。 |
| 邮件助理   | “回复 Bob 的邮件说我会参加晚餐，然后归档邮件。” | 1.搜索邮件（找到 Bob 的邮件）。2. 生成并发送邮件（确认出席）。3. 移动邮件（归档）。     | 代理能将抽象请求转化为涉及不同工具的具体操作序列。     |
| 编码系统   | 复杂的软件编写请求。                              | 生成一个构建清单，列出要构建的各个组件，然后逐一执行。                                  | 在高度代理化的场景中表现良好。                         |

3. 规划模式的价值与挑战

* **价值：** 极大地扩展了代理能执行的 **任务范围** 。开发者**无需事先硬编码**工具调用的确切序列，提高了系统的灵活性和自主性。
* **挑战：**
  * **控制难度：** 在运行时，开发者**无法预知** LLM 会生成什么样的计划，使得系统有时难以控制。
  * **应用现状：** 目前在**高度代理化的编码系统**中应用非常成功，但在其他领域的普及度仍在增长中， **仍具有一定的实验性** 。

2. ## **Creating and executing ****LLM**** plans** —— 创建并执行大语言模型计划

### 规划设计模式的实施细节——结构化输出

这段演讲深入探讨了**规划 (Planning) 设计模式**在实际实施中的关键技术，即如何利用**结构化输出**来保证 LLM 生成的计划能够被下游代码可靠地执行。

1. 结构化输出的需求与优势

* **问题：** 上一讲中的简单文本描述计划（如“先做什么，再做什么”） **不够清晰和明确** ，难以被下游代码稳定地解析和执行。
* **解决方案：** 要求 LLM 以 **结构化格式** （如 JSON 或 XML）输出计划。
* **优势：**
  * **清晰明确 (Clear and Unambiguous)：** 结构化格式能够清楚地界定计划的步骤、所需工具及其参数。
  * **下游代码可靠性：** 允许下游代码**更可靠地解析 (parse)** 计划的每个步骤，从而系统性地、一步一步地执行。

2. 推荐的结构化格式

| 格式     | 推荐度 | 特点                                                                                                   |
| -------- | ------ | ------------------------------------------------------------------------------------------------------ |
| JSON     | 高     | 流行的选择。LLM 非常擅长生成 JSON 输出。通过键值对清晰地定义步骤描述、要使用的工具和传递给工具的参数。 |
| XML      | 高     | 另一个良好的选择。使用 XML 标签来清晰指定计划的步骤和编号。                                            |
| Markdown | 低     | 解析起来可能稍微模糊。                                                                                 |
| 纯文本   | 最低   | 最不可靠的选项。                                                                                       |

3. JSON 格式示例（系统提示与输出）

* **系统提示要求：** 开发者向 LLM 指示：“您有权访问以下工具”，并要求它**“以 JSON 格式创建一个一步一步的计划”**，同时详细描述所需的 JSON 结构。
* **JSON**** 输出结构：** LLM 返回一个 JSON 列表，列表中的每个对象代表一个步骤，包含清晰的键值：
  * `description` (步骤描述)
  * `tool` (要调用的工具名称)
  * `arguments` (传递给工具的参数)

4. 下一步：用代码表达计划

演讲者引出了一个更巧妙的规划思路：让 LLM  **编写代码** ，并用 **代码来表达计划** 。这将是下一个视频讨论的重点。

3. ## **Planning with code execution** —— 结合代码执行的规划

### 规划设计模式的进阶——使用代码作为行动（Code as Action）

这段演讲介绍了**使用代码执行进行规划 (Planning with Code Execution)** 这一强大的设计模式，并将其与结构化数据规划进行了对比，说明了它在处理复杂数据任务中的显著优势。

1. 核心概念：代码作为行动 (Code as Action)

* **基本思想：** 与其让 LLM 输出 JSON 等结构化数据来表示计划，不如让 LLM 直接 **编写软件代码** （如 Python），并用这段代码来 **表达计划的多个步骤和工具调用** 。
* **执行方式：** 开发者执行 LLM 生成的代码，从而实现复杂的计划。

2. 代码规划的动机与优势（以数据查询为例）

* **传统工具集的局限性：** 在处理复杂的数据查询（如“哪个月份热巧克力销量最高？”）时，如果只提供少量基础工具（如 `获取最大值`、`过滤行`），代理需要**极其复杂且冗长的工具调用序列**来解决问题。更糟糕的是，对于新的、更复杂的查询（如“上周有多少独特交易？”），可能需要不断地 **创建新的定制工具** ，这种方法是**脆弱且低效**的**。**
* **代码规划的优势：**
  * **利用大型库：** 允许 LLM 利用像 **Pandas** 这样的数据处理库中 **数百甚至数千个内置函数** 。
  * **高表达能力：** LLM 能够编写简洁的代码来表达一个涉及多步骤、复杂逻辑的计划（例如：解析日期、按日期排序、过滤、去重、计数）。
  * **性能更优：** 研究表明，在许多任务中，让 LLM 编写代码来采取行动（Code as Action）的性能**优于**让它编写 JSON 或纯文本计划。

3. 实施细节与注意事项

* **提示要求：** 提示 LLM 明确要求LLM“编写代码来解决用户的查询，并以 Python 代码返回您的答案”，通常使用 `<execute_python>` 等标签进行分隔。
* **安全问题（**  **沙箱** **）：** 运行 LLM 生成的代码存在安全风险，**需要考虑使用沙箱 (Sandbox)** 等安全执行环境。

4. 规划模式的现状总结

* **最强应用：** **高度代理化的软件编码系统**是规划模式目前最强大、最成熟的应用。LLM 可以生成一个详细的“构建清单”并逐步执行复杂的软件开发任务。
* **挑战：** 规划模式的**缺点**是 **难以控制** ，因为开发者无法预先知道 LLM 会生成什么样的行动序列。
* **结论：** 尽管存在控制问题，但**放弃一些控制权**可以 **显著增加模型可以尝试的事物范围** 。这是一项前沿技术，仍在其他领域发展中。

5. 下一步预告

下一个设计模式是 **多代理系统 (Multi-Agent Systems)** ，即让多个代理协同工作来完成复杂任务。

4. ## **【实验】Ungraded Lab: ****Customer Service**** Agent** —— 非评分实验：客服代理
5. ## **Multi-agentic workflows** —— 多代理工作流程

### 多代理系统 (Multi-Agent Systems) 设计模式

这段演讲介绍了**多代理系统 (Multi-Agent Systems)** 设计模式，该模式通过让**多个具有不同角色的代理**协作来解决复杂的任务，从而提高系统的效率和模块化。

1. 多代理系统的基本原理与优势

* **核心理念：** 尽管所有代理可能都基于同一个 LLM 运行在同一台电脑上，但将复杂任务**分解**成多个**独立的角色**或**进程**是一种更有效的开发方法（类似于人类团队协作或计算机的多线程/多进程）。
* **优势：**
  * **任务分解 (Decomposition)：** 像人类团队一样，将复杂任务自然地分解为拥有**不同角色和技能**的子任务。
  * **专注性 (Focus)：** 允许开发者 **一次专注于构建一个特定角色** （例如，只需专注于构建最好的“平面设计师代理”）。
  * **模块化与复用：** 有机会创建可**复用于其他应用**的通用代理（例如，一个通用的“平面设计师代理”可以用于营销手册和社交媒体帖子）。

2. 构建单个代理的方法

* **角色提示 (Role Prompting)：** 通过**提示词使 ****LLM**** 扮演**特定的角色身份（例如：“你是一名研究代理，擅长分析市场趋势”），并为其配备完成该角色任务所需的 **特定工具** 。
  | 代理角色                      | 任务描述                             | 可能需要的工具                                 |
  | ----------------------------- | ------------------------------------ | ---------------------------------------------- |
  | 研究员 (Researcher)           | 分析市场趋势，研究竞争对手。         | 网页搜索 (Web Search)。                        |
  | 平面设计师 (Graphic Designer) | 创建数据可视化图表和艺术作品。       | 图像生成/操作 API、代码执行（生成图表）。      |
  | 撰稿人 (Writer)               | 将研究成果转化为报告文本和营销文案。 | LLM 自身的文本生成能力（可能不需要额外工具）。 |

3. 两种主要的协作模式

多代理系统的设计核心在于 **代理之间的通信模式** 。

| 模式                                 | 描述                                                                                  | 结构                                                         | 特点                                                                 |
| ------------------------------------ | ------------------------------------------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------- |
| 1. 线性工作流程 (Linear Workflow)    | 代理依次执行任务，将输出传递给下一个代理，直到最终完成。                              | 研究员$\rightarrow$ 平面设计师 $\rightarrow$ 撰稿人      | 简单、直接，适用于步骤顺序固定的任务。                               |
| 2. 规划/管理器模式 (Manager Pattern) | 一个主要的 LLM 充当“经理”（第四个代理），负责制定计划并委托任务给团队中的其他代理。 | 营销经理 (LLM)$\rightarrow$ (研究员 / 平面设计师 / 撰稿人) | 更灵活。LLM 可以在运行时决定任务顺序，甚至在最后一步进行反思或审查。 |

4. 下一步

下一个视频将深入探讨**代理之间通信模式**的设计，介绍一些最常见的模式，以指导开发者如何让多个代理有效地相互协作。

6. ## **Communication patterns for multi-agent systems** —— 多代理系统的通信模式

### 多代理系统的通信模式

这段演讲讨论了在多代理系统中，代理之间**如何组织和交流**是决定系统效率和复杂性的关键设计决策，并介绍了当前最常见的几种通信模式。

1. 通信模式的重要性

* **复杂性：** 就像设计人类团队的组织结构图一样，设计多代理系统中的通信模式也是一个复杂的研究领域。
* **目标：** 选择合适的模式来协调代理的工作，以确保高效的协作。

2. 常见的通信设计模式

演讲者介绍了两种最常用的模式，以及两种更复杂和实验性的模式：

| 模式                                 | 结构特点                                                                                                                           | 优点与应用                                                                                                           |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| 1. 线性模式 (Linear)                 | 代理依次行动。前一个代理的输出是后一个代理的输入。                                                                                 | 最常见之一。 结构简单，适用于步骤顺序固定、依赖关系明确的任务（如：研究$\rightarrow$ 设计 $\rightarrow$ 撰写）。 |
| 2. 层级模式 (Hierarchical)           | 有一个中心经理代理，负责与多个团队成员代理沟通并协调他们的工作。                                                                   | 最常见之一。 经理负责制定方向和委托任务，提高了工作的协调性和集中控制能力。                                          |
| 3. 更深的层级结构 (Deeper Hierarchy) | 顶层代理（如经理）将其任务委托给其他代理，而这些代理本身又可以进一步调用子代理（例如：研究员调用“网络研究员”和“事实核查员”）。 | 复杂性高。 适用于需要多层专业分工的大型复杂任务，目前使用较少。                                                      |
| 4. 全互联模式 (All-to-All)           | 团队中的任何代理都可以在任何时间与任何其他代理交流。通过将消息添加到接收代理的“联系人”中，让其自行决定何时回复。                 | 实验性高。 结果难以预测，但适用于那些可以容忍一定程度混乱和不可预测性的应用，能显著增加模型探索问题解法的范围。      |

3. 总结与展望

* **软件框架：** 目前有许多软件框架支持轻松构建多代理系统，并简化了上述通信模式的实现。
* **设计决策：** 代理间的通信模式是构建多代理系统时需要做的**关键设计决策**之一。
* **课程结束：** 这部分内容标志着本课程所有设计模式和关键概念的讲解结束。

7.  ## **Conclusion** —— 总结

### 代理式 AI 课程回顾与展望

这段视频是对整个课程内容的简要回顾，强调了所学技能在构建创新应用和职业发展中的重要性。

1. 课程核心内容回顾

| 模块         | 核心主题                     | 关键设计模式与概念                                                                                    |
| ------------ | ---------------------------- | ----------------------------------------------------------------------------------------------------- |
| 应用与基础   | 代理式 AI 的应用范围和潜力。 | 构建以前不可能实现的新型应用。                                                                        |
| 设计模式 I   | 提升系统性能与功能的方法。   | 反思 (Reflection)：简单的性能提升手段。                                                               |
| 设计模式 II  | 扩展 LLM 能力。              | 工具使用 (Tool Use) / 函数调用 (Function Calling)：以代码执行为例，扩展模型的可操作范围。             |
| 开发流程     | 确保系统持续改进的高效方法。 | 评估 (Evals) & 错误分析 (Error Analysis)：驱动严谨的构建与分析流程，高效提升系统性能。                |
| 高级设计模式 | 构建更强大、更自主的系统。   | 规划 (Planning) 和 多代理系统 (Multi-Agent Systems)：用于构建功能更强大、但控制和预测难度更高的系统。 |

2. 技能的价值与展望

* **构建能力：** 课程教授的技能使学习者能够构建许多酷炫、令人兴奋的代理式 AI 应用。
* **职业机会：** 演讲者指出，许多公司在面试时会评估候选人是否具备本课程所教授的技能，因此这些知识有望为学习者开启新的职业发展机会。
* **最终寄语：** 鼓励学习者负责任地运用所学技能，去“构建酷炫的东西”。

