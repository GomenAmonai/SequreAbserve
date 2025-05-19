import subprocess, secrets, base64, shutil

WG = shutil.which("wg")
OPENSSL = shutil.which("openssl") or "openssl"

def _run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd).decode().strip()

def gen_wg_keypair() -> tuple[str, str]:
    if not WG:
        raise RuntimeError("wireguard-tools not installed")
    priv = _run([WG, "genkey"])
    pub  = _run(["bash", "-c", f"echo {priv} | {WG} pubkey"])
    return priv, pub

def gen_ss_password() -> str:
    if OPENSSL:
        return _run([OPENSSL, "rand", "-base64", "32"])
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()