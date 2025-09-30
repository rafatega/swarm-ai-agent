import json
from app.google_api import create_service

client_secret = r"C:\Users\Tega\Documents\Projetos\APIs\client_secret.json"


def construct_google_calendar_client(client_secret):
    """
    Constrói um cliente da API do Google Agenda.

    Parâmetros:
    - client_secret (str): O caminho para o arquivo JSON do client secret.

    Retorna:
    - service: A instância do serviço da API do Google Agenda.
    """
    api_name = 'calendar'
    api_version = 'v3'
    scopes = ['https://www.googleapis.com/auth/calendar']

    service = create_service(client_secret, api_name, api_version, scopes)
    return service


calendar_service = construct_google_calendar_client(client_secret)


def create_calendar_list(calendar_name):
    """
    Cria uma nova lista de calendários.

    Parâmetros:
    - calendar_name (str): O nome da nova lista de calendários.

    Retorna:
    - dict: Um dicionário contendo o ID da nova lista de calendários.
    """
    calendar_list = {
        'summary': calendar_name
    }
    created_calendar_list = calendar_service.calendars().insert(
        body=calendar_list).execute()
    return created_calendar_list


def list_calendar_list(max_capacity=200):
    """
    Lista calendários até que o número total de itens atinja max_capacity.

    Parâmetros:
    - max_capacity (int ou str, opcional): O número máximo de listas de calendários a serem recuperadas. 
      O padrão é 200. Se for fornecida uma string, ela será convertida para inteiro.

    Retorna:
    - list: Uma lista de dicionários contendo informações limpas da lista de calendários, com os campos 
      'id', 'name' e 'description'.
    """
    if isinstance(max_capacity, str):
        max_capacity = int(max_capacity)

    all_calendars = []
    all_calendars_cleaned = []
    next_page_token = None
    capacity_tracker = 0

    while True:
        calendar_list = calendar_service.calendarList().list(
            maxResults=min(200, max_capacity - capacity_tracker),
            pageToken=next_page_token
        ).execute()
        calendars = calendar_list.get('items', [])
        all_calendars.extend(calendars)
        capacity_tracker += len(calendars)
        next_page_token = calendar_list.get('nextPageToken')
        if capacity_tracker >= max_capacity or not next_page_token:
            break

    for calendar in all_calendars:
        all_calendars_cleaned.append(
            {
                'id': calendar['id'],
                'name': calendar['summary'],
                'description': calendar.get('description', '')
            })
    return all_calendars_cleaned


def list_calendar_events(calendar_id, max_capacity=20):
    """
    Lista eventos de um calendário específico até que o número total de eventos atinja max_capacity.

    Parâmetros:
    - calendar_id (str): O ID do calendário do qual listar os eventos.
    - max_capacity (int ou str, opcional): O número máximo de eventos a serem recuperados. O padrão é 20.
      Se uma string for fornecida, será convertida para inteiro.

    Retorna:
    - list: Uma lista de eventos do calendário especificado.
    """
    if isinstance(max_capacity, str):
        max_capacity = int(max_capacity)

    all_events = []
    next_page_token = None
    capacity_tracker = 0

    while True:
        events_list = calendar_service.events().list(
            calendarId=calendar_id,
            maxResults=min(250, max_capacity - capacity_tracker),
            pageToken=next_page_token
        ).execute()

        events = events_list.get('items', [])
        all_events.extend(events)
        capacity_tracker += len(events)
        if capacity_tracker >= max_capacity:
            break
        next_page_token = events_list.get('nextPageToken')
        if not next_page_token:
            break
        return all_events


def insert_calendar_event(calendar_id, **kwargs):
    """
    Insere um evento no calendário especificado.

    Parâmetros:
    - service: A instância do serviço da API do Google Agenda.
    - calendar_id: O ID do calendário onde o evento será inserido.
    - **kwargs: Argumentos nomeados adicionais representando os detalhes do evento.

    Retorna:
    - O evento criado.
    """
    request_body = json.loads(kwargs['kwargs'])
    event = calendar_service.events().insert(
        calendarId=calendar_id,
        body=request_body
    ).execute()
    return event
