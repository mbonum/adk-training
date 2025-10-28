from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='agent_pippo',
    description='A helpful assistant for user questions.',
    instruction='Siamo in Italia, rispondi in italiano.',
    # generate_content_config=types.GenerateContentConfig(temperature=0.7, max_output_tokens=1024)
)
