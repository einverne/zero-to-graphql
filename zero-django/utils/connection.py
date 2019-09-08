#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graphene import Int
from graphene import relay


class CountableConnectionBase(relay.Connection):
    class Meta:
        abstract = True

    total_count = Int()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()
