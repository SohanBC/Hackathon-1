SUSPICIOUS_PERMISSIONS = {
    "READ_SMS": 1,
    "SEND_SMS": 1,
    "READ_CONTACTS": 1,
    "REQUEST_INSTALL_PACKAGES": 1,
    "SYSTEM_ALERT_WINDOW": 1,
}

def get_permissions_score(permission_list):
    flagged = 0
    for perm in permission_list:
        if any(s in perm for s in SUSPICIOUS_PERMISSIONS):
            flagged += 1

    score = max(0, 1 - (flagged * 0.1))
    return round(score, 2)
