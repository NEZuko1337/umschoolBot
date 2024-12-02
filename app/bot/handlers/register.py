from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.bot.models import Student
from app.db.connection import Transaction

register_router = Router()

class RegistrationState(StatesGroup):
    first_name = State()
    last_name = State()

@register_router.message(commands=["register"])
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(RegistrationState.first_name)

@register_router.message(RegistrationState.first_name)
async def get_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Введите вашу фамилию:")
    await state.set_state(RegistrationState.last_name)

@register_router.message(RegistrationState.last_name)
async def finish_registration(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = message.from_user.id
    new_student = Student(
        id=user_id,
        first_name=user_data["first_name"],
        last_name=message.text
    )
    async with Transaction():
        await Student.register_student(
            user_id=new_student.id,
            first_name=new_student.first_name,
            last_name=new_student.last_name
        )
    await state.clear()
    await message.answer("Вы успешно зарегистрированы!")
