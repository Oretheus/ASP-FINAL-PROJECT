from fastapi import HTTPException

class RBACManager:

    @staticmethod
    def require_role(user: dict, allowed_roles: list):
        """
        Validate user's role.
        """
        role = user.get("role")
        if role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access forbidden: Role '{role}' not allowed.",
            )
