HEALTH_ANALYSIS_PROMPT = """
Analyze the following health data and provide insights:
{health_data}

Please provide:
1. Overall health status summary
2. Notable trends or patterns
3. Potential areas of concern
4. Recommendations for improvement
5. Positive achievements to highlight

Format the response in a clear, structured way.
"""

HEALTH_RECOMMENDATION_PROMPT = """
Based on the following health metrics:
{health_metrics}

Generate personalized recommendations for:
1. Exercise routine
2. Sleep optimization
3. Diet suggestions
4. Stress management
5. Lifestyle improvements

Consider the user's current habits and limitations.
"""

HEALTH_GOAL_SETTING_PROMPT = """
Based on the user's current health data:
{current_data}

And their stated goals:
{goals}

Generate:
1. Specific, measurable goals
2. Timeline for achievement
3. Milestone markers
4. Actionable steps
5. Progress tracking methods
""" 