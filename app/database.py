from sqlalchemy import (
    Float,
    Integer,
    Text,
    create_engine,
    delete,
    select,
    update,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

engine = create_engine("sqlite:///urdoc.db", echo=False)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# class User(Base):
#     __tablename__ = "user"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(Text, nullable=True)
#     role: Mapped[str] = mapped_column(Text, nullable=True)


class Model(Base):
    __tablename__ = "model"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    use: Mapped[bool] = mapped_column(Integer, nullable=True)
    free: Mapped[bool] = mapped_column(Integer, nullable=True)
    platform: Mapped[str] = mapped_column(Text, nullable=True)
    series: Mapped[str] = mapped_column(Text, nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=True)
    module: Mapped[str] = mapped_column(Text, nullable=True)
    price_input: Mapped[float] = mapped_column(Float, nullable=True)
    price_output: Mapped[float] = mapped_column(Float, nullable=True)


class Prompt(Base):
    __tablename__ = "prompt"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    use: Mapped[bool] = mapped_column(Integer, nullable=True)
    category: Mapped[str] = mapped_column(Text, nullable=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=True)
    memo: Mapped[str] = mapped_column(Text, nullable=True)
    model: Mapped[str] = mapped_column(Text, nullable=True)
    creator: Mapped[str] = mapped_column(Text, nullable=True)
    public: Mapped[bool] = mapped_column(Integer, nullable=True)


class Case(Base):
    __tablename__ = "case"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    creator: Mapped[str] = mapped_column(Text, nullable=True)
    profile: Mapped[str] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    test: Mapped[str] = mapped_column(Text, nullable=True)
    story: Mapped[str] = mapped_column(Text, nullable=True)
    book: Mapped[str] = mapped_column(Text, nullable=False)
    chapter: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False)


# def create_table(table: Base):
#     Base.metadata.create_all(engine, tables=[table.__table__])


# ####################### CRUD - READ ###############################
# # @st.cache_data(ttl=60)
# def read_table(table: str):
#     query = f'SELECT * FROM "{table}"'
#     return pd.read_sql(query, con=engine)


# ###################################################################
# #### model - CREAT ####
# @st.dialog("添加模型")
# def create_model():
#     use = st.checkbox("使用")
#     free = st.checkbox("免费")
#     platform = st.text_input("平台")
#     series = st.text_input("系列")
#     name = st.text_input("名称")
#     module = st.text_input("模块")
#     price_input = st.number_input("输入价格")
#     price_output = st.number_input("输出价格")
#     col_confirm, col_cancel = st.columns(2)
#     with col_confirm:
#         if st.button("**添加**", use_container_width=True):
#             model = Model(
#                 use=use,
#                 free=free,
#                 platform=platform,
#                 series=series,
#                 name=name,
#                 module=module,
#                 price_input=price_input,
#                 price_output=price_output,
#             )
#             with Session() as session:
#                 session.add(model)
#                 session.commit()
#             st.rerun()
#     with col_cancel:
#         if st.button("**取消**", use_container_width=True):
#             st.rerun()


# #### model - READ #####
# def read_use_model():
#     return pd.read_sql(
#         "SELECT name, module FROM model WHERE use=True", con=engine
#     ).to_dict(orient="records")

def read_use_model():
    with Session() as session:
        result = session.execute(select(Model).where(Model.use == True))
        model = result.scalar()
    return model.name

# #### model - UPDATE #####
# def update_model(modified_models: pd.DataFrame):
#     with Session() as session:
#         session.bulk_update_mappings(Model, modified_models.to_dict(orient="records"))
#         session.commit()
#     return


# #### model - DELETE #####
# @st.dialog("删除模型")
# def delete_model(models_df: pd.DataFrame):
#     id = st.number_input("id", min_value=1, step=1)
#     model = models_df.loc[models_df["id"] == id]
#     if not model.empty:
#         model.columns = [
#             "ID",
#             "使用",
#             "免费",
#             "平台",
#             "系列",
#             "名称",
#             "模块",
#             "输入价格",
#             "输出价格",
#         ]
#         model = model.astype(str)
#         model_T = model.T.reset_index()
#         model_T.columns = ["name", "info"]
#         st.dataframe(
#             model_T,
#             use_container_width=True,
#             hide_index=True,
#             column_config={
#                 "name": st.column_config.TextColumn(
#                     "项目",
#                 ),
#                 "info": st.column_config.TextColumn(
#                     "信息",
#                 ),
#             },
#         )
#     else:
#         st.markdown("没有相关模型")
#     col_confirm, col_cancel = st.columns(2)
#     with col_confirm:
#         if st.button("**删除**", use_container_width=True):
#             with Session() as session:
#                 session.execute(delete(Model).where(Model.id == id))
#                 session.commit()
#             st.rerun()
#     with col_cancel:
#         if st.button("**取消**", use_container_width=True):
#             st.rerun()


# ###################################################################
# #### user - CREATE ####
# @st.dialog("注册验证")
# def create_user(username, password):
#     st.markdown(f"**用户名：{username}**")
#     validate_password = st.text_input("**再次输入密码**", type="password")
#     if st.button("**确认注册**"):
#         if password == validate_password:
#             with Session() as session:
#                 user = User(name=username, password=password, role="student")
#                 session.add(user)
#                 session.commit()
#             st.rerun()
#         else:
#             st.warning(":material/key: **密码错误**")


