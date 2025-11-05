# 人工总结

## 一、规划设计模式与高度自主代理（ **Planning workflows** ）

就像复杂软件系统需要工厂模式、单例模式、依赖倒置等等设计模式和原则一样，Agent系统想要实现复杂度与效率并重，也需要一些设计模式。

本节我们将介绍规划 (Planning) 设计模式，规划模式的Agent系统高度自主，能够自行决定执行复杂任务所需的工具调用序列，而无需事先硬编码。

---

**真实案例：客服助理Agnet**

![](https://ucn3l6pxxkfq.feishu.cn/space/api/box/stream/download/asynccode/?code=MTUzZGQwMDA5MjkzNTE2NjA4ZmI4NTZiODM1MGE2OTdfWVVYVjdKYVVQMnpWRzlkYUNpMk9vZ1U5bVZpMGNEcXVfVG9rZW46VGFtSGIxRGlIb3BqVFZ4YURBNWNDSU05bmdDXzE3NjIzMDU2MDU6MTc2MjMwOTIwNV9WNA)

* 目标： 构建能够回答广泛、复杂查询的代理，在运行时灵活地决定采取哪些行动。在本系统中，是一个能够回答客户像“你们有没有库存中售价低于100美元的圆形太阳眼镜？”这类复杂问题的Agent。
* 方法：
  * 提供工具集： 给 LLM 提供一套功能工具。在本例中，是如下工具：

    | 工具名                  | 功能说明                                                       | 示例用途                                                                |
    | ----------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------- |
    | get_item_descriptions   | 获取商品的文字描述或元数据（如名称、款式、材质、颜色、形状等） | 当用户说“round sunglasses”时，用它来查出所有带“round”特征的太阳眼镜 |
    | get_item_price          | 查询指定商品的价格                                             | 在找到商品后，用它来判断哪些低于 $100                                   |
    | check_inventory         | 检查商品是否有库存（以及库存数量）                             | 找到圆形眼镜后，查询这些商品是否在库                                    |
    | check_past_transactions | 查看用户的历史交易记录（如购买过哪些商品、是否退换货过）       | 用于客户支持场景，如“我上周买的眼镜有问题”                            |
    | process_item_sale       | 处理购买行为，即创建销售订单或执行购买交易                     | 当用户确认要买时，调用这个工具执行交易                                  |
    | process_item_return     | 处理退货操作                                                   | 当用户想退货时，用它发起退货请求                                        |
  * LLM 编写计划： 要求LLM根据用户请求返回一个逐步的执行计划，说明应按什么顺序调用哪些工具。在本例中，是如下流程：

    1. LLM 计划调用 `get_item_descriptions` 来找“round sunglasses”
    2. 根据 Step 1 的输出（找到的产品）
    3. 再调用 `check_inventory` 查看库存
    4. 对库存中有货的结果
    5. 调用 `get_item_price` 检查哪些低于 $100
    6. 输出最终结果
  * 逐步执行： 按照计划，将每一步的指令和上一步的输出/上下文依次喂给 LLM，让它调用相应的工具并执行。
  * 最终输出： 将所有步骤的结果反馈给 LLM，生成最终的用户答案。

---

可以看出，规划模式的Agent有许多好处，比如Agent拥有非常丰富的能力，进而扩展了能执行的任务范围。开发者也无需事先编排工具调用的确切序列，提高了系统的灵活性和自主性。

规划模式的Agent系统在流程控制与实际场景上也有些风险点。在运行时，开发者无法预知 LLM 会生成什么样的计划，带来了结果不稳定/出错/越权的风险。目前，规划模式在AI Coding应用中非常成功，但在其他领域仍然处在尝试阶段。

> 不过，可以看到的是，随着基础模型的智能程度不断提高，现在使用这种完全由Agent控制流程的AI系统的场景也越发多了，笔者自己开发应用时也经常用到。这种规划模式灵活度高，代码量小，难点在于工具设计与流程设计。
>
> 对于同一个场景，经验丰富的开发者可能会抽象出三个封装好了复杂逻辑的核心工具即可解决问题，而经验不足的开发者往往容易过度抽象出十几种工具，或是索性直接提供最基本的一两个工具（在本例中，有可能是商品系统后台的数据库session——这是极其不安全的！），让AI自己编写代码来写业务。
>
> 这里推荐一个笔者个人十分喜欢的Agent框架：来自Huggingface社区的[smolagents](https://huggingface.co/docs/smolagents/index)框架。它代码简洁，抽象程度少，工具开发难度低（只需要一个@tool装饰器），自由程度高，也具有流程跟踪功能，开发者很容易入门，也很方便理解重写其中的一些逻辑，来实现自己定制化的系统。

## 二、规划设计模式的实施细节——结构化输出（**Creating and executing ****LLM** ** plans** ）

在规划模式中，如何利用结构化输出来保证 LLM 生成的计划能够被下游代码可靠地执行，是非常重要的。

在上一讲中，我们让LLM直接讲出自己的任务规划，但自然语言不够清晰和明确，难以被下游代码稳定地解析和执行。所以在本节中，我们要求 LLM 以结构化格式（如 JSON 或 XML）输出计划。

结构化格式能够清楚地界定计划的步骤、所需工具及其参数，从而允许下游代码更可靠地解析 (parse) 计划的每个步骤，从而系统性地、一步一步地执行。

---

为了实现结构化输出，开发者应该这样写 LLM 指示词：“你可以访问以下工具，并需要以 JSON 格式创建一个分步计划”，同时详细描述所需的 JSON 结构。

![](https://ucn3l6pxxkfq.feishu.cn/space/api/box/stream/download/asynccode/?code=NTNmOTBkYzY1MGM5ZWNmYjg3NDkxMGEyZjdlNDYzMmNfeDdreklFZ1RhbDVKa2VYSUdud0RKcE9LSnNlaTZueHZfVG9rZW46QW1KTGJOS2Fkb0drV2x4b1Jmd2M3R0MyblRnXzE3NjIzMDU2MDU6MTc2MjMwOTIwNV9WNA)

LLM 会返回一个 JSON 列表，列表中的每个对象代表一个步骤，包含清晰的键值：

* `description` (步骤描述)
* `tool` (要调用的工具名称)
* `arguments` (传递给工具的参数)

这样一来，我们只要接收LLM的字符串输出，转化为JSON格式，并提取参数，执行对应函数即可。这样的解析器编写起来非常方便。

## 三、规划设计模式的进阶——使用代码作为行动（ **Planning with code execution** ）

在上节中，我们让LLM用JSON描述了自己的动作。但是不妨想想，与其让 LLM 输出 JSON 等结构化数据来表示计划，不如直接让 LLM 直接编写软件代码来的效果更好。LLM可以直接用代码来表达计划的多个步骤和工具调用。

> 许多论文也表示，同样的工具与参数，让LLM直接编写代码的任务评估分数通常明显大于编写JSON而后解析。Huggingface出品的smolagents框架中的CodeAgent概念正是在这种思想的指导下设计出的。

在处理复杂的数据查询（如“哪个月份热巧克力销量最高？”）时，如果只提供少量基础工具（如 `获取最大值`、`过滤行`），代理需要极其复杂且冗长的工具调用序列来解决问题。

更糟糕的是，对于新的、更复杂的查询（如“上周有多少风险交易？”），还需要不断地创建新的定制工具，这种方法是脆弱且低效的。

而若是允许LLM直接执行代码，就能获得下列优势：

* 利用大型库： LLM 得以利用像 Pandas 这样的数据处理库中数百甚至数千个内置函数。
* 高表达能力： LLM 能够编写简洁的代码来表达一个涉及多步骤、复杂逻辑的计划，例如解析日期、按日期排序、过滤、去重、计数。
* 性能更优： 研究表明，在许多任务中，让 LLM 编写代码来采取行动的性能**优于**让它编写 JSON 或纯文本计划。

![](https://ucn3l6pxxkfq.feishu.cn/space/api/box/stream/download/asynccode/?code=NGFkMzc1ZTljNzI3Zjk0NmNmMWUwYTQ4ZjMzYzAwYzNfREZPUGRHbTJJOUVlN2tNVTRnSDVZQ1QwYVBVVnVpSVdfVG9rZW46THd4YWJxTDF1b1RTbHF4b0xZemN4NHR5bnZnXzE3NjIzMDU2MDU6MTc2MjMwOTIwNV9WNA)

不过，这种CodeAgent的形式也有些需要注意的风险点：

* 提示词要求：  明确要求LLM编写代码来解决用户的查询，并以 Python 代码返回结果，通常使用 `````或 `<code>` 等标签进行分隔。
* 安全问题： 直接运行 LLM 生成的代码存在安全风险，需要考虑使用沙箱 (Sandbox) 等安全执行环境。

现在，我们已经充分了解了这种使用代码执行任务的规划模式Agent系统。该模式下 LLM 可以生成一个详细的“构建清单”并逐步执行复杂的软件开发任务。

规划模式的缺点是难以控制，因为开发者无法预先知道 LLM 会生成什么样的行动序列。尽管如此，放弃一些控制权可以显著增加模型的能力范围，大多数时候这是值得的。

## 四、多代理系统（ **Multi-agentic workflows** ）

尽管所有Agent可能都基于同一个底层 LLM ，并运行在同一台电脑上，但将复杂任务**分解**成多个**独立的角色**或**进程**是一种更有效的开发方法，就像团队协作或计算机的多线程/多进程一样。

想想看，你现在有一个十分复杂的AI业务系统，LLM需要调用十几种甚至几十种工具，并在一段几千字的提示词的指导下运行。一个典型的业务流程都需要七八步才能实现。

在这种情况下，把一个Agent拆成很多次级Agent，并构成一个多Agent系统，即MultiAgent系统，就十分有必要了。多个承担不同任务的Agent可以靠互相协作来解决复杂的任务，提高系统的效率和模块化。

---

下图就是一个拆分市场Agent的例子，拆出了调研、生成报表、创建文件三个子Agent

![](https://ucn3l6pxxkfq.feishu.cn/space/api/box/stream/download/asynccode/?code=NTkxMDQ5NTY2NDgwYjhiNDk1YTFmNGZlNTBiMWIwNzdfYk94TXRqbWd5Q0h1ZlNxODJONDBZTk1SMUJ5c3A5N0JfVG9rZW46Q3czY2JOYmZNb0hueVJ4VFI5aWM0cXRmbmxoXzE3NjIzMDU2MDU6MTc2MjMwOTIwNV9WNA)

![](https://ucn3l6pxxkfq.feishu.cn/space/api/box/stream/download/asynccode/?code=YjkxMmVhMGQwY2Q2ZjljYmJiYzA1ODdlYWI5ZThmNzdfQUxMRG1EZTJOSlRZcjgzMVdMMktGU3ZSSGRqdkh1c2xfVG9rZW46S3VyZGI2Vmlib0VCVDJ4SW96ZWNySW9ObnJkXzE3NjIzMDU2MDU6MTc2MjMwOTIwNV9WNA)

MultiAgent系统具有以下优势：

* 任务分解： 像人类团队一样，将复杂任务自然地分解为拥有不同角色和技能的子任务。
* 专注性： 允许开发者一次专注于构建一个特定角色，就像只需专注于构建最好的“平面设计师代理”。通常，单个Agent的任务越简单，任务完成的效果就越好。
* 模块化与复用： 有机会创建可复用于其他应用的通用代理，就像一个通用的“平面设计师代理”可以用于营销手册和社交媒体帖子。

> 此外，笔者还认为MultiAgnet系统有以下两个优势：
>
> * 突破上下文限制。现在绝大多数模型都具有128k的上下文，对于一些需要多轮规划执行的调研类任务或业务分析任务来说是完全不够的。但如果让每个Agent只负责自己的部分，最终只返回自己部分的调研结果，让一个总结Agent总结各个子Agent的调研结果，生成最终报告，就能规避上下文的限制，因为总结Agent不必在上下文中存储其它Agent的调研过程，它只看结果就够了。
> * 节约成本。在资金成本上，每次请求都附带大量上下文是非常烧钱的，即使命中缓存。MultiAgent体系中每个Agent上下文都比较短，更节约Tokens费用；在时间成本上，上下文越短，LLM回复速度越快，延迟越低，同时多个Agent还能并行处理任务，可以将时间成本大大降低。

通常，我们通过提示词+工具的组合来创建不同的Agent。比如对于一个市场分析Agent，就需要告诉LLM它具有高超的市场分析技巧，和他讲一些市场分析的范式与最佳实践，并给它配备网页浏览工具，以便它可以自己去做市场调研。

接下来，我们会深入探讨**代理之间通信模式**的设计，介绍一些最常见的模式，了解如何让多个代理有效地相互协作。

## 五、多代理系统的协作模式（ **Communication patterns for multi-agent systems** ）

当一个团队一起工作时，他们之间的沟通模式可能会非常复杂。类似地，设计多智能体系统的通信模式也同样复杂，而组织结构的好坏会极大影响系统的效率与结果。

本节我们会基于上面一节里的市场调研Agent，介绍四种协作模式：线性、双层、多层和去中心。

---

1. **线性模式（Linear communication pattern）**

就像一个市场团队的工作流：研究员 → 平面设计师 → 文案撰写者。每个人只和下一个环节沟通。

线性模式按顺序执行任务，信息单向流动；

* 优点：结构简单、易于理解；
* 缺点：不灵活，出错时难以反馈或修正。

---

2. **双层模式（Hierarchical communication pattern）**

有一个“管理员（Manager Agent）”负责协调所有下属Agent。
就像项目负责人依次给研究员、设计师、写手分配任务，收集结果，再整合。

![](https://ucn3l6pxxkfq.feishu.cn/space/api/box/stream/download/asynccode/?code=MmI5NmVlMTVkMmQwZDYzZDRkYTQ1Y2MzZWFjMDBmZDVfakpBMU9tUDJQVm9pOGdJVFVqQ3RTaldBekI3aTFreFpfVG9rZW46VmpxOGJVdmNGb2FQd2p4QzFIcmNkUXlNbk9iXzE3NjIzMDU2MDU6MTc2MjMwOTIwNV9WNA)

双层模式下，所有通信都经过经理；

* **优点** ：清晰、易于控制、任务协调性强；
* **缺点** ：可能成为瓶颈（manager负担重）。

---

3. **多层模式（Deep Hierarchy）**

一些高级系统会让子Agent自己也拥有下属Agent。
 例如“研究员”下面有“网页研究员”和“事实核查员”，“作家”下面有“风格写手”和“引用校对员”。

![](https://ucn3l6pxxkfq.feishu.cn/space/api/box/stream/download/asynccode/?code=OWY3NTlkN2FlMDAwNTQyNTZhMDc4MDdlMjcwOTg3MjlfNWsweXJVeEhRam9OcVdSNVF0RVR1MUo5RmthNFBZMExfVG9rZW46THFkU2JkUjhab0pKSVV4ckpva2NCOHFmbjJmXzE3NjIzMDU2MDU6MTc2MjMwOTIwNV9WNA)

* 优点：可扩展、模块化、可分层调度；
* 缺点：通信复杂、难以调试、出错难追踪。

---

4. **去中心模式（All-to-all communication）**

在这种模式下，每个Agent都能随时与其他Agent交流，没有中心，也没有固定顺序。

每个Agent都知道其他Agent是谁，他们可以互相发消息，谁都可以决定何时回复。直到最后大家都“认为任务完成”时，产出最终结果。

![](https://ucn3l6pxxkfq.feishu.cn/space/api/box/stream/download/asynccode/?code=YWMyZDc1ZTRhNDQxZTE4ZDU3NTg5Y2NhNmRjZmE2ODBfQ2dlUHpjWTNzNFBITk5tSHZTZUdtcTlab1lUcFFjMnhfVG9rZW46T3ZxOWJ4ekQ2b3ZYak54MXROb2NLMmFJbjZjXzE3NjIzMDU2MDU6MTc2MjMwOTIwNV9WNA)

特点：高度去中心化、非常灵活、创意性强，但也 难以预测结果。

这种模式适用于容忍一定混乱、追求创造性结果的场景。

---

我们将这四种通信模式总结为下表：

| 模式类型               | 结构特征           | 优点     | 缺点     | 适用场景           |
| ---------------------- | ------------------ | -------- | -------- | ------------------ |
| 线性（Linear）         | 顺序执行，单向通信 | 简单     | 不灵活   | 固定流程任务       |
| 双层（Hierarchical）   | 中心协调           | 易控制   | 管理负担 | 多任务协调         |
| 多层（Deep Hierarchy） | 子Agent层次化      | 模块化   | 复杂     | 大型系统           |
| 去中心（All-to-all）   | 自由对话           | 创造性强 | 不可预测 | 探索型、生成型任务 |

> 实际生产中，线性模式与双层模式会更常用一些，因为至少对于当前LLM的能力而言，信息会在层级之间传递时丢失部分信息，层级越多，信息越匮乏/失真。
>
> 其实在这四种模式外，还有一种对话模式，比较类似去中心模式的降级版。对话模式每次都只有两个Agent互相对话交流，一方执行任务，另一方审查任务，最终交出一份双方都满意的结果。
>
> 在常见的Agent框架中，langchain是忠实的线性结构，smolagents更青睐于双层/多层结构，而metagpt、camelai则致力于做去中心结构。当然，大部分框架都可以同时实现这些不同的结构，只是代码风格不同，读者可以自行多尝试，找到自己最喜欢的框架，与最适合某项具体任务的框架。

## **六、** 总结

吴恩达教授在本节中，回顾了整套课程涉及到的内容。

课程首先介绍了 Agentic AI 能实现以往无法做到的应用场景，随后讲解了关键设计模式，如 反思（reflection） 与 工具调用（tool use / function calling），以及如何通过 评估与误差分析 持续改进系统性能。

最后一模块探讨了 规划（planning） 与 多智能体系统（multi-agent systems），让开发者能构建更强大但也更复杂的 AI 系统。

吴恩达教授希望学习者掌握这些技能后，能在实践中构建创新的 Agentic AI 应用，提升职业竞争力，并鼓励大家在未来负责任地运用这些知识，去创造有趣且有价值的成果。

作为曾经承蒙吴恩达教授系列课程帮助的大模型行业从业者，笔者有些话想和大家分享。

如果某项技术能低成本而平滑地提高一个增长期行业的生产力，就一定能大行其道。AI技术从上世纪开始，经历了诸多阶段，到现在迎来了以Tansformer为核心的大模型浪潮，终于到了爆发点。现在各行各业的数字化需求还很多，数字生产力与实现元宇宙的需求距离还很远，还有足够的需求可以填补，而大模型很能填补这个空缺——这也是为什么同样都是受资本追捧，元宇宙项目多半流产，而大模型在当下能大行其道的一个重要原因。

当然，大模型不可能是一颗常青树。随着时间流逝，大模型也总有成为明日黄花的一天。世界是运动的，任何技术形态都受到生产力与生产关系、技术基础与社会结构之间矛盾的制约与推动，而在大模型技术从新兴技术普及为基础建设的过程中，也势必孕育出更新的技术与载体，从而被取代。这也是否定之否定的哲学。

所以，当我们在学习大模型时，我们应该学习的是大模型技术背后那些有迁移性的思想，比如对复杂系统的编排拆分，比如项目中的工程与科研思维，比如从平滑迁移到打碎繁琐旧系统，用新技术的特点重建新系统的经验，比如对各类业务系统的底层逻辑总结。同时，在大模型领域深耕与发散的过程中，也要时刻留意新兴技术的萌芽——技术不是常青树，但持续掌握新技术的人可以是。

诸君，共勉！