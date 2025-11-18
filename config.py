import os
os.environ['window_name']="MuMu安卓设备"
# 注意要加r表示原始字符串，防止路径中的反斜杠被转义
os.environ['adb_path']=r"C:\Program Files\Netease\MuMu\nx_main\adb.exe"
# 这只是示例，替换为你自己的智谱AI key，免费的
os.environ["OPENAI_API_KEY"] = "b96acc38a2c4474d842b958db97927de.LOMHdpUqeOP5Vwgj"

# 种植采集类的最大数目
os.environ["plant_num_limit"] = str(20)
# 生产类最大数目
os.environ["produce_num_limit"] =  str(8)

# 种植采集类的卖的阈值
os.environ["plant_num_sale"] = str(40)
# 生产类的卖的阈值
os.environ["produce_num_sale"] = str(10)

# 小的延迟时间
os.environ["small_delay"] = str(1.5)
# 大的延迟时间
os.environ["big_delay"] = str(3)
