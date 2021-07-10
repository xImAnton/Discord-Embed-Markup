from typing import Optional


class NonEmptyValueDict(dict):
    """
    acts like a normal dict but doesn't set falsy values
    """
    
    def __init__(self, d: Optional[dict] = None):
        if d is None:
            d = {}
        super_dict = {k: v for k, v in d.items() if v}
        super(NonEmptyValueDict, self).__init__(super_dict)

    def __setitem__(self, key, value):
        if not value:
            return
        super(NonEmptyValueDict, self).__setitem__(key, value)
