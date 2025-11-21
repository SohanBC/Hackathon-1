import tempfile
from androguard.core.bytecodes.apk import APK


def extract_apk_data(apk_path):
    apk = APK(apk_path)

    temp_icon_path = tempfile.mktemp(suffix=".png")
    with open(temp_icon_path, "wb") as f:
        f.write(apk.get_app_icon())

    return {
        "package_name": apk.get_package(),
        "permissions": apk.get_permissions(),
        "certificate_hash": apk.get_signature_name(),
        "developer": apk.get_app_name(),
        "icon_path": temp_icon_path
    }
