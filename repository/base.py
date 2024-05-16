import abc
import logging
from typing import Optional, TypeVar, Generic, List, get_args

from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, inspect, tuple_

from constant.constant import DES
from must.db import db
from must.error import CANNOT_BULK_UPSERT_OBJECTS, CANNOT_GET_OBJECT, CANNOT_GET_LIST_OBJECTS, CANNOT_GET_ALL_COUNT, \
    CANNOT_INSERT_OBJECT, CANNOT_MERGE_MODEL
from serializers.api import SortCriterion

T = TypeVar("T")


class BaseRepository(Generic[T], metaclass=abc.ABCMeta):

    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def get(self, id, *options) -> Optional[T]:
        clazz = get_args(self.__orig_bases__[0])[0]
        columns = inspect(clazz).primary_key
        if len(columns) == 1:
            primary_key = columns[0]
            try:
                query = self.db.session.query(clazz).filter(primary_key == id)
                if options:
                    query = query.options(options)
                entity = query.first()
                return entity
            except:
                self.logger.error(CANNOT_GET_OBJECT, exc_info=True)
                self.db.session.rollback()
                return None
        else:
            return None

    def get_multiple(self, ids) -> List[T]:
        clazz = get_args(self.__orig_bases__[0])[0]
        try:
            query = self.db.session.query(clazz).filter(clazz.id.in_(ids))
            return query.all()
        except:
            self.logger.error(CANNOT_GET_LIST_OBJECTS, exc_info=True)
            self.db.session.rollback()
            return None

    def get_all(self, offset, limit) -> List[T]:
        clazz = get_args(self.__orig_bases__[0])[0]
        try:
            query = self.db.session.query(clazz)
            return self.paginate(query, offset, limit).all()
        except:
            self.logger.error(CANNOT_GET_OBJECT, exc_info=True)
            self.db.session.rollback()
            return []

    def get_all_count(self):
        clazz = get_args(self.__orig_bases__[0])[0]
        try:
            query = self.db.session.query(clazz)
            return query.count()
        except:
            self.logger.error(CANNOT_GET_ALL_COUNT, exc_info=True)
            self.db.session.rollback()
            return 0

    def bulk_insert(self, items):
        try:
            self.db.session.bulk_save_objects(items)
            self.db.session.commit()
            return items
        except:
            self.logger.error(CANNOT_BULK_UPSERT_OBJECTS, exc_info=True)
            self.db.session.rollback()
            return None

    def insert(self, item: T) -> Optional[T]:
        try:
            self.db.session.add(item)
            self.db.session.commit()
            return item
        except:
            self.logger.error(CANNOT_INSERT_OBJECT, exc_info=True)
            self.db.session.rollback()
            return None

    def merge(self, model_object: db.Model, commit=True) -> T:
        try:
            result = self.db.session.merge(model_object)
            if commit:
                self.db.session.commit()
            else:
                self.db.session.flush()
            return result
        except:
            self.logger.error(CANNOT_MERGE_MODEL, exc_info=True)
            self.db.session.rollback()
            return None

    def bulk_upsert(self, models: List[T], commit=True) -> List[T]:
        """
        Bulk insert products
        :param models: the list of products
        :return:
        """
        try:
            clazz = get_args(self.__orig_bases__[0])[0]
            columns = inspect(clazz).primary_key
            if len(columns) == 1:
                primary_key = columns[0]
                primary_key_name = primary_key.name
                models_no_prim = list(
                    filter(
                        lambda model: model.__getattribute__(primary_key_name) is None,
                        models,
                    )
                )
                models_with_prim = list(
                    filter(
                        lambda model: model.__getattribute__(primary_key_name)
                                      is not None,
                        models,
                    )
                )
                bulk_upserted_models = {
                    model.__getattribute__(primary_key_name): model
                    for model in models_with_prim
                }
                for model in (
                    self.db.session.query(clazz)
                        .filter(primary_key.in_(bulk_upserted_models.keys()))
                        .all()
                ):
                    self.db.session.merge(
                        bulk_upserted_models.pop(
                            model.__getattribute__(primary_key_name)
                        )
                    )
                if bulk_upserted_models:
                    self.db.session.add_all(bulk_upserted_models.values())
                if models_no_prim:
                    self.db.session.add_all(models_no_prim)
            else:
                primary_keys = tuple_(*columns)
                bulk_upserted_models = {}
                models_no_prim = []
                for model in models:
                    list_prims = list(
                        str(model.__getattribute__(column.name)) for column in columns
                    )
                    null_keys = list(filter(lambda key: key is None, list_prims))
                    if null_keys:
                        models_no_prim.append(model)
                    else:
                        key = tuple(list_prims)
                        bulk_upserted_models[key] = model
                for model in (
                    self.db.session.query(clazz)
                        .filter(primary_keys.in_(bulk_upserted_models.keys()))
                        .all()
                ):
                    key = tuple(
                        list(
                            str(model.__getattribute__(column.name))
                            for column in columns
                        )
                    )
                    self.db.session.merge(bulk_upserted_models.pop(key))
                if bulk_upserted_models:
                    self.db.session.add_all(bulk_upserted_models.values())
                if models_no_prim:
                    self.db.session.add_all(models_no_prim)
            if commit:
                self.db.session.commit()
            else:
                self.db.session.flush()
            return models
        except:
            self.logger.error(CANNOT_BULK_UPSERT_OBJECTS, exc_info=True)
            self.db.session.rollback()
            return []

    def paginate(self, query, offset, limit):
        return query.offset(offset).limit(limit)

    def add_sort(self, query, list_sort_object: List[SortCriterion], sort_fields: dict):
        if list_sort_object and len(list_sort_object):
            for element in list_sort_object:
                field = element.field
                order = element.order
                if field not in sort_fields:
                    continue
                if order == DES:
                    query = query.order_by(desc(sort_fields[field]))
                else:
                    query = query.order_by(sort_fields[field])
        return query

    def delete(self, model) -> bool:
        try:
            self.db.session.delete(model)
            self.db.session.commit()
            return True
        except Exception as e:
            self.logger.error("Cannot delete model", exc_info=True)
            self.db.session.rollback()
            return False

    def render_query(self, statement, db_session):
        """
        Generate an SQL expression string with bound parameters rendered inline
        for the given SQLAlchemy statement.
        WARNING: This method of escaping is insecure, incomplete, and for debugging
        purposes only. Executing SQL statements with inline-rendered user values is
        extremely insecure.
        Based on http://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query
        """
        from datetime import date, datetime, timedelta
        from sqlalchemy.orm import Query

        if isinstance(statement, Query):
            statement = statement.statement
        dialect = db_session.bind.dialect

        class LiteralCompiler(dialect.statement_compiler):
            def visit_bindparam(
                self,
                bindparam,
                within_columns_clause=False,
                literal_binds=False,
                **kwargs,
            ):
                return self.render_literal_value(bindparam.value, bindparam.type)

            def render_array_value(self, val, item_type):
                if isinstance(val, list):
                    return "{}".format(
                        ",".join([self.render_array_value(x, item_type) for x in val])
                    )
                return self.render_literal_value(val, item_type)

            def render_literal_value(self, value, type_):
                if isinstance(value, int):
                    return str(value)
                elif isinstance(value, (str, date, datetime, timedelta)):
                    return "'{}'".format(str(value).replace("'", "''"))
                elif isinstance(value, list):
                    return "'{{{}}}'".format(
                        ",".join(
                            [self.render_array_value(x, type_.item_type) for x in value]
                        )
                    )
                return super(LiteralCompiler, self).render_literal_value(value, type_)

        return LiteralCompiler(dialect, statement).process(statement)

    def count_from_query(self, query):
        try:
            count = query.count()
            return count
        except:
            self.db.session.rollback()
            return 0

    def paginate_query_by_page(self, base_query, search_schema):
        limit = search_schema.limit
        page = search_schema.page
        offset = limit * (page - 1) if page > 1 else 0
        base_query = base_query.limit(limit).offset(offset)
        return base_query

    def rollback(self):
        self.db.session.rollback()

    def commit(self):
        try:
            self.db.session.commit()
        except:
            self.db.session.rollback()

    def delete_by_id(self, id):
        clazz = get_args(self.__orig_bases__[0])[0]
        columns = inspect(clazz).primary_key
        if len(columns) == 1:
            primary_key = columns[0]
            try:
                result = self.db.session.query(clazz).filter(primary_key == id).delete()
                self.db.session.commit()
                return result
            except:
                self.logger.error("Cannot delete object", exc_info=True)
                self.db.session.rollback()
                return None
        else:
            return 0

    def add_filter_permission_po_cate(self, query, clazz, cate_id_column_name):
        columns = inspect(clazz).columns
        cate_id_column = None
        for column in columns:
            if column.name == cate_id_column_name:
                cate_id_column = column
                break
        user = request.user
        category_permissions = request.user_category_permission_service.get(user.id)
        category_permissions_id = list(
            map(lambda x: x.po_cate_id, category_permissions)
        )
        if category_permissions and cate_id_column is not None:
            query = query.filter(cate_id_column.in_(category_permissions_id))
        return query

    def add_filter_permission_sub_cate(self, query, clazz, sub_cate_column_name):
        columns = inspect(clazz).columns
        cate_id_column = None
        for column in columns:
            if column.name == sub_cate_column_name:
                cate_id_column = column
        user = request.user
        category_permissions = request.user_category_permission_service.get(user.id)
        sub_category_permissions = list(map(lambda x: x.sub_cate, category_permissions))
        if category_permissions and cate_id_column:
            query = query.filter(cate_id_column.in_(sub_category_permissions))
        return query
