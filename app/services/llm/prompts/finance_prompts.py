FINANCE_ANALYSIS_PROMPT = """
Analyze the following financial data and provide insights:
{finance_data}

Please provide:
1. Overall financial health summary
2. Spending patterns and trends
3. Investment performance
4. Areas for potential savings
5. Financial goals progress

Format the response in a clear, structured way.
"""

FINANCE_RECOMMENDATION_PROMPT = """
Based on the following financial metrics:
{finance_metrics}

Generate personalized recommendations for:
1. Budget optimization
2. Investment strategies
3. Savings opportunities
4. Debt management
5. Financial planning

Consider the user's current financial situation and goals.
"""

FINANCE_GOAL_SETTING_PROMPT = """
Based on the user's current financial data:
{current_data}

And their stated goals:
{goals}

Generate:
1. Specific financial goals
2. Timeline for achievement
3. Milestone markers
4. Actionable steps
5. Progress tracking methods
""" 