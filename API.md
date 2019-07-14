# API
## /search
### 参数
1. key，关键词，别传空的
2. catalog，分类，0介绍，1使用手册，2源码分析，3demo，4教学视频，5相关问题
3. page，页数，从1开始
4. size，每页的大小
5. delta，过滤时间，0:所有，1:一天内，2:一周内，3:一月内，4:一年内
### example
http://10.214.213.43:9999/search?key=Docker&catalog=2&page=1&size=10&delta=0
### 返回包格式
```json
{
	message: "",
	code: 200,
	data: {
		total: 10,
		result: [
			{
				_id: "",
				title: "",
        summary: "",
        url: "",
        tags: ["", "", ]
        catalog: 2,
        content: ""，
        source: "",
        date: "",
        author: "",
        score: 1.1,
			},
		]
	}
}
```
## /getAllTag
### 参数
1. key，标签名字，为空则表示显示所有标签
2. page，页数，从1开始
3. size，每页的大小
### example
http://10.214.213.43:9999/getAllTag?page=1&size=10key=
### 返回包格式
1. 当key为空时
```json
{
	message: "",
	code: 200,
	data: {
		total: 10,
		result: [
			{
				tag: "",
				count: 22
			},
		]
	}
}
```
2. 当key不为空时
```json
{
	message: "",
	code: 200,
	data: {
		total: 10,
		result: [
			{
				_id: "",
				title: "",
        summary: "",
        url: "",
        tags: ["", "", ]
        catalog: 2,
        content: ""，
        source: "",
        date: "",
        author: "",
			},
		]
	}
}
```
