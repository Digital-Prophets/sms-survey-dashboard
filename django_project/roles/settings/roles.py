# coding=utf-8
__author__ = "Alison Mukoma <mukomalison@gmail.com>Alison "
__date__ = "15/12/2021"


from rolepermissions.roles import AbstractUserRole


class User(AbstractUserRole):
    available_permissions = {}
