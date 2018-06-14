# -*- coding: utf-8 -*-

import os
import sys

from apps.trade.execution import OrderMatcher
from apps.trade.models import User, Order, Balance
from apps.trade.trade_application import TradeApplication

ROOT_PATH = os.path.abspath( os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert( 0, ROOT_PATH)

import unittest
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import  datetime
import mock

TradeApplication.instance().publish = mock.MagicMock()


class BaseTest(unittest.TestCase):

    def tearDown(self):
        self.db_session.commit()

    def setUp(self):

        OrderMatcher.get(u'BTCUSD').clean()

        self.balance1 = self.db_session.query(Balance).filter_by(id=1).first()
        self.balance1.balance = 1000 * 2
        self.balance2 = self.db_session.query(Balance).filter_by(id=2).first()
        self.balance2.balance = 1000 * 2

        self.order = self.db_session.query(Order).filter(Order.id == 1).first()
        self.order.account_id = '90000002'
        self.order.status = '0'
        self.order.side = '1'
        self.order.type = '2' # 限价
        self.order.price = 5
        self.order.order_qty = 100
        self.order.leaves_qty = 100
        self.order.cum_qty = 0
        self.order.cxl_qty = 0
        self.order.has_cxl_qty = 0
        self.order.has_cum_qty = 0
        self.order.has_leaves_qty = 1

        # 对手盘
        self.balance3 = self.db_session.query(Balance).filter_by(id=3).first()
        self.balance3.balance = 1000 * 2
        self.balance4 = self.db_session.query(Balance).filter_by(id=4).first()
        self.balance4.balance = 1000 * 2

        self.order1 = self.db_session.query(Order).filter(Order.id == 2).first()
        self.order1.account_id = '90000003'
        self.order1.status = '0'
        self.order1.side = '2'
        self.order1.price = 5
        self.order1.type = '2' # 限价
        self.order1.order_qty = 100
        self.order1.leaves_qty = 100
        self.order1.cum_qty = 0
        self.order1.cxl_qty = 0
        self.order1.has_cxl_qty = 0
        self.order1.has_cum_qty = 0
        self.order1.has_leaves_qty = 1

    @classmethod
    def tearDownClass(self):
        # 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
        print('4444444')

    @classmethod
    def setUpClass(self):
        # 必须使用@classmethod 装饰器,所有test运行前运行一次
        self.engine = create_engine('sqlite:////Users/newcity/study/bitex/db/bitex.sqlite', echo=False)
        self.db_session = scoped_session(sessionmaker(bind=self.engine))
        TradeApplication.instance().db_session = self.db_session

class UserTest(BaseTest):
    def testAuthenticate(self):
        # User.signup(self.db_session, 'rodrigo', 'r@blinktrade.com', 'abc12345', 'NY', 'US', 5)
        self.assertTrue(User.authenticate(self.db_session, 5, 'rodrigo', 'abc12345', None) is not None)

    # 对等匹配
    def test_001(self):
        # 初始化数据
        OrderMatcher.get(u'BTCUSD').match(self.db_session, self.order1, False)

        self.order.order_qty = 100
        self.order.leaves_qty = 100

        OrderMatcher.get(u'BTCUSD').match(self.db_session,self.order,False,60)

        self.assertTrue(self.balance1.balance == 2100)
        self.assertTrue(self.balance2.balance == 2000)

        self.assertTrue(self.balance3.balance == 1900)
        self.assertTrue(self.balance4.balance == 2000)
        self.assertTrue(self.order.status == '2')

    # 部分匹配
    def test_002(self):
        # 初始化数据
        OrderMatcher.get(u'BTCUSD').match(self.db_session, self.order1, False)

        self.order.order_qty = 50
        self.order.leaves_qty = 50

        OrderMatcher.get(u'BTCUSD').match(self.db_session,self.order,False,60)

        self.assertTrue(self.balance1.balance == 2050)
        self.assertTrue(self.balance2.balance == 2000)

        self.assertTrue(self.balance3.balance == 1950)
        self.assertTrue(self.balance4.balance == 2000)
        self.assertTrue(self.order.status == '2')
        self.assertTrue(self.order1.status == '1')

    # 冗余匹配
    def test_003(self):
        # 初始化数据
        OrderMatcher.get(u'BTCUSD').match(self.db_session, self.order1, False)

        self.order.order_qty = 200
        self.order.leaves_qty = 200

        OrderMatcher.get(u'BTCUSD').match(self.db_session,self.order,False,60)

        self.assertTrue(self.balance1.balance == 2100)
        self.assertTrue(self.balance2.balance == 2000)

        self.assertTrue(self.balance3.balance == 1900)
        self.assertTrue(self.balance4.balance == 2000)
        self.assertTrue(self.order.status == '1')
        self.assertTrue(self.order1.status == '2')

    # 市价匹配
    def test_004(self):
        # 初始化数据
        OrderMatcher.get(u'BTCUSD').match(self.db_session, self.order1, False)

        self.order1.price = 15

        self.order.order_qty = 100
        self.order.leaves_qty = 100
        self.order.price = 5
        self.order.type = '1'

        OrderMatcher.get(u'BTCUSD').match(self.db_session,self.order,False,60)

        self.assertTrue(self.balance1.balance == 2100)
        self.assertTrue(self.balance2.balance == 2000)

        self.assertTrue(self.balance3.balance == 1900)
        self.assertTrue(self.balance4.balance == 2000)
        self.assertTrue(self.order.status == '2')
        self.assertTrue(self.order1.status == '2')

    # 自动取消个人上笔交易
    def test_005(self):
        # 初始化数据
        OrderMatcher.get(u'BTCUSD').match(self.db_session, self.order1, False)

        self.order1.account_id = '90000002'

        self.order.order_qty = 100
        self.order.leaves_qty = 100
        self.order.price = 5

        OrderMatcher.get(u'BTCUSD').match(self.db_session,self.order,False,60)

        self.assertTrue(self.balance1.balance == 2000)
        self.assertTrue(self.balance2.balance == 2000)

        self.assertTrue(self.balance3.balance == 2000)
        self.assertTrue(self.balance4.balance == 2000)
        self.assertTrue(self.order.status == '0')
        self.assertTrue(self.order1.status == '4')
