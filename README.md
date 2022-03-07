# GKC-III-F
A project to accomplish some tasks of controlling a car


## Camera Calibration
https://blog.csdn.net/chenshiming1995/article/details/106546455
https://www.cnblogs.com/wenbozhu/p/10697374.html


## 小车开发进度
### 2.14第一周
1. 确定分组，车型：飞思卡尔车
### 2.21第二周
1. 熟悉小车硬软件
2. 讨论任务，大概分工
3. 建立github仓库
4. 相机矫正畸变
5. 采集赛道图像

### 2.28第三周
1. 实现巡双线代码1.0版：
   数字图像处理：畸变矫正、图像压缩、透视变化、二值化、腐蚀降噪、霍夫检测-------》提取车道线
   控制算法：Stanley算法，横向偏差+角度偏差
   控制周期：0.4s
2. 在采集图像上的测试效果：
![43fffd320f897bba76f1949171874af](https://user-images.githubusercontent.com/62023129/157029778-31c21b97-0f01-448d-afdb-e94a7c1ae788.png)
3. 实地测试效果：图像显示错乱，与预先测试完全不同；预期速度太快，降速（0.1）；小车运行结果错乱；完全不可用
#### 可能解决：
1. 控制率太低？精简代码1.1版，控制周期:0.2S，无效；
2. 控制率太高？增加time.sleep，控制周期：2.2S,无效；

### 3.7第四周
1. 


