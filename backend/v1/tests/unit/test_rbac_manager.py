import pytest
from fastapi import HTTPException
from v1.shared.rbac_manager import RBACManager

def test_require_role():
    """
    Test: require_role with allowed roles
    """
    user = {"role": "admin"}
    RBACManager.require_role(user, ["admin", "user"])

def test_require_role_forbidden():
    """
    Test: require_role with disallowed roles
    """
    user = {"role": "user"}
    with pytest.raises(HTTPException, match="Access forbidden"):
        RBACManager.require_role(user, ["admin"])