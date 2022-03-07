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
#### 开发
1. 实现巡双线代码：smart_car_1.0
   数字图像处理：畸变矫正、图像压缩、透视变化、二值化、腐蚀降噪、霍夫检测-------》提取车道线\
   控制算法：Stanley算法，横向偏差+角度偏差\
   https://blog.csdn.net/renyushuai900/article/details/98460758\
   控制周期：0.4s
2. 在采集图像上的测试效果：中间白色空心线为计算的道路中线，即控制跟踪线；基本能提取出车道线，并计算控制速度及转角；略受反光影响。
![43fffd320f897bba76f1949171874af](https://user-images.githubusercontent.com/62023129/157029778-31c21b97-0f01-448d-afdb-e94a7c1ae788.png)
3. 实现对倒车入库车位进行区分：HSV滤颜色
4. 采集图像测试效果：
![image](https://user-images.githubusercontent.com/62023129/157034840-50eceeb9-2a1b-4e2f-93a1-d0b73a536fd2.png)
![image](https://user-images.githubusercontent.com/62023129/157034986-3284e10b-aa5f-4101-9d23-2b72c27fe4fd.png)
![image](https://user-images.githubusercontent.com/62023129/157035144-a3215b55-9f8f-4ad7-8b18-0389632f5dc4.png)

#### 实地测试
1. 图像显示错乱，与预先测试完全不同；预期速度太快，降速（0.1）；小车运行结果错乱；完全不可用 
2. 可能解决：\
   控制率太低？精简代码，控制周期:0.2S，无效；\
   控制率太高？增加time.sleep，控制周期：2.2S,无效；\

### 3.7第四周
#### 开发
1. 完善巡双线代码细节：smart_car_1.1
#### 实地测试
1. 发现小车用错图像（错用后摄像头图像），图像处理结果显示正常
2. 控制率问题：控制周期太小，发送指令过于频繁，指令堆积；使用time.sleep增加控制周期，整个程序sleep,控制延时巨大\
   发现d.getStatus()占用通讯，造成指令堆积，注释后小车控制正常，现控制周期：0.5S
3. 调整小车速度和转角参数，小车成功完成赛道，巡线较为平滑，速度很慢


### 3.14第五周
#### 开发

#### 实地测试


