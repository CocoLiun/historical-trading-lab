"""UI labels; persisted field names remain language independent."""

TRANSLATIONS = {'📈 Historical Trading Lab': '📈 Historical Trading Lab',
 '历史行情回放 · 收盘后决策 · 下一交易日开盘模拟成交 · 教学用途': 'Replay historical prices · Decide after close · Fill at '
                                        'next open · Learning only',
 '仅供学习。当前为单资产日线模型；未实现完整交易所规则、公司行动和订单簿撮合。': 'Educational single-asset daily simulation. Full '
                                           'exchange rules, corporate actions and order-book '
                                           'matching are not implemented.',
 '恢复已有练习': 'Resume a saved practice',
 '新建 / 输入名称': 'New / enter a name',
 '模拟账户名称（用于保存和恢复）': 'Practice name (for saving and restoring)',
 '获取一份默认练习行情': 'Step 1 · Choose your practice data',
 '默认标的：SPY（美国上市的标普500 ETF），最近约 5 年日线。点击后从 Yahoo Finance 获取，并保存到你这台 Mac 的 SQLite；不会把行情文件提交到 GitHub。仅供个人学习，数据使用受 Yahoo 条款约束。': 'Default: '
                                                                                                                             'SPY, '
                                                                                                                             'a '
                                                                                                                             'US-listed '
                                                                                                                             'S&P '
                                                                                                                             '500 '
                                                                                                                             'ETF, '
                                                                                                                             'with '
                                                                                                                             'about '
                                                                                                                             'five '
                                                                                                                             'years '
                                                                                                                             'of '
                                                                                                                             'daily '
                                                                                                                             'prices. '
                                                                                                                             'Download '
                                                                                                                             'from '
                                                                                                                             'Yahoo '
                                                                                                                             'Finance '
                                                                                                                             'and '
                                                                                                                             'save '
                                                                                                                             'locally. '
                                                                                                                             'Personal '
                                                                                                                             'learning '
                                                                                                                             'use; '
                                                                                                                             'Yahoo '
                                                                                                                             'terms '
                                                                                                                             'apply.',
 '下载 SPY 默认练习数据（约 5 年）': 'Download SPY practice data (about 5 years)',
 '正在获取历史行情…': 'Downloading historical prices…',
 '已下载并保存到本机 SQLite。': 'Downloaded and saved locally.',
 '或者上传自己的历史日线 CSV：date,open,high,low,close,volume': 'Upload your own daily CSV: '
                                                    'date,open,high,low,close,volume',
 '此数据与当前练习不同。替换会清空该练习的进度；也可以输入新账户名称另建练习。': 'This dataset differs from your saved practice. '
                                           'Replacing it resets progress. Enter a new practice '
                                           'name to keep the original.',
 '确认替换当前练习的数据并清空进度': 'Confirm replacing this dataset and resetting progress',
 '先点击上方按钮获取默认 SPY 行情，或者上传自己的 CSV。': 'Click Download SPY practice data above to begin. Uploading '
                                    'your own CSV is optional.',
 '交易模式': 'Trading mode',
 '通用模式': 'General mode',
 'A 股基础规则（买入100股整数倍、T+1）': 'Basic A-share rules (buy lots of 100, T+1)',
 'A 股基础模式未模拟板块涨跌停、历史制度变化和公司行动；切换模式会在下次保存时记录。': 'Basic A-share mode excludes board-specific price '
                                               'limits, historical rule changes and corporate '
                                               'actions. Mode changes are saved with your next '
                                               'action.',
 '现金': 'Cash',
 '持仓': 'Shares',
 '估算总资产': 'Estimated equity',
 '只展示当前模拟日及之前行情；下单按下一交易日开盘价加假设滑点成交。': 'Only current and earlier prices are shown. Orders fill at '
                                      'the next trading day open with assumed slippage.',
 '交易方向': 'Order side',
 '数量（尚未应用各市场整手限制）': 'Shares (basic A-share mode: buy multiples of 100)',
 '决策理由（可选）': 'Decision note (optional)',
 '下单并推进一个交易日': 'Place order and advance one day',
 '跳过一个交易日': 'Skip one trading day',
 '累计收益': 'Total return',
 '买入持有基准（不计费用，可分股）': 'Buy-and-hold benchmark (no fees, fractional shares)',
 '相对基准收益（百分点）': 'Relative return (percentage points)',
 '交易流水': 'Trade history',
 '最大回撤': 'Maximum drawdown',
 '账户': 'Account',
 '买入持有': 'Buy and hold',
 '每日盈亏': 'Daily P&L',
 '决策笔记': 'Decision notes',
 '重置当前模拟账户': 'Reset this practice',
 '买入': 'Buy',
 '卖出': 'Sell',
 '日期': 'Date',
 '数量': 'Shares',
 '成交价': 'Fill price',
 '手续费': 'Fee',
 '笔记': 'Note',
 '决策': 'Decision',
 '收盘价': 'Close',
 '无需准备报表，直接下载行情就能开始。': 'No report required. Download prices to start.',
 '① 选择数据 → ② 每天决定买入、卖出或跳过 → ③ 查看收益和笔记。操作后自动保存，下次选择账户即可继续。': '1. Choose data → 2. Buy, sell or skip '
                                                            'each day → 3. Review returns and '
                                                            'notes. Actions save automatically; '
                                                            'select your practice to resume.',
 '已有行情已就绪，可直接向下开始练习。': 'Saved prices are ready. Continue to the practice below.',
 '上传自己的 CSV（可选）': 'Upload your own CSV (optional)',
 '第 2 步 · 看行情，做决策': 'Step 2 · Review prices and decide',
 '第 3 步 · 查看收益与复盘': 'Step 3 · Review performance',
 '已到最后一个交易日，可查看复盘或重置练习。': 'You reached the last trading day. Review results or reset the practice.',
 '账户管理': 'Practice settings',
 '下载失败，请检查网络后重试。': 'Download failed. Check your connection and retry.',
 '数据导入失败，请检查 CSV 格式。': 'Import failed. Check your CSV format.',
 '收盘后决策': 'Decision after close',
 '订单已成交': 'Order filled',
 '订单被拒绝，时间不会推进：': 'Order rejected; time has not advanced: ',
 'Insufficient cash': 'Insufficient cash'}

ERRORS_ZH = {'A-share T+1: shares bought today cannot be sold': 'A 股 T+1：当天买入的股票不能当天卖出',
 'A-share buys require multiples of 100 shares': 'A 股买入数量必须是100股的整数倍',
 'Cannot trade a zero-volume bar': '当天无成交量，无法交易，可选择跳过',
 'Insufficient cash': '现金不足',
 'Insufficient shares': '可卖持仓不足'}

def translate(text, language):
    if language == "English":
        return TRANSLATIONS.get(text, text)
    return ERRORS_ZH.get(text, text)
