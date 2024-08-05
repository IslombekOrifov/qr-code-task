import asyncpg
from typing import Union
import datetime

from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, user_id, full_name):
        sql = "INSERT INTO main_telegramuser (user_id, full_name) VALUES($1, $2) returning *"
        return await self.execute(sql,  user_id, full_name, fetchrow=True)
    
    async def select_all_users(self):
        sql = "SELECT * FROM main_telegramuser"
        return await self.execute(sql, fetch=True)
    
    async def get_user(self, user_id):
        sql = "SELECT * FROM main_telegramuser WHERE user_id = $1;"
        return await self.execute(sql, user_id, fetchrow=True)

    async def add_qrcode(self,  user_id, qrcode, uid, is_active, is_end):
        sql = "INSERT INTO  main_userqrcode(user_id, qr_code, uid, is_active, is_end) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql,  user_id, qrcode, uid, is_active, is_end, fetchrow=True)
    
    async def get_qrcode(self, user_id: int):
        sql = """SELECT uq.* FROM main_userqrcode uq 
                 JOIN main_telegramuser tu ON uq.user_id = tu.id 
                 WHERE tu.user_id = $1 ORDER BY uq.id DESC 
                 LIMIT 1;"""
        return await self.execute(sql, user_id, fetchrow=True)

    async def get_qrcodes(self, user_id: int):
        sql = """SELECT uq.* FROM main_userqrcode uq 
                 JOIN main_telegramuser tu ON uq.user_id = tu.id 
                 WHERE uq.is_active = true AND tu.user_id = $1;"""
        return await self.execute(sql, user_id, fetch=True)
    
    async def get_working_qrcodes(self, user_id: int):
        sql = """SELECT uq.* FROM main_userqrcode uq 
                 JOIN main_telegramuser tu ON uq.user_id = tu.id 
                 WHERE uq.is_active = false AND uq.is_end = false AND tu.user_id = $1;"""
        return await self.execute(sql, user_id, fetch=True)
    
    async def get_active_qrs_count(self, user_id: int):
        sql = """SELECT COUNT(uq.id) FROM main_userqrcode uq 
                 JOIN main_telegramuser tu ON uq.user_id = tu.id 
                 WHERE uq.is_active = true AND uq.is_end = false  AND tu.user_id = $1;"""
        return await self.execute(sql, user_id, fetchrow=True)
    
    async def get_working_qrs_count(self, user_id: int):
        sql = """SELECT COUNT(uq.id) FROM main_userqrcode uq 
                 JOIN main_telegramuser tu ON uq.user_id = tu.id 
                 WHERE uq.is_active = false AND uq.is_end = false AND tu.user_id = $1;"""
        return await self.execute(sql, user_id, fetchrow=True)
   
    async def activate_qr_code(self, start_time, qr_id):
        sql = """UPDATE main_userqrcode
                 SET is_active = false, is_end = false, start_time = $1
                 WHERE id = $2;"""
        return await self.execute(sql, start_time, qr_id, fetchrow=True)
    
    async def finish_qr_code(self, end_time, cost, qr_id):
        sql = """UPDATE main_userqrcode
                 SET is_active = false, is_end = true, end_time = $1, cost = $2
                 WHERE id = $3;"""
        return await self.execute(sql, end_time, cost, qr_id, fetchrow=True)
   
    async def get_price(self):
        sql = "SELECT * FROM main_pricing ORDER BY id DESC LIMIT 1;"
        return await self.execute(sql, fetchrow=True)