from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def verify_answers(given_answers, real_answers, db):
    for input in given_answers:
        real_answer_query = db.query(real_answers).filter(real_answers.id == input.question_id)
        real_answer = real_answer_query.first()
        if real_answer == input.answer:
            real_answer_query.update({real_answers.passed:True},synchronize_session=False)
                