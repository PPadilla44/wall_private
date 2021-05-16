from logging import StrFormatStyle
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
from flask_app import app

import datetime, timeago

class Message:
    def __init__(self,data):
        self.id = data['id']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all_received_mssgs(cls,data):
        query = "SELECT * from messages JOIN users as sender on sender.id = \
        messages.sender_id JOIN users as receiver on receiver.id = \
        messages.receiver_id WHERE receiver_id = %(id)s ORDER BY messages.created_at desc;"
        return connectToMySQL('wall_schema').query_db(query,data)


    @classmethod
    def count_all_received_mssgs(cls,data):
        query = "SELECT Count(*) from messages JOIN users as sender on sender.id = \
        messages.sender_id JOIN users as receiver on receiver.id = \
        messages.receiver_id WHERE receiver_id = %(id)s;"
        results = connectToMySQL('wall_schema').query_db(query,data)
        return results[0]


    @classmethod
    def count_all_sent_mssgs(cls,data):
        query = "SELECT Count(*) from messages JOIN users as sender on sender.id = \
        messages.sender_id JOIN users as receiver on receiver.id = \
        messages.receiver_id WHERE sender_id = %(id)s;"
        results = connectToMySQL('wall_schema').query_db(query,data)
        return results[0]


    @classmethod
    def send_mssg(cls,data):
        query = "INSERT INTO messages (sender_id,receiver_id,content,created_at,updated_at) \
        VALUES (%(sender)s,%(receiver)s,%(content)s,NOW(),NOW());"
        return connectToMySQL('wall_schema').query_db(query,data)

    @classmethod
    def delete_mssg(cls,data):
        query = "DELETE FROM messages WHERE id = %(msg_id)s;"
        return connectToMySQL('wall_schema').query_db(query,data)

    @classmethod
    def delete_mssg_from_user(cls,data):
        query = "DELETE FROM messages WHERE sender_id = %(id)s OR receiver_id = %(id)s;"
        return connectToMySQL('wall_schema').query_db(query,data)


    @classmethod
    def get_timeof_all_received_mssgs(cls,data):
        
        dates = Message.get_all_received_mssgs(data)
        now = datetime.datetime.now()

        times_ago = []

        for time in dates:
            times_ago.append(timeago.format(time['created_at'],now))        
        return times_ago
