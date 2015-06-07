# -*- coding: utf-8 -*-
{
    'name': "Cubie Odoo Basico",
    'summary': """
        Modulo base para inciar con proyecto de domotica 
        utilizando Cubiboard y Odoo.""",
    'description': """
        Con este modulo se propone empezar a hacer pruebas
        con conexión a hardware utilizando un cubieboard ARM.
    """,
    'author': "Pablo Esteban Riaño",
    'category': 'Domotica',
    'version': '0.1',
    'depends': [
        'base'
    ],
    'data': [
        'views/led_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
}