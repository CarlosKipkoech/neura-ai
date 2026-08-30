ROLE_DEPARTMENTS = {
    "finance": "Finance",
    "hr": "Human Resources",
    "marketing": "Marketing",
    "engineering": "Engineering",
    "executive": "Executive",
    "employee": "Operations",
    "admin": "IT Security",
}


def department_for_role(role: str) -> str:
    return ROLE_DEPARTMENTS.get(role, role.title())
