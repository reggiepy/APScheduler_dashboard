# code: 0 0 F F F F
#       \-/ \-/ \-/
#         \--------- 类别
#             \--------- 标识码
#                 \--------- 错误码


# @formatter:off
class StatusCode:
    STATUS_SUCCESS                                  = 0  # noqa  操作成功
    STATUS_FAILED                                   = 1  # noqa  操作失败

    PAYLOAD_NEED_SET                                = 100001  # noqa  请配置接口jwt

def error_code_to_message(code):
    code_tab = {
        StatusCode.STATUS_SUCCESS: "操作成功",
        StatusCode.STATUS_FAILED: "操作失败",
        StatusCode.PAYLOAD_NEED_SET: "请配置接口jwt",
    }
    return code_tab.get(code, "未知异常: code={}".format(code))
