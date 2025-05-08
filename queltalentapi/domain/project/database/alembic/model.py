from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint


class AttendeeDatabaseModel(BaseModel):
    __tablename__ = "attendees"

    prim = Column(Integer, primary_key=True)

    id = Column(String, index=True, nullable=False)  # FIXME use an association table later ? (id might not be consistent across occurrences though )
    is_staff = Column(Boolean, nullable=False, default=False)
    occurrence_id = Column(Integer, index=True, nullable=False)
    team_id = Column(Integer, index=True, nullable=False)

    __table_args__ = (
        UniqueConstraint('id', 'occurrence_id', name='uq_user_occurrence'),
    )
