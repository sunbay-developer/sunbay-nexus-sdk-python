## Sunbay Nexus Python SDK 设计文档（草案）

### 1. 项目概述

- **项目名称**：Sunbay Nexus Python SDK  
- **目标**：为 Python 开发者提供一个专业、主流风格、与 Java SDK 功能等价的开放 API SDK，用于访问 Sunbay Nexus 支付平台。  
- **参考实现**：`sunbay-nexus-sdk-java` 中的 `NexusClient`、`HttpClient`、`ApiConstants`、各类 `*Request` / `*Response` / `BaseResponse` / 异常类。  
- **参考平台**：阿里云 Python SDK、AWS Boto3、Stripe Python SDK 等主流开放平台 SDK。

### 2. 设计目标

- **功能等价**：覆盖 Java SDK 中 `NexusClient` 当前暴露的全部能力：  
  - `sale`, `auth`, `forcedAuth`, `incrementalAuth`, `postAuth`, `refund`, `voidTransaction`, `abort`, `tipAdjust`, `query`, `batchClose`。  
- **Python 风格**：接口命名、异常处理、模块组织遵循 Python 社区惯例（PEP 8），同时保持与 Java SDK 术语一致（便于跨语言维护）。  
- **线程安全 & 连接复用**：仿照 Java 基于连接池的 `HttpClient`，Python 版提供长连接会话对象，适合高并发服务端场景。  
- **无魔法值**：所有关键参数（超时、重试次数、基础 URL、HTTP 路径、状态码区间等）集中在配置常量中管理，避免散落在代码里的硬编码魔法值。  
- **错误清晰**：区分“业务异常”和“网络异常”，对应 Java 的 `SunbayBusinessException` 和 `SunbayNetworkException`，异常文案统一使用英文。  
- **主流环境兼容**：支持当前主流 Python 版本和运行环境（Linux 服务器、macOS 开发机、Windows、虚拟环境、Docker）。  
- **标准发布形态**：在 PyPI 上发布，支持 `pip install` 安装，开发者集成体验与 AWS/Stripe/阿里云等平台保持一致。

### 3. 与 Java SDK 的能力对齐

Java 端 `NexusClient` 方法（统一通过内部 `HttpClient` 调用 REST API）：

- **交易类接口**  
  - `sale(SaleRequest): SaleResponse`  
  - `auth(AuthRequest): AuthResponse`  
  - `forcedAuth(ForcedAuthRequest): ForcedAuthResponse`  
  - `incrementalAuth(IncrementalAuthRequest): IncrementalAuthResponse`  
  - `postAuth(PostAuthRequest): PostAuthResponse`  
  - `refund(RefundRequest): RefundResponse`  
  - `voidTransaction(VoidRequest): VoidResponse`  
  - `abort(AbortRequest): AbortResponse`  
  - `tipAdjust(TipAdjustRequest): TipAdjustResponse`  

- **查询类接口**  
  - `query(QueryRequest): QueryResponse`（GET，参数拼在 QueryString 中）  

- **结算类接口**  
  - `batchClose(BatchCloseRequest): BatchCloseResponse`  

Python SDK 需要在 `NexusClient` 中提供对应的同名方法（函数名采用小写加下划线或保持驼峰，在最终实现阶段再定，但文档中保持与 Java 一一对应），请求/响应模型字段保持与 Java 一致。

### 4. 主流平台 SDK 的版本兼容策略调研

- **Python 2 支持现状**  
  - Python 2.7 官方支持已于 2020-01-01 结束。  
  - 阿里云官方 SDK 已宣布停止对 Python 2.7 的支持（以及陆续停止对 Python 3.6 的支持）。  
  - AWS、Stripe 等新版本 SDK 也都已经不再支持 Python 2。  
  - 新设计的对外 SDK 若仍声称支持 Python 2，反而容易被认为“过时、不专业”，并且会严重增加维护成本（类型注解、语法差异、依赖兼容等问题）。  