# #### user - READ ####
# def read_user_role(username: str) -> str:
#     with Session() as session:
#         result = session.execute(select(User).where(User.name == username))
#         user = result.scalar()
#     return user.role


# def read_user_exist(username: str) -> bool:
#     with Session() as session:
#         result = session.execute(select(User).where(User.name == username))
#         user = result.scalar()
#     return True if user else False


# def read_user_login(username, password):
#     with Session() as session:
#         result = session.execute(select(User).where(User.name == username))
#         user = result.scalar()
#     return True if user and user.password == password else False


# #### user - UPDATE ####
# @st.dialog("更改权限")
# def update_user_role():
#     username = st.text_input("**用户名**")
#     role = st.selectbox("**权限**", ["student", "teacher"])
#     if st.button("更改"):
#         with Session() as session:
#             session.execute(update(User).where(User.name == username).values(role=role))
#             session.commit()
#         st.rerun()
#     return


# ###################################################################
# #### chapter - CREATE ####
# # @st.dialog("添加章节")
# # def create_case_category():
# #     book = st.text_input("**教科书**")
# #     chapter = st.text_input("**章节**")
# #     subject = st.text_input("**主题**")
# #     if st.button("添加"):
# #         with Session() as session:
# #             category = Category(book=book, chapter=chapter, subject=subject)
# #             session.add(category)
# #             session.commit()
# #         st.rerun()
# #     return


# #########################################################

# #################### prompt - CREATE ####################
# def create_prompt(
#     category: str, prompt: str, memo: str, model: str, creator: str, public: bool
# ):
#     with Session() as session:
#         prompt = Prompt(
#             category=category,
#             prompt=prompt,
#             memo=memo,
#             model=model,
#             creator=creator,
#             public=public,
#         )
#         session.add(prompt)
#         session.commit()
#     return


# #################### prompt - READ ####################
# def read_prompt(category: str, creator: str = None) -> list[dict]:
#     query = "SELECT * FROM prompt WHERE (creator = ? OR public = True) AND category = ?"
#     return pd.read_sql(
#         query,
#         con=engine,
#         params=(creator, category),
#     ).to_dict(orient="records")

def read_use_prompt(category: str):
    with Session() as session:
        result = session.execute(select(Prompt).where(Prompt.category == category, Prompt.use == True))
        prompt = result.scalar()
    return prompt.prompt

# #################### prompt - UPDATE ####################
# def update_prompt(
#     id: str,
#     category: str,
#     prompt: str,
#     memo: str,
#     model: str,
#     creator: str,
#     public: bool,
# ):
#     with Session() as session:
#         session.execute(
#             update(Prompt)
#             .where(Prompt.id == id)
#             .values(
#                 category=category,
#                 prompt=prompt,
#                 memo=memo,
#                 model=model,
#                 creator=creator,
#                 public=public,
#             )
#         )
#         session.commit()
#     return


# #################### prompt - DELETE ####################
# def delete_prompt(id: str):
#     with Session() as session:
#         session.execute(delete(Prompt).where(Prompt.id == id))
#         session.commit()
#     return

# #########################################################

# #############################################################
# #### case - CREATE ####
# def create_case(
#     creator: str,
#     profile: str,
#     content: str,
#     test: str,
#     story: str,
#     book: str,
#     chapter: str,
#     subject: str,
# ):
#     case = Case(
#         creator=creator,
#         profile=profile,
#         content=content,
#         test=test,
#         story=story,
#         book=book,
#         chapter=chapter,
#         subject=subject,
#     )
#     with Session() as session:
#         session.add(case)
#         session.commit()
#     return


# #### case - READ ####
# def read_case(id: str, field: str = None) -> Case | None:
#     with Session() as session:
#         result = session.execute(select(Case).where(Case.id == id))
#         case = result.scalar()
#     if case is None:
#         return None
#     if field:
#         return getattr(case, field)
#     else:
#         return case

def read_case(id:int):
    with Session() as session:
        result = session.execute(select(Case).where(Case.id == id))
        case = result.scalar()
    return case.content

# #### case - UPDATE ####
# @st.dialog("更改病例类别")
# def update_case_info(case: Case):
#     profile = st.text_input("**简介**", value=case.profile)
#     book = st.text_input("**教科书**", value=case.book)
#     chapter = st.text_input("**章节**", value=case.chapter)
#     subject = st.text_input("**主题**", value=case.subject)
#     if st.button("更新"):
#         with Session() as session:
#             session.execute(
#                 update(Case)
#                 .where(Case.id == case.id)
#                 .values(profile=profile, book=book, chapter=chapter, subject=subject)
#             )
#             session.commit()
#         st.rerun()
#     return


# def update_case_field(id: str, field: str, value: str):
#     with Session() as session:
#         session.execute(update(Case).where(Case.id == id).values(**{field: value}))
#         session.commit()
#     return


# #### case - DELETE ####
# def delete_case(id):
#     with Session() as session:
#         session.execute(delete(Case).where(Case.id == id))
#         session.commit()
#     return
