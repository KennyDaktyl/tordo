import imp
import re


def mobile(request):

    MOBILE_AGENT_RE = re.compile(
        r".*(iphone|mobile|androidtouch|ipad|tablet|android|blackberry|opera|mini|windows\sce|palm|smartphone|iemobile)",
        re.IGNORECASE,
    )

    if MOBILE_AGENT_RE.match(request.META["HTTP_USER_AGENT"]):
        return True
    else:
        return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    