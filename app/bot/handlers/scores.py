from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.bot.models import Student, Score
from app.db.connection import Transaction


scores_router = Router()


class ScoreEntryState(StatesGroup):
    subject = State()
    score = State()


@scores_router.message(commands=["enter_scores"])
async def start_score_entry(message: Message, state: FSMContext):
    await message.answer("Введите название предмета:")
    await state.set_state(ScoreEntryState.subject)


@scores_router.message(ScoreEntryState.subject)
async def get_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("Введите ваш балл:")
    await state.set_state(ScoreEntryState.score)


@scores_router.message(ScoreEntryState.score)
async def finish_score_entry(message: Message, state: FSMContext):
    user_data = await state.get_data()
    async with Transaction():
        student = await Student.get_student(student_id=message.from_user.id)
        if not student:
            await message.answer("Вы не зарегистрированы.")
            return
        new_score = Score(
            subject=user_data["subject"],
            score=int(message.text),
            student_id=student.id
        )
        await Score.register_subject(
            student_id=new_score.student_id,
            subject=new_score.subject,
            score=new_score.score
        )

    await state.clear()
    await message.answer("Балл успешно сохранен!")


@scores_router.message(commands=["view_scores"])
async def view_scores(message: Message):
    async with Transaction():
        student = await Student.get_student(student_id=message.from_user.id)
        if not student:
            await message.answer("Вы не зарегистрированы.")
            return
        scores = await Score.get_all_scores(student_id=message.from_user.id)

        response = "\n".join([f"{subject.subject}: {subject.score}" for subject in scores]) if scores else "У вас еще нет сохраненных баллов."
        await message.answer(response)
