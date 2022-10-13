# -*- coding: utf-8 -*-
import re

mes = "Python is the best language in the world"

result = re.match('(.*) is (.*?) .*', mes)

print(result.group(1))