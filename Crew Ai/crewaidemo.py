import os
from crewai import LLM
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from crewai_tools import SerperDevTool


os.environ["OPEN_API_KEY"] = "NA"
os.environ["SERPER_API_KEY"] = "your serper api key"

search_tool=SerperDevTool()

llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434",
    temperature=0.5
)

topic = " The business case for AI Agents in customer support"

Researcher=Agent(
    role="research analyst",
    goal=f"find accurate and citable facts about {topic}",
    backstory="you're a meticulous analyst who never states a number without a source",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

Trend_Analyst=Agent(
    role="Senior News Analyst",
    goal="Synthesize raw web search results, filter out filler, and extract 3 core insights.",
    backstory="You excel at connecting the dots. You take chaotic snippets of information and structure them into clear, actionable bullet points with fact verification."
    ,tools=[search_tool],
    llm=llm,
    verbose=True
)

Content_Strategist_and_Scriptwriter = Agent(
    role="Viral Content Creator",
    goal="get the analysis and write a blog about it in about 50-100 words.",
    backstory="ou are a master storyteller who knows how to hook an audience in the first 3 seconds and explain complex tech simply.",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

research_task = Task(
    description="Search the web for top news regarding {topic} from the past week. Gather headlines, key statistics, and source links.",
    expected_output="A raw research brief containing raw text and source URLs.",
    agent=Researcher
)

analysis_task = Task(
    description = "Review the research brief. Identify the 3 most important takeaways, explain why they matter, and eliminate redundant info.",
    expected_output="A clean 3-bullet summary with context and key stats.",
    agent=Trend_Analyst
)

writing_task =Task(
    description="Take the key takeaways and craft: A 50-100 words blog on the AI and Agentic AI.",
    expected_output="A structured markdown document containing both the script and the post.",
    agent=Content_Strategist_and_Scriptwriter
)

crew=Crew(
    agents=[Researcher,Trend_Analyst,Content_Strategist_and_Scriptwriter ],
    tasks=[research_task,analysis_task,writing_task],
    process=Process.sequential,
    max_rpm=10,
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff(
        inputs={"topic": "Agentic AI developments and tools"}
    )
    print("\n\n########################")
    print("## FINAL CREW OUTPUT ##")
    print("########################\n")
    print(result)