- **Python 3 版本下界选择**  
  - 历史上很多 SDK 从 3.6 开始支持；但 3.6 本身在 2021 年已经停止官方支持，阿里云等也计划停止。  
  - 当前主流平台的 SDK（如阿里云、AWS Boto3、Stripe Python SDK 的最新版本）一般支持的范围集中在 3.7/3.8 以上。  
  - 考虑到：
    - 开发者实际使用情况中，3.7 及以上版本覆盖率已经非常高；  
    - 低于 3.7 的版本已逐步退出生产环境；  
    - 过度向后兼容会牺牲类型标注、现代语法、依赖选择等的质量；  
  - **本 SDK 计划的最低支持版本设定为：Python 3.7**，并推荐 3.8+。  

> 结论：  
> - **不再考虑对 Python 2 的支持**（与阿里云/AWS/Stripe 等当前主流做法保持一致，这样才是“专业”的选择）。  
> - **官方声明支持：Python 3.7 及以上版本**，并在文档、`pyproject.toml` 的 `requires-python` 字段中明确标注。  

### 5. SDK 兼容策略设计

- **版本声明**  
  - 在打包配置（如 `pyproject.toml`）中设置：  
    - `requires-python = ">=3.7"`  
  - 在 README 与本设计文档中明确写出：  
    - “Sunbay Nexus Python SDK officially supports Python 3.7 and above. Python 2 is not supported.”  

- **语法与特性选择**  
  - 只使用 Python 3 语法和标准库特性（如类型注解、f-string、`dataclasses` 等），不做 Python 2 兼容层。  
  - 避免使用仅在最新少数版本可用的特性（例如特别新的标准库 API），以保证在 3.7~3.12 之间都可正常运行。  

- **依赖库选择**  
  - 选用在 3.7 以上有良好支持、且不依赖 Python 2 的主流库，例如：  
    - HTTP 客户端：`httpx` 或 `requests`。  
  - 在依赖声明中约束版本范围，确保与 Python 3.7+ 兼容。  

- **测试矩阵**  
  - 在 CI（如 GitHub Actions）中，使用矩阵测试：  
    - Python 3.7 / 3.8 / 3.9 / 3.10 / 3.11 / 3.12。  
  - 保证所有对外发布版本在上述版本上都运行通过。  

- **向后兼容策略**  
  - 遵循语义化版本控制（SemVer）：  
    - `MAJOR`：有破坏性变更（例如彻底放弃某个 Python 次版本支持、或大改接口）；  
    - `MINOR`：向后兼容的新功能；  
    - `PATCH`：兼容性的缺陷修复。  
  - 当未来决定不再支持某个较低版本（如 3.7）时，在 README/变更日志中提前公告，并在下一大版本中调整 `requires-python`。  

### 6. 包结构设计

采用主流 Python `src` 布局，包名蛇形（当前实现中目录略有调整，但语义一致）：

```text
sunbay-nexus-sdk-python/
├── pyproject.toml                          # 打包与元数据
├── README.md
├── LICENSE
├── DESIGN.md                               # 本设计文档
├── src/
│   └── sunbay_nexus_sdk/
│       ├── __init__.py
│       ├── client.py                       # NexusClient 主入口
│       ├── constant/
│       │   └── api_constants.py            # 常量与默认配置（替代魔法值）
│       ├── http/                           # HTTP 客户端封装（Session/重试/日志）
│       │   └── __init__.py
│       ├── exception/
│       │   └── __init__.py                 # 异常体系
│       ├── model/
│       │   ├── base.py                     # BaseResponse 等
│       │   ├── common.py                   # Amount/PaymentMethodInfo 等
│       │   ├── request.py                  # 各类 *Request
│       │   └── response.py                 # 各类 *Response
│       └── util/
│           └── id_generator.py             # RequestId 生成，对齐 Java IdGenerator
└── tests/                                  # 本地/集成测试（不随 PyPI 包发布）
```

说明：

