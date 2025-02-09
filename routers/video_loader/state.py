from aiogram.fsm.state import StatesGroup, State



class VideoDetails(StatesGroup):
    link = State()
