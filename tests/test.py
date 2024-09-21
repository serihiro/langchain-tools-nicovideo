from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType
from langchain import hub

from langchain_tools_nicovideo.tools.nicovideo.tool import NicovideoQueryRun
from langchain_tools_nicovideo.utilities import NicovideoSnapshotApiWrapper

llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)
tools = load_tools(["human"], llm=llm)

niconicoAPIClient = SnapshotSearchAPIV2()
tools.append(
    NicovideoQueryRun(
        api_wrapper=NicovideoSnapshotApiWrapper(
            nicovideo_client=niconicoAPIClient,
            nicovideo_field_type=FieldType,
            nicovideo_agent_name="NicoApiClient",
        )
    )
)
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)
response = agent_executor.invoke({"input": "みっくみくにしてやんよの再生数は？"})
print(response)