- **config/常量集中管理**  
  - HTTP 路径：与 Java `ApiConstants.PATH_*` 一一对应。  
  - 成功 code：`RESPONSE_SUCCESS_CODE = "0"`。  
  - HTTP 状态区间：2xx / 4xx / 5xx 边界。  
  - 默认配置：`DEFAULT_BASE_URL`、超时、重试次数、连接池大小等。  

- **对外 API 面**  
  - 在 `sunbay_nexus_sdk.__init__.py` 中暴露：  
    - `NexusClient`  
    - 异常类：`SunbayBusinessError`, `SunbayNetworkError`  
    - 核心请求/响应模型类（方便类型提示与 IDE 补全）  

### 7. 核心类与行为设计

#### 7.1 NexusClient

职责：

- 管理 API Key / Base URL / HTTP 客户端 / 超时 / 重试策略 / 连接池配置。  
- 提供所有业务 API：  
  - 交易类：`sale`、`auth`、`forced_auth`、`incremental_auth`、`post_auth`、`refund`、`void_transaction`、`abort`、`tip_adjust`。  
  - 查询类：`query`。  
  - 结算类：`batch_close`。  
- 保证线程安全：内部只持有不可变配置和线程安全的 HTTP 会话对象。  

初始化接口（Python 风格，后续实现时再细化默认值单位）：

```text
NexusClient(
    api_key: str = None,
    base_url: str = DEFAULT_BASE_URL,
    connect_timeout: float = DEFAULT_CONNECT_TIMEOUT_SECONDS,
    read_timeout: float = DEFAULT_READ_TIMEOUT_SECONDS,
    max_retries: int = DEFAULT_MAX_RETRIES,
    max_connections: int = DEFAULT_MAX_TOTAL,
)
```

- 若未显式传入 `api_key`，可尝试从环境变量（例如 `SUNBAY_API_KEY`）读取；若仍为空，则抛业务异常，错误信息使用英文。  
- 推荐在服务端项目中将 `NexusClient` 作为单例创建并复用。  

#### 7.2 HTTP 客户端封装

参考 Java `HttpClient`：

- 拼 URL：`base_url + path`。  
- 设置请求头：  
  - `Authorization: Bearer {api_key}`  
  - `X-Client-Request-Id`：通过 `id_generator` 生成，与 Java `IdGenerator` 行为一致。  
  - `X-Timestamp`：毫秒时间戳字符串。  
  - `Content-Type: application/json`（POST 请求）。  
- 执行请求和重试：  
  - `POST`：请求体序列化为 JSON；  
  - `GET`：通过请求模型（dataclass）的字段生成 query 参数，忽略值为 `None` 的字段；  
  - GET 请求可根据配置进行多次重试，间隔采用简单线性或指数回退（与 Java `RETRY_DELAY_BASE_MS * attempts` 类似）。  
- 解析响应：  
  - 支持结构：`{"code":"0","msg":"Success","data":{...},"traceId":"..."}`；  
  - 先解析外层 `code/msg/traceId`，再将 `data` 映射为具体的 `*Response` 类型；  
  - 若 `code != "0"`，记录错误日志并抛出 `SunbayBusinessError`。  
- 错误映射：  
  - 超时/网络异常：抛出 `SunbayNetworkError(message, retryable=True/False)`；  
  - HTTP 非 2xx：组装英文错误信息并抛 `SunbayNetworkError`；  
  - JSON 解析失败：抛 `SunbayNetworkError`，并在日志中记录原始响应。  

### 8. 模型设计

- **BaseResponse**（对齐 Java）  
  - 字段：`code: str`, `msg: str`, `trace_id: Optional[str]`。  
  - 方法：`is_success()` 判断 `code == "0"`。  

- **各类 *Response**  
  - 继承 `BaseResponse`，添加自己的业务字段（例如 `SaleResponse.transactionId` 等，命名尽量与 Java 一致）。  

