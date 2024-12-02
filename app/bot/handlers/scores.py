from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.bot.models import Student, Score
from app.db.connection import Transaction


scores_router = Router()


class ScoreEntryState(StatesGroup):
    subject = State()
    score = State()


@scores_router.message(Command(commands=["enter_scores"]))
async def start_score_entry(message: Message, state: FSMContext):
    await message.answer("Введите название предмета:")
    await state.set_state(ScoreEntryState.subject)


@scores_router.message(ScoreEntryState.subject)
async def get_subject(message: Message, state: FSMContext):
    async with Transaction():
        student = await Student.get_student(student_id=message.from_user.id)
        if not student:
            await message.answer("Вы не зарегистрированы.")
            await state.clear()
            return

        subject_name = message.text.strip()
        existing_scores = await Score.get_all_scores(student_id=student.id)
        if any(score.subject.lower() == subject_name.lower() for score in existing_scores):
            await message.answer("Вы уже ввели баллы для этого предмета. Попробуйте снова.")
            return

        await state.update_data(subject=subject_name)
        await message.answer("Введите ваш балл:")
        await state.set_state(ScoreEntryState.score)


@scores_router.message(ScoreEntryState.score)
async def finish_score_entry(message: Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        score_value = int(message.text.strip())
        if score_value < 0 or score_value > 100:
            await message.answer("Пожалуйста, введите число от 0 до 100.")
            return
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")
        return

    async with Transaction():
        student = await Student.get_student(student_id=message.from_user.id)
        if not student:
            await message.answer("Вы не зарегистрированы.")
            await state.clear()
            return

        new_score = Score(
            subject=user_data["subject"],
            score=score_value,
            student_id=student.id
        )
        await Score.register_subject(
            student_id=new_score.student_id,
            subject=new_score.subject,
            score=new_score.score
        )

    await state.clear()
    await message.answer("Балл успешно сохранен!")


@scores_router.message(Command(commands=["view_scores"]))
async def view_scores(message: Message):
    async with Transaction():
        student = await Student.get_student(student_id=message.from_user.id)
        if not student:
            await message.answer("Вы не зарегистрированы.")
            return

        scores = await Score.get_all_scores(student_id=message.from_user.id)

        if scores:
            scores_text = "\n".join([f"{subject.subject}: {subject.score}" for subject in scores])
            response = (
                f"{student.first_name} {student.last_name}, ваши результаты:\n"
                f"{scores_text}\n\nОтличный результат, так держать!"
            )
        else:
            response = f"{student.first_name} {student.last_name}, у вас еще нет сохраненных баллов."

        await message.answer(response)
