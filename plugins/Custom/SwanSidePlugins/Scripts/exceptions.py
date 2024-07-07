#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

class PublishNukeFailed(Exception):

    def __init__(self, message, path):
        self.path = path
        self.message = message
        super().__init__(self.message)