- **各类 *Request**  
  - 使用 `@dataclass` 定义，字段与 Java 对应类保持一致：  
    - 如 `SaleRequest` 中的 `appId`, `merchantId`, `referenceOrderId`, `transactionRequestId`, `amount`, `paymentMethod`, `description`, `terminalSn`, `attach`, `notifyUrl`, `timeExpire` 等。  
  - 提供从字典构造、转字典等便捷方法（可以依赖 dataclass 的 `asdict`）。  
  - 在调用侧主要是直接通过构造函数使用，避免在 Python 中引入复杂的 Builder 模式。  

### 9. 异常与日志规范

- **异常类**  
  - `SunbayBusinessError`：业务异常与参数校验异常，对应 Java `SunbayBusinessException`。  
    - 字段：`code: Optional[str]`, `trace_id: Optional[str]`, `message: str`。  
  - `SunbayNetworkError`：网络/HTTP 异常，对应 Java `SunbayNetworkException`。  
    - 字段：`retryable: bool`。  

- **语言约束**  
  - 所有异常 message、日志内容均使用英文，不在 SDK 内输出中文，方便全球开发者和排查问题。  

- **日志**  
  - 使用标准库 `logging`；默认 logger 名称：`sunbay_nexus_sdk`；  
  - SDK 自己不创建 Handler，由业务方统一配置；  
  - 请求/响应日志只在 info/debug 级别输出，避免打印敏感字段（如完整卡号等）。  

### 10. 版本管理、打包与发布（PyPI）

- **版本号**  
  - 采用语义化版本（SemVer）：`MAJOR.MINOR.PATCH`；  
  - 与 Java SDK 的版本保持语义上的对应（便于文档标注“Python SDK 1.0.x 对应 Java SDK 1.0.x”）。  

- **打包配置**  
  - 推荐使用 `pyproject.toml`（PEP 621）描述元数据：  
    - `name = "sunbay-nexus-sdk"`  
    - `version = "1.0.0"`（示例）  
    - `requires-python = ">=3.7"`  
    - `dependencies = [...]`  
    - `classifiers` 中标明支持的 Python 版本和 License（例如 MIT）。  

- **构建与上传流程**  
  - 构建：`python -m build`。  
  - 上传：`twine upload dist/*`。  
  - 首次上传前在 PyPI 注册账号并配置 API token。  

- **与 Java/Maven 的类比**  
  - PyPI 对应 Maven Central，`pip install sunbay-nexus-sdk` 对应 Java 的 Maven 依赖声明。  
  - README 中需要有清晰的安装章节，示例：  
    - `pip install sunbay-nexus-sdk`。  

### 11. 测试与质量保证

- **单元测试**  
  - 使用 `pytest` 编写；  
  - 使用 HTTP mock（如 `responses` 或 `pytest-httpx`）覆盖：  
    - 成功响应解析；  
    - 业务错误返回；  
    - HTTP 错误、超时与重试；  
    - 空请求参数导致的本地业务异常（对齐 Java 在 `request == null` 时抛业务异常）。  

- **静态检查与风格**  
  - 可选集成：`mypy`（类型检查）、`ruff` 或 `flake8`（代码风格）。  
  - 遵守 PEP 8，确保 SDK 代码和示例看起来“像主流 Python 库”。  

- **CI 测试矩阵**  
  - 针对 Python 3.7~3.12 的版本矩阵执行：  
    - 安装依赖；  
    - 运行单元测试；  
    - 运行静态检查。  

### 12. 文档与示例

- 在仓库中提供：  
  - `README.md`：快速开始、安装、示例代码、错误处理示例。  
  - `examples/`：  
    - `quick_start_sale.py`：模拟完成一次 `sale` 交易；  
    - `quick_start_auth.py`：预授权示例；  
    - `quick_start_query.py`：查询交易示例。  
  - 视情况使用 Sphinx / mkdocs 生成更完整的 API 文档。  

---

本设计文档仅定义架构、兼容策略和对齐规则，不包含具体实现代码。  
后续可以在此基础上逐步实现 `NexusClient`、HTTP 封装和各类模型，并严格对齐 Java SDK 的行为与错误语义。


