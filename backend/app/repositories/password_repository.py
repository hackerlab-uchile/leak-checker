from models.password import Password
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session


def add_or_create_all_passwords(
    db: Session, list_passwords: list[Password]
) -> list[Password]:
    saved_passwords = []
    # Construct the SQL statement
    chunk_size = 20000
    for i in range(0, len(list_passwords), chunk_size):
        insert_stmt = insert(Password).values(
            [
                {"hash_password": item.hash_password, "count": item.count}
                for item in list_passwords[i : i + chunk_size]
            ]
        )
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=["hash_password"],
            set_=dict(count=Password.__table__.c.count + insert_stmt.excluded.count),
        )
        # Execute the statement
        db.execute(do_update_stmt)
        db.flush()

    return saved_passwords
