from backend.app import db
from backend.models import Result, User
from flask_login import login_user


def add_user_to_db(username: str, password: str) -> None:
    user_check = User.query.filter_by(username=username).first()
    if user_check is not None:
        raise
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


def check_validate_user(username: str, password: str) -> bool:
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return True
    return False


def check_login_user(username: str, remember: bool) -> None:
    user = User.query.filter_by(username=username).first()
    login_user(user, remember=remember)


def send_success_result_task(uuid: str, msisdn: float, radius: float, delta: float) -> Result:
    result_task = Result(uuid=uuid, msisdn=msisdn, radius=radius, delta=delta)
    db.session.add(result_task)
    db.session.commit()
    return result_task


# TODO: дописать
def get_result_task():
    pass


def get_status_task():
    pass
