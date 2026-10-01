# ===== Day 2:查询参数(Query Parameters)=====
#
# 昨天(Day 1)你学了"路径参数":/hello/{name},名字在网址路径里,必填。
# 今天学"查询参数":它在网址的 ? 后面,通常是"可选的筛选条件"。
#
# 【餐厅比喻】
#   路径参数 = 你点了"哪道菜"(/steak 牛排)      —— 必须选一个
#   查询参数 = 你对这道菜的"额外要求"(?spicy=true) —— 可选,是筛选/定制
#
# 查询参数长这样:  /search?keyword=苹果&limit=10
#   ? 后面是查询参数,格式是 key=value,多个用 & 连接
#
# 【FastAPI 的魔法】函数参数只要没出现在路径的 {} 里,就自动是"查询参数"。


from fastapi import FastAPI

app = FastAPI()


# ---------- 例子1:最基础的查询参数(必填)----------
# 人话:访问 /search?keyword=苹果,把 keyword 的值接住
# 关键:参数 keyword 没有出现在路径里,所以 FastAPI 自动把它当查询参数
@app.get("/search")
def search(keyword: str):
    return {"你搜索的是": keyword}


# ---------- 例子2:带默认值的查询参数(变成可选)----------
# 人话:limit 可以不传,不传就用默认值 10
# 关键:给参数一个默认值(limit: int = 10),它就从"必填"变成"可选"了
@app.get("/list")
def list_items(limit: int = 10):
    return {"最多返回": limit, "说明": "试试 /list?limit=3,或者不带参数直接访问 /list"}


# ---------- 例子3:可选 + 可能为空(用上你 Day1 学的 str | None)----------
# 人话:name 可传可不传;不传时它是 None,我们给个兜底问候
@app.get("/greet")
def greet(name: str | None = None):
    if name is None:
        return {"message": "你好,陌生人!"}
    return {"message": f"你好,{name}!"}


# ---------- 例子4:路径参数 + 查询参数 一起用 ----------
# 人话:/students/{student_id}?detail=true
#   student_id 在路径 {} 里 -> 路径参数(必填)
#   detail 在 ? 后面        -> 查询参数(可选,带默认值 False)
@app.get("/students/{student_id}")
def get_student(student_id: int, detail: bool = False):
    result = {"学生ID": student_id}
    if detail:
        # 只有当 detail=true 时,才补充详细信息
        result["姓名"] = "王梓铭"
        result["年龄"] = 18
    return result


@app.get("/sum")
def sum(n: int = 5):
    sum = 0
    for i in range(n):
        sum += i
    return {"sum": sum}

