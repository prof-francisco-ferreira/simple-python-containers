# -*- coding: utf-8 -*-
#!usr/bin/env python3

"""


"""
import logging
import os

from flask import Flask, json, jsonify, request
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

logging.basicConfig(filename='main.log', level=logging.INFO)

@app.route('/')
def help():
    """Help
    """
    help = {}    
    help['1+1'] = '2'
    return jsonify(help)

@app.route('/soma2/<int:number1>/<int:number2>', methods=["GET", "POST"])
def sum2(number1, number2):
    """Return sum two numbers from arguments
    """
    result = f"{number1} + {number2} = {(number2+number1)}"
    app.logger.info(result)  
    return jsonify(result)

@app.route('/soma1/<int:number>', methods=["GET", "POST"])
def sum(number):
    try:
        current_value = redis.get('soma') or 0
        result = f"Previous value: {current_value}. Value informed: {number}. "
        current_value = int(current_value) + int(number)
        redis.set('soma', current_value)
        result = f"{result} Sum: {current_value}. "                        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': 'Erro: {}'.format(str(e)) }), 500

def get_env_or_default(ENV: str, default: str):
    """Gets environment variables or sets a default

    Args:
        ENV (str): the Env variable
        default (str): the default value to return if ENV is not find

    Returns:
        The value of ENV or default
    """
    if os.environ.get(ENV):
        app.logger.info("ENV {}".format(os.environ.get(ENV)))
        return os.environ.get(ENV)
    return default

if __name__ == '__main__':
    app_args = {}

    app_args["host"] = get_env_or_default("A_HOST", '0.0.0.0')
    app_args["port"] = int(get_env_or_default("A_PORT", 5001))
    app_args["debug"] = bool(get_env_or_default("A_DEBUG", True))

    app.run(**app_args)