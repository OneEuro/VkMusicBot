class VkApiError(Exception):
    pass

class AccessDenied(VkApiError):
    pass

class VkAudioException(Exception):
    pass


class VkAudioUrlDecodeError(VkAudioException):
    pass


    