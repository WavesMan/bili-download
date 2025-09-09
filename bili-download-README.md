# B站API接口形式详解

本文档详细解析哔哩哔哩（Bilibili）Web端API的接口形式、认证机制和技术实现细节。

## 📋 整体架构

B站API采用客户端-服务器（C/S）架构，主要包含以下特点：

- **协议类型**: 主要使用REST API和gRPC，少量使用WebSocket
- **数据格式**: 请求数据多为URL query表单或JSON，响应数据多为JSON或Protobuf
- **安全要求**: 强制使用HTTPS协议
- **API版本**: 支持多版本API共存，通过URL路径或参数区分

API站：[https://api.bilibili.com](https://api.bilibili.com)

## 🔐 认证机制

### 1. Cookie认证
Web端主要依赖Cookie进行身份验证，关键Cookie包括：

- `SESSDATA`: 用户会话标识，有效期通常为30天
- `bili_jct`: CSRF token，用于防跨站请求伪造
- `DedeUserID`: 用户UID
- `buvid3`: 设备唯一标识

```http
GET /api/endpoint HTTP/1.1
Host: api.bilibili.com
Cookie: SESSDATA=xxx; bili_jct=xxx; DedeUserID=123456; buvid3=xxx
```

### 2. WBI签名算法
部分接口需要WBI签名验证，防止API滥用：

```javascript
// 签名生成算法
const w_rid = md5(wts + params + salt)
```

参数说明：
- `wts`: 当前时间戳（秒级）
- `salt`: 从接口动态获取的盐值
- `params`: 排序后的请求参数

### 3. APP端签名
移动端API使用appkey和sign进行签名：

```javascript
const sign = md5(sorted_params + app_secret)
```

## 📊 请求格式

### 1. URL Query格式
```http
GET /x/relation/stat?vmid=123456&jsonp=jsonp HTTP/1.1
```

### 2. JSON Body格式
```http
POST /x/v2/reply/add HTTP/1.1
Content-Type: application/json

{
  "oid": 123456789,
  "type": 1,
  "message": "测试评论",
  "plat": 1
}
```

### 3. Protobuf格式
gRPC接口使用Protobuf进行序列化：

```protobuf
message VideoInfoRequest {
  int64 aid = 1;
  string bvid = 2;
}
```

## 📡 响应格式

### 1. JSON响应
```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "aid": 123456789,
    "bvid": "BV1xxx",
    "title": "视频标题",
    "owner": {
      "mid": 123456,
      "name": "up主名称"
    }
  }
}
```

### 2. Protobuf响应
gRPC接口返回二进制Protobuf数据，需要反序列化处理。

### 3. 错误码规范
- `0`: 成功
- `-101`: 账号未登录
- `-400`: 请求错误
- `-403`: 访问权限不足
- `-404`: 接口不存在
- `-500`: 服务器错误

## 🗂️ 主要接口分类

### 1. 用户相关接口
- `GET /x/space/acc/info` - 用户基本信息
- `GET /x/relation/stat` - 用户关系统计
- `GET /x/v2/medal` - 粉丝勋章信息

### 2. 视频相关接口
- `GET /x/web-interface/view` - 视频基本信息
- `GET /x/player/playurl` - 视频播放地址
- `POST /x/v2/view/like` - 视频点赞操作

### 3. 动态相关接口
- `GET /x/polymer/web-dynamic/v1/feed/all` - 全部动态
- `GET /x/polymer/web-dynamic/v1/feed/space` - 用户空间动态

### 4. 评论相关接口
- `GET /x/v2/reply` - 获取评论列表
- `POST /x/v2/reply/add` - 添加评论
- `POST /x/v2/reply/action` - 评论操作（点赞、删除等）

### 5. 搜索相关接口
- `GET /x/web-interface/search/type` - 分类搜索
- `GET /x/web-interface/search/default` - 默认搜索词
- `GET /x/web-interface/search/suggest` - 搜索建议

## 🔧 技术实现细节

### 1. 接口版本控制
B站API通过URL路径进行版本控制：
- `/x/interface/v1/` - v1版本接口
- `/x/interface/v2/` - v2版本接口
- `/x/interface/` - 当前版本接口

### 2. 分页机制
大多数列表接口支持分页参数：
```http
GET /x/v2/reply?oid=123456&type=1&pn=1&ps=20
```
- `pn`: 页码（page number）
- `ps`: 每页数量（page size）

### 3. 时间戳验证
重要接口包含时间戳验证，防止重放攻击：
```http
GET /api/endpoint?_=1640995200000
```

### 4. 设备标识
接口请求需要携带设备标识：
- `buvid3`: Web端设备标识
- `buvid4`: 移动端设备标识
- `build`: 客户端版本号

## 🛡️ 安全机制

### 1. CSRF防护
所有修改操作需要验证`bili_jct` Cookie：
```javascript
const csrf = getCookie('bili_jct');
```

### 2. 频率限制
API接口有严格的频率限制：
- 普通接口：1-5次/秒
- 敏感接口：更严格的限制
- 基于IP和账号双重限制

### 3. 人机验证
敏感操作触发极验验证：
- 登录操作
- 频繁评论
- 异常行为检测

## 📝 开发注意事项

### 1. Cookie管理
- 定期刷新SESSDATA（通常30天有效期）
- 正确处理Cookie的HttpOnly和Secure属性
- 避免Cookie泄露风险

### 2. 错误处理
- 正确处理各种错误码
- 实现重试机制（特别是网络错误）
- 记录详细的错误日志

### 3. 性能优化
- 合理使用缓存（视频信息、用户信息等）
- 批量请求优化（减少API调用次数）
- 连接复用和Keep-Alive

### 4. 合规使用
- 遵守B站API使用规范
- 尊重用户隐私和数据安全
- 避免对服务器造成过大压力

## 🔗 相关资源

- [官方API文档](https://github.com/SocialSisterYi/bilibili-API-collect)
- [gRPC接口定义](grpc_api/)
- [错误码说明](docs/misc/errcode.md)
- [WBI签名算法](docs/misc/sign/wbi.md)

## ⚠️ 免责声明

本文档仅用于技术学习和研究目的，请勿用于商业用途或违反B站用户协议的行为。使用API时请尊重版权和用户隐私，遵守相关法律法规。

---

*最后更新: 2025年9月8日*
*基于 bilibili-API-collect 项目文档分析整理*
