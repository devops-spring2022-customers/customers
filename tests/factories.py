# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Customer, Address


class CustomerFactory(factory.Factory):
    """Creates fake customers that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""
        model = Customer

    id = factory.Sequence(lambda n: n)
    first_name = FuzzyChoice(choices=["chensong", "yueteng", "bohan", "harsh", "Jash"])
    last_name = FuzzyChoice(choices=["zhang", "doshi", "rofrano", "patel"])
    userid = FuzzyChoice(choices=["devops2022", "customers2022", "random2022", "username2022"])
    password = factory.Faker("password")
    addresses = []

class AddressFactory(factory.Factory):
    """Creates fake addresses that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""
        model = Address

    id = factory.Sequence(lambda n: n)
    address = FuzzyChoice(choices=["2022 New York", "2022 Jersey"])