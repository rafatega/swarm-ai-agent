from swarm import Agent
from app.google_api_prompts import calendar_agent_system_prompt, main_agent_system_prompt
from app.google_api_calendar_tools import list_calendar_list, list_calendar_events, insert_calendar_event, create_calendar_list

MODEL = 'gpt-4o-mini'


def transfer_to_main_agent():
    return main_agent


def transfer_to_calendar_agent():
    return calendar_agent


main_agent = Agent(
    name='Main Agent',
    model=MODEL,
    instruction=main_agent_system_prompt,
    functions=[transfer_to_calendar_agent]
)

calendar_agent = Agent(
    name='Google Calendar Agent',
    model=MODEL,
    instruction=calendar_agent_system_prompt,
    functions=[transfer_to_main_agent]
)

calendar_agent.functions.extend([
    list_calendar_list,
    list_calendar_events,
    insert_calendar_event,
    create_calendar_list
])
