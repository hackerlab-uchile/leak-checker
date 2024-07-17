import copy
from typing import Any, TypeVar

from core.database import Base
from models.emails import Email
from schemas.emails import EmailCreate as EmailCreateSchema
from sqlalchemy import any_, select
from sqlalchemy.orm import Session

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()

T = TypeVar("T", bound=Any)


def filter_already_added(db: Session, email_list: list[str]) -> list[str]:
    # emails_to_create = copy.deepcopy(list(email_list))
    emails_to_create = []
    # existing_emails = db.query(Email).where(Email.value.in_(email_list)).all()
    print(f"Emails to create: {emails_to_create[:3]}")
    # validated_user_ids = db.scalars(
    #     select(Users.user_id).where(Users.user_id.in_(user_ids_list))
    # ).all()
    existing_emails = []
    index = 0
    while index <= len(email_list):
        existing_emails += (
            db.query(Email)
            .where(Email.value.in_(email_list[index : index + 50000]))
            .all()
        )
        index += 50000
    print(f"Number of existing emails: {len(existing_emails)}")
    filtered = filter(lambda x: x not in existing_emails, email_list)
    # for email in email_list:
    #     if email not in existing_emails:
    #         emails_to_create.append(email)
    # return emails_to_create
    return list(filtered)


def create_all_emails(db: Session, email_list: set[str]) -> list[Email]:
    filtered_email_list = filter_already_added(db, list(email_list))
    # print(f"Emails to add: {filtered_email_list}")
    print(f"Total emails to add: {len(filtered_email_list)}")
    emails_to_create: list[Email] = []
    for email in filtered_email_list:
        instance = Email(value=email)
        emails_to_create.append(instance)
    if len(emails_to_create) > 0 and False:
        db.add_all(emails_to_create)
        db.commit()
    return emails_to_create


# def create_all_emails(db: Session, email_list: list[EmailCreateSchema]) -> list[Email]:
#     emails_to_create: list[Email] = []
#     for email in email_list:
#         instance = db.query(Email).filter_by(**email.model_dump()).one_or_none()
#         if instance:
#             continue
#         else:
#             instance = Email(**email.model_dump())
#             emails_to_create.append(instance)
#     db.add_all(emails_to_create)
#     db.commit()
#     return emails_to_create


def get_or_create(db: Session, model: T, **kwargs) -> T:
    instance = db.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
        return instance
