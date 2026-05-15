def get_rbd_age(year_of_birth: int) -> float:
    if year_of_birth <= 1949:
        return 70.5

    if year_of_birth <= 1950:
        return 72

    if year_of_birth <= 1959:
        return 73

    return 75