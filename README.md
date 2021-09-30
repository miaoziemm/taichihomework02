# 太极图形课S1-02 加了一点点交互的行星恒星系统

## 背景简介
以天添老师的Galaxy代码为基础，增加了三个交互。分别是：鼠标点击增加恒星或者行星，在中心增加一个“黑洞”，还有星体的“冻结”效果。

## 成功效果展示
鼠标左键点击增加恒星，右键点击增加行星。

![LRMB](./image/LRMB.gif)

按b在窗口中心添加一个黑洞。（因为不太了解黑洞的物理描述方法，我就直接在中间添加了一个质量非常大的星体，并且规定这个星体不会移动，而且当其他星体靠近时会产生一个吸收的效果。QAQ）

![LRMB](./image/Blackhole.gif)

按f使窗口内的星体“冻结”即在很短时间内速度衰减到一个很小的值，本来是想做一个类似子弹时间的效果，但是子弹时间内可能还需要考虑动量守恒，于是就先做了一个冻结的简单效果。

![LRMB](./image/freeze.gif)

## 整体结构（Optional）

```
-LICENSE
-|data
-|image
-README.MD
-galaxy.py
-celestial_objects.py
-requirements.txt
```

## 运行方式 
 `python galaxy.py`
